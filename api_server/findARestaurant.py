from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

#foursquare_client_id = "K1K1KFYXX1HR5RCWHF4010DAK41G0YQCDSMOJGUOZMY1AX4E"
#foursquare_client_secret = "LKZ24X3WZX4US5ZX0P1JRBXVPCJO4ZDXP2I0FNJBDKMJ1Q0B"
foursquare_client_id = "BMA5WROHT5YF25245QB0OP3LLFPILNELGIZQWFNAZFR1XK0F"
foursquare_client_secret = "2KYE50NQXA2ASPWQFV1XH1HTE04CGNFINB5XX53ENVDBI3RK"


def findARestaurant(mealType,location):
    #print ("mealtype:%s,location:%s" % (mealType, location))
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    latLong = getGeocodeLocation(location)
    latStr = str(latLong[0]) 
    longStr = str(latLong[1]) 
    #latitude, longitude = getGeocodeLocation(location)
    #print("latitude:%s, longitude:%s" % (latStr,longStr))
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like:
    #https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s'% (foursquare_client_id, foursquare_client_secret, latStr, longStr, mealType))
    #print("url:%s" % url)
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    status = result['meta']['code']
    print(status)
    if result['response']['venues']:
    	#3.  Grab the first restaurant
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        address = ""
        for i in restaurant_address:
            address += i + " "

        restaurant_address = address
        #4.  Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])
        #print(result)
        #5.  Grab the first image
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            #6.  if no image available, insert default image url
            imageURL = "https://thumb1.shutterstock.com/display_pic_with_logo/288100/316591013/stock-photo-gourmet-tasty-steak-burgers-with-ham-slices-on-a-wooden-tray-with-potato-wedges-and-dipping-sauce-316591013.jpg"
        
        #7.  return a dictionary containing the restaurant name, address, and image url
        restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
        print "Restaurant Name: %s" % restaurantInfo['name']
        print "Restaurant Address: %s" % restaurantInfo['address']
        print "Image: %s \n" % restaurantInfo['image']
        return restaurantInfo
    else:
        print "No Restaurants Found for %s" % location
        return "No Restaurants Found"

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")