class event:   
    def __init__(self, element): 

        try:        self.subject = element['properties']['Subject']["select"]['name']
        except:     self.subject = "No name"

        try:        self.type = element['properties']['Type']["select"]['name']
        except:     self.type = " "
            
        try:        self.name = element['properties']['Name']["title"][0]["text"]["content"]
        except:     self.name = " "        

        try:        self.comments = element['properties']['Comments']["rich_text"][0]["text"]["content"]
        except:     self.comments = " "

        try:        self.status = element['properties']['Status']['multi_select'][0]['name']
        except:     self.status = " "

        self.eventId = element['id'].replace('-','')       
        self.date = element['properties']['Date']['date']["start"]
   
   
    def __eq__(self, e):
            if not isinstance(self,e): return False
            return self.subject == e.subject and self.type == e.type and e.name == self.name and self.date == e.date and self.comments==e.comments
   
    def __hash__(self):       
        return hash((self.subject, self.type, self.name, self.date, self.comments))