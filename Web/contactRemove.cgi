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
		<link rel="stylesheet" href="css/index.css">
    <link rel="stylesheet" href="css/boardAllPost.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
		<script>
function redirect (url) {
window.location.replace(url);
}

</script>
	</head>"""
form = cgi.FieldStorage()
contact = form.getfirst('contact','')
html="""<body onload="redirect('reportList.cgi')">{content}"""

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
admin = False
moderator = False
userConfirm = False

html += """</form>
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

#change the status of veriable
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True

#main contents to insert
content = ""

if contact != "":
        if admin==True or userConfirm==True:
                try:
                        SQL = "Delete FROM contacts WHERE contactID = "
                        SQL += str(contact)+";"
                        cursor.execute(SQL)
                        db_con.commit()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        content += ""
                        
        else:
                content += "<p> You don't have the right access to this page</p>"
                content += """<a href="reportList.cgi">Return</a>"""



#print out html
print(htmlOpen)
print(html.format(content = content))
