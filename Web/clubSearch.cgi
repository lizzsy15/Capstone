#!/usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
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
    <body onload="redirect(clubMain.cgi')">
    </body>
    </html>"""

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

#main contents to insert
searchWord = form.getfirst('searchWord', '')

try:
        SQL = "SELECT clubID, icon, clubname, description FROM club;"
        cursor.execute(SQL)
        results = cursor.fetchall()
        
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
            if searchWord in row[2] or searchWord in row[3] :
                print(row[2])
            else:
                print("")

print(html)

