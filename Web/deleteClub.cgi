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
    <body onload="redirect('clubMain.cgi')">
    </body>
    </html>
    """
form = cgi.FieldStorage()
clubID = form.getfirst("club", "")


#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

try:
    SQL = "DELETE FROM club_message WHERE clubID="+str(clubID)+";"
    cursor.execute(SQL)
    db_con.commit()
except Exception as e:
    print('<p>Something went wrong with the SQL!</p>')
    print(SQL, "Error:", e)
else:
    try:
        SQL = "DELETE FROM club_user WHERE clubID="+str(clubID)+";"
        cursor.execute(SQL)
        db_con.commit()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        try:
            SQL = "DELETE FROM club WHERE clubID="+str(clubID)+";"
            cursor.execute(SQL)
            db_con.commit()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            print("success delete club")

print(html)
