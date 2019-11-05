#! /usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os,EchooFunctions
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
    <link rel="stylesheet" href="css/newsMain.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
html += EchooFunctions.setLoginStatus('news')
html+="""<!-- article box-->
		<article class="block">
		<div class='row'>
			<h1>New Articles</h1>
			{function}
			<div class="interBlock">
			{message}
	      <div class="pageRow">
{PageContent}
	      </div>
			</div>
		</article>

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

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

userName = ""
userID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
#main contents to insert
message = ""
function = ""
administrator = False
footer = EchooFunctions.setFooter()

page = form.getfirst("page", "1")
page = int(page)


lastPage = False
post_count=1
totalNum = 0
PageContent = ""

if "echooUser" in str(os.environ):
        if EchooFunctions.checkUserType(cursor, userName) == 'administrator':
                administrator = True

if administrator == True:
        function += '	<div class="functionbutton"><a href="createNewsAnnoun.cgi?type=news">Create Article</a></div></div>'

try:
        SQL = "SELECT count(newsID) from news;"
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
                                PageContent +='<a href="news_main.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                break
                        else:
                                PageContent +='<a href="news_main.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                PageContent +='<a href="news_main.cgi?page='+str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                PageContent +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                PageContent +='<a href="#" class="currentPage">1</a>'
                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
if page != 1:
        if lastPage == False:
                PageContent +='<a href="news_main.cgi?page='+str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                PageContent +='<a href="news_main.cgi?page='+str((int(page)-1))+'">'+str(int(page)-1)+'</a>'
                page_count = int(page)
                for i in range(4):
                        if ((int(page_count))*5)>int(totalNum):
                                PageContent +='<a href="news_main.cgi?page='+str(page_count)+'" class="currentPage">'+str(page_count)+'</a>'
                                break
                        else:
                                PageContent +='<a href="news_main.cgi?page='+str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                PageContent +='<a href="news_main.cgi?page='+str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                PageContent +='<a href="news_main.cgi?page='+str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                PageContent +='<a href="news_main.cgi?page='+str((int(page)-1))+'">'+str((int(page)-1))+'</a>'
                PageContent +='<a href="#" class="currentPage">'+str(page)+'</a>'
                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                

page = form.getfirst("page", "1")
page = int(page)

try:
        SQL = "SELECT icon, title, detail, newsID FROM news ORDER BY publish_time DESC;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                if post_count <= int(page)*5 and post_count >(int(page)-1)*5:
                        message += '<div class="article">'
                        message += '<img src="images/news/'+str(row[0])+'" alt="article1">'
                        message += '<div class="title"><p><a href="news_page.cgi?newsID='+str(row[3])+'">'+row[1]+'</a></p>'
                        articleContent = ""
                        wordCount = 0
                        for x in str(row[2]):
                                if wordCount <=100:
                                        articleContent += x
                                        wordCount += 1
                                if wordCount >100:
                                        articleContent += "..."
                                        break   
                        message += '<p>'+str(articleContent)+'</p>'
                        if administrator == True:
                                message += '<p class="remove"><a href="removeNews.cgi?news='+str(row[3])+'">Remove</a></p>'
                        message += '</div></div>'
                        post_count += 1
                else:
                        post_count += 1

#print out html
print(html.format(function = function, PageContent = PageContent, message = message, footer = footer))
