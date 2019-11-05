#! /usr/bin/env python3

import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os
print ('Content-type: text/html\n')

html = """
<!doctype html>
<html>
<head><meta charset="utf-8">
<title>Confirmation Page</title>
<script>

function redirect (url) {
window.location.replace(url);
}

</script></head>
    <body onload="redirect('news_main.cgi')">
    </body>
    </html>
    """
#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

form = cgi.FieldStorage()
newsID = form.getfirst("news", "")
userName = ""
userID = ""
admin = False
#change the status of veriable


if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)

if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True

if admin == True:
        print("1")
        try:
            SQL = "DELETE FROM news WHERE newsID="+str(newsID)+";"
            cursor.execute(SQL)
            db_con.commit()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            print("success leave club")

        print(html)
else:
        print("<p>Wrong access</p><a href='index.cgi'>Return</a>")
