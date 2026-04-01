import requests

### connection / authentication

def for_connection():
    myparams = {'username': 'administrator@pve', 'password': 'password'}
    url = "https://10.11.3.87:8006/api2/json/access/ticket"

    myResponse = requests.post(url,myparams,verify=False)
    cook={'PVEAuthCookie':myResponse.json()['data']['ticket']}
    head={'CSRFPreventionToken':myResponse.json()['data']['CSRFPreventionToken']}

    return cook,head

def for_get_requests(pathTo):
    url = f"https://10.11.3.87:8006/api2/json/{pathTo}"
    info_con = for_connection()
    myResponse = requests.get(url,headers=info_con[1],cookies=info_con[0],verify=False)
    data = myResponse.json()['data']
    return data

def for_post_requests(pathTo):
    url = f"https://10.11.3.87:8006/api2/json/{pathTo}"
    info_con = for_connection()
    myResponse = requests.post(url,headers=info_con[1],cookies=info_con[0],verify=False)
    data = myResponse.json()['data']
    return data

data_noeud = for_get_requests('nodes')[0]
data_lxc = for_get_requests('nodes/pve/lxc')
data_users = for_get_requests('access/users')

def get_node_info(data):
    print(
    f"Noeud : {data['node']}\nCPU : {data['maxcpu']}\nMemoire disponible : {int(data['maxmem'])/1024}\nMemoire utilisee : {int(data['mem'])/1024}"
)
    
def get_lxc_info(data):
    for i in data:
        print(
            f"Conteneur : {i['name']}\nConteneur ID: {i['vmid']}\nConteneur status : {i['status']}"
            )

def get_users_id(data):
    for i in data:
        print(f"Users ID : {i['userid']}")

def lxc_start(data_lxc):
    conteneurID = [i['vmid'] for i in data_lxc]
    for i in conteneurID:
         for_post_requests((f"nodes/pve/lxc/{i}/status/start"))
         print(f"Conteneur {i} started")

    print("\nStarting end")

def lxc_stop(data_lxc):
    conteneurID = [i['vmid'] for i in data_lxc]
    for i in conteneurID:
         for_post_requests((f"nodes/pve/lxc/{i}/status/stop"))
         print(f"Conteneur {i} stopped")
    print("\nStoping end")

# get_node_info(data_noeud)
#get_lxc_info(data_lxc)
# get_users_id(data_users)

lxc_start(data_lxc)
#lxc_stop(data_lxc)