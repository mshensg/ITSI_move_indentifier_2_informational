import requests,json,time
from urllib3.exceptions import InsecureRequestWarning;
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning);

server="----"
user="----"
password="----"
url="https://{}:8089/servicesNS/nobody/SA-ITOA/itoa_interface/entity".format(server)
headers = {"Content-Type":"application/json"}
move_field = "-----"
params={
    "output_mode":"json",
    "filter":json.dumps({
        move_field:{"$regex":".*"}
    }),
    "fields":"_key,title,identifier.fields,informational.fields"
}
response = requests.get(url,auth=(user,password),headers=headers,params=params,verify=False)
results = response.json()

for item in results:
    if move_field in item["identifier"]["fields"]:
        print("updating item {} with key {}".format(item["title"],item["_key"]))
        key = item["_key"]
        update_url="https://{}:8089/servicesNS/nobody/SA-ITOA/itoa_interface/entity/{}".format(server,key)
        update_params={
            "output_mode":"json",
            "is_partial_data":1
        }
        indentify_fields=[i for i in item["identifier"]["fields"] if i!=move_field]
        informational_fields=[i for i in item["informational"]["fields"]]
        informational_fields.append(move_field)
        update_data=json.dumps({
            "identifier": {"fields": indentify_fields},
            "informational":{"fields":informational_fields}
        })
        response = requests.post(update_url,auth=(user,password),headers=headers,params=update_params,data=update_data,verify=False)
        if response.status_code in [200,201]:
            print(response.json())
        else:
            print("failed")
            print(response.content)
