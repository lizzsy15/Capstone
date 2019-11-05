#! /usr/bin/env python3

import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

html="""<!doctype html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>Echooo</title>
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<script>
function redirect (url) {
window.location.replace(url);
}

</script>
	</head>"""
	
html2="""
    </body>
</html>"""


form = cgi.FieldStorage()

title = form.getfirst("title", "")
detail = form.getfirst("content", "")
detail = EchooFunctions.specialChara(detail)
detail = detail.replace("&","&amp;")
detail = detail.replace("'","&rsquo;")
detail = detail.replace("\n","<p>")
detail = detail.replace("-","&mdash;")
detail = detail.replace('"',"Alt 34")
time_in = EchooFunctions.getDateTime()
boardID = form.getfirst("board","")
message = ""
error = False
#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

userID = EchooFunctions.getUserID(cursor, EchooFunctions.getUserName()[0])

htmlDirect = """<body onload="redirect('boardAllPost.cgi?board="""
htmlDirect += boardID
htmlDirect += """&page=1')">"""
if title.replace(" ","") == "" or detail.replace(" ","") == "":
	message += "<p>missing text</p>"
	error = True
if boardID == "":
	message += "<p>missing boardID</p>"
	error = True

if EchooFunctions.wordCensor(title):
        message = "Detected one or more banned words in title"
        error = True
if EchooFunctions.wordCensor(detail):
        message = "Detected one or more banned words in content"
        error = True
        
if error == False:
        try:
                SQL = "INSERT INTO post(title, detail, time_in, userID, boardID)"
                SQL += 'VALUES ("'+title+'", "'+detail+'", "'+time_in+'", '+str(userID)+','+str(boardID)+');'
                cursor.execute(SQL)
                db_con.commit()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
        else:
                message += "<p>Successful!</p>"


        
print(html)
if error == False:
        print(htmlDirect)
if error == True:
        print("<form action='boardAllPost.cgi'>")
        print("<input type='hidden' name='ddd' value='ddd'>")
        print("<input type='hidden' name='errorTitle' value='"+str(title)+"'>")
        print("<input type='hidden' name='errorDetail' value='"+str(detail)+"'>")
        print("<input type='hidden' name='board' value='"+str(boardID)+"'>")
        print('<input type="submit" value="Return"></form>')
        
print(message)
print(html2)
