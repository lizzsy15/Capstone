#!/usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

form = cgi.FieldStorage()
selection = form.getfirst("type", "")

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
email = form.getfirst('email',"")
subject = form.getfirst('subject',"")
subject = EchooFunctions.specialChara(subject)
subject = subject.replace("&","&amp;")
subject = subject.replace("'","&rsquo;")
subject = subject.replace("?","&rsquo;")
subject = subject.replace("?","&rsquo;")
subject = subject.replace("\n","<p>")
subject = subject.replace("-","&mdash;")
subject = subject.replace('"',"Alt 34")
subject = subject.replace('?',"Alt 34")
subject = subject.replace('?',"Alt 34")
detail = form.getfirst("detail", "")
detail = EchooFunctions.specialChara(detail)
detail = detail.replace("&","&amp;")
detail = detail.replace("'","&rsquo;")
detail = detail.replace("?","&rsquo;")
detail = detail.replace("?","&rsquo;")
detail = detail.replace("\n","<p>")
detail = detail.replace("-","&mdash;")
detail = detail.replace('"',"Alt 34")
detail = detail.replace('?',"Alt 34")
detail = detail.replace('?',"Alt 34")
time_in = EchooFunctions.getDateTime()
message = ""

html = """
<!doctype html>
<html>
<head><meta charset="utf-8">
<title>Confirmation Page</title>
<script>

function redirect (url) {
window.location.replace(url);
}

</script></head>"""


if detail.replace(" ","") == "" or subject.replace(" ","") == "" or email.replace(" ","") == "" :
    message += "<p>missing text</p>"
    html+=    """<body onload="redirect('contactUS.cgi')">
    </body>
    </html>"""
    print(message)
    print(html)

elif "@" not in email:
        message += "<p>not a valid email</p>"
        html+=    """<body onload="redirect('contactUS.cgi')">
    </body>
    </html>"""
        print(message)
        print(html)
        
else:
        try:
                SQL = "INSERT INTO contacts(email, title, detail, time_in) VALUES('"+email+"', '"+subject+"', '"+detail+"', '"+time_in+"');"
                cursor.execute(SQL)
                db_con.commit()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
        else:
                message += "<p>Contact Sent!</p>"
                html+=    """<body onload="redirect('index.cgi')">
    </body>
    </html>"""
                print(message)
                print(html)

