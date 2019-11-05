#!/usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions

print ('Content-type: text/html\n')
form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()


#main contents to insert
clubID = form.getfirst('club', '4')
chatroom = ""
memberList = ""
exist = False
userName = ""
userID = ""
clubControl = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)

try:
        SQL = "SELECT u.icon, u.username, cm.detail, cm.send_time FROM user as u, club_message as cm, club_user as cu"
        SQL += " WHERE cm.clubID = cu.clubID AND cm.userID = u.userID AND cm.clubID = " + clubID
        SQL += " GROUP BY club_messageID;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
            icon = ""
            if str(row[0]) == "None":
                icon='nullicon.jpg'
            if str(row[0]) != "None":
                icon=str(row[0])

            specialChar=row[2]
            specialChar=EchooFunctions.returnSpecialChara(specialChar)
            specialChar2 = ""
            word_count = 0
            for x in specialChar:
                    if word_count<=20:
                            specialChar2 += x
                            word_count+=1
                    else:
                        specialChar2 += x +"<p>"
                        word_count = 0
            if str(row[1]) == str(userName):
                    chatroom += '<li class="chatDate">'+str(row[3])+'</li>'
                    chatroom += '<li class="mainUser">'+str(row[1])+'<img src="images/user/'+icon+' "alt="club1"><br>'
                    chatroom += '<div class="messageLineMain">'+str(specialChar2)+'</div></li>'
            if str(row[1]) != str(userName):
                    chatroom += '<li class="chatDate">'+str(row[3])+'</li>'
                    chatroom += '<li class="otherUser"><img src="images/user/'+icon+' "alt="club1">'+str(row[1])+'<br>'
                    chatroom += '<div class="messageLine">'+str(specialChar2)+'</div></li>'

chatroom += '<h1 id="current"></h1>'

print(chatroom)
