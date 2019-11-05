#! /usr/bin/env python3
print('Content-type: text/html\n')

import cgi, MySQLdb, hashlib, EchooFunctions

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
    <body onload="redirect('article.cgi?post="""


html2="""</body>
    </html>"""

form = cgi.FieldStorage()

string = "i494f18_team34"
dbpw = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=string, passwd=dbpw, db=string)
cursor = db_con.cursor()

postID = form.getfirst("postID", "")
selection = form.getfirst("type", "")
userID = ""
message = ""
count = 0
NotThing = False
favorite = False
username = EchooFunctions.getUserName()[0]

html +=postID
html +="""#like')">"""

try:
        SQL = "SELECT userID FROM user WHERE username = '{username}';"
        cursor.execute(SQL.format(username=username))
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SELECT USER SQL!</p>')
        print(SQL, "Error:", e)
else:
        for row in results:
                userID += str(row[0])
                
        if str(selection) == "like":
                try:
                        SQL = "SELECT * FROM post_likes;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SELECT POST LIKES SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        for row in results:
                                if str(row[0])==userID and str(row[1])==postID:
                                        if str(row[3])=="YES":
                                                try:
                                                        SQL = " DELETE FROM post_likes WHERE userID='{userID}' AND postID='{postID}';"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the REMOVE LIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Remove Liked!</p>"
                                                        NotThing = False

                                                try:
                                                        SQL = "INSERT INTO post_likes(userID, postID, liked) VALUES ('{userID}', '{postID}', 'YES');"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the LIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Liked!</p>"
                                                        NotThing = False
                                                        break
                                        
                                        if str(row[2])=="YES":
                                                try:
                                                        SQL = " DELETE FROM post_likes WHERE userID='{userID}' AND postID='{postID}';"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the REMOVE LIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Remove Liked!</p>"
                                                        NotThing = False
                                                        break

                                        else:
                                                try:
                                                        SQL = "INSERT INTO post_likes(userID, postID, liked) VALUES ('{userID}', '{postID}', 'YES');"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the LIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Liked!</p>"
                                                        NotThing = False
                                                        break
                                else:
                                        NotThing = True
                        if NotThing == True:
                                try:
                                        SQL = "INSERT INTO post_likes(userID, postID, liked) VALUES ('{userID}', '{postID}', 'YES');"
                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                        db_con.commit()
                                except Exception as e:
                                        print('<p>Something went wrong with the LIKE SQL!</p>')
                                        print(SQL, "Error:", e)
                                else:
                                        message += "<p>Liked!</p>"
                                

        if str(selection) == "dislike":
                try:
                        SQL = "SELECT * FROM post_likes;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SELECT POST LIKES SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        for row in results:
                                if str(row[0])==userID and str(row[1])==postID:
                                        if str(row[2])=="YES":
                                                try:
                                                        SQL = " DELETE FROM post_likes WHERE userID='{userID}' AND postID='{postID}';"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the REMOVE DISLIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Remove Dislike!</p>"
                                                        NotThing = False

                                                try:
                                                        SQL = "INSERT INTO post_likes(userID, postID, dislike) VALUES ('{userID}', '{postID}', 'YES');"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the DISLIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Disliked!</p>"
                                                        NotThing = False
                                                        break
                                        if str(row[3])=="YES":
                                                try:
                                                        SQL = " DELETE FROM post_likes WHERE userID='{userID}' AND postID='{postID}';"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the REMOVE DISLIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Remove Dislike!</p>"
                                                        NotThing = False
                                                        break



                                        else:
                                                try:
                                                        SQL = "INSERT INTO post_likes(userID, postID, dislike) VALUES ('{userID}', '{postID}', 'YES');"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the DISLIKE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Disliked!</p>"
                                                        NotThing = False
                                                        break
                                else:
                                        NotThing = True
                        if NotThing == True:
                                try:
                                        SQL = "INSERT INTO post_likes(userID, postID, dislike) VALUES ('{userID}', '{postID}', 'YES');"
                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                        db_con.commit()
                                except Exception as e:
                                        print('<p>Something went wrong with the DISLIKE SQL!</p>')
                                        print(SQL, "Error:", e)
                                else:
                                        message += "<p>Disliked!</p>"

                                                        
        if str(selection) == "favorite":
                try:
                        SQL = "SELECT * FROM favorite WHERE userID='{userID}' AND postID='{postID}';"
                        cursor.execute(SQL.format(userID=userID, postID=postID))
                        results = cursor.fetchall()

                except Exception as e:
                        print('<p>Something went wrong with the SELECT FAVORITE SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        if results:
                                favorite = True
                                for row in results:
                                        if str(row[0])==userID and str(row[1])==postID:
                                                try:
                                                        SQL = " DELETE FROM favorite WHERE userID='{userID}' AND postID='{postID}';"
                                                        cursor.execute(SQL.format(userID=userID, postID=postID))
                                                        db_con.commit()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the REMOVE FAVORITE SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        message += "<p>Remove from Favorites!</p>"
                                                                                                        
                                                
                if favorite == False:
                        try:
                                SQL = "INSERT INTO favorite(userID, postID) VALUES ('{userID}', '{postID}');"
                                cursor.execute(SQL.format(userID=userID, postID=postID))
                                db_con.commit()
                        except Exception as e:
                                print('<p>Something went wrong with the FAVORITE SQL!</p>')
                                print(SQL, "Error:", e)
                        else:
                                message += "<p>Added to Favorites!</p>"
                                favorite = True
                                                




print(html)
print(message)
print(html2)
