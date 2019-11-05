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
		<link rel="stylesheet" href="css/article.css">
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
if "echooUser" in str(os.environ):
        userID = EchooFunctions.getUserID(cursor, userName)
admin = False
moderator = False
guest = False
postID = form.getfirst('post', '4')
post_count = 1
like = EchooFunctions.postLike(cursor,postID, userID)
dislike = EchooFunctions.postDislike(cursor,postID, userID)
favorite = EchooFunctions.postFavorite(cursor,postID, userID)

likeNum = ""
dislikeNum = ""
favNum = ""

#change the status of veriable
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
if userName == "":
        guest = True

#main contents to insert
content = ""
commentContent = ""
footer = EchooFunctions.setFooter()

try:
        SQL = "select post.title, post.detail, post.time_in, user.username, post.boardID, board.boardname, user.userID From post,board,"
        SQL += "user WHERE post.userID = user.userID AND post.boardID=board.boardID AND postID =" + str(postID) + ";"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
else:
        for row in results:
                content+='<div class="return"><a href=boardMain.cgi>Board</a>/<a href=boardAllPost.cgi?board='+str(row[4])+'&page=1>'+str(row[5])+'</a></div>'
                content+='<h3>'+str(row[0])+'</h3><h6><a href="userProfile.cgi?userid='+str(row[6])+'">'
                content+= str(row[3])+'</a><span class="date">'+str(row[2])+'</span></h6><article class="content">'
                specialChara = str(row[1])
                specialChara =EchooFunctions.returnSpecialChara(specialChara)
                content += specialChara

try:
        SQL = "select user.icon, user.username, comment.detail, user.userID from user,"
        SQL += "comment where user.userID = comment.userID AND postID ="+str(postID)+";"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
else:
        for row in results:
                commentContent+='<li class="odd"><img src="images/user/'
                if str(row[0]) == "None":
                        commentContent+='nullicon.jpg'
                else:
                        commentContent+=str(row[0])
                commentContent+='" alt="club1"><span class="userComment">'
                commentContent+='<span class="userName"><a href=userProfile.cgi?userid='+str(row[3])+'>'+str(row[1])
                commentContent+='</a></span><br>'+str(row[2])+'</span></li>'

#add numbers

try:
        SQL = "select count(liked) FROM post_likes "
        SQL += "WHERE postID  =" + str(postID) + " and liked = 'YES';"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
else:
        likeNum = results[0][0]

try:
        SQL = "select count(dislike) FROM post_likes "
        SQL += "WHERE postID =" + str(postID) + " and dislike = 'YES';"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
else:
        dislikeNum = results[0][0]


try:
        SQL = "select count(postID) FROM favorite "
        SQL += "WHERE postID =" + str(postID) +";"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
else:
        favNum = results[0][0]

html=""
html+=content
html+="""</article>
<script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
<script language="javascript" type="text/javascript">
function SubmitFormData(){
var post = """
html+=str(postID)
html+=""";
var comment = $("#comment").val();
$.post("createComment.cgi", { post: post, comment: comment},
function(data) {
 $('#sendCommentForm')[0].reset();
});
}
</script>
		<!-- Comment -->
		<article>
			<div class="row">"""
if userID != "":
        html+="<form method='post' id='sendCommentForm'"
if userID == "":
        html+="<form method='post' action='#'"   
html+=""">
						<textarea name="comment" id="comment" placeholder="comment"></textarea>
						<button type="submit" id="submitFormData" onclick="SubmitFormData();">Post</button>
				</form>
				<ul class="row">
					<li><div class="likeCol">"""
if userID != "":
        html+='<a href="post_like.cgi?type=like&postID='+str(postID)+'"><i class'
if userID == "":
        html+="""<a href=""><i class"""

if userID != "":
        if not like:
                html+='="far fa-thumbs-up">'
        else:
                if str(like[0][0]) == "YES":
                        html+='="fas fa-thumbs-up">'
                if str(like[0][0]) == "None":
                        html+='="far fa-thumbs-up">'   
                
        html+='</i></a><h4>'+str(likeNum)+'</h4></div></li>'
        html+='<li><div class="likeCol"><a href="post_like.cgi?type=dislike&postID='+str(postID)+'"><i class'

        if not dislike:
                html+='="far fa-thumbs-down">'
        else:
                if str(dislike[0][0]) == "YES":
                        html+='="fas fa-thumbs-down">'
                if str(dislike[0][0]) == "None":
                        html+='="far fa-thumbs-down">'
                        
        html+='</i></a><h4>'+str(dislikeNum)+'</h4></div></li>'
        html+='<li id="like"><div class="likeCol"><a href="post_like.cgi?type=favorite&postID='+str(postID)+'"><i class'
        if not favorite:
                html+='="far fa-heart">'
        else:
                html+='="fas fa-heart">'
else:
        if not like:
                html+='="far fa-thumbs-up">'
        else:
                if str(like[0][0]) == "YES":
                        html+='="fas fa-thumbs-up">'
                if str(like[0][0]) == "None":
                        html+='="far fa-thumbs-up">'   
                
        html+='</i></a><h4>'+str(likeNum)+'</h4></div></li>'
        html+="""<li><div class="likeCol"><a href=""><i class"""

        if not dislike:
                html+='="far fa-thumbs-down">'
        else:
                if str(dislike[0][0]) == "YES":
                        html+='="fas fa-thumbs-down">'
                if str(dislike[0][0]) == "None":
                        html+='="far fa-thumbs-down">'
                        
        html+='</i></a><h4>'+str(dislikeNum)+'</h4></div></li>'
        html+="""<li id="like"><div class="likeCol"><a href=""><i class"""
        if not favorite:
                html+='="far fa-heart">'
        else:
                html+='="fas fa-heart">'
html += '</i></a><h4>'+str(favNum)
html+="""</h4></div></li>
				</ul>
			</div>
		</article>

		<div class="commentBox">
			<h6>Comments</h6>
			<div class="contact">
				<div class="comments">
					<ul>"""
html+=str(commentContent)
html += """</ul>
				</div>
			</div>
		</div>

		<!-- footer -->"""
html+=str(footer)
html+="""</div>
	</body>
</html>"""



#print out html
print(htmlOpen)
print(html)
