import EchooFunctions, cgi, MySQLdb, hashlib, time, requests, os, re, datetime
  
#return the user rank
def checkUserType(cursor, name):
    try:
        SQL = "select type from user where username = '" + name + "';"
        cursor.execute(SQL)
        results = cursor.fetchall()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        return results[0][0]

def getUserID(cursor, name):
    try:
        SQL = "select userID from user where username = '" + str(name) + "';"
        cursor.execute(SQL)
        results = cursor.fetchall()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        return results[0][0]
    
def getUserName():
    if "echooUser" in str(os.environ):
        userName = re.findall("(?<=echooUser=).+?(?=_339458012)",str(os.environ))
        return userName
    else:
        userName = ""
        return userName

def checkFriend(cursor, userID, ID):
    Result = False
    try:
        SQL = "select * from friend_list where userID = " + str(userID)
        SQL+=" AND friend_userID =" + str(ID)+";"
        cursor.execute(SQL)
        results = cursor.fetchall()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        if results:
            Result = True
        else:
            Result = False
    try:
        SQL = "select * from friend_list where userID = " + str(ID)
        SQL+=" AND friend_userID =" + str(userID)+";"
        cursor.execute(SQL)
        results = cursor.fetchall()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        if results:
            Result = True
        else:
            Result = False
    return Result

def checkRequest(cursor, userID, ID):
    try:
        SQL = "select * from request where senderID = " + str(userID)
        SQL+=" AND receiverID =" + str(ID)+";"
        cursor.execute(SQL)
        results = cursor.fetchall()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        if results:
            return True
        else:
            return False

def postLike(cursor, postID, userID):
    if userID!="":
        try:
            SQL = "select liked from post_likes where postID = " + str(postID)
            SQL+=" AND userID =" + str(userID)+";"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            return results
    else:
        return ""

def postDislike(cursor, postID, userID):
    if userID!="":
        try:
            SQL = "select dislike from post_likes where postID = " + str(postID)
            SQL+=" AND userID =" + str(userID)+";"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            return results
    else:
        return ""

def postFavorite(cursor, postID, userID):
    if userID!="":
        try:
            SQL = "select userID from favorite where postID = " + str(postID)
            SQL+=" AND userID =" + str(userID)+";"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            return results
    else:
        return ""

def checkClubMemberRole(cursor, clubID, userID):
    if userID != "":
        try:
            SQL = "select role from club_user where clubID = " + str(clubID)
            SQL+=" AND userID =" + str(userID)+";"
            cursor.execute(SQL)
            results = cursor.fetchall()[0]
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            return results
    else:
        return ""
    
def specialChara (text):
    text=text.replace("&","&amp;")
    text=text.replace("'","&rsquo;")
    text=text.replace("-","&mdash;")
    text=text.replace("”","&rdquo;")
    text=text.replace("“","&ldquo;")
    return text

def wordCensor(text):
    user = "i494f18_team34"
    db_pass = "my+sql=i494f18_team34"
    db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
    cursor = db_con.cursor()
    text = text.lower()
    try:
        SQL = "select keyword from ban_word;"
        cursor.execute(SQL)
        results = cursor.fetchall()
    except Exception as e:
        print('<p>Something went wrong with the SQL!</p>')
        print(SQL, "Error:", e)
    else:
        for row in results:
            if row[0] in text:
                return True
                break
    return False
    
def returnSpecialChara (text):
    text=text.replace("&amp;","&")
    text=text.replace("Alt 34",'"')
    text=text.replace("&rsquo;","'")
    text=text.replace("&mdash;","-")
    text=text.replace("&rdquo;",'"')
    text=text.replace("&ldquo;",'"')
    return text

def getDateTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def setLoginStatus(redirect):
    if "echooUser" in str(os.environ):
        user = "i494f18_team34"
        db_pass = "my+sql=i494f18_team34"

        db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
        cursor = db_con.cursor()
        userName = re.findall("(?<=echooUser=).+?(?=_339458012)",str(os.environ))
        userName = userName[0]
        userID = ""
        try:
            SQL = "select userID from user where username = '" + str(userName) + "';"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            userID = results[0][0]
        html = """<body>
        <!-- JavaScript --><!-- Navigation --><div class="container"><nav><div class="container"><div class="row"><div class="logo">
        <a href="index.cgi"><img src="images/logo.jpg" alt="Riddle Joker"></a></div>
        <h1>Echooo</h1><ul><li><div class="user"><a href="privateMessageList.cgi"><i class="fas fa-envelope"></i></a><a href"""
        html += '="userProfile.cgi?userid='+str(userID)+'">'
        html += re.findall("(?<=echooUser=).+?(?=_339458012)",str(os.environ))[0]
        html += """</a><a href="logout.cgi">log out</a>
        </div></li><div class="search-container"><form action="searchMain.cgi">
        <input type="text" placeholder="Search.." name="search">
        <button type="submit"><i class="fa fa-search"></i></button>
        </form></div></li></ul></div><div class="bar"><ul>
        <li class="current"><a href="index.cgi"><i class="fas fa-home"></i> Home</a></li>
        <li><a href="whatsNewsPage.cgi"><i class="fas fa-globe-americas"></i> What's New</a></li>
        <li><a href="boardMain.cgi"><i class="fas fa-users"></i> Boards</a></li>
        <li><a href="clubMain.cgi"><i class="fas fa-users"></i> Clubs</a></li>
        <li><a href="news_main.cgi"><i class="fas fa-scroll"></i> News</a></li>
        <li><a href="help.cgi"><i class="far fa-question-circle"></i> Help</a></li>
        </ul></div></div></nav>"""
    else :
        html = """<body>
        <!-- JavaScript --><!-- Navigation --><div class="container"><nav>
        <div class="container"><div class="row"><div class="logo">
        <a href="index.cgi"><img src="images/logo.jpg" alt="Riddle Joker"></a>
        </div><h1>Echooo</h1><ul><li><div class="user">
        <a href="signUpPage."""
        html+='cgi?redirect='+str(redirect)+'"><i '
        html+= """class="fas fa-user"></i> Sign Up</a>
        <a href="loginPage."""
        html+='cgi?redirect='+str(redirect)+'"><i '
        html+="""class="fas fa-user"></i> Login</a>
        </div></li></li><div class="search-container"><form action="searchMain.cgi">
        <input type="text" placeholder="Search.." name="search">
        <button type="submit"><i class="fa fa-search"></i></button>
        </form></div></li></ul></div><div class="bar"><ul>
        <li class="current"><a href="index.cgi"><i class="fas fa-home"></i> Home</a></li>
        <li><a href="whatsNewsPage.cgi"><i class="fas fa-globe-americas"></i> What's New</a></li>
        <li><a href="boardMain.cgi"><i class="fas fa-users"></i> Boards</a></li>
        <li><a href="clubMain.cgi"><i class="fas fa-users"></i> Clubs</a></li>
        <li><a href="news_main.cgi"><i class="fas fa-scroll"></i> News</a></li>
        <li><a href="help.cgi"><i class="far fa-question-circle"></i> Help</a></li>
        </ul></div></div></nav>"""
    return html

def setFooter():
    role = ""
    userID = ""
    if "echooUser" in str(os.environ):
        user = "i494f18_team34"
        db_pass = "my+sql=i494f18_team34"

        db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306, user=user, passwd=db_pass, db=user)
        cursor = db_con.cursor()
        userName = re.findall("(?<=echooUser=).+?(?=_339458012)",str(os.environ))
        userName = userName[0]
        userID = ""
        try:
            SQL = "select userID from user where username = '" + str(userName) + "';"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            userID = results[0][0]
    if userID != "":
        try:
            SQL = "select type from user where userID = " + str(userID)+";"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print('<p>Something went wrong with the SQL!</p>')
            print(SQL, "Error:", e)
        else:
            role = results[0][0]
    footer = """<!-- footer -->
    <footer>
    <div class="container">
    <section class="footer-menu">
    <h1 class="sr-only">Footer</h1>
    <div class="row">
            <div class="footer-menu-main">
                    <a href="index.cgi"><p>Home</p></a> <p class="line">|</p>
                    <a href="contactUS.cgi"><p>Contact Us</p></a> <p class="line">|</p>
                    <a href="terms.cgi"><p>Terms</p></a> <p class="line">|</p>"""
    if role == "administrator":
        footer += '<a href="ForbiddenWordsList.cgi"><p>ForbiddenWords</p></a> <p class="line">|</p>'
        footer += '<a href="adminList.cgi"><p>Administrator</p></a> <p class="line">|</p>'
        footer += '<a href="reportList.cgi"><p>Reports</p></a> <p class="line">|</p>'
    footer +="""<div class="soical-media">
                    <a href="https://www.facebook.com/Echooo-Forum-757463234654244/"><i class="fab fa-facebook"></i></a>
                    <a href="https://twitter.com/Echooo28844222"><i class="fab fa-twitter"></i></a>
                    <a href="https://discord.gg/7xTCNfb"><i class="fab fa-discord"></i></a>
            </div></div>
            </div>
            </section>
            </div>
		</footer>"""
    return footer
