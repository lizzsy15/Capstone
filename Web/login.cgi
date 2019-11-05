#! /usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

html_1="""
<!doctype HTML>
<html lang="en">

	<!--
		I494 Capstone
		LTP03
	-->

	<head>
		<meta charset="utf-8">
		<title>Echooo</title>
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">"""

html_2="""		<!-- Stylesheets -->
		<link rel="stylesheet" href="css/normalize.css">
		<link rel="stylesheet" href="css/styles.css">

		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>

	<body>

		<div class="container">"""

html_2JS = """
<!-- Stylesheets -->
<link rel="stylesheet" href="css/normalize.css">
<link rel="stylesheet" href="css/styles.css">

<!--[if lte IE 9]>
	<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
<![endif]-->
<script>

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    window.location.replace('"""




html_en="""                </div>
	</body>
</html>"""

form = cgi.FieldStorage()
error_message = ""
status = False

user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user
                         )
cursor = db_con.cursor()


loginUserName = form.getfirst('username','Null')
password = form.getfirst('password','Null')
redirect = form.getfirst('redirect','index')
if redirect == "index":
    html_2JS += "index.cgi"
elif redirect == "board":
    html_2JS += "boardMain.cgi"
elif redirect == "club":
    html_2JS += "clubMain.cgi"
elif redirect == "news":
    html_2JS += "news_main.cgi"
elif redirect == "whatsNews":
    html_2JS += "whatsNewsPage.cgi"
elif redirect == "helps":
    html_2JS += "help.cgi"
else:
    html_2JS += "index.cgi"
html_2JS +="""');
}

</script>
</head>

<body onload="setCookie('echooUser','"""
password2 = password
failed="<p>you have failed login</p><br><h1><a href='login.html'>Return</a></h1>"
salt = "skr"

#add up the username into the cookie
html_2JS += loginUserName 
html_2JS += "_339458012"
html_2JS += """',500000)">"""

def get_userpw(cursor, loginUserName):
    try:
        SQL="SELECT password FROM user WHERE username = '"+loginUserName+"'"
        cursor.execute(SQL)
        hash_password = cursor.fetchall()
        if hash_password:
            hash_password = hash_password[0][0]
        else:
            print("username not exist<br><h1><a href='login.html'>Return</a></h1>")
    except Exception as e:
        hash_password = ""
    return hash_password

password = password + salt
password = hashlib.md5(password.encode()).hexdigest()
if password == get_userpw(cursor, loginUserName):
    status = True

if(EchooFunctions.checkUserType(cursor, loginUserName)) == "administrator":
   welcome = """ <h1>Welcome, Administrator</h1>"""
else:
   welcome = """ <h1>Welcome</h1>"""
blank = ""

Login = False

if "echooUser" in str(os.environ):
        Login = True

if Login == False:
    if status == False or loginUserName == 'Null' or password == 'Null':
        print(html_1)
        print(html_2)
        print(failed)
        print(html_en)

    if status == True:
        print(html_1)
        print(html_2JS)
        print(welcome)
        print(html_en)
        try:
            SQL = "SELECT userID FROM user WHERE username = '"+loginUserName+"';"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            userID = results[0][0]
            try:
                SQL = "UPDATE user SET status = 'online' WHERE userID = "+str(userID)+";"
                cursor.execute(SQL)
                db_con.commit()
            except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
            else:
                print("")
else:
    print("<h1>You have already login with an account</h1><br>")
    print("<h2><a href='index.cgi'>Return to Home Page</a></h2>")
