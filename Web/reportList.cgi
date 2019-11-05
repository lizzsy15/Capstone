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
    <link rel="stylesheet" href="css/infoIN.css">
    <link rel="stylesheet" href="css/memberRole.css">
    <link rel="stylesheet" href="css/reportList.css">
		<link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">

		<!-- Font Awesome - For use in I360 -->
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" integrity="sha384-/rXc/GQVaYpyDdyxK+ecHPVYJSN9bmVFBvjA/9eOB+pb3F2w2N6fc5qB9Ew5yIns" crossorigin="anonymous">



		<!--[if lte IE 9]>
			<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
		<![endif]-->
	</head>"""
htmlOpen += EchooFunctions.setLoginStatus('index')
html="""<!-- Log in box-->
		<article class="block">
      <div class="infoBlock">
        <form method="post" action="ForbiddenWordsAdd.cgi" class="infoBlock">
          <h2>Report List:</h2>
          <table>
            <tr><th>ReportID</th><th>Reporter</th><th>Subject</th><th>Detail</th><th> </th></tr>
          {content}        </table><div class="pageRow">{PageContent}</div>

          <h2>Contact List:</h2>
          <table>
          <tr><th>ContactID</th><th>Email</th><th>Subject</th><th>Detail</th><th> </th></tr>
          {content2}
          </table><div class="pageRow">{PageContent2}</div>

          
      </div>
		</article>"""


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

page = form.getfirst("page", "1")
page = int(page)

page2 = form.getfirst("page2", "1")
page2 = int(page2)

html+="""<!-- footer -->
        {footer}
	</div>
	</body>
