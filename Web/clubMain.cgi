#! /usr/bin/env python3
 
import cgi, MySQLdb, hashlib, time, requests, os, EchooFunctions
print ('Content-type: text/html\n')

html="""
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
		<link rel="stylesheet" href="css/signUp.css">
    <link rel="stylesheet" href="css/clubMain.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
html+= EchooFunctions.setLoginStatus('club')
html+="""<div class="searchRow">
      <form action="SearchClub.cgi" class="searchBar">
        <input type="text" placeholder="Search.." name="search">
        <button type="submit"><i class="fa fa-search"></i></button>
      </form>
      <a href="createClub.cgi" class="createClubLink">Create Club</a>
    </div>
		<!-- article box-->
		<article class="block">
			<h1>My Favorite Clubs</h1>
				<div class="interBlock1">
				{message1}

			</div>
							<div class="pageRow">
					{page1}
				</div>
		</article>

		<article class="block">
			<h1>Clubs</h1>
				<div class="interBlock2">
				{message2}

			</div>
							<div class="pageRow">
					{page2}
				</div>
		</article>

		<!-- footer -->
		{footer}
	</div>
	</body>
</html>

"""

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"
topPage= form.getfirst('topPage', '1')
topPage = int(topPage)
buttomPage = form.getfirst('buttomPage', '1')
buttomPage = int(buttomPage)
userName = ""
userID = ""
footer = EchooFunctions.setFooter()
isGuest = True
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
        isGuest = False
message1 = ""
message2=""
page2=""
page1 = ""
numberInPage1 = "test"
lastPage1 = True
lastPage2 = True
#delete
if isGuest == False:
        try:
                SQL = "select count(userID) from club_user where userID = " + str(userID) +" ;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                if results:
                        numberInPage1 = str(results[0][0])
                        different = int(numberInPage1)-int(topPage)*6
                        if different > 0:
                                lastPage1 = False
                else:
                        numberInPage1 = 0
                        lastPage1 = True
        
        if int(topPage) == 1:
                page1 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                page1 +='<a href="#" class="currentPage">1</a>'
                if lastPage1 == False:
                        for i in range(7):
                                topPage+= 1
                                if topPage*6 < int(numberInPage1):
                                        page1 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                        page1 += str(buttomPage) + '">'+str(topPage)+'</a>'
                                if topPage*6 > int(numberInPage1):
                                        page1 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                        page1 += str(buttomPage) + '">'+str(topPage)+'</a>'
                                        break
                topPage= form.getfirst('topPage', '1')
                topPage = int(topPage)
                if lastPage1 == False:
                        page1 +='<a href="clubMain.cgi?topPage='+str(topPage+1)+'&buttomPage='
                        page1 += str(buttomPage)+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                page1 +='<a href="clubMain.cgi?topPage='+str(topPage-1)+'&buttomPage='
                page1 += str(buttomPage)+'"><i class="fas fa-arrow-left"></i></a>'
                page1 +='<a href="clubMain.cgi?platform='+str(topPage-1)+'&buttomPage='
                page1 += str(buttomPage)+'">'+str(topPage-1)+'</a>'
                for i in range(7):
                        if topPage*6 < int(numberInPage1):
                                page1 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                page1 += str(buttomPage) + '">'+str(topPage)+'</a>'
                                topPage += 1
                        if topPage*6 > int(numberInPage1):
                                page1 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                page1 += str(buttomPage) + '">'+str(topPage)+'</a>'
                                break
                topPage= form.getfirst('topPage', '1')
                topPage = int(topPage)
                if lastPage1 == False:
                        page1 +='<a href="clubMain.cgi?topPage='+str(topPage+1)+'&buttomPage='
                        page1 += str(buttomPage)+'"><i class="fas fa-arrow-right"></i></a>'
                        

        topPage= form.getfirst('topPage', '1')
        topPage = int(topPage)

        page2 = ""

        try:
                SQL = "SELECT c.clubID, c.icon,c.clubname,c.description FROM club AS c, club_user AS cu WHERE  NOT EXISTS(SELECT * FROM club_user AS cu WHERE c.clubID = cu.clubID AND cu.userID ="
                SQL += str(userID)+" ) GROUP BY c.clubname ORDER BY clubID DESC;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                if results:
                        numberInPage2 = str(len(results))
                        different = int(numberInPage2)-int(buttomPage)*9
                        if different > 0:
                                lastPage2 = False
                else:
                        numberInPage2 = 0
                        lastPage2 = True
                
        if int(buttomPage) == 1:
                page2 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                page2 +='<a href="#" class="currentPage">1</a>'
                if lastPage2 == False:
                        for i in range(7):
                                buttomPage+= 1
                                if buttomPage*9 < int(numberInPage2):
                                        page2 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                        page2 += str(buttomPage) + '">'+str(buttomPage)+'</a>'
                                if buttomPage*9 > int(numberInPage2):
                                        page2 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                        page2 += str(buttomPage) + '">'+str(buttomPage)+'</a>'
                                        break
                buttomPage = form.getfirst('buttomPage', '1')
                buttomPage = int(buttomPage)
                if lastPage2 == False:                
                        page2 +='<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                        page2 += str(buttomPage+1)+'"><i class="fas fa-arrow-right"></i></a>'
        else:
                page2 +='<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                page2 += str(buttomPage-1)+'"><i class="fas fa-arrow-left"></i></a>'
                page2 +='<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                page2 += str(buttomPage-1)+'">'+str(buttomPage-1)+'</a>'
                for i in range(7):
                        if buttomPage*9 < int(numberInPage2):
                                page2 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                page2 += str(buttomPage) + '">'+str(buttomPage)+'</a>'
                                buttomPage += 1
                        if buttomPage*9 > int(numberInPage2):
                                page2 += '<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                                page2 += str(buttomPage) + '">'+str(buttomPage)+'</a>'
                                break
                buttomPage = form.getfirst('buttomPage', '1')
                buttomPage = int(buttomPage)
                if lastPage2 == False:
                        page2 +='<a href="clubMain.cgi?topPage='+str(topPage)+'&buttomPage='
                        page2 += str(buttomPage+1)+'"><i class="fas fa-arrow-right"></i></a>'

        buttomPage = form.getfirst('buttomPage', '1')
        buttomPage = int(buttomPage)
        #main contents to insert
        message1 = ""
        club_count = 1
        try:
                SQL = "SELECT c.clubID, c.icon,c.clubname,c.description FROM club AS c, club_user AS cu WHERE c.clubID = cu.clubID AND cu.userID= "+str(userID)+" ;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                for row in results:   
                        if club_count <= int(topPage)*6 and club_count >(int(topPage)-1)*6:
                                icon = ""
                                if str(row[1]) == "None":
                                        icon = "nullivon.jpg"
                                else:
                                        icon = str(row[1])
                                message1 += '<div class="article">'
                                message1 += '<img src="images/club/'+str(icon)+'" alt="article1">'
                                message1 += '<div class="title"><p><a href="clubMessage.cgi?club='+str(row[0])
                                clubName2 = ""
                                word_count3 = 0
                                for x in row[2]:
                                        if word_count3 <= 20:
                                                clubName2 += x
                                                word_count3 += 1
                                                
                                        else:
                                                clubName2+="..."
                                                break
                                message1 +='#current">'+clubName2+'</a></p>'
                                message1 += '<p>'+row[3]+'</p></div></div>'
                                club_count+=1
                        else:
                                club_count+=1
        club_count = 1
        message2 = ""

        try:
                SQL = "SELECT c.clubID, c.icon,c.clubname,c.description FROM club AS c, club_user AS cu WHERE  NOT EXISTS(SELECT * FROM club_user AS cu WHERE c.clubID = cu.clubID AND cu.userID = "+str(userID)+" ) GROUP BY c.clubname "
                SQL += "ORDER BY clubID DESC;"
                cursor.execute(SQL)
                results = cursor.fetchall()
        except Exception as e:
                print('<p>Something went wrong with the SQL!</p>')
                print(SQL, "Error:", e)

        else:
                if results:
                        for row in results:
                                if club_count <= int(buttomPage)*9 and club_count >(int(buttomPage)-1)*9:
                                        icon = ""
                                        if str(row[1]) == "None":
                                                icon = "nullivon.jpg"
                                        else:
                                                icon = str(row[1])
                                        message2 += '<div class="article">'
                                        message2 += '<img src="images/club/'+str(icon)+'" alt="article1">'
                                        message2 += '<div class="title"><p><a href="clubMessage.cgi?club='+str(row[0])
                                        clubName3 = ""
                                        word_count4 = 0
                                        for x in row[2]:
                                                if word_count4 <= 20:
                                                        clubName3 += x
                                                        word_count4 += 1
                                                else:
                                                        clubName3+="..."
                                                        break
                                        message2 += '#current">'+clubName3+'</a></p>'
                                        message2 += '<p>'+row[3]+'</p></div></div>'
                                        club_count+=1
                                else:
                                        club_count+=1

        #print out html
        print(html.format(message1 = message1, message2=message2, page1 = page1, page2=page2, footer = footer))
else:
        message1 = "Please sign up or log in before you use the club functions"
        print(html.format(message1 = message1, message2=message2, page1 = page1, page2=page2, footer = footer))
