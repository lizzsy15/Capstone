#!/usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

form = cgi.FieldStorage()

action = form.getfirst("action", "")
receiverID = form.getfirst("user","")

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
    <body onload="redirect('userProfile.cgi?userid="""
html += str(receiverID)
html +="""')">
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


if action == "remove":
    try:
        SQL = "DELETE FROM request WHERE senderID = "+str(userID)+" AND receiverID = "+str(receiverID)+";"
        cursor.execute(SQL)
        db_con.commit()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        print("<p>Remove Friend Request!</p>")


if action == "send":
    try:
        SQL = "INSERT INTO request(senderID, receiverID) VALUES("+str(userID)+", "+str(receiverID)+");"
        cursor.execute(SQL)
        db_con.commit()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        print("<p>Sent Friend Request!</p>")


if action == "unfriend":
    try:
        SQL = "DELETE FROM friend_list WHERE userID = "+str(userID)+" AND friend_userID = "+str(receiverID)+";"
        cursor.execute(SQL)
        db_con.commit()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        try:
                SQL1 = "DELETE FROM friend_list WHERE userID = "+str(receiverID)+" AND friend_userID = "+str(userID)+";"
                cursor.execute(SQL1)
                db_con.commit()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
        else:
                print("<p>Unfriended!</p>")

print(html)
