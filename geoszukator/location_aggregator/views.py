from django.core.checks import messages
from location_aggregator.models import Cities, Continents, Countries, Flags, Languages, Regions
from django.http.response import HttpResponse
from django.shortcuts import render
import requests

from .config import ipstack_base_url, access_key

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


def execute_IP_search(ip: str):
    """Sends HTTP request GET to ipstack.com to obtain location of requested IP. 
    URL = http://api.ipstack.com/{IP}?access_key={api_access_key}
    
    Args: ip
    
    Returns:
        A response from request GET
    """

    url = ipstack_base_url + ip + access_key

    return requests.get(url=url, timeout=5)

def insert_to_database(location, result):
    """Make an insert into a database. 
    step 1 insert to table continent
    step 2 insert to table flags
    step 3 insert to table languages
    step 4 get the ids from dictionaries tables
    step 5 insert to table countries
    step 6 insert to table regions
    step 7 insert to table cities

    Args: database insert, column_name='value'

    Returns:
    """

    # step 1 insert to table continent
    try:
        continent = Continents.objects.create(continent_code=location["continent_code"], continent_name=location["continent_name"])
    except:
        print("the continent exists")
        result['message'] = "the continent exists"

    # step 2 insert to table flags
    try:
        flag = Flags.objects.create(
                                    flag_emoji_unicode=location["location"]["country_flag_emoji_unicode"],
                                    flag=location["location"]["country_flag"],
                                    flag_emoji=location["location"]["country_flag_emoji"]
                                    )
    except:
        print("flag exists")
        result['message'] = "the continent exists"
    
    # step 3 insert to table languages
    try:
        language = Languages.objects.create(language=location["location"]["languages"][0]["name"],
                                            language_code=location["location"]["languages"][0]["code"]
                                            )
    except:
        print("language exist")
        result['message'] = "the language exist"


    try:
        # step 4 get the ids from dictionaries tables
        continents_id = Continents.objects.get(continent_name=location["continent_name"])
        continents_id = continents_id.id
        print(continents_id)
        flag_id = Flags.objects.get(flag_emoji_unicode=location["location"]["country_flag_emoji_unicode"])
        flag_id = flag_id.id
        languages_id = Languages.objects.get(language=location["location"]["languages"][0]["name"])
        languages_id = languages_id.id
        print("banda", flag_id, languages_id)
        print(type(location["location"]["calling_code"]))
        
        # step 5 insert to table countries
        country = Countries.objects.create(country_name=location["country_name"],
                                        country_code=location["country_code"],
                                        capital=location["location"]["capital"],
                                        country_flag_id=flag_id,
                                        continent_id=continents_id,
                                        language_id=languages_id,
                                        calling_code=location["location"]["calling_code"],
                                        is_eu=location["location"]["is_eu"]
                                        )
    except:
        print('err')

    # step 6 insert to table regions
    try:
        countrys_id = Countries.objects.get(country_name=location["country_name"])
        countrys_id = countrys_id.id
        region = Regions.objects.create(region_code=location["region_code"], 
                                        region_name=location["region_name"],
                                        country_id=countrys_id)
    except:
        print("region exists")
        result['message'] = "the region exists"
    
    # step 7 insert to table cities
    try:
        regions_id = Regions.objects.get(region_name=location["region_name"])
        regions_id = regions_id.id
        zip_val = str(location["zip"])
        city = Cities.objects.create(city_name=location["city"],
                                zip_value=zip_val,
                                latitude=location["latitude"],
                                longitude=location["longitude"],
                                ip_code=location["ip"],
                                region_id=regions_id)
        result['message'] = "OK"
    except:
        result["message"] = "there is that location in the table"


    return result



@api_view(['GET'])
def check_the_location(request):
    """ 
    step 1: type ip of searching location to the execute_IP_search function
                and send request to ipstack
    step 2: insert data to the tables, if data already exist skip the insert

    Returns: json with data from ipstock, and error messages
    """

    result = {
        'message': None,
        'status': None,
        'location': None,
    }

    # step 1
    location = execute_IP_search(ip='1.1.1.1')

    result['message'] = 'There was a problem with send request'
    result['status'] = location.status_code

    if location.status_code in [200, 201, 202]:
        location = location.json()
        result['location'] = location
        print(location)
        result['message'] = 'OK'

        #Step 2
        insert = insert_to_database(location=location, result=result)

    return Response(result)


@api_view(['GET'])
def delete_record_from_db(request):
    """
    delete record, which possess certain ip, from database 
    
    Returns: json result with message about deletion
    """

    result = {
        'message': None,
    }
    ip='1.1.1.1'
    try:

        delete_city = Cities.objects.get(ip_code=ip).delete()
        result["message"]= f"data with ip={ip} deleted from database"
    except:
        result["message"]= f"There was not data connected with ip={ip}"

    return Response(result)

@api_view(['GET'])
def update_record_in_db(request):
    """ 
    step 1. search of ip in ipstack database.
    step 2. check if data from dictionary tables match data from request, 
        if something is missing, insert into dictionaries tables.
    step 3. update table city using data from json.
    """

    result = {
        'message': None,
        'status': None, #przemyslec czy to jest tutaj potrzebne
        'location': None
    }
    ip='1.1.1.1'

    #step 1. search of ip in ipstack database
    location = execute_IP_search(ip)
    result["status"]= location.status_code
    if location.status_code in [200,201,202]:
        location = location.json()
        result["location"]= location

        #step 2. check if data from dictionary tables match data from request
        try: 
            continents_id = Continents.objects.get(continent_name=location["continent_name"])
            continents_id = continents_id.id
            flag_id = Flags.objects.get(flag_emoji_unicode=location["location"]["country_flag_emoji_unicode"])
            flag_id = flag_id.id
            languages_id = Languages.objects.get(language=location["location"]["languages"][0]["name"])
            languages_id = languages_id.id
            regions_id = Regions.objects.get(region_name=location["region_name"])
            countrys_id = Countries.objects.get(country_name=location["country_name"])
            countrys_id = countrys_id.id
            regions_id = Regions.objects.get(region_name=location["region_name"])
            regions_id = regions_id.id

        except:
            try:
                insert = insert_to_database(location=location, result=result)
            except:
                result["message"]= "there was a problem with insert, check connection to the database"
            
            try:
                delete_city = Cities.objects.get(ip_code=location["ip"]).delete()
            except:
                result["message"]= "there was nothing to delete"
            result["message"]= "new data inserted to the dictionaries tables"

        # step 3 update table city using data from json.
        try:
            regions_id = Regions.objects.get(region_name=location["region_name"])
            regions_id = regions_id.id
            city_to_update = Cities.objects.filter(ip_code=location["ip"]).update(
                                                    city_name=location["city"],
                                                    latitude=location["latitude"],
                                                    longitude=location["longitude"],
                                                    region_id=regions_id,
                                                    zip_value=location["zip"],
                                                    ip_code=location["ip"],
                                                    )
            result["message"]="succesfully updated"
        except:
            result["message"]="an error occured"
    
    else:
        result["message"]= location.reason    
    
    return Response(result)