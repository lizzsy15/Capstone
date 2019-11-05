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
		<link rel="stylesheet" href="css/infoIN.css">
		<link rel="stylesheet" href="css/createClub.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
form = cgi.FieldStorage()
string = "i494f18_team34"
dbpw = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=string, passwd=dbpw, db=string)
cursor = db_con.cursor()

html += EchooFunctions.setLoginStatus('club')
userName = ""
userID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
admin = False
userConfirm = False
userList=[]
selection = form.getfirst('selection','')
clubID = form.getfirst('club','')
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
        try:
                SQL = "SELECT userID from user;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
        else:
                for user in results:
                        userList.append(str(user[0]))
        if str(userID) in userList:
                userConfirm = True
        
                
        
if admin==True or userConfirm==True:
        if selection != "edit":
                avbeghj = EchooFunctions.getUserID(cursor, userName)
                html+="""	
                <!-- Log in box-->
                                <article class="block">
                      <h1>Create Club </h1>
                      <div class="form">
                        <form action="clubUpload.php"""
                html+='" method="post" enctype="multipart/form-data">'
                html+="""<img src="images/clubIcon.png" alt="sampleIcon"><br>
                      <input type = "file" name = "image" class="imageUpload"/>
                      <div class="infoBlock">"""
                html+='<input type="hidden" name="avbeghj" value="'+userName+'" />'
                html += """<p>Club Name: <span class="in1"><input type="text" name="clubName" class="clubName"></span></p>
                          <p>Description: <span class="in5"><textarea name="description" class="description"></textarea></p>
                                                        <a href="clubMain.cgi">Cancel</a>
                                                        <input type="submit" value="Create" name="submit">
                      </div>
                                                </form>
                                </article>

                                <!-- footer -->
                                """
                html += EchooFunctions.setFooter()
                html +="""
                        </div>
                        </body>
                </html>
                """
                print(html)
        else:
                if clubID != "":
                        try:
                                SQL = "select * from club where clubID = "
                                SQL += str(clubID) + " ;"
                                cursor.execute(SQL)
                                results = cursor.fetchall()
                        except Exception as e:
                                print('<p>Something went wrong with the SQL!</p>')
                                print(SQL, "Error:", e)

                        else:
                                if results:
                                        for row in results:
                                                if userName != row[4]:
                                                        print("you dont have right access to this page")
                                                else:
                                                        avbeghj = EchooFunctions.getUserID(cursor, userName)
                                                        html+="""	
                                                        <!-- Log in box-->
                                                                        <article class="block">
                                                              <h1>Edit Club </h1>
                                                              <div class="form">
                                                                <form action="clubEdit.php?club="""
                                                        html+=str(row[0])
                                                        html+='" method="post" enctype="multipart/form-data">'
                                                        html+='<img src="images/club/'+str(row[3])+'" alt="sampleIcon"><br>'
                                                        html+="""<input type = "file" name = "image" />
                                                              <div class="infoBlock">"""
                                                        html+='<input type="hidden" name="avbeghj" value="'+userName+'" />'
                                                        html += """<p>Club Name: <span class="in1"><input type="text" name="clubName" class="clubName" value="""
                                                        html+="'"+str(row[1])+"'"
                                                        html+="""></span></p>
                                                                  <p>Description: <span class="in5"><textarea name="description" class="description">"""
                                                        html+= str(row[2])
                                                        html+="""</textarea></p>
                                                                                                <a href="clubMessage.cgi?club="""
                                                        html+=str(clubID)
                                                        html+='">Cancel</a>'
                                                        html+="""
                                                                                                <input type="submit" value="Edit" name="submit">
                                                              </div>
                                                                                        </form>
                                                                        </article>

                                                                        <!-- footer -->
                                                                        """
                                                        html += EchooFunctions.setFooter()
                                                        html +="""
                                                                </div>
                                                                </body>
                                                        </html>
                                                        """
                                                        print(html)
                                                        

                else:
                        print("error, club is missing")

else:
    print("<h1>You aren't permit to visit this page</h1>")
    print("<a href='index.cgi'>Return</a>")
    
