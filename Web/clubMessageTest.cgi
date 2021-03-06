#!/usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')
html1 = """<!doctype html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>Echooo</title>
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<!-- Stylesheets -->
		<link rel="stylesheet" href="css/normalize.css">
		<link rel="stylesheet" href="css/styles.css">
		<link rel="stylesheet" href="css/signUp.css">
    <link rel="stylesheet" href="css/help.css">
    <link rel="stylesheet" href="css/ClubHome.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>
"""
html1 += EchooFunctions.setLoginStatus()
html1 += """{content}<!-- footer -->
		<footer>
			<div class="container">
				<section class="footer-menu">
					<h1 class="sr-only">Footer</h1>
					<div class="row">
						<div class="footer-menu-main">
							<a href="#"><p>Home</p></a> <p class="line">|</p>
							<a href="#"><p>Contact Us</p></a> <p class="line">|</p>
							<a href="#"><p>Terms</p></a> <p class="line">|</p>
						<div class="soical-media">
							<a href="#"><i class="fab fa-facebook"></i></a>
							<a href="#"><i class="fab fa-twitter"></i></a>
							<a href="#"><i class="fab fa-discord"></i></a>
						</div></div>
					</div>
				</section>
			</div>
		</footer>
	</div>
	</body>
</html>"""

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()


#main contents to insert
clubID = form.getfirst('club', '4')
chatroom = ""
memberList = ""
exist = False
userName = ""
userID = ""
clubControl = ""
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)

html2="""
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
		<link rel="stylesheet" href="css/clubMessage.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head><body>
		<!-- JavaScript -->


		<!-- Navigation -->
		<div class="container">
		<nav>
			<div class="container">
				<div class="row">
					<div class="logo">
						<a href="#"><img src="images/logo.jpg" alt="logo"></a>
					</div>
					<h1>Echooo</h1>
					<ul>
						<li><div class="user">
							<a href="#"><i class="fas fa-user"></i> Sign Up</a>
							<a href="#"><i class="fas fa-user"></i> Login</a>
						</div></li>
						</li>
							<div class="search-container">
								<form action="#">
									<input type="text" placeholder="Search.." name="search">
									<button type="submit"><i class="fa fa-search"></i></button>
								</form>
							</div></li>
					</ul>
				</div>
				<div class="bar">
					<ul>
						<li><a href="#"><i class="far fa-question-circle"></i> Home</a></li>
						<li><a href="#"><i class="fas fa-globe-americas"></i> What's New</a></li>
						<li><a href="#"><i class="fas fa-users"></i> Boards</a></li>
						<li><a href="#"><i class="fas fa-users"></i> Clubs</a></li>
						<li><a href="#"><i class="fas fa-scroll"></i> News</a></li>
						<li><a href="#"><i class="fas fa-scroll"></i> Help</a></li>
					</ul>
				</div>
			</div>
		</nav>"""
print("1")
html2+="""<!-- the whole container -->
<script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
<script language="javascript" type="text/javascript">

var timeout = setInterval(reloadChat, 1000);    
function reloadChat () {

     $('#chatroom').load('clubChatRoom.cgi?"""
html2+="club="+clubID
html2+="""');
}
</script>
		<article class="CenterPart">"""

html3="""<div class="chatroom">
            <ul><div id="chatroom">test</div>
					"""
html4="""</ul>
					<form method="post" action="sendMessage.cgi">"""
print("2")
html4+='<input type="hidden" name="club" value="'+str(clubID)+'"/>'
html4+="""
							<textarea name="comment"></textarea>
							<button type="submit">Send</button>
					</form>
        </div>
        <div class="memberList">
					<h1> Club Members </h1>
					<ul>"""
html5="""</ul>
        </div>
			</article>

		<!-- footer -->
		<footer>
			<div class="container">
				<section class="footer-menu">
					<h1 class="sr-only">Footer</h1>
					<div class="row">
						<div class="footer-menu-main">
							<a href="#"><p>Home</p></a> <p class="line">|</p>
							<a href="#"><p>Contact Us</p></a> <p class="line">|</p>
							<a href="#"><p>Terms</p></a> <p class="line">|</p>
						<div class="soical-media">
							<a href="#"><i class="fab fa-facebook"></i></a>
							<a href="#"><i class="fab fa-twitter"></i></a>
							<a href="#"><i class="fab fa-discord"></i></a>
						</div></div>
					</div>
				</section>
			</div>
		</footer>
	</div>
	</body>
</html>"""

