#!/usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

clubID = form.getfirst("club", "")
userName = ""
userID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
detail = form.getfirst("comment", "")
detail = EchooFunctions.specialChara(detail)
detail = detail.replace("&","&amp;")
detail = detail.replace("'","&rsquo;")
detail = detail.replace("\n","<p>")
detail = detail.replace("-","&mdash;")
detail = detail.replace('"',"Alt 34")
detail = detail.replace("‘","&rsquo;")
detail = detail.replace("’","&rsquo;")
time_in = EchooFunctions.getDateTime()
message = ""
error=False

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
    <body onload="redirect('clubMessage.cgi?club="""
html += str(clubID)
html +="""#current')">
    </body>
    </html>"""

if detail.replace(" ","") == "":
    message += "<p>missing text</p>"
    error=True
    
if EchooFunctions.wordCensor(detail):
        message += "Detected one or more banned words in text"
        error = True

if error == False:
        try:
            SQL = "INSERT INTO club_message(clubID, userID, detail, send_time) VALUES("+str(clubID)+", "+str(userID)+", '"+detail+"', '"+time_in+"');"
            cursor.execute(SQL)
            db_con.commit()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            message += "<p>Message Sent!</p>"

print(html)
