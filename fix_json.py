import json
import pprint
from datetime import datetime


f = json.load(open("./animals.json","r"))

def fix_date(string):
    """input : MM/DD/YYYY {%H:%M:%S} 
    output : YYYY-MM-DD %H:%M:%S
    """
    if not string:
        return "0000-00-00 00:00:00"
    try:
        date_obj = datetime.strptime(string, "%m/%d/%Y")
    except ValueError:
        date_obj = datetime.strptime(string, "%m/%d/%Y %H:%M:%S")
        
    return datetime.strftime(date_obj, "%Y-%m-%d %H:%M:%S")


new_doc = open("./animals_edited.sql", "w+")
i = 1
for doc in f:
    doc["date_started"] = fix_date(doc["date_started"])
    doc["date_closed"] = fix_date(doc["date_closed"])
    doc["resolution_action_updated"] = fix_date(doc["resolution_action_updated"])
    doc["zip_code"] = doc["site_city_zip"].split(" ")[-1].strip()
    doc["site_city"] = " ".join(doc["site_city_zip"].split(" ")[:-1])

    keys = ",".join(map(str,doc.keys()))
    if i > 1:
        if keys != old_keys:
            raise KeyError()
    

    values = doc.values()
    for index in range(len(values)):
        if "'" in str(values[index]):
            values[index] = values[index].replace("'","''")
    values = "','".join(map(str,doc.values()))

    new_line = "INSERT INTO incidents({}) VALUES ('{}');\n".format(keys, values)
    new_doc.write(new_line)
    old_keys = keys
    i += 1
new_doc.close()
