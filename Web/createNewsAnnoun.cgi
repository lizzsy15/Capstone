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
    <link rel="stylesheet" href="css/createClub.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
htmlOpen += EchooFunctions.setLoginStatus('index')
html="""{content}"""


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
if "echooUser" in str(os.environ):
        userID = EchooFunctions.getUserID(cursor, userName)
admin = False
moderator = False
guest = False
selection = form.getfirst('type', '')
dateTime = EchooFunctions.getDateTime()


html += """

		<!-- footer -->
                {footer}
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
commentContent = ""
footer = EchooFunctions.setFooter()

if admin:
        if selection == 'news':
                content += """		<!-- Log in box-->
                        <article class="block">
              <h1>Create News Article </h1>
                                <form action="createNewsArticle.php" method="post" enctype="multipart/form-data">
                                                picture: <input type = "file" name = "image" />
              <div class="infoBlock">
              <input type="hidden"  name="userID" value"""
                content+='="'+str(userID)+'">'
                content+= """<input type="hidden"  name="dateTime" value"""
                content+='="'+str(dateTime)+'">'
                content+="""<p>title: <span class="in1"><input type="text" name="clubName" class="clubName"></span></p>
                  <p>Content: <span class="in5"><textarea name="description" class="description"></textarea></p>
                                                <a href="news_main.cgi">Cancel</a>
                                                <input type="submit" value="Create" name="submit">
              </div>
                                        </form>
                        </article>"""

        if selection == 'announ':
                        content += """		<!-- Log in box-->
                        <article class="block">
              <h1>Create News Announcement </h1>
                                <form action="createNewsAnnouncement.cgi" method="post">
              <div class="infoBlock">
                  <p>title: <span class="in1"><input type="text" name="clubName" class="clubName"></span></p>
                  <p>Content: <span class="in5"><textarea name="description" class="description"></textarea></p>
                                                <a href="index.cgi">Cancel</a>
                                                <input type="submit" value="Create" name="submit">
              </div>
                                        </form>
                        </article>"""
if admin == False:
        content += """<p>You dont have right access to this page</p>
					<a href="index.cgi">Return</a>"""
        

#print out html
print(htmlOpen)
print(html.format(content = content, footer = footer))




