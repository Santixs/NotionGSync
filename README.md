# NotionGSync

NotionGSync is a project with the aim of automatizing the synchronization of the notion databases with Google Calendar and thus improve my productivity.

In Notion, I have 2 databases, one with the assignments and exams of the university and the other with the relevant appointments that I have as the student representative of my school while in Google Calendar I have my personal events. 
Thanks to this project, I can take a look at all my events in the same calendar without sacrificing the tools that notions provide.

The integration has been made using the REST API of notion and Google. For the authentication part, I have used a personal token for Notion and Oauth for google.

The next steps are to implement a 2 ways sync (from G. Calendar to Notion too) using Incremental sync and lexical analyzers to transform the titles and comments of each event into the entities of the database.

![alt text](https://github.com/Santixs/NotionGSync/blob/main/Images%20(for%20readme)/Notion.png)
![alt text](https://github.com/Santixs/NotionGSync/blob/main/Images%20(for%20readme)/Gcalendar.png)


