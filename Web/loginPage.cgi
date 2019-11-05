#! /usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
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
    <link rel="stylesheet" href="css/login.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>

	{nav}

		<!-- Log in box-->
		<article class="block">
			<h1 class="sr-only">SignUp</h1>
			<div class="signUpBox">
				<h2>Log in</h2>
          <form method="post" action="login.cgi?redirect={redirect}">
            <p>Username: <input type="text" name="username"></p>
            <p>Password: <input type="password" name="password"></p>
            <button type="submit" class="firstbt">Log in</button>
            <p>Haven't account? <a href="signUpPage.cgi?redirect={redirect}">Sign Up</a></p>
          </form>
        </div>
		</article>

		<!-- footer -->
		<footer>
			<div class="container">
				<section class="footer-menu">
					<h1 class="sr-only">Footer</h1>
					<div class="row">
						<div class="footer-menu-main">
							<a href="index.cgi"><p>Home</p></a> <p class="line">|</p>
							<a href="contactUS.cgi"><p>Contact Us</p></a> <p class="line">|</p>
							<a href="#"><p>Terms</p></a> <p class="line">|</p>
						<div class="soical-media">
							<a href="https://www.facebook.com/Echooo-Forum-757463234654244/"><i class="fab fa-facebook"></i></a>
							<a href="https://twitter.com/Echooo28844222"><i class="fab fa-twitter"></i></a>
							<a href="https://discord.gg/7xTCNfb"><i class="fab fa-discord"></i></a>
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
error_message = ""
status = False

user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user
                         )
cursor = db_con.cursor()
nav = EchooFunctions.setLoginStatus('index')

redirect = form.getfirst('redirect','')

Login = False

if "echooUser" in str(os.environ):
        Login = True

if Login == True:
    print("<h1>You have already login</h1>")
    print("<a href='index.cgi'>Return</a>")
else:
    print(html.format(redirect=redirect, nav = nav))
    
