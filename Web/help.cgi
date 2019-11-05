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
		<link rel="stylesheet" href="css/signUp.css">
    <link rel="stylesheet" href="css/help.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>

	"""
html+=EchooFunctions.setLoginStatus('helps')
html+="""

		<!-- Announcement-->
		<article class="block">
			<h1>Frequently Asked Questions</h1>
			<div class="interBlock">"""

	      
html2="""<div class="pageRow">{PageContent}</div>
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

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

#main contents to insert
content = ""

page = form.getfirst("page", "1")
page = int(page)


lastPage = False
post_count=1
totalNum = 0
PageContent = ""

try:
        SQL = "SELECT count(question) from help;"
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
                                PageContent +='<a href="help.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                break
                        else:
                                PageContent +='<a href="help.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                PageContent +='<a href="help.cgi?page='+str((int(page)-1))+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                PageContent +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                PageContent +='<a href="#" class="currentPage">1</a>'
                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
if page != 1:
        if lastPage == False:
                PageContent +='<a href="help.cgi?page='+str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                PageContent +='<a href="help.cgi?page='+str((int(page)-1))+'">'+str(int(page)-1)+'</a>'
                page_count = int(page)
                for i in range(4):
                        if ((int(page_count))*5)>int(totalNum):
                                PageContent +='<a href="help.cgi?page='+str(page_count)+'" class="currentPage">'+str(page_count)+'</a>'
                                break
                        else:
                                PageContent +='<a href="help.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                PageContent +='<a href="help.cgi?page='+str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                PageContent +='<a href="help.cgi?page='+str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                PageContent +='<a href="help.cgi?page='+str((int(page)-1))+'">'+str((int(page)-1))+'</a>'
                PageContent +='<a href="#" class="currentPage">'+str(page)+'</a>'
                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                

page = form.getfirst("page", "1")
page = int(page)
                
try:
        SQL = "SELECT question, answer FROM help"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:

	help_info = ""
	for row in results:
		count = 0
		for entry in row:
			if count == 0:
				help_info += "<p class='question'>" +str(entry) +"</p>"
			if count == 1:
				help_info += "<p class='ans'>" + str(entry) + "</p>"
			count += 1
			

		
#print out html
print(html)
print(help_info)
print(html2.format(PageContent = PageContent))

