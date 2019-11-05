#! /usr/bin/env python3
 
import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os
print ('Content-type: text/html\n')

htmlOpen="""
    <!doctype html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>Echooo</title>
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<!-- Stylesheets -->
		<link rel="stylesheet" href="css/normalize.css">
		<link rel="stylesheet" href="css/styles.css">
		<link rel="stylesheet" href="css/index.css">
    <link rel="stylesheet" href="css/boardAllPost.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
htmlOpen += EchooFunctions.setLoginStatus('board')

form = cgi.FieldStorage()

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
        
admin = False
#change the status of veriable
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
                
moderator = False
page = form.getfirst('page', '1')
page = int(page)
board = form.getfirst('board', '37')
errorTitle = form.getfirst('errorTitle', '')
errorDetail = form.getfirst('errorDetail', '')
sort_order = form.getfirst("sortingList", "desc")
post_count = 1
boardName = ""

try:
        SQL = "SELECT boardname FROM board WHERE boardID = "+str(board)+";"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                boardName = row[0]
html="""
    <div class="row post_sort">"""

if admin == True:
        html+="""<div class="makeAPost">
                <a href="confirmationPageEBOPT.cgi?board="""
        html+= board
        html+='" >Delete this Board</a></div>'
html+="<h3>"+str(boardName)+"</h3>"
html+="""<div class="sorting">
        <p>Sort By:</p>
        <select id="sortingList" onchange="sorting()">"""
if sort_order == "desc":
        html+="""
          <option value="desc">From newest to oldest</option>
          <option value="asc">From oldest to newest</option>"""
else:
        html+="""
<option value="asc">From oldest to newest</option>
<option value="desc">From newest to oldest</option>"""
html+="""</select>
      </div>
    </div>
        		<script>
		function sorting() {
			var x = document.getElementById("sortingList").value;"""
html+="window.location.replace('boardAllPost.cgi?board="+str(board)
html+="""&sortingList='+x);
		}

		</script>
    <!-- Main -->
		<article class="main">
      <table>
        <thead>
          <tr><td class="title">Title:</td><td class="middleHead">Author:</td><td class="middleHead">Date:</td></tr>
        </thead>
        <tbody>"""
html2="""</tbody>
      </table>
      <div class="pageRow">"""

lastPage = False
post_count=1
totalNum = 0

try:
        SQL = "SELECT count(postID) FROM post WHERE boardID = "+str(board)+";"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                totalNum += int(row[0])
                if int(row[0]) <= (10*int(page)):
                        lastPage = True
if page == 1:
        if lastPage == False:
                html2 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                html2 +='<a href="#" class="currentPage">1</a>'
                page_count = 2
                for i in range(9):
                        if ((int(page_count)+1)*10)>int(totalNum):
                                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                                html2 += str(page_count)+'">'+str(page_count)+'</a>'
                                break
                        else:
                                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                                html2 += str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                html2 += str(2)+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                html2 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                html2 +='<a href="#" class="currentPage">1</a>'
                html2 +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
