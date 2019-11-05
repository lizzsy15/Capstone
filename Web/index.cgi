#!/usr/bin/env python3
  
import cgi, MySQLdb, hashlib, time, requests, os, re, EchooFunctions
print ('Content-type: text/html\n')
html6 = """
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
    <link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

    <!-- Font Awesome - For use in I360 -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



    <!--[if lte IE 9]>
      <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
    <![endif]-->
  </head>"""

html7 = """    <!-- Header -->
    <header>
      <div class="content container">
        <a href="#"><img class="mySlides" src="images/banner/pic1.jpg" alt="COD"></a>
        <a href="#"><img class="mySlides" src="images/banner/pic2.jpg" alt="Kingdom Heart"></a>
      </div>
    </header>

    <script>

    var myIndex = 0;
    slideShow();

    function slideShow() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}
    x[myIndex-1].style.display = "block";
    setTimeout(slideShow, 3000);
    }
    </script>

    <!-- Announcement-->
    <article class="block">
      <h1 class="sr-only">Announcement</h1>
      <div class="box announ">
        <h2>Announcement"""
html8 = """</h2><div class="innerBox announInner">"""

html1_5 ="""</div>
      </div>
    </article>

    <!-- Main -->
    <article class="main">
      <h1 class="sr-only">Main</h1>
      <div class="container">
        <section class="right">
            <h2> Popular Boards </h2>
            <div class="BoardBox">
              <table>
                <tr><td>Board</td><td>Posts</td></tr>"""
html2 = """</table>
              <div class="more"><a href="http://cgi.soic.indiana.edu/~team34/Capstone/boardMain.cgi">Find More</a></div>
            </div>
        </section>
        <section>
            <h2> Popular Clubs </h2>
            <div class="BoardBox">"""
html3 ="""              <div class="more"><a href="http://cgi.soic.indiana.edu/~team34/Capstone/clubMain.cgi">Find More</a></div>
            </div>
        </section>
      </div>
    </article>

    <!-- footer -->
"""
html3 += EchooFunctions.setFooter()
html3 +="""
  </div>
  </body>
</html>
"""

form = cgi.FieldStorage()

#database connection
user = "i494f18_team34"
db_pass = "my+sql=i494f18_team34"

db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
cursor = db_con.cursor()

#main contents to insert
boardTable = ""
popularClub = ""
announ = ""
addAnnoun = ""
club_count = 0
board_count = 0
announ_count = 0
userName = ""
userID = ""
administrator = False
if "echooUser" in str(os.environ):
        userName = EchooFunctions.getUserName()
        userName = userName[0]
        userID = EchooFunctions.getUserID(cursor, userName)
        if EchooFunctions.checkUserType(cursor, userName) == 'administrator':
                administrator = True

if administrator == True:
        addAnnoun += "<a href='createNewsAnnoun.cgi?type=announ'>Add New</a>"
try:
        SQL = """SELECT b.boardname, COUNT(p.postID) as num_of_post, b.boardID
        FROM board as b, post as p
        WHERE b.boardID = p.boardID
        GROUP BY b.boardname
        ORDER BY count(p.postID) DESC
        LIMIT 5;"""
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)

else:
    for row in results:
            boardTable += "<tr>"
            boardTable += "<td><a href='boardAllPost.cgi?board="+str(row[2])+"&page=1'>" + row[0] + "</a></td>"
            boardTable += "<td>" + str(row[1]) +"</td>"
            boardTable += "</tr>"

try:
        SQL = "SELECT c.icon,c.clubname, c.clubID from club as c, club_user as cu where c.clubID = cu.clubID group by clubname order by count(userID) desc;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
else:
        for row in results:
                if club_count < 5:
                        popularClub += '<ul>'
                        popularClub += '<li><img src="images/club/'+row[0]+'" alt="'+row[1]+'">'
                        popularClub += '<a href="clubMessage.cgi?club='+str(row[2])+'#current">'+row[1]+'</a></li>'
                        popularClub += '</ul>'
                        club_count += 1

try:
        SQL = "SELECT title, detail from announcement Order by announcementID DESC;"
        cursor.execute(SQL)
        results = cursor.fetchall()
except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
else:
        for row in results:
                if announ_count < 2:
                        announ += '<h3>'
                        announ += row[0]+'</h3><p>'+row[1]+'</p>'
                        announ_count += 1

        print(html6)
        print(EchooFunctions.setLoginStatus('index'))
        print(html7)
        if administrator == True:
                print(addAnnoun)
        print(html8)
        print(announ)
        print(html1_5)
        print(boardTable)
        print(html2)
        print(popularClub)
        print(html3)
