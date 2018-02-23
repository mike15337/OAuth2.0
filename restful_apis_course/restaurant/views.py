from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




foursquare_client_id = "BMA5WROHT5YF25245QB0OP3LLFPILNELGIZQWFNAZFR1XK0F"
foursquare_client_secret = "2KYE50NQXA2ASPWQFV1XH1HTE04CGNFINB5XX53ENVDBI3RK"
google_api_key = "AIzaSyAsvR-YtKDDuWnPo_gPFhZTfjlAEeB3jis"

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        #Call the method to Get all of the restaurants
        return getAllRestaurants()
    elif request.method == 'POST':
        #Call the method to make a new restaurant
        print "Making a New restaurant"
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        print location
        print mealType
        return makeANewRestaurant(location, mealType)

    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    #YOUR CODE HERE
    print("Restaurant Handler")
    if request.method == 'GET':
        return getRestaurant(id)
    #Call the method to edit a specific restaurant
    elif request.method == 'PUT':
        name = request.args.get('name', '')
        address = request.args.get('address', '')
        image = request.args.get('image', '')
        return updateRestaurant(id, name, address, image)
    #Call the method to remove a puppy 
    elif request.method == 'DELETE':
        return deleteRestaurant(id)
    
    return

def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    # Probably should have used a lowercase "Restaurants"
    return jsonify(Restaurants=[i.serialize for i in restaurants])

def makeANewRestaurant(location, mealType):
    restaurant = findARestaurant(mealType,location)
    if restaurant:
        dbRestaurant = Restaurant(restaurant_name = restaurant['name'], 
                                  restaurant_address = restaurant['address'], 
                                  restaurant_image = restaurant['image'])
        session.add(dbRestaurant)
        session.commit()
        return jsonify(Restaurant=dbRestaurant.serialize)

def getRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    return jsonify(restaurant=restaurant.serialize) 
  

def updateRestaurant(id, name, address, image):
    print("Call with id:%s, name:%s, address:%s, image:%s" % (id,name,address,image))
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    if name:
        print("change name from:%s to %s" % (restaurant.restaurant_name, name))
        restaurant.restaurant_name = name
    if address:
        restaurant.restaurant_address = address
        print("update address to:%s" % address)
    if image:
        restaurant.restaurant_image = image 
        print("update image to:%s" % image)
    session.add(restaurant)
    session.commit()
    return jsonify(Restaurant=restaurant.serialize)

def deleteRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    session.delete(restaurant)
    session.commit()
    print("Removed Restaurant with id %s" % id)
    return jsonify({"message": "Restaurant Deleted"})
    #return jsonify(Restaurant=restaurant.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


