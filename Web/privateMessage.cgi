#! /usr/bin/env python3

import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os
print ('Content-type: text/html\n')

htmlOpen="""
<!doctype html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>Echooo</title>
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<!-- Stylesheets -->
		<link rel="stylesheet" href="css/normalize.css">
		<link rel="stylesheet" href="css/styles.css">
		<link rel="stylesheet" href="css/privateMessage.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
htmlOpen += EchooFunctions.setLoginStatus('index')

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
                SQL = "select userID, icon, username from user where userID = "+str(receiverID)+";"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the first SQL!</p>')
                print(SQL, "Error:", e)
        else:
                for row in results:
                        friend+='<img src="images/user/'
                        if str(row[1]) == 'None':
                                friend+='nullicon.jpg'+'" alt="club1" '
                        else:
                                friend+=str(row[1])+'" alt="club1" '
                        friend+='class="topImg"><h1><a href="userProfile.cgi?userid='+str(row[0])+'">'+row[2]+'</a></h1>'
        try:
                SQL = "select u.userID, u.username, u.icon, u.status, m.time_in from user as u, private_message as m where m.receiver = u.userID  and m.sender="+str(userID)
                SQL +=" UNION select u.userID, u.username, u.icon, u.status, m.time_in from user as u, private_message as m "
                SQL +="where m.sender = u.userID  and m.receiver="+str(userID)+" Group by u.userID Order By time_in;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the first SQL!</p>')
                print(SQL, "Error:", e)
        else:
                if results:
                        for row in results:
                                if str(row[0]) not in userList:
                                        userList.append(str(row[0]))
                                        friendList+='<li class="userOnList"><div class="groupTogether"><img src="images/user/'
                                        if str(row[2]) == 'None':
                                                friendList+='nullicon.jpg'+'" alt="club1">'
                                        else:
                                                friendList+=str(row[2])+'" alt="club1">'
                                        friendList+='<a href="privateMessage.cgi?user='+str(row[0])+'#current">'+row[1]+'</a></div><span class="status">'+row[3]+'</span></li>'
        try:
                SQL = "select u.userID, u.username, u.icon, u.status from user as u, friend_list as f"
                SQL += " where f.friend_userID = u.userID and f.userID = "+str(userID)+";"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the first SQL!</p>')
                print(SQL, "Error:", e)
        else:
                if results:
                        for row in results:
                                if str(row[0]) not in userList:
                                        userList.append(str(row[0]))
                                        friendList+='<li class="userOnList"><div class="groupTogether"><img src="images/user/'
                                        if str(row[2]) == 'None':
                                                friendList+='nullicon.jpg'+'" alt="club1">'
                                        else:
                                                friendList+=str(row[2])+'" alt="club1">'
                                        friendList+='<a href="privateMessage.cgi?user='+str(row[0])+'">'+row[1]+'</a></div><span class="status">'+row[3]+'</span></li>'
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
                                        chatroom+='<li class="mainUser">'+'<a href="userProfile.cgi?userid='+str(row[0])+'">'+row[1]+'</a><img src="images/user/'+row[2]+'" alt="club1">'
                                        chatroom+='<br><div class="messageLine">'+specialChar2+'</div></li>'
                                else:
                                        count+=1
                                        chatroom+='<li class="otherUser"><img src="images/user/'+row[2]+'" alt="club1">'
                                        chatroom+='<a href="userProfile.cgi?userid='+str(row[0])+'">'+row[1]+'</a><br><div class="messageLine">'+specialChar2+'</div></li>'

html="""<div class="toprow">"""
html += friend + "</div>"
html+="""<!-- the whole container -->
<script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
<script language="javascript" type="text/javascript">

var timeout = setInterval(reloadChat, 1500);    
function reloadChat () {

     $('#chatroom').load('privateChatroom.cgi?"""
html+="user="+str(receiverID)
html+="""');
}

function SubmitFormData(){
var receive = $("#receive").val();
var comment = $("#comment").val();
$.post("sendPMessage.cgi", { receive: receive, comment: comment},
function(data) {
 $('#sendMessageForm')[0].reset();
});
}
</script>
		<article class="CenterPart">"""
html+="""<div class="memberList">
				<h1> Users </h1>
				<ul>"""
html+=friendList
html+="""</ul>
			</div>
        <div class="chatroom">
					<ul><div id="chatroom">"""
html+=chatroom
html+="""</div><h1 id="current"></h1></ul>
					<form id="sendMessageForm" method="post">"""
html+='<input type="hidden" name="receive" id="receive" value="'+str(receiverID)+'"/>'
html+="""							<textarea name="comment" id="comment"></textarea>
							<button type="submit" id="submitFormData" onclick="SubmitFormData();">Send</button>
					</form>
        </div>

			</article>

		<!-- footer -->
		"""
html += EchooFunctions.setFooter()
html +="""
	</div>
	</body>
</html>
"""

#print out html
print(htmlOpen)
if userID == "" or receiverID =="":
        content ="""<p>You don't have right access to this page</p>
<a href='index.cgi'></a>"""
print(html)
