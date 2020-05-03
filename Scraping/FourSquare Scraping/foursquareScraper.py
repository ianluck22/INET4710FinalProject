# Parker Erickson
# INET 4710 Final Project

# Credits: https://medium.com/@aboutiana/a-brief-guide-to-using-foursquare-api-with-a-hands-on-example-on-python-6fc4d5451203

import json
import requests
import cfg

class foursquareScraper():
    def __init__(self, clientID, clientSecret):
        self.clientID = clientID
        self.clientSecret = clientSecret

    # Get nearby establishments, using latitude, longitude, radius (in meters/defaults to about a mile), limit responses (defaults to 100) and section (food, drink, etc)
    # Returns json response
    def getNearby(self, latitude, longitude, radius = 1600, limit = 100, section=""):
        url = url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}&section={}'.format(
            self.clientID, 
            self.clientSecret, 
            "20180323", 
            str(latitude), 
            str(longitude), 
            str(radius), 
            str(limit),
            section)

        response = requests.get(url=url)
        result = response.json()
        return result

    # Returns a dictionary with a count of the various categories in the response data. 
    # Takes latitude, longitude, raidus (in meters/defaults to about a mile), and limit of responses (default 100)
    def getCategoryCount(self, latitude, longitude, radius=1600, limit=100):
        typesOfLocations = ["food", "drinks", "coffee", "shops", "arts", "outdoors", "sights"]
        finalCounts = {}
        for locationType in typesOfLocations:
            places = self.getNearby(latitude, longitude, radius, limit, locationType)["response"]["groups"][0]["items"]
            for place in places:
                category = place["venue"]["categories"][0]["name"]
                try:
                    finalCounts[category] += 1
                except:
                    finalCounts[category] = 1

        return finalCounts

def main():
    scraper = foursquareScraper(cfg.clientid, cfg.secret)
    print(scraper.getCategoryCount(44.9752386, -93.22132))

if __name__ == "__main__":
    main()