#! /usr/bin/env python3

import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os
print ('Content-type: text/html\n')

html="""
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
		<script>

function redirect (url) {
window.location.replace(url);
}
</script></head>
    <body onload="redirect('index.cgi')">
    </body>
    </html>"""
    
html2="""
    </body>
</html>"""

form = cgi.FieldStorage()

title = form.getfirst("clubName", "")
detail = form.getfirst("description", "")
detail = EchooFunctions.specialChara(detail)
detail = detail.replace("&","&amp;")
detail = detail.replace("\n","<p>")
detail = detail.replace("-","&mdash;")
detail = detail.replace('"',"Alt 34")
publish_time = EchooFunctions.getDateTime()
message = ""

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

userName = ""
userID = ""
admin = False
moderator = False
guest = False
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)

if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
                
htmlDirect = """<body onload="redirect('index.cgi"""
htmlDirect += """')">"""
if admin == True:
        if title.replace(" ","") == "" or detail.replace(" ","") == "":
                message += "<p>missing text</p>"
                
        else:
                try:
                        SQL = "INSERT INTO announcement(authorID, title, detail, publish_time)"
                        SQL += 'VALUES ('+str(userID)+', "'+title+'", "'+detail+'", "'+str(publish_time)+'");'
                        cursor.execute(SQL)
                        db_con.commit()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        message += "<p>Successful!</p>"
                
        print(html)
        print(htmlDirect)
        print(message)
        print(html2)

else:
        print("<h1>You arn't permited to visit this page</h1>")
        print("<a href='index.cgi'>Return</a>")

