#! /usr/bin/env python3

import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os
print ('Content-type: text/html\n')

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()
receiverID = form.getfirst('user','')
userName = ""
userID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)

admin = False
#change the status of veriable
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
#main contents to insert
friend = ""
friendList = ""
chatroom = ""
userList = []
if userID != "" and receiverID !="":
        try:
                SQL = "select u.userID, u.username, u.icon, m.detail, m.time_in,m.messageID from user as u, private_message as m where u.userID = "
                SQL+= "m.sender and m.receiver = "+str(userID)+" and m.sender = "+str(receiverID)
                SQL+= " Union select u.userID, u.username, u.icon, m.detail, m.time_in ,m.messageID from user as u, private_message as m where u.userID = "
                SQL+= "m.sender and m.receiver = "+str(receiverID)+" and m.sender = "+str(userID)
                SQL+=" Order By messageID ;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the first SQL!</p>')
                print(SQL, "Error:", e)
        else:
                if results:
                        count = 5
                        for row in results:
                                word_count = 0
                                specialChar=row[3]
                                specialChar2 = ""
                                specialChar=EchooFunctions.returnSpecialChara(specialChar)
                                for x in specialChar:
                                        if word_count<=20:
                                                specialChar2 += x
                                                word_count+=1
                                        else:
                                                specialChar2 += x +"<p>"
                                                word_count = 0
                                if count >= 5:
                                        chatroom+='<li class="chatDate">'+str(row[4])+'</li>'
                                        count=0
                                if str(row[0]) ==str(userID):
                                        count+=1
                                        chatroom+='<li class="mainUser">'+'<a href="userProfile.cgi?user='+str(row[0])+'">'+row[1]+'</a><img src="images/user/'+row[2]+'" alt="club1">'
                                        chatroom+='<br><div class="messageLine">'+specialChar2+'</div></li>'
                                else:
                                        count+=1
                                        chatroom+='<li class="otherUser"><img src="images/user/'+row[2]+'" alt="club1">'
                                        chatroom+='<a href="userProfile.cgi?userid='+str(row[0])+'">'+row[1]+'</a><br><div class="messageLine">'+specialChar2+'</div></li>'

if userID == "" or receiverID =="":
        content ="""<p>You don't have right access to this page</p>
<a href='index.cgi'></a>"""
        print(content)
print(chatroom)
