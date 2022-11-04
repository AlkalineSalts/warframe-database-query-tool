import urllib3
import certifi
import sys
import os
import time
import json

https = urllib3.PoolManager(ca_certs=certifi.where())

#Represents the amount of seconds that a store will be valid for in seconds
store_time = 3600

def _getJsonFromWeb():
    try:
        r = https.request('GET', 'http://drops.warframestat.us/data/all.json')
        if (r.status == 200):
            return r.data.decode('utf-8')
        else:
            raise LookupError("Return code was not 200, was http code: " + r.status)
    except urllib3.exceptions.MaxRetryError:
        raise LookupError("Could not connect to website.")
def _saveJson(file_path, Json_to_save):
    file = open(file_path, 'w')
    file.write(Json_to_save)
    file.close()
def _readJsonFromFile(file_path):
    file = open(file_path, 'r')
    data = file.read()
    file.close()
    return data

#Returns a loaded json object
def getJson(forceUpdate=False):
    #Sets up the file_path so that this will work no matter where this file is called from
    file_path = sys.argv[0]
    file_path = os.path.split(file_path)[0]
    file_path = os.path.join(file_path, "DropTablesStore.json")
    json_data = None
    if not os.path.exists(file_path):
        json_data = _getJsonFromWeb()
        _saveJson(file_path, json_data)
    else:
        lastEdit = os.stat(file_path).st_mtime
        systime = time.time()
        if (systime >= lastEdit + store_time) or forceUpdate:
            json_data = _getJsonFromWeb()
            _saveJson(file_path, json_data)

    #Can only be in this state if the store file exists and is still valid
    if json_data is None:
        json_data = _readJsonFromFile(file_path)
    return json.loads(json_data)

    
    
