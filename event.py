class event:   
    def __init__(self, element): 


        self.icon = ""
        self.eventId = element['id'].replace('-','')       
        self.date = element['properties']['Date']['date']["start"]
   
        try:        self.subject = element['properties']['Subject']["select"]['name']
        except:     self.subject = ""

        try:        self.type = element['properties']['Type']["select"]['name']
        except:     self.type = " "
            
        try:        self.name = element['properties']['Name']["title"][0]["text"]["content"]
        except:     self.name = " "        

        try:        self.comments = element['properties']['Comments']["rich_text"][0]["text"]["content"]
        except:     self.comments = " "

        try:        self.status = element['properties']['Status']['multi_select'][0]['name']
        except:     self.status = " "

        self.endDate = element['properties']['Date']['date']["end"]
        if self.endDate == None:   self.endDate = self.date

        self.progress = element['properties']['Progress']['number']; 
        if self.progress == None: self.progress = -1
        


    def __eq__(self, e):
            if not isinstance(self,type(e)): return False
            return self.subject == e.subject and self.type == e.type and e.name == self.name and self.date == e.date and self.comments==e.comments and self.progress == e.progress and self.status == e.status and self.endDate == e.endDate
   
    def __hash__(self):       
        return hash((self.subject, self.type, self.name, self.date, self.comments, self.status, self.endDate))