#! /usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

form = cgi.FieldStorage()

clubID = form.getfirst("clubID", "")
clubName = form.getfirst("clubName", "")
description = form.getfirst("description", "")
icon = form.getfirst("file_name","")



html="""<!doctype html>
<html>
<head><meta charset="utf-8">
<title>Confirmation Page</title>
<script>

function redirect (url) {
window.location.replace(url);
}

</script></head>
    <body onload="redirect('clubMessage.cgi?club="""
html+=str(clubID)
html+="""')">
    </body>
    </html>"""

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
if "echooUser" not in str(os.environ) or clubName == "":
        print("<!doctype html><html><head><meta charset='utf-8'><title>Confirmation Page</title><script>")
        print("function redirect (url) {window.location.replace(url);}</script></head><body onload='redirect('index.cgi')'>You cannot access this page</body></html>")
else:
    if EchooFunctions.wordCensor(clubName):
        print("<p>Fail to update club name</p>")
        print("<p>Detected one or more banned words in club name</p>")
        print("<a href='clubMessage.cgi?club="+str(clubID)+"#current"+"'>Return</a>")
    elif EchooFunctions.wordCensor(description):
        print("<p>Fail to update club description</p>")
        print("<p>Detected one or more banned words in club description</p>")
        print("<a href='clubMessage.cgi?club="+str(clubID)+"#current"+"'>Return</a>")
    else:
        if icon == "":
            print("1")
            try:
                SQL="UPDATE club SET clubname='"+clubName+"', description='"+description+"' WHERE clubID="+str(clubID)+";"
                cursor.execute(SQL)
                db_con.commit()
                print("2")
            except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
            else:
                print(html)
        else:
            try:
                SQL="UPDATE club SET clubname='"+clubName+"', description='"+description+"', icon='"+icon+"' WHERE clubID="+str(clubID)+";"
                cursor.execute(SQL)
                db_con.commit()
            except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
            else:
                print(html)



                            
                            
