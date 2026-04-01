import requests
import json
# import sys

# def for_connection():
myparams = {'username': 'administrator@pve', 'password': 'password'}
url = "https://10.11.3.87:8006/api2/json/access/ticket"

myResponse = requests.post(url,myparams,verify=False)
cook={'PVEAuthCookie':myResponse.json()['data']['ticket']}
head={'CSRFPreventionToken':myResponse.json()['data']['CSRFPreventionToken']}

def for_post_requests(pathTo, user_data):
    url = f"https://10.11.3.87:8006/api2/json/{pathTo}"
    myResponse = requests.post(url, data=user_data, headers=head,cookies=cook,verify=False)
    data = myResponse.json()['data']
    return data

def for_del_requests(pathTo):
    url = f"https://10.11.3.87:8006/api2/json/{pathTo}"
    myResponse = requests.delete(url,headers=head,cookies=cook,verify=False)
    data = myResponse.json()['data']
    return data

def create_user(jsonFile):
    with open(jsonFile, 'r', encoding='utf-8') as f:
        my_users = json.load(f)
    for user in my_users:
        if for_post_requests('access/users', user):
            print(f"OK. User {user['userid']} created !\n")

def delete_user(userid):
    if for_del_requests(f'access/users/{userid}'):
        print(f"OK. User {userid} deleted !\n")

create_user("./scripts-folder/users-creation-type.json")
#delete_user('user2@pve')