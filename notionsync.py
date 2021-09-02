import json
from os import name
import requests
from requests.models import Response
from event import event

database_url = "https://api.notion.com/v1/databases/"

class NotionGet:    

    def __init__(self, token):   
        self.token = token
        self.header = {"Authorization":self.token,
                       "Notion-Version":"2021-08-16"}
                        #,Content-Type": "application/json" 
        self.response = None

    def query_database(self, database_id, query):
        url = database_url + database_id + "/query"
        self.response = requests.post(url, headers = self.header, data=query)    
        return self.response  

    def save_json(self,name):
        with open(name, 'w') as outfile:
            json.dump(self.response.json(), outfile, indent=4, sort_keys=True)
  


   

def get_events(origin):         
    return [event(i) for i in origin["results"] if i['properties']['Date']['date'] is not None] 
    #To create an event, at least, it has to have a date

def get_changes():
            
    with open("data/dataNew.json") as f:
        NewestData = json.load(f)
    
    with open("data/dataOld.json") as f2:
        OldestData = json.load(f2)
    
    NewEv = get_events(NewestData)
    OldEv = get_events(OldestData)       

    added =  [x for x in NewEv if x not in OldEv]
    deleted = [x for x in OldEv if x not in NewEv]

    modified=[]
    for e in added:
        for e2 in deleted:
            if e.eventId == e2.eventId and e is not e2: 
                modified.append(e)
                added.remove(e)
                deleted.remove(e2)
                
    return {"added": added, "deleted": deleted, "modified":modified}

#Create a dictionary with the objects of class 'element' which contains the properties (name, type, subject, ...)

