#! /usr/bin/env python3
print('Content-type: text/html\n')

import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os

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
		<link rel="stylesheet" href="css/createBoard.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""

string = "i494f18_team34"
dbpw = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=string, passwd=dbpw, db=string)
cursor = db_con.cursor()

html += EchooFunctions.setLoginStatus('board')
userName = ""
userID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
admin = False
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
if admin == True:
    avbeghj = EchooFunctions.getUserID(cursor, userName)
    html+="""		<!-- Log in box-->
                    <article class="block">
          <h1>Create Board </h1>
          <div class="form">
            <form action="boardUpload.php?avbeghj="""
    html += str(avbeghj)
    html+='" method="post" enctype="multipart/form-data">'
    html+="""<div class="uploadImage">
                <img src="images/clubIcon.png" alt="sampleIcon"><br>
                <input type = "file" name = "image" />
              </div>
              <div class="infoBlock">
                  <p>Board Name: <span class="in1"><input type="text" name="boardName"></span></p>
                  <p>Platform: <span class="in2"><select name="platform">
                    <option value="pc">PC</option>
                    <option value="PS4">PS4</option>
                    <option value="XBOX">XBOX</option>
                    <option value="switch">SWITCH</option>
                    <option value="mobile">MOBILE</option>
                  </select></span></p>
                  <a href="boardMain.cgi">Cancel</a>
                  <input type="submit" value="Upload Image" name="submit">
              </div>
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

    form = cgi.FieldStorage()

    print(html)
    
else:
    print("<h1>You arn't permit to visit this page</h1>")
    print("<a href='index.cgi'>Return</a>")
    
