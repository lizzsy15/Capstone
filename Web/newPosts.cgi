#!/usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, re, EchooFunctions
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
					{content}
						</ul>
						<div class="pageRow">
							<a href="#"><i class="fas fa-arrow-left"></i></a>
							<a href="#">1</a>
							<a href="#">2</a>
							<a href="#">3</a>
							<a href="#">4</a>
							<a href="#">5</a>
							<a href="#">6</a>
							<a href="#">7</a>
							<a href="#">8</a>
							<a href="#"><i class="fas fa-arrow-right"></i></a>
						</div>
					</div>
				</div>

			<!-- newClubs -->
        <div class="newClubs">
          <h1> New Clubs </h1>
					<div class="innerContent">
						<div class="club">
			        <img src="images/article/article1.jpg" alt="article1">
			        <div class="clubContent">
			          <p class="title"><a href="#">Club 2</a></p>
			          <p>Feb 17, 2018 - The brain can be affected by just 1 hour of playing video games,
			          according to new research published in the journal Frontiers in Human ...</p>
			        </div>
			      </div>
			      <div class="club">
			        <img src="images/article/article2.jpg" alt="article1">
			        <div class="clubContent">
			          <p class="title"><a href="#">Club 3</a></p>
			          <p>Feb 17, 2018 - The brain can be affected by just 1 hour of playing video games,
			          according to new research published in the journal Frontiers in Human ...</p>
			        </div>
			      </div>
			      <div class="club">
			        <img src="images/article/article3.jpg" alt="article1">
			        <div class="clubContent">
			          <p class="title"><a href="#">Club 4</a></p>
			          <p>This image showcases the Avengers at their most classic, with a familiar lineup of powerhouse heroes
			            combining to confront a threat greater than any of them could face alone.......</p>
			        </div>
			      </div>
						<div class="pageRow">
							<a href="#"><i class="fas fa-arrow-left"></i></a>
							<a href="#">1</a>
							<a href="#">2</a>
							<a href="#">3</a>
							<a href="#">4</a>
							<a href="#">5</a>
							<a href="#">6</a>
							<a href="#">7</a>
							<a href="#">8</a>
							<a href="#"><i class="fas fa-arrow-right"></i></a>
						</div>
					</div>
        </div>
			</article>
			<!-- newGames -->
			<article class="CenterPart2">
			<div class="newGames">
				<h1> New Games </h1>
				<div class="innerContent">
					<div class="club">
						<img src="images/article/article1.jpg" alt="article1">
						<div class="clubContent">
							<p class="title"><a href="#">NBA2K 2019</a></p>
							<p>Release Date: 07-08-2019</p>
						</div>
					</div>
					<div class="club">
						<img src="images/article/article2.jpg" alt="article1">
						<div class="clubContent">
							<p class="title"><a href="#">PUBG 2020</a></p>
							<p>Release Date: 01-01-2020</p>
						</div>
					</div>
					<div class="club">
						<img src="images/article/article3.jpg" alt="article1">
						<div class="clubContent">
							<p class="title"><a href="#">SPiderman VS IronMan</a></p>
							<p>Release Date: 03-24-2025</p>
						</div>
					</div>
					<div class="pageRow">
						<a href="#"><i class="fas fa-arrow-left"></i></a>
						<a href="#">1</a>
						<a href="#">2</a>
						<a href="#">3</a>
						<a href="#">4</a>
						<a href="#">5</a>
						<a href="#">6</a>
						<a href="#">7</a>
						<a href="#">8</a>
						<a href="#"><i class="fas fa-arrow-right"></i></a>
					</div>
				</div>
			</div>
			<!-- newArticles -->
			<div class="newArticles">
				<h1> New Articles </h1>
				<div class="innerContent">
					<div class="club">
						<img src="images/article/article1.jpg" alt="article1">
						<div class="clubContent">
							<p class="title"><a href="#">PS4 news: Sony PlayStation and Xbox facing...</a></p>
							<p>LeiKuok Kan</p>
							<p>Feb 17, 2018 - The brain can be affected by just 1 hour of playing video games,
							according to new research published in the journal Frontiers in Human ...</p>
						</div>
					</div>
					<div class="club">
						<img src="images/article/article2.jpg" alt="article1">
						<div class="clubContent">
							<p class="title"><a href="#">PS4 FREE GAME: Download a great PlayStation...</a></p>
							<p>LeiKuok Kan</p>
							<p>Feb 17, 2018 - The brain can be affected by just 1 hour of playing video games,
							according to new research published in the journal Frontiers in Human ...</p>
						</div>
					</div>
					<div class="club">
						<img src="images/article/article3.jpg" alt="article1">
						<div class="clubContent">
							<p class="title"><a href="#">Apex Legends PS4 Crossplay gets little ...</a></p>
							<p>LeiKuok Kan</p>
							<p>This image showcases the Avengers at their most classic, with a familiar lineup of powerhouse heroes
								combining to confront a threat greater than any of them could face alone.......</p>
						</div>
					</div>
					<div class="pageRow">
						<a href="#"><i class="fas fa-arrow-left"></i></a>
						<a href="#">1</a>
						<a href="#">2</a>
						<a href="#">3</a>
						<a href="#">4</a>
						<a href="#">5</a>
						<a href="#">6</a>
						<a href="#">7</a>
						<a href="#">8</a>
						<a href="#"><i class="fas fa-arrow-right"></i></a>
					</div>
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
platform = form.getfirst("platform", "pc")

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

#main contents to insert
content = ""

try:
        SQL = "SELECT p.title, b.boardname FROM post as p, board as b WHERE p.boardID = b.boardID ORDER BY p.time_in desc LIMIT 10;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
            content += '<li><div class="listRow">'
            content += '<p><a href="#">'+row[0]+'</a></p>'
            content += '<p class="boardTitle">'
            content += '<a href="#">'+row[1]+'</a></p></div></li>'
			
#print out html
print(html.format(content = content))
