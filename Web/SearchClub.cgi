#!/usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

html = """
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
    <link rel="stylesheet" href="css/clubMain.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>

	{navigation}

    <div class="searchRow">
      <form action="SearchClub.cgi" class="searchBar">
        <input type="text" placeholder="search..." name="search">
        <button type="submit"><i class="fa fa-search"></i></button>
      </form>
      <a href="#" class="createClubLink">Create Club</a>
    </div>
		<!-- article box-->
		<h3>Search with Key Word '{searchWord}'</h3>

		<article class="block">
			<h1>Clubs</h1>
				<div class="interBlock2">
	    		{content}

			</div>
							<div class="pageRow">
{pageNumber}
				</div>
		</article>

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

#main contents to insert
searchWord = form.getfirst('search', '')
content=""
navigation = EchooFunctions.setLoginStatus('club')
page = form.getfirst("page", "1")
page = int(page)
pageNumber = ""
footer = EchooFunctions.setFooter()

lastPage = False
post_count=1
totalNum = 0

if page == 1:
        if lastPage == False:
                pageNumber +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                pageNumber +='<a href="#" class="currentPage">1</a>'
                page_count = 2
                for i in range(7):
                        if ((int(page_count)+1)*15)>int(totalNum):
                                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                                pageNumber += str(page_count)+'">'+str(page_count)+'</a>'
                                break
                        else:
                                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                                pageNumber += str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                pageNumber += str(2)+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                pageNumber +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                pageNumber +='<a href="#" class="currentPage">1</a>'
                pageNumber +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
if page != 1:
        if lastPage == False:
                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                pageNumber += str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                pageNumber += str((int(page)-1))+'">'+str(int(page)-1)+'</a>'
                page_count = int(page)
                for i in range(7):
                        if ((int(page_count))*15)>int(totalNum):
                                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                                pageNumber += str(page_count)+'" class="currentPage">'+str(page_count)+'</a>'
                                break
                        else:
                                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                                pageNumber += str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                pageNumber += str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                pageNumber += str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                pageNumber +='<a href="SearchClub.cgi?search='+searchWord+'&page='
                pageNumber += str((int(page)-1))+'">'+str((int(page)-1))+'</a>'
                pageNumber +='<a href="#" class="currentPage">'+str(page)+'</a>'
                pageNumber +='<a href="#"><i class="fas fa-arrow-right"></i></a>'

try:
        SQL = "SELECT clubID, icon, clubname, description FROM club;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                if searchWord.lower() in row[2].lower() or searchWord.lower() in row[3].lower():
                        totalNum += int(row[0])
                        if int(row[0]) <= (15*int(page)):
                                lastPage = True
try:
        SQL = "SELECT clubID, icon, clubname, description FROM club;"
        cursor.execute(SQL)
        results = cursor.fetchall()
        
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                if searchWord.lower() in row[2].lower() or searchWord.lower() in row[3].lower():
                        if post_count <= int(page)*15 and post_count >(int(page)-1)*15:
                                content += '<div class="article">'
                                content += '<img src="images/club/'+row[1]+'" alt="article1">'
                                content += '<div class="title">'
                                content += '<p class="title"><a href="clubMessage.cgi?club='+str(row[0])+'">'+row[2]+'</a></p>'
                                content += '<p>'+row[3]+'</p></div></div>'
                                post_count += 1
                        else:
                                post_count += 1

print(html.format(navigation = navigation, searchWord = searchWord, content = content, pageNumber = pageNumber, footer = footer))

