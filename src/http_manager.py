import os
import json
import dotenv
import requests

dotenv.load_dotenv()

def build_url(path):
    return f'https://discord.com/api/v9/{path}'

def headers():
    try:
        return {'authorization': 'Bot ' + os.getenv('DISCORD_TOKEN')}
    except TypeError:
        raise PermissionError('No bot token in .env found.')

def get_request(path, params=None):
    '''Retuns a <dict> of a API call, whereas path is the URL path after the base URL'''
    response = requests.get(build_url(path), headers=headers(), params=params).text
    
    return json.loads(response)

def post_request(path, data: dict=None, params_data: dict=None, json_data: dict=None):
    '''Send a get request with a path & data, returns its response'''
    response = requests.post(build_url(path), headers=headers(), data=data, params=params_data, json=json_data)

    try:
        return json.loads(response.text)
    except AttributeError:
        return json.loads(response.json)

def put_request(path):
    '''Send a put request with a path, returns its response code'''
    response = requests.put(build_url(path), headers=headers())

    return response.ok

def delete_request(path):
    '''Send a delete request with a path, returns its response code'''
    response = requests.delete(build_url(path), headers=headers())

    return response.ok

def patch_request(path, data: dict):
    '''Send a patch request with a path, returns its response code'''
    response = requests.patch(build_url(path), headers=headers(), json=data)

    return response.ok