#! /usr/bin/env python3
print('Content-type: text/html\n')

import cgi, MySQLdb, hashlib, requests, os, EchooFunctions

html = """
<!doctype html>
<html>
<head><meta charset="utf-8">
<title>Confirmation Page</title>
<script>
function delete_cookie( name ) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;';
  window.location.replace('index.cgi');
}

function redirect (url) {
window.location.replace(url);
}

</script></head>
    <body onload="delete_cookie('echooUser')">
    </body>
    </html>"""

form = cgi.FieldStorage()

string = "i494f18_team34"
dbpw = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=string, passwd=dbpw, db=string)
cursor = db_con.cursor()

userName = ""
userID = ""
if "echooUser" in str(os.environ):
    userName = EchooFunctions.getUserName()
    userName = userName[0]
    userID = EchooFunctions.getUserID(cursor, userName)
try:
    SQL = "UPDATE user SET status = 'offline' WHERE userID = "+str(userID)+";"
    cursor.execute(SQL)
    db_con.commit()
except Exception as e:
    print('<p>Something went wrong with the SQL!</p>')
    print(SQL, "Error:", e)
else:
    print("See You!")

print(html)