if page != 1:
        if lastPage == False:
                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                html2 += str((int(page)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                html2 += str((int(page)-1))+'">'+str(int(page)-1)+'</a>'
                page_count = int(page)
                for i in range(9):
                        if ((int(page_count)+1)*10)>int(totalNum):
                                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                                html2 += str(page_count)+'" class="currentPage">'+str(page_count)+'</a>'
                                break
                        else:
                                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                                html2 += str(page_count)+'">'+str(page_count)+'</a>'
                                page_count += 1
                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                html2 += str((int(page)+1))+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                html2 += str((int(page)-1))+'"><i class="fas -arrow-left"></i></a>'
                html2 +='<a href="boardAllPost.cgi?board='+str(board)+'&page='
                html2 += str((int(page)-1))+'">'+str((int(page)-1))+'</a>'
                html2 +='<a href="#" class="currentPage">'+str(page)+'</a>'
                html2 +='<a href="#"><i class="fas fa-arrow-right"></i></a>'

page = form.getfirst("page", "1")
page = int(page)
html2 += """</div>
    </article>

    <!-- MakePost -->
    <article class="postBlock">
			<h1 class="sr-only">Post</h1>
      <form method="post" action='createPost.cgi?board="""
html2 += board
html2 += """'>
        <input type="text" name="title" """

if errorTitle != "":
        html2+='value="'
        html2 += errorTitle
else:
        html2 += 'placeholder="title"'
html2+='" class="titleInput"><textarea name="content"'
if "echooUser" in str(os.environ):
        if errorDetail != "":
                html2 += ' class="contentInput">'+str(errorDetail)+'</textarea><button type="submit">Post</button>'
        else:
                html2 += 'placeholder="content" class="contentInput"></textarea><button type="submit">Post</button>'
else:
        html2 += """="Login before you can make a post" class="contentInput"></textarea>"""
html2 += """</form>
		</article>

		<!-- footer -->
"""
html2 += EchooFunctions.setFooter()
html2 +="""
            </div>
	</body>
</html>
"""



#main contents to insert
content = ""
black_list=[]
if userID!= '':
        try:
                SQL = "SELECT userID FROM black_list WHERE block_userID="+str(userID)+";"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the first SQL!</p>')
                print(SQL, "Error:", e)
        else:
                if results:
                        for row in results:
                                black_list.append(row[0])

        try:
                SQL = "SELECT block_userID FROM black_list WHERE userID="+str(userID)+";"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the first SQL!</p>')
                print(SQL, "Error:", e)
        else:
                if results:
                        for row in results:
                                black_list.append(row[0])
try:
        SQL = "SELECT post.postID, post.title, user.username, post.time_in, user.userID FROM post, user, sticky WHERE post.boardID = "
        SQL += board + " and post.userID = user.userID and post.postID = sticky.postID ORDER BY post.time_in desc;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the first SQL!</p>')
        print(SQL, "Error:", e)

else:
        for row in results:
                if row[4] not in black_list:
                        if post_count<=(int(page)*10) and post_count>=(int(page)-1)*10:
                                if userID != "":
                                        if admin == True or moderator == True or userName == row[2]:
                                                content += '<tr><td><div class="row"><a href="article.cgi?post='+str(row[0])+'"><i class="fas fa-map-pin"></i>'+row[1]+'</a>'
                                        else:
                                                content += '<tr><td><a href="article.cgi?post='+str(row[0])+'"><i class="fas fa-map-pin"></i>'+row[1]+'</a>'
                                        if admin == True or moderator == True or userName == row[2]:
                                                content += '<div class="selection"><a href="editPost.cgi?post='+str(row[0])+'&board='+str(board)
                                                content +='">Edit</a><a href="confirmationPage.cgi?deletePost='+str(row[0])+'&board='+str(board)+'">Delete</a>'
                                                if admin == True or moderator == True:
                                                        content += '<a href="stickyPost.cgi?postID='+str(row[0])+'&boardID='+str(board)+'">Sticky</a>'
                                                        content += '<a href="report.cgi?type=post&postID='+str(row[0])+'&boardID='+str(board)+'">Report</a></div>'
                                        if admin == False and userName != row[2]:
                                                content += '<div class="selection"><a href="report.cgi?type=post&postID='+str(row[0])+'&boardID='+str(board)+'">Report</a>'
                                if userID == "":
                                        content += '<tr><td><a href="article.cgi?post='+str(row[0])+'"><i class="fas fa-map-pin"></i>'+row[1]+'</a>'
                                content += '</td><td class="middle">' + '<a href="userProfile.cgi?userid='+str(row[4])+'">'+str(row[2])+'</a>'
                                content += '</td><td>'+str(row[3])
                                content += '</td></tr>'
                                post_count += 1
                        if post_count>=((int(page)+1)*10):
                                break
                        if post_count<=((int(page)-1)*10):
                                post_count+=1

if sort_order =="desc":
        try:
                SQL = "SELECT post.postID, post.title, user.username, post.time_in,user.userID FROM post, user WHERE post.boardID = "
                SQL += board
                SQL += " and post.userID = user.userID and post.postID NOT IN (SELECT postID from sticky) ORDER BY post.time_in desc;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the second SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:
                        if row[4] not in black_list:
                                if post_count<=(int(page)*10) and post_count>(int(page)-1)*10:
                                        if userID != "":
                                                if admin == True or moderator == True or userName == row[2]:
                                                                content += '<tr><td><div class="row"><a href="article.cgi?post='+str(row[0])+'">'+row[1]+'</a>'
                                                else:
                                                        content += '<tr><td><a href="article.cgi?post='+str(row[0])+'">'+row[1]+'</a>'
                                                if admin == True or moderator == True or userName == row[2]:
                                                        content += '<div class="selection"><a href="editPost.cgi?post='+str(row[0])+'&board='+str(board)
                                                        content +='">Edit</a><a href="confirmationPage.cgi?deletePost='+str(row[0])+'&board='+str(board)+'">Delete</a>'
                                                        if admin == True or moderator == True:
                                                                content += '<a href="stickyPost.cgi?postID='+str(row[0])+'&boardID='+str(board)+'">Sticky</a>'
                                                                content += '<a href="report.cgi?type=post&postID='+str(row[0])+'&boardID='+str(board)+'">Report</a></div>'
                                                if admin == False and userName != row[2]:
                                                        content += '<div class="selection"><a href="report.cgi?type=post&postID='+str(row[0])+'&boardID='+str(board)+'">Report</a>'
                                        if userID == "":
                                                content += '<tr><td><a href="article.cgi?post='+str(row[0])+'">'+row[1]+'</a>'
                                        content += '</td><td class="middle">' + '<a href="userProfile.cgi?userid='+str(row[4])+'">'+str(row[2])+'</a>'
                                        content += '</td><td>'+str(row[3])
                                        content += '</td></tr>'
                                        post_count += 1
                                if post_count>=((int(page)+1)*10):
                                        break
                                if post_count<=((int(page)-1)*10):
                                        post_count+=1
if sort_order == "asc":
        try:
                SQL = "SELECT post.postID, post.title, user.username, post.time_in, user.userID FROM post, user WHERE post.boardID = "
                SQL += board
                SQL += " and post.userID = user.userID and post.postID NOT IN (SELECT postID from sticky) ORDER BY post.time_in asc;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the second SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:
                        if row[4] not in black_list:
                                if post_count<=(int(page)*10) and post_count>(int(page)-1)*10:
                                        if userID != "":
                                                if admin == True or moderator == True or userName == row[2]:
                                                                content += '<tr><td><div class="row"><a href="article.cgi?post='+str(row[0])+'">'+row[1]+'</a>'
                                                else:
                                                        content += '<tr><td><div class="row"><a href="article.cgi?post='+str(row[0])+'">'+row[1]+'</a>'
                                                if admin == True or moderator == True or userName == row[2]:
                                                        content += '<div class="selection"><a href="editPost.cgi?post='+str(row[0])+'&board='+str(board)
                                                        content +='">Edit</a><a href="confirmationPage.cgi?deletePost='+str(row[0])+'&board='+str(board)+'">Delete</a>'
                                                        if admin == True or moderator == True:
                                                                content += '<a href="stickyPost.cgi?postID='+str(row[0])+'&boardID='+str(board)+'">Sticky</a>'
                                                        content += '<a href="report.cgi?type=post&postID='+str(row[0])+'&boardID='+str(board)+'">Report</a></div></div>'
                                                if admin == False and userName != row[2]:
                                                        content += '<div class="selection"><a href="report.cgi?type=post&postID='+str(row[0])+'&boardID='+str(board)+'">Report</a>'
                                        if userID == "":
                                                content += '<tr><td><div class="row"><a href="article.cgi?post='+str(row[0])+'">'+row[1]+'</a>'
                                        content += '</td><td class="middle">' + '<a href="userProfile.cgi?userid='+str(row[4])+'">'+str(row[2])+'</a>'
                                        content += '</td><td>'+str(row[3])
                                        content += '</td></tr>'
                                        post_count += 1
                                if post_count>=((int(page)+1)*10):
                                        break
                                if post_count<=((int(page)-1)*10):
                                        post_count+=1


#print out html
print(htmlOpen)
print(html)
print(content)
print(html2)
