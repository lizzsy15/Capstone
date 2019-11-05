#!/usr/bin/env python3
  
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
		<link rel="stylesheet" href="css/whatsNews.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>

	{userBlock}

    <!-- the whole container -->
    <h3>Search for Key Word '{keyWord}'</h3>
		<article class="CenterPart">
			<div class="userBlock">
				<h1> User </h1>
				<div class="interBlock1">
					{searchUser}



				</div>
				<div class="pageRow">
{page5Content}
				</div>
			</div>
			<!-- newPosts -->
				<div class="newPosts">
          <h1> New Posts </h1>
					<div class="innerContent">
					<ul>
					{post}
					</ul>
										<div class="pageRow">
					{page1Content}
					</div>
					</div>

				</div>

			<!-- newClubs -->
        <div class="newClubs">
          <h1> New Clubs </h1>
					<div class="innerContent">
					{club}
					<div class="pageRow">
                                        {page2Content}
                                        </div>
					</div>
        </div>
			</article>
			<!-- newGames -->
			<article class="CenterPart2">
			<div class="newGames">
				<h1> New Boards </h1>
				<div class="innerContent">
				{board}
				<div class="pageRow">
				{page3Content}
				</div>
				</div>
			</div>
			<!-- newArticles -->
			<div class="newArticles">
				<h1> New Articles </h1>
				<div class="innerContent">
				{article}
								<div class="pageRow">
				{page4Content}
				</div>
				</div>

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
searchUser= ""
keyWord = form.getfirst('search', '')
page1 = int(form.getfirst('page1', 1))
page2 = int(form.getfirst('page2', 1))
page3 = int(form.getfirst('page3', 1))
page4 = int(form.getfirst('page4', 1))
page5 = int(form.getfirst('page5', 1))
page1Content = ""
page2Content=""
page3Content=""
page4Content=""
page5Content=""
pageCount1 = 1
pageCount2 = 1
pageCount3 = 1
pageCount4 = 1
pageCount5 = 1
userBlock = ""
article = ""
board = ""
club = ""
post = ""
footer = EchooFunctions.setFooter()
userBlock += EchooFunctions.setLoginStatus('index')

