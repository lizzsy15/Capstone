#! /usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
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
    <link rel="stylesheet" href="css/article.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
html +=EchooFunctions.setLoginStatus('news')
html+= """{message}

		<!-- footer -->
	{footer}
	</div>
	</body>
</html>

"""

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
newsID = form.getfirst('newsID', '1')

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

#main contents to insert
message = ""
footer = EchooFunctions.setFooter()

try:
        SQL = "SELECT n.title, n.detail,n.publish_time,u.username,n.icon FROM news AS n, user AS u WHERE authorID=userID AND newsID = "
        SQL += newsID + ";"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                title = ""
                wordCount = 0
                spaceCount = 0
                for x in str(row[0]):
                        if x == " ":
                                title+=x
                        if spaceCount >= 20:
                                title += " "
                                spaceCount = 0
                        title+=x
                        spaceCount += 1
                message += '<h3>'+title+'</h3>'
                message += '<h6>'+row[3]+'<span class="date">'+str(row[2])+'</span></h6>'
                message += '<article class="content"><img src="images/news/'+row[4]+'" alt="article1"><br>'
                message += '<p>'+row[1]+'</p></article>'

#print out html
print(html.format(message = message, footer = footer))
