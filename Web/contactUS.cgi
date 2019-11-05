#!/usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

#variables
userName = ""
userID = ""
content=""
navigation = EchooFunctions.setLoginStatus('index')
footer = EchooFunctions.setFooter()

if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)

guest = False
if "echooUser" not in str(os.environ):
        guest = True

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
				<link rel="stylesheet" href="css/signUp.css">
    <link rel="stylesheet" href="css/login.css">
		<link rel="stylesheet" href="css/report.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>

	{navigation}

    <article class="block">
			<h1 class="sr-only">Report</h1>
			<div class="signUpBox">
				<h2>Contact US</h2>
          <form method="post" action="sendContactUS.cgi">"""


html+="""            Your email: <input type="text" name = "email"></input><br>
                        Subject: <input type="text" name = "subject"></input><br>
            <textarea name="detail" placeholder="content" class="contentInput"></textarea>
            <button type="submit" class="firstbt">Submit</button>
          </form>
        </div>
		</article>

		<!-- footer -->
                {footer}
	</div>
	</body>
</html>

"""
print(html.format(navigation = navigation, footer = footer))
