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
    
    added = [];     modified = [];    removed= []

    for ne in NewEv: 
        j = 0; found = False

        while not found and j < len(OldEv) :    
            oe = OldEv[j]; j+=1
            if ne == oe:  OldEv.remove(oe); found = True; 
            elif ne.eventId == oe.eventId: OldEv.remove(oe); modified.append(ne); found = True;       
            
        if not found: added.append(ne)

    removed.extend(OldEv)

#     ---------- For debugging purposes ---------#     
#     aa = []; mm = []; rr = []
#     for e in added: aa.append(e.name)
#     for e in modified: mm.append(e.name)
#     for e in removed: rr.append(e.name)
#     print(f"added: {aa} modified {mm} removed: {rr}")

    return {"added": added, "deleted": removed, "modified":modified}
