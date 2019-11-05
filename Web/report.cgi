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
report_userID = form.getfirst('user','')
selection = form.getfirst('type','')
club = form.getfirst('club','')
post = form.getfirst('postID','')
board = form.getfirst('board','')
userName = ""
userID = ""
content=""
navigation = EchooFunctions.setLoginStatus('index')
footer = EchooFunctions.setFooter()

if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
if str(report_userID) == str(userID):
        isUser = True

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
				<h2>Report</h2>
          <form method="post" action="sendReport.cgi?{content2}">"""
if selection == "user":
        html+='<input type="hidden" name="user" value="'+str(report_userID)+'"/>'
                
if selection == "club":
        html+='<input type="hidden" name="club" value="'+str(club)+'"/>'
                
if selection == "post":
        html+='<input type="hidden" name="postID" value="'+str(post)+'"/>'


html+="""            <p>Report {content}</p>
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



content2 = ""
if selection == "user":
        if report_userID != "":
                content2+="type=user&"
                try:
                        SQL = "select username from user where userID = "+str(report_userID)+";"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the first SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        content += "User "+results[0][0]
        else:
                content += "You have wrong access to this page"

if selection == "club":
        if club != "":
                content2+="type=club&"
                try:
                        SQL = "select clubname from club where clubID = "+str(club)+";"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the first SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        content += "Club "+results[0][0]
        else:
                content += "You have wrong access to this page"

if selection == "post":
        if post != "":
                content2+="type=post&"
                try:
                        SQL = "select title from post where postID = "+str(post)+";"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the first SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        count = 0
                        title=""
                        for x in results[0][0]:
                                if count <= 30:
                                        title += str(x)
                                        count +1
                        content += "Post '"+title+"'"
        else:
                content += "You have wrong access to this page"
if selection == "":
        content += "You have wrong access to this page"
                

content2 += "postID="+str(post)+"&user="+str(report_userID)+"&club="+str(club)
print(html.format(navigation = navigation, content=content, content2=content2, footer = footer))
