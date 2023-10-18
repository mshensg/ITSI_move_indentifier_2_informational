import requests,json,time
from urllib3.exceptions import InsecureRequestWarning;
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning);

server="----"
user=user
password=password
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

bulk_job=[]
for item in results:
    if move_field in item["identifier"]["fields"]:
        key = item["_key"]
        indentify_fields=[i for i in item["identifier"]["fields"] if i!=move_field]
        informational_fields=[i for i in item["informational"]["fields"]]
        informational_fields.append(move_field)
        bulk_job.append({
            "_key": key,
            "identifier": {"fields": indentify_fields},
            "informational":{"fields":informational_fields}
        })

update_url="https://{}:8089/servicesNS/nobody/SA-ITOA/itoa_interface/entity/bulk_update".format(server)
update_params={
    "output_mode":"json",
    "is_partial_data":1
}

update_data=json.dumps(bulk_job)
response = requests.post(update_url,auth=(user,password),headers=headers,params=update_params,data=update_data,verify=False)
print(response.json())
  
