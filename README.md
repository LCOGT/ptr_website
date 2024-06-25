Photon Ranch content website
============================

A Django site for the content side of Photon Ranch, written using the Wagtail CMS framework.

This website will host the front page of PTR, news etc. and Learn @ PTR.

## Development

To install locally (after creating an appropriate python virtual environment)

```
pip install -r requirements.txt
python manage.py migrate

```

### Get snapshot of live site:

```
kubectl exec -it <pod-name> -n prod -c backend -- python manage.py dumpdata --natural-foreign --indent 2 \
    -e contenttypes -e auth.permission -e postgres_search.indexentry \
    -e wagtailcore.groupcollectionpermission \
    -e wagtailcore.grouppagepermission -e wagtailimages.rendition \
    -e sessions | gzip > fullsite.json.gz
```

Remove bogus logentries:

Replace all `"data": null` with `"data": {}`  
```
gsed -i 's+"data": null+"data": {}+g' fullsite.json
```

Read data into local sandbox with:
```
./manage.py migrate; ./manage.py remove_demo_page; ./manage.py loaddata fullsite.json.gz
```

## Deployment 

TBD
