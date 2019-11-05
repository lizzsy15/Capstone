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
		<link rel="stylesheet" href="css/privateMessageList.css">
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


html="""<div class="toprow">
			<h1>Recent Message</h1><a href="userProfile.cgi?userid={userID}">Return</a>
		</div>
    <!-- the whole container -->
		<article class="CenterPart">
			<ul>
{content}
			</ul>
			</article>
"""
html += """

		<!-- footer -->
                {footer}
	</div>
	</body>
</html>
"""



#main contents to insert
content = ""
footer = EchooFunctions.setFooter()

if userID != "":
        try:
                SQL = "select u.userID, u.username, u.icon, m.detail, m.time_in from user as u, private_message as m"
                SQL +=' where m.receiver = u.userID and m.sender='+str(userID)+' UNION select u.userID, u.username, u.icon, m.detail, m.time_in '
                SQL +='from user as u, private_message as m where m.sender = u.userID  and m.receiver=' + str(userID)
                SQL += ' Group by u.userID Order By time_in desc;'
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the first SQL!</p>')
                print(SQL, "Error:", e)
        else:
                if results:
                        userList = []
                        for row in results:
                                
                                if str(row[0]) not in userList:
                                        userList.append(str(row[0]))
                                        content+="<li><a href='privateMessage.cgi?user="+str(row[0])+"#current'><div class='column'><div class='row'>"
                                        content+='<div class="sender"><img src="images/user/'
                                        if str(row[2]) == "None":
                                                content+= 'nullicon.jpg'
                                        else:
                                                content+=str(row[2])
                                        content+='" alt="user" class="topImg"><h1>'+str(row[1])
                                        content+='</h1></div><h6>'+str(row[4])+'</h6></div><div class="detail"><p>'+str(row[3])
                                        content+='</p></div></div></a></li>'


#print out html
print(htmlOpen)
if userID == "":
        content ="""<p>You dont have right access to this page</p>
<a href='index.cgi'></a>"""
print(html.format(userID = userID, content = content, footer = footer))
