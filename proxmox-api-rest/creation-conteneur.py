import requests
import json

myparams = {'username': 'administrator@pve', 'password': 'password'}
url = "https://10.11.3.87:8006/api2/json/access/ticket"

myResponse = requests.post(url,myparams,verify=False)
cook={'PVEAuthCookie':myResponse.json()['data']['ticket']}
head={'CSRFPreventionToken':myResponse.json()['data']['CSRFPreventionToken']}

def for_post_requests(pathTo, data_to_send):
    url = f"https://10.11.3.87:8006/api2/json/{pathTo}"
    myResponse = requests.post(url,data=data_to_send,headers=head,cookies=cook,verify=False)
    data = myResponse.json()['data']
    return data

def create_ctn(jsonFile):
    with open(jsonFile, 'r', encoding='utf-8') as f:
        my_ctn = json.load(f)
        
    for ctn in my_ctn['containers'] :
        for_post_requests('nodes/pve/lxc', ctn)

create_ctn("./scripts-folder/ctn-creation.json")