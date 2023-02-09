import requests
import json

# url = "https://api.yelp.com/v3/businesses/search"
url = "https://api.yelp.com/v3/businesses/search"
access_token = "c9uBfCGxe7-me1YAOGqCD1NuziufQ5Kck0D5eaZmqckIzG_nCllAPs-3JGE0pY78GvtvTNOsUxUHrrYB9bISI9zwb_Nzzq1jEQyYHleQfQov6deSjvuFTDZ9KdvRY3Yx"
headers = {
    'Authorization': 'Bearer ' + access_token,
    'accept': 'application/json'
}

def get_activities(location, experience):
    params = {
        'location': location,
        'term': experience
    }
    res = requests.get(url=url, params=params, headers=headers)
    res_dict = (res.json())
    business = res_dict["businesses"]
    return business
