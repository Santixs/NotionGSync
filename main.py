from notionsync import NotionGet, get_changes
import gcalendarsync
import os

def main():


    token_notion = os.environ.get('token_notion')
    database_id = os.environ.get('database_id')

    print("Connecting to the bbdd")

    bbdd = NotionGet(token = token_notion)
    query = {"filter": {"property": "Sync","checkbox": {"equals": True}}}
    NewestData = bbdd.query_database(database_id, query)
    bbdd.save_json("data/dataNew.json") #Aqui guardamos el json y justo después lo abrimos en notionSYnc, ver si se puede pasar como param


    if os.path.isfile('data/dataOld.json'):
        print("There is a previous record")         
        changes = get_changes() 
        print(changes)    
        service = gcalendarsync.connect()

        for event in changes["deleted"]:
            gcalendarsync.delete_event(service,event)

        for event in changes["added"]:                    
            gcalendarsync.create_event(service,event)
        
        for event in changes["modified"]:           
            gcalendarsync.update_event(service, event)

    else:
        print("There are no previous records")           
    
    os.rename('data/dataNew.json', 'data/dataOld.json')


if __name__ == "__main__":
    main()