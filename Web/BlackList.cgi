#! /usr/bin/env python3
 
import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os
print ('Content-type: text/html\n')

form = cgi.FieldStorage()
action = form.getfirst("action", "")
receiverID = form.getfirst("user", "")

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
if "echooUser" in str(os.environ):
        userID = EchooFunctions.getUserID(cursor, userName)

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
    <body onload="redirect('friendList.cgi?user="""
html += str(userID)
html +="""')">
    </body>
    </html>"""

if action=="BlackList":
        try:
                SQL1 = "INSERT INTO black_list VALUES("+str(userID)+", "+str(receiverID)+");"
                cursor.execute(SQL1)
                db_con.commit()
        except Exception as e:
                print('<p>Something went wrong with the SQL1!</p>')
                print(SQL, "Error:", e)
        else:
                
                try:
                        SQL2 = "DELETE FROM friend_list WHERE userID = "+str(userID)+" AND friend_userID = "+str(receiverID)+";"
                        cursor.execute(SQL2)
                        db_con.commit()
                except Exception as e:
                        print('<p>Something went wrong with the SQL2!</p>')
                        print(SQL, "Error:", e)
                else:
     
                        try:
                                SQL3 = "DELETE FROM friend_list WHERE userID = "+str(receiverID)+" AND friend_userID = "+str(userID)+";"
                                cursor.execute(SQL3)
                                db_con.commit()
                        except Exception as e:
                                print('<p>Something went wrong with the SQL3!</p>')
                                print(SQL, "Error:", e)
                        else:
                                try:
                                        SQL4 = "DELETE FROM request WHERE senderID = "+str(receiverID)+" AND receiverID = "+str(userID)+";"
                                        cursor.execute(SQL4)
                                        db_con.commit()
                                except Exception as e:
                                        print('<p>Something went wrong with the SQL4!</p>')
                                        print(SQL, "Error:", e)
                                else:
                                        try:
                                                SQL5 = "DELETE FROM request WHERE senderID = "+str(userID)+" AND receiverID = "+str(receiverID)+";"
                                                cursor.execute(SQL5)
                                                db_con.commit()
                                        except Exception as e:
                                                print('<p>Something went wrong with the SQL5!</p>')
                                                print(SQL, "Error:", e)
                                        else:
                                                print("<p>Block success!</p>")
                                        

print(html)
