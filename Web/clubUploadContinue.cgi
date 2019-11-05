#! /usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

html="""<!doctype html>
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
    </html>"""



form = cgi.FieldStorage()

clubName = str(form.getfirst("clubName", ''))

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

userName = ""
userID = ""
clubID = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
if "echooUser" not in str(os.environ) or clubName == "":
        print("<!doctype html><html><head><meta charset='utf-8'><title>Confirmation Page</title><script>")
        print("function redirect (url) {window.location.replace(url);}</script></head><body onload='redirect('index.cgi')'>You cannot access this page</body></html>")
else:
        try:
                SQL = 'Select clubID from club where clubname = "'
                SQL += str(clubName)+'";'
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
        else:
                clubID = results[0][0]

                try:
                        SQL = 'SELECT clubname, description FROM club WHERE clubID = '+str(clubID)+';'
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        clubname = results[0][0]
                        description = results[0][1]
                        if EchooFunctions.wordCensor(clubname):
                                try:
                                        SQL = "DELETE FROM club WHERE clubID = "+str(clubID)+";"
                                        cursor.execute(SQL)
                                        db_con.commit()
                                except Exception as e:
                                        print('<p>Something went wrong with the SQL!</p>')
                                        print(SQL, "Error:", e)
                                else:
                                        print("<p>Fail to create club</p>")
                                        print("<p>Detected one or more banned words in club name</p>")
                                        print("<form action='createClub.cgi'>")
                                        print('<input type="submit" value="Return"></form>')
                        elif EchooFunctions.wordCensor(description):
                                try:
                                        SQL = "DELETE FROM club WHERE clubID = "+str(clubID)+";"
                                        cursor.execute(SQL)
                                        db_con.commit()
                                except Exception as e:
                                        print('<p>Something went wrong with the SQL!</p>')
                                        print(SQL, "Error:", e)
                                else:
                                        print("<p>Fail to create club</p>")
                                        print("<p>Detected one or more banned words in club description</p>")
                                        print("<form action='createClub.cgi'>")
                                        print('<input type="submit" value="Return"></form>')
                        else:
                                try:
                                        SQL = "Insert into club_user Values("
                                        SQL += str(userID)+','+str(clubID)+','+'"owner");'
                                        cursor.execute(SQL)
                                        db_con.commit()
                                except Exception as e:
                                        print('<p>Something went wrong with the SQL!</p>')
                                        print(SQL, "Error:", e)
                                else:
                                        print(html)

