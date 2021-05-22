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
    print('jestem w execute')

    return requests.get(url=url, timeout=5)




@api_view(['GET'])
def check_the_location(request):
    """ komentarz """

    result = {
        'message': None,
        'status': None,
        'location': None,
    }

    location = execute_IP_search(ip='8.8.8.8')

    result['message'] = 'There was a problem with send request'
    result['status'] = location.status_code

    if location.status_code in [200, 201, 202]:
        location = location.json()
        result['location'] = location
        print(location)
        result['message'] = 'OK'

    return Response(result)