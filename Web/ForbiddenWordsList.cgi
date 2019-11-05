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
    <link rel="stylesheet" href="css/forbiddenWordsList.css">
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
        <form method="post" action="ForbiddenWordsAdd.cgi" class="infoBlock">
        <div class='row'><h3>Add New Forbidden Words:</h3><br><input type="text" name="newForbidden"><input type="Submit" value="ADD"></div>
          <h2>Forbidden List:</h2>
          {content}        </form>
      <div class="pageRow">{PageContent}</div></div>
		</article>"""


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

page = form.getfirst("page", "1")
page = int(page)


lastPage = False
post_count=1
totalNum = 0
PageContent = ""

html+="""<!-- footer -->
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
footer = EchooFunctions.setFooter()
if admin == True:
        if userID != "":
                try:
                        SQL = "SELECT count(wordID) from ban_word;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)

                else:
                        for row in results:
                                totalNum += int(row[0])
                                if int(row[0]) <= (5*int(page)):
                                        lastPage = True

                if page == 1:
                        if lastPage == False:
                                PageContent +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="#" class="currentPage">1</a>'
                                page_count = 2
                                for i in range(4):
                                        if ((int(page_count)+1)*5)>int(totalNum):
                                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                                break
                                        else:
                                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                                page_count += 1
                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
                        else:
                                PageContent +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="#" class="currentPage">1</a>'
                                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                if page != 1:
                        if lastPage == False:
                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str((int(page)-1))+'">'+str(int(page)-1)+'</a>'
                                page_count = int(page)
                                for i in range(4):
                                        if ((int(page_count))*5)>int(totalNum):
                                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str(page_count)+'" class="currentPage">'+str(page_count)+'</a>'
                                                break
                                        else:
                                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                                page_count += 1
                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
                        else:
                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="ForbiddenWordsList.cgi?page='+str((int(page)-1))+'">'+str((int(page)-1))+'</a>'
                                PageContent +='<a href="#" class="currentPage">'+str(page)+'</a>'
                                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                                

                page = form.getfirst("page", "1")
                page = int(page)

                try:
                        SQL = "select * from ban_word;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        for row in results:
                                if post_count <= int(page)*5 and post_count >(int(page)-1)*5:
                                        content+='<p>'+str(row[0])+'      '+row[1]+' '
                                        content+='<a href="removeForbidden.cgi?word='+str(row[0])+'">Remove</a>'+'</p>'
                                        post_count += 1
                                else:
                                        post_count += 1
                        

        #print out html
        print(htmlOpen)
        print(html.format(content = content, PageContent = PageContent, footer = footer))
else:
        print("<h1>You arn't permit to visit this page</h1>")
        print("<a href='index.cgi'>Return</a>")
