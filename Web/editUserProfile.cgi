#! /usr/bin/env python3
print('Content-type: text/html\n')

import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os

html="""
    <!doctype html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>I360 Project3</title>
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<!-- Stylesheets -->
		<link rel="stylesheet" href="css/normalize.css">
		<link rel="stylesheet" href="css/styles.css">
		<link rel="stylesheet" href="css/signUp.css">
    <link rel="stylesheet" href="css/login.css">
    <link rel="stylesheet" href="css/editPost.css">
    <link rel="stylesheet" href="css/editUserProfile.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>

	{login}

		<!-- Log in box-->
		<article class="block">
			<h1 class="sr-only">Edit Profile</h1>
				<h2>Edit Profile</h2>
          <form action="editUserProfileConfirm.php?user={userID}" method="post" enctype="multipart/form-data">
            <div class="uploadImage">
              Icon: <input type = "file" name = "image" />
            </div>
            <p>Nickname: <input type="text" name="nicknameEdit" placeholder="{nickname}" value="{nickname}"></p>
            <p>Region: <input type="text" name="regionEdit" placeholder="{region}" value="{region}"></p>
            <p>Gender: <select name="genderEdit">
            {gender}
            </select></p>
            <p>Date of Birth: <input type="date" name="dobEdit"
            value="{dob}"
            min="1950-01-01" max="2018-12-31"></p>
            <p>Description: <textarea name="descriptionEdit" placeholder="{description}" value="{description}" class="formContent">{description}</textarea></p>
            <p>Facebook Link (included http://www.): <input type="text" name="facebookEdit" placeholder="{facebook}" value="{facebook}"></p>
            <p>Twitter Link (included http://www.): <input type="text" name="twitterEdit" placeholder="{twitter}" value="{twitter}"></p>
            <a href="userProfile.cgi?userid={userID}">Cancel</a>
            <button type="submit" class="firstbt">Submit</button>
          </form>
		</article>

		<!-- footer -->
		{footer}
	</div>
	</body>
</html>"""

form = cgi.FieldStorage()

string = "i494f18_team34"
dbpw = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=string, passwd=dbpw, db=string)
cursor = db_con.cursor()
ID = form.getfirst("user","")
userName = ""
userID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
        
login = EchooFunctions.setLoginStatus('index')
nickname = ""
region = ""
gender=""
dob=""
description = ""
facebook = ""
twitter = ""
discord = ""
footer = EchooFunctions.setFooter()


try:
        SQL = "select * from user where userID = "
        SQL += ID + ";"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
    for row in results:
            nickname =row[4]
            region = row[5]
            if str(row[6]) == "F":
                gender = '<option value="F">F</option><option value="M">M</option>'
            else:
                gender = '<option value="M">M</option><option value="F">F</option>'
            dob=row[7]
            description = row[8]
            facebook = row[13]
            twitter = row[14]
            discord = row[15]

#if str(ID) != str(userID):
    #html="<html><head></head><body><p>You don't have correct access to this page</p></body></html>"
    #print(html)
#else:
print(html.format(userID = userID, login=login, nickname = nickname, region = region, gender = gender, dob = dob,description = description, facebook = facebook, twitter = twitter, footer = footer))

