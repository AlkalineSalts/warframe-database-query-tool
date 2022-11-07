import urllib3
import certifi
import sys
import os
import time
import json

https = urllib3.PoolManager(ca_certs=certifi.where())

#Represents the amount of seconds that a store will be valid for in seconds

_web_base_url = 'http://drops.warframestat.us'
def _getJsonFromWeb(endpoint):
    url = _web_base_url + endpoint
    try:
        r = https.request('GET', url)
        if (r.status == 200):
            return r.data.decode('utf-8')
        else:
            raise LookupError("Return code was not 200, was http code: " + r.status)
    except urllib3.exceptions.MaxRetryError:
        raise LookupError("Could not connect to website (" + _web_base_url + ").")
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
    global_file_path = sys.argv[0]
    global_file_path = os.path.split(global_file_path)[0]
    file_path = os.path.join(global_file_path, "DropTablesStore.json")
    hashes_file_path = os.path.join(global_file_path, "Info.json")
    json_data = None
    if not os.path.exists(file_path) or not os.path.exists(hashes_file_path):
        json_data = _getJsonFromWeb("/data/all.json")
        hashes_json = _getJsonFromWeb("/data/info.json")
        _saveJson(file_path, json_data)
        _saveJson(hashes_file_path, hashes_json)
    else:
        try:
            hash_web_json = _getJsonFromWeb("/data/info.json")
            hash_web_dict = json.loads(hash_web_json)
            hash_file_dict = json.loads(_readJsonFromFile(hashes_file_path))
            if hash_web_dict['hash'] != hash_file_dict['hash'] or forceUpdate:
                json_data = _getJsonFromWeb("/data/all.json")
                _saveJson(file_path, json_data)
                _saveJson(hashes_file_path, hash_web_json)
        except LookupError:
            print("Could not access web, using cached data.")

    #Can only be in this state if the store file exists and is still valid (or cannot connect)
    if json_data is None:
        json_data = _readJsonFromFile(file_path)
    return json.loads(json_data)

    
    