print("3")
#change the status of veriable
if userName != "":
        try:
                SQL = "SELECT * from club_user where userID = " + str(userID)
                SQL += " and clubID = " + clubID +" ;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                if results:
                        exist = True

if exist == True:
        role = EchooFunctions.checkClubMemberRole(cursor, clubID, userID)[0]
        try:
                SQL = "SELECT * FROM club"
                SQL += " WHERE clubID = " + str(clubID)
                SQL += " ;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:
                        specialChar1=row[1]
                        specialChar1=EchooFunctions.returnSpecialChara(specialChar1)
                        specialChar2=row[2]
                        specialChar2=EchooFunctions.returnSpecialChara(specialChar2)
                        clubControl += '<div class="clubDescribe">'
                        clubControl += '<img src="images/club/'+row[3]+'" alt="sampleIcon">'
                        clubControl += '<h1>'+specialChar1+'</h1>'
                        clubControl += '<p>'+specialChar2+'</p>'
                        if role == "owner":
                                clubControl += '<a href="editClub.cgi?club='+clubID+'" class="editClubLink">Edit Club</a><br><br>'
                                clubControl += '<a href="deleteClub.cgi?club='+clubID+'" class="editClubLink">Delete Club</a>'
                        if role == "normal":
                                clubControl += '<a href="leaveClub.cgi?club='+clubID+'" class="editClubLink">Leave Club</a><br><br>'
                                clubControl += '<a href="report.cgi?type=club&club='+clubID+'" class="editClubLink">Report</a>'
                        clubControl +='</div>'
        try:
                SQL = "SELECT u.icon, u.username, cm.detail, cm.send_time FROM user as u, club_message as cm, club_user as cu"
                SQL += " WHERE cm.clubID = cu.clubID AND cm.userID = u.userID AND cm.clubID = " + clubID
                SQL += " GROUP BY club_messageID;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:
                    icon = ""
                    if str(row[0]) == "None":
                        icon='nullicon.jpg'
                    if str(row[0]) != "None":
                        icon=str(row[0])

                    specialChar=row[2]
                    specialChar=EchooFunctions.returnSpecialChara(specialChar)
                    if str(row[1]) == str(userName):
                            chatroom += '<li class="chatDate">'+str(row[3])+'</li>'
                            chatroom += '<li class="mainUser">'+str(row[1])+'<img src="images/user/'+icon+' "alt="club1"><br>'
                            chatroom += '<div class="messageLineMain">'+str(specialChar)+'</div></li>'
                    if str(row[1]) != str(userName):
                            chatroom += '<li class="chatDate">'+str(row[3])+'</li>'
                            chatroom += '<li class="otherUser"><img src="images/user/'+icon+' "alt="club1">'+str(row[1])+'<br>'
                            chatroom += '<div class="messageLine">'+str(specialChar)+'</div></li>'

        chatroom += '<h1 id="current"></h1>'
        print("4")
        chatroom = ""
        print("5")

        try:
                SQL = "SELECT u.icon,u.username,u.status,u.userID FROM user as u, club_user as cu WHERE u.userID = cu.userID AND cu.clubID=" + clubID +";"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
        else:
                for row in results:
                        memberList += '<li class="userOnList"><div class="groupTogether">'
                        if str(row[0]) == "None":
                                memberList +='<img src="images/user/nullicon.jpg'
                        if str(row[0]) != "None":
                                memberList +='<img src="images/user/'+str(row[0])
                        memberList +='" alt="'+row[1]+'"><a href="userProfile.cgi?userid='+str(row[3])+'">'
                        memberList += row[1]+'</a></div><span class="status">'+row[2]+'</span></li>'
        #print out html
        print("6")
        print(html2)
        print(clubControl)
        print(html3)
        print(chatroom)
        print(html4)
        print(memberList)
        print(html5)
        print("7")

if exist == False:
        try:
                SQL = "SELECT * from club where clubID = "
                SQL += clubID + ";"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)
        else:
                for row in results:
                        content ="""
                                <article class="block">
                                        <h1>"""
                        content+=row[1]+'</h1>'
                        content+= """<div class="interBlock">
                        <img src="images/club/"""
                        content += row[3] + '" alt="article1">'
                        content += """<div class="something">
                              <p class="question">Description:</p>
                              <p class="ans">"""
                        specialChar=row[2]
                        specialChar=EchooFunctions.returnSpecialChara(specialChar)
                        content += specialChar
                        content+='</p><a href="'
                        content += 'join.cgi?club='+clubID+'">Join</a></div></div></article>'
        print(html1.format(content = content))
        

