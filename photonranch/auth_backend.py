from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate as dj_authenticate
from django.contrib.auth import get_user_model
import requests
import logging

from user.models import User

UserModel = get_user_model()

logger = logging.getLogger(__name__)


class DjangoBackend(object):
    """
    Authenticate against the Django user database.
    Fallback for Django Admin user.
    """

    def authenticate(self, request, username=None, password=None):
        print("here")
        return dj_authenticate(request, username=username, password=password)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class PortalBackend(object):
    """
    Authenticate against the Observing portal API.
    """

    def authenticate(self, request, username=None, password=None):
        return lco_authenticate(request, username, password)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def lco_authenticate(request, username, password):
    token = api_auth(settings.PORTAL_TOKEN_URL, username, password)
    profile, msg = get_profile(token)
    if token and profile:
        username = profile[0]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a new user. There's no need to set a password
            # because Observation Portal auth will always be used.
            user = User(username=username)
        user.token = token
        user.default_proposal = profile[2]
        user.email = profile[3]
        user.save()
        return user

    return None


def api_auth(url, username, password):
    '''
    Request authentication cookie from the Scheduler API
    '''
    try:
        r= requests.post(url,data = {
            'username': username,
            'password': password
            }, timeout=20.0);
    except requests.exceptions.Timeout:
        msg = "Observing portal API timed out"
        logger.error(msg)
        return False
    except requests.exceptions.ConnectionError:
        msg = "Trouble with internet"
        logger.error(msg)
        return False

    if r.status_code in [200,201]:
        logger.debug('Login successful for {}'.format(username))
        return r.json()['token']
    else:
        logger.error("Could not login {}: {}".format(username, r.json()['non_field_errors']))
        return False

def get_profile(token):
    url = settings.PORTAL_PROFILE_URL
    token = {'Authorization': 'Token {}'.format(token)}
    try:
        r = requests.get(url, headers=token, timeout=20.0);
    except requests.exceptions.Timeout:
        msg = "Observing portal API timed out"
        logger.error(msg)
        return False, "We are currently having problems. Please bear with us"

    if r.status_code in [200,201]:
        logger.debug('Profile successful')
        proposal = check_proposal_membership(r.json()['proposals'])
        if proposal:
            return (r.json()['username'], r.json()['tokens']['archive'], proposal, r.json()['email']), False
        else:
            logger.debug('No active proposal')
            return False, "Please <a href='/accounts/register/'>register</a>"
    else:
        logger.error("Could not get profile {}".format(r.content))
        return False, "Please check your login details"

def check_proposal_membership(proposals):
    return True
    '''
    # Check user has a proposal we authorize
    proposals = [p['id'] for p in proposals if p['current'] == True]
    my_proposals = Proposal.objects.filter(code__in=proposals, active=True)
    if my_proposals:
        return my_proposals[0]
    else:
        return False
    '''