</html>"""

lastPage = False
post_count=1
totalNum = 0
PageContent = ""


content2 = ""
PageContent2 = ""
lastPage2 = False
post_count2=1
totalNum2 = 0
#change the status of veriable
if userName != "":
        if EchooFunctions.checkUserType(cursor, userName) == "administrator":
                admin = True
if userName == "":
        guest = True
#main contents to insert
content = ""
footer = EchooFunctions.setFooter()
if admin == True:
        if userID != "":
                try:
                        SQL = "SELECT count(reportID) from report;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)

                else:
                        for row in results:
                                totalNum += int(row[0])
                                if int(row[0]) <= (3*int(page)):
                                        lastPage = True

                if page == 1:
                        if lastPage == False:
                                PageContent +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="#" class="currentPage">1</a>'
                                page_count = 2
                                for i in range(2):
                                        if ((int(page_count)+1)*3)>int(totalNum):
                                                PageContent +='<a href="reportList.cgi?page='+str(page_count)+'&page2='+str(page2)+'">'+str(page_count)+'</a>'
                                                break
                                        else:
                                                PageContent +='<a href="reportList.cgi?page='+str(page_count)+'&page2='+str(page2)+'">'+str(page_count)+'</a>'
                                                page_count += 1
                                PageContent +='<a href="reportList.cgi?page='+str((int(page)+1))+'&page2='+str(page2)+'"><i class="fas fa-arrow-right"></i></a>'
                        else:
                                PageContent +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="#" class="currentPage">1</a>'
                                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                if page != 1:
                        if lastPage == False:
                                PageContent +='<a href="reportList.cgi?page='+str((int(page)-1))+'&page2='+str(page2)+'"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="reportList.cgi?page='+str((int(page)-1))+'&page2='+str(page2)+'">'+str(int(page)-1)+'</a>'
                                page_count = int(page)
                                for i in range(2):
                                        if ((int(page_count))*3)>int(totalNum):
                                                PageContent +='<a href="reportList.cgi?page='+str(page_count)+'&page2='+str(page2)+'" class="currentPage">'+str(page_count)+'</a>'
                                                break
                                        else:
                                                PageContent +='<a href="reportList.cgi?page='+str(page_count)+'&page2='+str(page2)+'">'+str(page_count)+'</a>'
                                                page_count += 1
                                PageContent +='<a href="reportList.cgi?page='+str((int(page)+1))+'&page2='+str(page2)+'"><i class="fas fa-arrow-right"></i></a>'
                        else:
                                PageContent +='<a href="reportList.cgi?page='+str((int(page)-1))+'&page2='+str(page2)+'"><i class="fas fa-arrow-left"></i></a>'
                                PageContent +='<a href="reportList.cgi?page='+str((int(page)-1))+'&page2='+str(page2)+'">'+str((int(page)-1))+'</a>'
                                PageContent +='<a href="#" class="currentPage">'+str(page)+'</a>'
                                PageContent +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                                

                page = form.getfirst("page", "1")
                page = int(page)
                
                try:
                        SQL = "select * from report;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        for row in results:
                                if post_count <= int(page)*3 and post_count >(int(page)-1)*3:
                                        reporter=""
                                        subject = ""
                                        
                                        try:
                                                SQL = "select username from user where userID = " +str(row[1])+";"
                                                cursor.execute(SQL)
                                                results = cursor.fetchall()
                                        except Exception as e:
                                                print('<p>Something went wrong with the SQL!</p>')
                                                print(SQL, "Error:", e)
                                        else:
                                                reporter = results[0][0]
                                        
                                        content+='<tr><td>'+str(row[0])
                                        content+='</td><td><a href="userProfile.cgi?userid='+str(row[1])+'">'+reporter+'</a></td>'
                                        if str(row[5]) != "None":
                                                try:
                                                        SQL = "select username from user where userID = " +str(row[5])+";"
                                                        cursor.execute(SQL)
                                                        results = cursor.fetchall()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        subject = results[0][0]
                                                        content+='<td><a href="userProfile.cgi?userid='+str(row[5])+'">User '+subject+'</a></td>'
                                        
                                        if str(row[6]) != "None":
                                                try:
                                                        SQL = "select title from post where postID = " +str(row[6])+";"
                                                        cursor.execute(SQL)
                                                        results = cursor.fetchall()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        subject = results[0][0]
                                                        new_subject = ""
                                                        for x in subject:
                                                                if len(new_subject)<= 30:
                                                                        new_subject += x
                                                                if len(new_subject) > 30:
                                                                        new_subject += "..."
                                                                        break
                                                        content+='<td><a href="article.cgi?post='+str(row[6])+'">Post '+new_subject+'</a></td>'
                                        
                                        if str(row[7]) != "None":
                                                try:
                                                        SQL = "select clubname from club where clubID = " +str(row[7])+";"
                                                        cursor.execute(SQL)
                                                        results = cursor.fetchall()
                                                except Exception as e:
                                                        print('<p>Something went wrong with the SQL!</p>')
                                                        print(SQL, "Error:", e)
                                                else:
                                                        subject = results[0][0]
                                                        content+='<td><a href="clubMessage.cgi?club='+str(row[7])+'">Club '+subject+'</a></td>'
                                        word_count = 1
                                        shortDetail = ""
                                        for x in str(row[3]):
                                                if word_count <= 10:
                                                        word_count += 1 
                                                        shortDetail += x
                                                else:
                                                        shortDetail += "... "
                                                        shortDetail += "<a href='viewReport.cgi?report="+str(row[0])+"'>View</a>"
                                                        break
                                        content+='<td class="detail">'+str(shortDetail)+'</td>'
                                        content+='<td><a href="reportRemove.cgi?report='+str(row[0])+'">Remove</a></td></tr>'
                                        
                                        
                                        post_count += 1
                                else:
                                        post_count += 1


if admin == True:
        if userID != "":
                try:
                        SQL = "SELECT count(contactID) from contacts;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)

                else:
                        for row in results:
                                totalNum2 += int(row[0])
                                if int(row[0]) <= (3*int(page2)):
                                        lastPage2 = True

                if page2 == 1:
                        if lastPage2 == False:
                                PageContent2 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                                PageContent2 +='<a href="#" class="currentPage">1</a>'
                                page_count2 = 2
                                for i in range(2):
                                        if ((int(page_count2)+1)*3)>int(totalNum2):
                                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str(page_count2)+'">'+str(page_count2)+'</a>'
                                                break
                                        else:
                                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str(page_count2)+'">'+str(page_count2)+'</a>'
                                                page_count2 += 1
                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str((int(page2)+1))+'"><i class="fas fa-arrow-right"></i></a>'
                        else:
                                PageContent2 +='<a href="#"><i class="fas fa-arrow-left"></i></a>'
                                PageContent2 +='<a href="#" class="currentPage">1</a>'
                                PageContent2 +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                if page2 != 1:
                        if lastPage2 == False:
                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str((int(page2)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str((int(page2)-1))+'">'+str(int(page2)-1)+'</a>'
                                page_count2 = int(page2)
                                for i in range(2):
                                        if ((int(page_count2))*3)>int(totalNum2):
                                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str(page_count2)+'" class="currentPage">'+str(page_count2)+'</a>'
                                                break
                                        else:
                                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str(page_count2)+'">'+str(page_count2)+'</a>'
                                                page_count2 += 1
                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str((int(page2)+1))+'"><i class="fas fa-arrow-right"></i></a>'
                        else:
                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str((int(page2)-1))+'"><i class="fas fa-arrow-left"></i></a>'
                                PageContent2 +='<a href="reportList.cgi?page='+str(page)+'&page2='+str((int(page2)-1))+'">'+str((int(page2)-1))+'</a>'
                                PageContent2 +='<a href="#" class="currentPage">'+str(page2)+'</a>'
                                PageContent2 +='<a href="#"><i class="fas fa-arrow-right"></i></a>'
                                

                page2 = form.getfirst("page2", "1")
                page2 = int(page2)
                
                try:
                        SQL = "select contactID, email, title, detail from contacts;"
                        cursor.execute(SQL)
                        results = cursor.fetchall()
                except Exception as e:
                        print('<p>Something went wrong with the SQL!</p>')
                        print(SQL, "Error:", e)
                else:
                        
                        for row in results:
                                contactID = str(row[0])
                                if post_count2 <= int(page2)*3 and post_count2 >(int(page2)-1)*3:
                                        content2 += "<tr>"
                                        content2 += "<td>"+str(row[0])+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td>"
                                        word_count2 = 1
                                        shortDetail2 = ""
                                        for x in str(row[3]):
                                                if word_count2 <= 10:
                                                        word_count2 += 1 
                                                        shortDetail2 += x
                                                else:
                                                        shortDetail2 += "... "
                                                        shortDetail2 += "<a href='viewContact.cgi?contact="+str(contactID)+"'>View</a>"
                                                        break
                                        content2+='<td class="detail">'+str(shortDetail2)+'</td>'
                                        content2+='<td><a href="contactRemove.cgi?contact='+str(contactID)+'">Remove</a></td></tr>'
                                        post_count2 += 1
                                else:
                                        post_count2 += 1
                        

        #print out html
        print(htmlOpen)
        print(html.format(content = content,content2 = content2, PageContent = PageContent, PageContent2 = PageContent2, footer = footer))
else:
        print("<h1>You arn't permit to visit this page</h1>")
        print("<a href='index.cgi'>Return</a>")
