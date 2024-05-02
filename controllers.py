"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        add_keow_url = URL('add_keow'),
        get_keows_url = URL('get_keows'),
        set_thumb_url = URL('set_thumb'),
    )

@action('add_keow', method="POST")
@action.uses(db, auth.user, auth)
def add_keow():
    keow_content = request.json.get('keow_content')
    id = db.keow.insert(keow_content=keow_content)
    print("keow_content:", keow_content)
    return dict(id=id)


@action('get_keows', method="GET")
@action.uses(db, auth.user, auth)
def get_keows():
    q = None
    s = request.params.get('search')
    if s:
        q = db.keow.keow_content.contains(s)
    result = db(q).select(
        db.keow.ALL, db.thumb.thumb, 
        left=db.thumb.on((db.keow.id == db.thumb.keow_id) & 
                         (db.thumb.rater == get_user_email()))).as_list()
    keows = [d['keow'] | d['thumb'] for d in result]
    # Now adds to this list the total kews for each keow. 
    for k in keows:
        thumb_values = db(db.thumb.keow_id == k['id']).select(db.thumb.thumb).as_list()
        k['total'] = sum([d['thumb'] for d in thumb_values])
    print("keows:", keows)
    return dict(keows=keows)

@action('set_thumb', method="POST")
@action.uses(db, auth.user, auth)
def set_thumb():
    keow_id = request.json.get('keow_id')
    thumb = request.json.get('thumb')
    db.thumb.update_or_insert(
        (db.thumb.keow_id == keow_id) & (db.thumb.rater == get_user_email()),
        keow_id=keow_id,
        rater=get_user_email(),
        thumb=thumb,
    )
    # Reads the total number of thumbs for this keow.
    thumb_values = db(db.thumb.keow_id == keow_id).select(db.thumb.thumb).as_list()
    return dict(total=sum([d['thumb'] for d in thumb_values]))