if keyWord != "":
        #User
        try:
                SQL = "SELECT userID, username, icon from user ORDER BY userID desc;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:
                        icon = ""
                        if str(row[2]) == "None":
                                    icon = "nullicon.jpg"
                        else:
                                icon = str(row[2])
                        if keyWord.lower() in row[1].lower():
                                if pageCount5 <= int(page5)*6 and pageCount5 > (int(page5)-1)*6:
                                        searchUser += '<div class="article"><img src="images/user/'+str(icon)+'" alt="article1"><div class="title">'
                                        searchUser += '<p><a href="userProfile.cgi?userid='+str(row[0])+'">'+str(row[1])+'</a></p></div></div>'
                                        pageCount5 +=1
                                else:
                                        pageCount5 +=1
        if int(page5) == 1:
                page5Content += '<a href="#"><i class="fas fa-arrow-left"></i></a><a href="#">1</a>'
        else:
                page5Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(int(page5)-1)+'"><i class="fas fa-arrow-left"></i></a>'
                page5Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5=1">1</a>...'
                page5Content += '<a href="#">'+str(page5)+'</a>'
        if int(page5) *6 >= (int(pageCount5)-1):
                page5Content += '<a href="#"><i class="fas fa-arrow-right"></i></a>'
        else:
                page5Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(int(page5)+1)+'"><i class="fas fa-arrow-right"></i></a>'

        #Post Board
        try:
                SQL = "SELECT p.title, b.boardname, p.postID, b.boardID FROM post as p, board as b WHERE p.boardID = b.boardID ORDER BY p.time_in desc;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:
                        if keyWord.lower() in row[1].lower():
                                if pageCount1 <= int(page1)*10 and pageCount1 > (int(page1)-1)*10:
                                        post += '<li><div class="listRow">'
                                        post += '<p><a href="article.cgi?post='+str(row[2])+'">'+row[0]+'</a></p>'
                                        post += '<p class="boardTitle">'
                                        post += '<a href="boardAllPost.cgi?board='+str(row[3])+'&page=1">'+row[1]+'</a></p></div></li>'
                                        pageCount1 +=1
                                else:
                                        pageCount1 +=1

        if int(page1) == 1:
                page1Content += '<a href="#"><i class="fas fa-arrow-left"></i></a><a href="#">1</a>'
        else:
                page1Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(int(page1)-1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(page5)+'"><i class="fas fa-arrow-left"></i></a>'
                page1Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1=1&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(page5)+'">1</a>...'
                page1Content += '<a href="#">'+str(page1)+'</a>'
        if int(page1) *10 >= (int(pageCount1)-1):
                page1Content += '<a href="#"><i class="fas fa-arrow-right"></i></a>'
        else:
                page1Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(int(page1)+1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(page5)+'"><i class="fas fa-arrow-right"></i></a>'

        #Club Board      
        try:
                SQL = "SELECT clubname, description, icon, clubID FROM club Order By clubID desc;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:
                        if keyWord.lower() in row[0].lower():
                                if pageCount2 <= int(page2)*3 and pageCount2 > (int(page2)-1)*3:
                                        club += '<div class="club">'
                                        club += '<img src="images/club/'+str(row[2])+'" alt="club1">'
                                        club += '<div class="clubContent">'
                                        club += '<p class="title"><a href="clubMessage.cgi?club='+str(row[3])+'">'+str(row[0])+'</a></p>'
                                        club += '<p>'+str(row[1])+'</p></div></div>'
                                        pageCount2 +=1
                                else:
                                        pageCount2 +=1

        if int(page2) == 1:
                page2Content += '<a href="#"><i class="fas fa-arrow-left"></i></a><a href="#">1</a>'
        else:
                page2Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(int(page2)-1)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(page5)+'"><i class="fas fa-arrow-left"></i></a>'
                page2Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2=1&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(page5)+'">1</a>...'
                page2Content += '<a href="#">'+str(page2)+'</a>'
        if int(page2) *3 >= (int(pageCount2)-1):
                page2Content += '<a href="#"><i class="fas fa-arrow-right"></i></a>'
        else:
                page2Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(int(page2)+1)+'&page3='+str(page3)+'&page4='+str(page4)+'&page5='+str(page5)+'"><i class="fas fa-arrow-right"></i></a>'
        #Board Block       
        try:
                SQL = "SELECT icon,boardname,platform,boardID FROM board ORDER BY boardID DESC;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
            for row in results:
                    if keyWord.lower() in row[1].lower():
                            if pageCount3 <= int(page3)*3 and pageCount3 > (int(page3)-1)*3:
                                    board += '<div class="club"><img src="images/board/'+str(row[2])+'/'+str(row[0])+' "alt="article1">'
                                    board += '<div class="clubContent"><p class="title"><a href="boardAllPost.cgi?board='+str(row[3])+'&page=1">'+str(row[1])+'</a></p>'
                                    board += '<p>'+str(row[2])+'</p>'
                                    board +='</div></div>'
                                    pageCount3 +=1
                            else:
                                    pageCount3 +=1

        if int(page3) == 1:
                page3Content += '<a href="#"><i class="fas fa-arrow-left"></i></a><a href="#">1</a>'
        else:
                page3Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(int(page3)-1)+'&page4='+str(page4)+'&page5='+str(page5)+'"><i class="fas fa-arrow-left"></i></a>'
                page3Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3=1&page4='+str(page4)+'&page5='+str(page5)+'">1</a>...'
                page3Content += '<a href="#">'+str(page3)+'</a>'
        if int(page3) *3 >= (int(pageCount3)-1):
                page3Content += '<a href="#"><i class="fas fa-arrow-right"></i></a>'
        else:
                page3Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(int(page3)+1)+'&page4='+str(page4)+'&page5='+str(page5)+'"><i class="fas fa-arrow-right"></i></a>'
        #article block
                
        try:
                SQL = "SELECT n.icon,n.title,n.detail,u.username, n.newsID FROM user AS u, news AS n WHERE u.userID=n.authorID ORDER BY n.publish_time DESC;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
            for row in results:
                    if keyWord.lower() in row[1].lower():
                            icon = ""
                            if str(row[0]) == "None":
                                    icon = "nullicon.jpg"
                            else:
                                    icon = str(row[0])
                            if pageCount4 <= int(page4)*3 and pageCount4 > (int(page4)-1)*3:
                                    article += '<div class="club"><img src="images/news/'+str(icon)+'"alt="article1">'
                                    article += '<div class="clubContent"><p class="title"><a href="news_page.cgi?newsID='+str(row[4])+'">'+str(row[1])+'</a></p>'
                                    article += '<p>'+str(row[3])+'</p>'
                                    articleContent = ""
                                    wordCount = 0
                                    for x in str(row[2]):
                                            if wordCount <=100:
                                                    articleContent += x
                                                    wordCount += 1
                                            if wordCount >100:
                                                    articleContent += "..."
                                                    break
                                    article += '<p>'+articleContent+'</p>'
                                    article += '</div></div>'
                                    pageCount4 +=1
                            else:
                                    pageCount4 +=1
        if int(page4) == 1:
                page4Content += '<a href="#"><i class="fas fa-arrow-left"></i></a><a href="#">1</a>'
        else:
                page4Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(int(page4)-1)+'&page5='+str(page5)+'"><i class="fas fa-arrow-left"></i></a>'
                page4Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page5='+str(page5)+'&page4=1">1</a>...'
                page4Content += '<a href="#">'+str(page4)+'</a>'
        if int(page4) *3 >= (int(pageCount4)-1):
                page4Content += '<a href="#"><i class="fas fa-arrow-right"></i></a>'
        else:
                page4Content += '<a href="searchMain.cgi?search='+str(keyWord)+'&page1='+str(page1)+'&page2='+str(page2)+'&page3='+str(page3)+'&page4='+str(int(page4)+1)+'&page5='+str(page5)+'"><i class="fas fa-arrow-right"></i></a>' 
        print(html.format(keyWord = keyWord, userBlock = userBlock, searchUser = searchUser, article = article, board = board, club = club, post = post, page1Content = page1Content, page2Content= page2Content, page3Content = page3Content, page4Content = page4Content, page5Content = page5Content, footer = footer))
else:
        print("<html><head></head><body>You didn't enter any words <br><a href='index.cgi'>Return</a></body></html>")


#print out html

