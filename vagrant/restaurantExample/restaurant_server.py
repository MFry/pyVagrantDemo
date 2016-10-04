from flask import Flask, render_template, url_for, jsonify, redirect, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Menu, connection_str

app = Flask(__name__)

engine = create_engine(connection_str)
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def home():
    restaurants = session.query(Restaurant).order_by(Restaurant.name)
    return render_template('restaurants_list.html',
                           restaurants=restaurants,
                           edit_func=edit_restaurant)


@app.route('/restaurants/json/', methods=['GET'])
def restaurants_json():
    r = session.query(Restaurant).order_by(Restaurant.id)
    json_objects = []
    for q in r:
        json_objects.append(q.serialize)
    return jsonify(restaurants=json_objects)


@app.route('/restaurants/<int:restaurant_id>/json/', methods=['GET'])
def restaurant_json(restaurant_id):
    r = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if r:
        return jsonify(restaurant=r.serialize)
    else:
        return None


@app.route('/restaurants/new/', methods=['POST'])
def new_restaurant():
    if request.method == 'POST':
        name = request.form['name']
        r = Restaurant(name=name)
        session.add(r)
        session.commit()
    return jsonify({'success': True})


@app.route('/restaurants/edit/', methods=['POST', 'GET'])
def edit_restaurant(restaurant_id):
    if request.method == 'POST':
        r = session.query(Restaurant).filter_by(id=restaurant_id).one()
        r.name = request.form['name']
        session.add(r)
        session.commit()
    return redirect(url_for('home'))


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json/')
def restaurant_menu_item_json(restaurant_id, menu_id):
    item = session.query(Menu).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(menu_item=item.serialize)


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['POST', 'GET'])
def delete_restaurant(restaurant_id):
    if request.method == 'POST':
        r = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(r)
        session.commit()
    return jsonify({'success': True})


@app.route('/restaurants/<int:restaurant_id>/menu/', methods=['POST', 'GET'])
def menu(restaurant_id):
    menu_items = session.query(Menu).filter_by(restaurant_id=restaurant_id).order_by(Menu.id)
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('menu_list.html', menu=menu_items, restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/json/')
def menu_json(restaurant_id):
    m = session.query(Menu).order_by(Menu.id).filter_by(restaurant_id=restaurant_id)
    menu_items = []
    for q in m:
        menu_items.append(q.serialize)
    return jsonify(menu_items=menu_items)


@app.route('/restaurants/<int:restaurant_id>/menu/add/', methods=['POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        m = Menu(name=request.form['name'],
                 description=request.form['desc'],
                 course=request.form['course'],
                 price=request.form['price'],
                 restaurant_id=restaurant_id)
        session.add(m)
        session.commit()
    return redirect(url_for('menu', restaurant_id=restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/menu/edit/', methods=['POST'])
def edit_menu_item(restaurant_id):
    if request.method == 'POST':
        menu_id = request.form['menu_id']
        name = request.form['name']
        item = session.query(Menu).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
        item.name = name
        session.add(item)
        session.commit()
    return redirect(url_for('menu', restaurant_id=restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/menu/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id):
    if request.method == 'POST' or request.method == 'GET':
        menu_id = request.form['menu_id']
        m = session.query(Menu).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
        session.delete(m)
        session.commit()
    return redirect(url_for('menu', restaurant_id=restaurant_id))


if __name__ == '__main__':
    # Developer password
    app.debug = True
    # app.add_url_rule()
    app.run('0.0.0.0', port=5000)
