#! /usr/bin/env python3
 
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
		<link rel="stylesheet" href="css/signUp.css">
    <link rel="stylesheet" href="css/clubMain.css">
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

    <div class="searchRow">
      <form action="#" class="searchBar">
        <input type="text" placeholder="Search.." name="search">
        <button type="submit"><i class="fa fa-search"></i></button>
      </form>
      <a href="#" class="createClubLink">Create Club</a>
    </div>
		<!-- article box-->
		<article class="block">
			<h1>My Favorite Clubs</h1>
				<div class="interBlock">
				{message1}
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
		</article>

		<article class="block">
			<h1>Clubs</h1>
				<div class="interBlock">
				{message2}
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
message1 = ""

try:
        SQL = "SELECT c.icon,c.clubname,c.description FROM club AS c, club_user AS cu WHERE c.clubID = cu.clubID AND cu.userID=1 LIMIT 6;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
            message1 += '<div class="article">'
            message1 += '<img src="images/'+row[0]+'" alt="article1">'
            message1 += '<div class="title"><p><a href="#">'+row[1]+'</a></p>'
            message1 += '<p>'+row[2]+'</p></div></div>'

message2 = ""

try:
        SQL = "SELECT c.icon,c.clubname,c.description FROM club AS c, club_user AS cu WHERE  NOT EXISTS(SELECT * FROM club_user AS cu WHERE c.clubID = cu.clubID AND cu.userID =1) GROUP BY c.clubname LIMIT 12;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
            message2 += '<div class="article">'
            message2 += '<img src="images/'+row[0]+'" alt="article1">'
            message2 += '<div class="title"><p><a href="#">'+row[1]+'</a></p>'
            message2 += '<p>'+row[2]+'</p></div></div>'

#print out html
print(html.format(message1 = message1, message2=message2))
