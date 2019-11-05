#!/usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os
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

	<body>
		<!-- JavaScript -->


		<!-- Navigation -->
		<div class="container">
		<nav>
			<div class="container">
				<div class="row">
					<div class="logo">
						<a href="#"><img src="images/logo.jpg" alt="logo"></a>
					</div>
					<h1>Echooo</h1>
					<ul>
						<li><div class="user">
							<a href="#"><i class="fas fa-user"></i> Sign Up</a>
							<a href="#"><i class="fas fa-user"></i> Login</a>
						</div></li>
						</li>
							<div class="search-container">
								<form action="#">
									<input type="text" placeholder="Search.." name="search">
									<button type="submit"><i class="fa fa-search"></i></button>
								</form>
							</div></li>
					</ul>
				</div>
				<div class="bar">
					<ul>
						<li><a href="#"><i class="far fa-question-circle"></i> Home</a></li>
						<li><a href="#"><i class="fas fa-globe-americas"></i> What's New</a></li>
						<li><a href="#"><i class="fas fa-users"></i> Boards</a></li>
						<li><a href="#"><i class="fas fa-users"></i> Clubs</a></li>
						<li><a href="#"><i class="fas fa-scroll"></i> News</a></li>
						<li><a href="#"><i class="fas fa-scroll"></i> Help</a></li>
					</ul>
				</div>
			</div>
		</nav>

    <!-- the whole container -->
		<article class="CenterPart">
			<!-- newPosts -->
				<div class="newPosts">
          <h1> New Posts </h1>
					<div class="innerContent">
					<ul>
					{post}
					</ul>
					</div>
				</div>

			<!-- newClubs -->
        <div class="newClubs">
          <h1> New Clubs </h1>
					<div class="innerContent">
					{club}
			      
					</div>
        </div>
			</article>
			<!-- newGames -->
			<article class="CenterPart2">
			<div class="newGames">
				<h1> New Boards </h1>
				<div class="innerContent">
				{board}
				</div>
			</div>
			<!-- newArticles -->
			<div class="newArticles">
				<h1> New Articles </h1>
				<div class="innerContent">
				{article}
				</div>
			</div>
		</article>

		<!-- footer -->
		<footer>
			<div class="container">
				<section class="footer-menu">
					<h1 class="sr-only">Footer</h1>
					<div class="row">
						<div class="footer-menu-main">
							<a href="#"><p>Home</p></a> <p class="line">|</p>
							<a href="#"><p>Contact Us</p></a> <p class="line">|</p>
							<a href="#"><p>Terms</p></a> <p class="line">|</p>
						<div class="soical-media">
							<a href="#"><i class="fab fa-facebook"></i></a>
							<a href="#"><i class="fab fa-twitter"></i></a>
							<a href="#"><i class="fab fa-discord"></i></a>
						</div></div>
					</div>
				</section>
			</div>
		</footer>
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
article = ""
board = ""
club = ""
post = ""

try:
        SQL = "SELECT p.title, b.boardname, p.postID FROM post as p, board as b WHERE p.boardID = b.boardID ORDER BY p.time_in desc LIMIT 10;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
            post += '<li><div class="listRow">'
            post += '<p><a href="article.cgi?post='+str(row[2])+'">'+row[0]+'</a></p>'
            post += '<p class="boardTitle">'
            post += '<a href="#">'+row[1]+'</a></p></div></li>'
            
try:
        SQL = "SELECT clubname, description, icon, clubID FROM club Order By clubID desc LIMIT 3;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
            club += '<div class="club">'
            club += '<img src="images/club/'+str(row[2])+'" alt="club1">'
            club += '<div class="clubContent">'
            club += '<p class="title"><a href="clubMessage.cgi?club='+str(row[3])+'">'+str(row[0])+'</a></p>'
            club += '<p>'+str(row[1])+'</p></div></div>'
            
try:
        SQL = "SELECT icon,boardname,platform,boardID FROM board ORDER BY boardID DESC LIMIT 3;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
    for row in results:
            board += '<div class="club"><img src="images/board/'+str(row[2])+'/'+str(row[0])+' "alt="article1">'
            board += '<div class="clubContent"><p class="title"><a href="boardAllPost.cgi?board='+str(row[3])+'&page=1">'+str(row[1])+'</a></p>'
            board += '<p>'+str(row[2])+'</p>'
            board +='</div></div>'
            
try:
        SQL = "SELECT n.icon,n.title,n.detail,u.username, n.newsID FROM user AS u, news AS n WHERE u.userID=n.authorID ORDER BY n.publish_time DESC LIMIT 3;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
    for row in results:
            article += '<div class="club"><img src="images/news/'+str(row[0])+'"alt="article1">'
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


#print out html
print(html.format(article = article, board = board, club = club, post = post))
