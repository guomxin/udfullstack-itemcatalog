import random
import string
import httplib2
import json
import requests

from flask import Flask,render_template, flash, request, url_for, redirect, jsonify
from flask import json, make_response, session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#-------------------------Helper functions-----------------------

# Add new user
def add_user(login_session):
    user = User(name=login_session['name'], email=login_session['email'])
    session.add(user)
    session.commit()
    return

# Check whether user in database or add it
def get_user_by_session(login_session):
    try:
        user = session.query(User).filter_by(email=login_session['email']).one()
        return user
    except:
        add_user(login_session)
        return session.query(User).filter_by(email=login_session['email']).one()

# Get category by id
def get_category_by_id(cat_id):
    return session.query(Category).filter_by(id=cat_id).one()

# Get all categories
def get_all_category():
    return session.query(Category).all()

# Get one item by id
def get_item_by_id(item_id):
    return session.query(Item).filter_by(id=item_id).one()

# Get items by category id
def get_items_by_cat(cat_id):
    return session.query(Item).filter_by(category_id=cat_id).all()

# Get last 10 items
def get_last_10_items():
    return session.query(Item).order_by(Item.id.desc()).limit(10)

# Add or update row
def add_item(row):
    session.add(row)
    session.commit()

# Delete row
def delete_item(row):
    session.delete(row)
    session.commit()

#-------------------------JSON Endpoints-----------------------

# Get all categories
@app.route('/api/catalog/JSON/')
def catalogJSON():
    categories = get_all_category()
    return jsonify(categories=[cat.serialize for cat in categories])

# Get all items of one category
@app.route('/api/catalog/<int:category_id>/items/JSON/')
def itemsJSON(category_id):
    items = get_items_by_cat(category_id)
    return jsonify(items=[item.serialize for item in items])


# Get one item
@app.route('/api/catalog/item/<int:item_id>/JSON/')
def itemJSON(item_id):
    item = get_item_by_id(item_id)
    return jsonify(item=item.serialize)

#-------------------------Google OAuth related functions-----------------------

# Connect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # check state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    """
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that  token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Tokens user ID does not match user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Tokens client ID does not match app ."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the  token in the session .
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # get user information email name picture)
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['name'] = data['name']
    login_session['email'] = data['email']
    """
    login_session['access_token'] = 'willbedeleted'
    login_session['gplus_id'] = 'willbedeleted'
    login_session['name'] = 'Guomao Xin'
    login_session['email'] = 'catty.xin@gmail.com' 
    
    
    # check if user in database or add it
    login_session['user_id'] = get_user_by_session(login_session).id
    show_output = ''
    show_output += '<br/>'
    show_output += '<h2>Welcome '
    show_output += login_session['name']
    show_output += '!</h2>'
    show_output += '<br/>'
    return show_output

# Disconnect
@app.route('/gdisconnect')
def gdisconnect():
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # check status code
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['name']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    """
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['name']
    del login_session['email']
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return redirect('/')

#-------------------------Catalog web services-----------------------

@app.route('/')
@app.route('/catalog/')
def allCategories():
    '''
    Show all categories and lastest items
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    categories = get_all_category()
    latest_items = get_last_10_items()
    return render_template('index.html',
            STATE=state,
            categories=categories,
            items=latest_items,
            user=login_session)


@app.route('/catalog/<int:cat_id>/')
def itemsByCategory(cat_id):
    '''
    Get all the items of one category
    '''
    # Call helper methods
    categories = get_all_category()
    category = get_category_by_id(cat_id)
    items = get_items_by_cat(cat_id)
    return render_template('category.html',
                           category=category,
                           categories=categories,
                           items=items,
                           user=login_session)

@app.route('/catalog/<int:cat_id>/item/<int:item_id>/')
def getItem(cat_id, item_id):
    '''
    Get item based on id
    '''
    cat = get_category_by_id(cat_id)
    i = get_item_by_id(item_id)
    return render_template('item.html',
                           category=cat,
                           item=i,
                           user=login_session)

@app.route('/catalog/<int:cat_id>/addItem', methods=['GET', 'POST'])
def addItemCat(cat_id):
    '''
    Add one item for a category. The method GET will open the 'add_item.html'
    The method POST insert new item and redirect the user 'category.html'.
    '''
    # If user doesn't login, redirect to home page
    if 'name' not in login_session:
        return redirect(url_for('allCategories'))
    else:
        cat = get_category_by_id(cat_id)
        if request.method == 'POST':
            new_item = Item(name=request.form['name'],
                            description=request.form['description'],
                            category_id=cat.id,
                            user_id=login_session['user_id'])
            add_item(new_item)
            return redirect(url_for('itemsByCategory', cat_id=cat.id))

        else:
            return render_template('add_item.html',
                                   cat=cat,
                                   user=login_session)

@app.route('/catalog/<int:cat_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(cat_id, item_id):
    '''
    Edit item information. The method GET will open the 'edit_item.html'.
    The method POST will update the item and redirect the user to 'item.html'.
    '''
    # If user doesn't login, redirect to home page
    if 'name' not in login_session:
        return redirect(url_for('allCategories'))
    else:
        categories = get_all_category()
        item = get_item_by_id(item_id)
        if request.method == 'POST':
            # Check if is the same user
            if login_session['user_id'] != item.user_id:
                return make_response("You are not authorized to edit this item.", 401)
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            if request.form['catalog']:
                item.category_id = request.form['catalog']
            # Update the item
            add_item(item)
            return redirect(url_for('getItem',
                            cat_id=item.category_id,
                            item_id=item.id))
        else:
            return render_template('edit_item.html',
                                   categories=categories,
                                   item=item,
                                   user=login_session)

@app.route('/catalog/<int:cat_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(cat_id, item_id):
    '''
    Delete an item
    '''
    # If user doesn't login, redirect to home page
    if 'name' not in login_session:
        return redirect(url_for('allCategories'))
    else:
        item = get_item_by_id(item_id)
        # Check if is the same user
        if login_session["user_id"] != item.user_id:
            return make_response("""You are not authorized to delete this item.""", 401)
        if request.method == 'POST':
            # Delete the item
            delete_item(item)
            return redirect(url_for('itemsByCategory',
                            cat_id=item.category_id))
        else:
            return render_template('delete_item.html',
                                   item=item,
                                   user=login_session)
if __name__ == "__main__":
    app.secret_key = "your_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
