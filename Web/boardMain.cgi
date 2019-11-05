#! /usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
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
		<link rel="stylesheet" href="css/signUp.css">
    <link rel="stylesheet" href="css/newsMain.css">
    <link rel="stylesheet" href="css/boardMain.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""

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
        userID = EchooFunctions.getUserID(cursor, userName)

html = """		<!-- article box-->
		<article class="block">
			<h4>Board</h4>
			<div class="interBlock">
				<h1>"""
html += '<a href="boardMain.cgi?platform=pc&page=1">PC</a>/<a href="'
html += 'boardMain.cgi?platform=PS4&page=1">PS4</a>/<a href="'
html += 'boardMain.cgi?platform=XBOX&page=1">XBOX</a>/<a href="'
html += 'boardMain.cgi?platform=switch&page=1">SWITCH</a>/<a href="'
html += 'boardMain.cgi?platform=mobile&page=1">MOBILE</a>'
if "echooUser" in str(os.environ):
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                html += '<a href="createBoard.cgi" class="CreateButton">Create Board</a>'
html += """</h1><div class="boardContainer">"""

html2="""</div>
	      <div class="pageRow">"""

form = cgi.FieldStorage()
platform = form.getfirst("platform", "pc")
page = form.getfirst("page", "1")
page = int(page)


lastPage = False
post_count=1
totalNum = 0

try:
        SQL = "SELECT count(boardID) FROM board WHERE platform = '{platform}';"
        cursor.execute(SQL.format(platform=platform))
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                totalNum += int(row[0])
                if int(row[0]) <= (8*int(page)):
                        lastPage = True
if page == 1:
        if lastPage == False:
                html2 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                html2 +='<a href="#" class="currentPage">1</a>'
                page_count = 2
                for i in range(7):
                        if ((int(page_count)+1)*8)>int(totalNum):
                                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                                html2 += str(page_count)+'">'+str(page_count)+'</a>'
                                break
                        else:
                                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                                html2 += str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                html2 += str(2)+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                html2 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                html2 +='<a href="#" class="currentPage">1</a>'
                html2 +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
if page != 1:
        if lastPage == False:
                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                html2 += str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                html2 += str((int(page)-1))+'">'+str(int(page)-1)+'</a>'
                page_count = int(page)
                for i in range(7):
                        if ((int(page_count))*8)>int(totalNum):
                                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                                html2 += str(page_count)+'" class="currentPage">'+str(page_count)+'</a>'
                                break
                        else:
                                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                                html2 += str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                html2 += str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                html2 += str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                html2 +='<a href="boardMain.cgi?platform='+platform+'&page='
                html2 += str((int(page)-1))+'">'+str((int(page)-1))+'</a>'
                html2 +='<a href="#" class="currentPage">'+str(page)+'</a>'
                html2 +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                

page = form.getfirst("page", "1")
page = int(page)

html2 += """	      </div>
			</div>
		</article>

		<!-- footer -->
"""
html2 += EchooFunctions.setFooter()
html2 +="""
	</div>
	</body>
</html>

"""
try:
        SQL = "SELECT icon, boardID FROM board WHERE platform = '{platform}';"
        cursor.execute(SQL.format(platform=platform))
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
	board_images = ""
	for row in results:
		
		if post_count <= int(page)*8 and post_count >(int(page)-1)*8:
			board_images += '<a href="boardAllPost.cgi?board='+str(row[1])
			board_images += '&page=1"><img src="images/board/' + platform + '/' + str(row[0]) + '" alt="logo"></a>'
			post_count += 1
		else:
			post_count += 1

#print out html
print(htmlOpen)
print(EchooFunctions.setLoginStatus('board'))
print(html)
print(board_images)
print(html2)

