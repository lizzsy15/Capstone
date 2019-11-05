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
    <link rel="stylesheet" href="css/infoIN.css">
    <link rel="stylesheet" href="css/memberRole.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
htmlOpen += EchooFunctions.setLoginStatus('index')
html="""<!-- Log in box-->
		<article class="block">
      <div class="infoBlock">
        <form method="post" action="#" class="infoBlock">
          <h2>Friend List:</h2>
          {content}        </form>
      </div>
              <form method="post" action="#" class="infoBlock">
          <h2>BlackList:</h2>
          {blackListContact}        </form>
      </div>
		</article>"""


form = cgi.FieldStorage()

#database connection
ID = form.getfirst('user','')
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()
userName = ""
userID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
if "echooUser" in str(os.environ):
        userID = EchooFunctions.getUserID(cursor, userName)

admin = False
moderator = False
guest = False


html+="""{footer}
	</div>
	</body>
</html>"""

#change the status of veriable
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
if userName == "":
        guest = True

#main contents to insert
content = ""
blackListContact=""
footer = EchooFunctions.setFooter()
if userID != "" and ID != "":
        #friend list
        try:
                SQL = "select u.userID, u.icon, u.username from friend_list as f, user as u where f.friend_userID = u.userID and f.userID = '" + str(userID) + "';"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                
                print(SQL, "Error:", e)
        else:
                
                if results:
                        for row in results:
                                if str(row[1]) == "None":
                                        content+="<p><img src='images/user/nullicon.jpg' alt='user'></img>"
                                else:
                                        content+="<p><img src='images/user/"+row[1]+"' alt='user'></img>"
                                content+="<a href='userProfile.cgi?userid="+str(row[0])+"'>"
                                content+=row[2]+"</a><a href='BlackList.cgi?action=BlackList&user="+str(row[0])
                                content+="'>BlackList</a><a href='privateMessage.cgi?user="+str(row[0])
                                content+="'>Send Message</a></p>"

        #blacklist
        try:
                SQL = "select u.userID, u.icon, u.username from black_list as b, user as u where b.block_userID = u.userID and b.userID = '" + str(userID) + "';"
                cursor.execute(SQL)
                results = cursor.fetchall()             
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                
                print(SQL, "Error:", e)
        else:
                if results:
                        for row in results:
                                if str(row[1]) == "None":
                                        blackListContact+="<p><img src='images/user/nullicon.jpg' alt='user'></img>"
                                else:
                                        blackListContact+="<p><img src='images/user/"+str(row[1])+"' alt='user'></img>"
                                blackListContact+="<a href='userProfile.cgi?userid="+str(row[0])+"'>"
                                blackListContact+=row[2]+"</a><a href='removeBlackList.cgi?action=removeBlackList&user="+str(row[0])
                                blackListContact+="'>Remove</a></p>"
                
else:
        content+="<p>You dont have right access</p>"
        content+="<a href='index.cgi'>Return</a>"


#print out html
print(htmlOpen)
print(html.format(content = content, blackListContact = blackListContact, footer = footer))
