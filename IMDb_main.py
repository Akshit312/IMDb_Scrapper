# import libraries
import datetime
import smtplib
import mysql.connector
from mysql.connector import errorcode
import string
import urllib2
from bs4 import BeautifulSoup
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import psswrd
import date_compare

                                                                                   # Creating Database
try:
    mysql_user=psswrd.get_user()
    mysql_password=psswrd.get_password()
    db1 = mysql.connector.connect(host="localhost",user=mysql_user,passwd=mysql_password,db="mydata")
    cursor = db1.cursor()
except:
    print "Error in connection to mysql"
    
try:
    cursor.execute("CREATE database IF NOT EXISTS mydata;")
    db1.commit()
except:
    db1.rollback()    
    
try:
    cursor.execute("CREATE table IF NOT EXISTS test1(Email varchar(255),Tv_series varchar(255));")
    db1.commit()
except:
    db1.rollback()
    
try:        
    cursor.execute("use mydata;")
    db1.commit()
except:
    db1.rollback()
    
    
#Function to add values to Database
def database(email,series_name):                                        
    try:
        cursor.execute("insert into test1 (Email,Tv_series) values('email','series_name');")
    except:
        db1.rollback()

serviceurl='https://www.imdb.com/find?ref_=nv_sr_fn&q='
message=""
output=""
email=raw_input("Enter Email address : ")
seasons=raw_input("Enter season name : ").split(',')
print "\nFetching data...\n"
for xin in seasons:
    i=1
    count=0
    x=xin.replace(" ","")
    database(email,xin)
                                                                                    # Doing category search on imdb according to TV series
    url_sortTV=serviceurl+x+'&&s=tt&ttype=tv&ref_=fn_tv'
    page = urllib2.urlopen(url_sortTV)
    soup = BeautifulSoup(page, 'html.parser')
    try: 
        title_season=soup.find_all('td',class_="result_text")[0:5]                  # Get title of top 5 TV series
        if title_season==[]:
            output+= "No details found for " + xin
            break
           
        for y in title_season[0:5]:                                                 # Display top 5 results
            print str(i) + ":",
            print y.text + ".",
            i=i+1
        if i==1:
            break;    
        else:
            index=input("\n\nEnter the index of the TV Series: ")
            
        if index>=5 or index<=0:                                                    # Check input validity
            print "Invalid index"
            break;  
        else:
            a=title_season[index-1].a.get('href')
            
            url1='https://www.imdb.com'+a
            page1 = urllib2.urlopen(url1)
            soup1 = BeautifulSoup(page1, 'html.parser')
            title_page=soup1.find('div',class_="title_wrapper")
            title=title_page.h1.text.strip()
            link_img=soup1.find('div',class_="poster")
            
            
            url_season = soup1.find_all('div', class_ = 'seasons-and-year-nav')      # url of latest season
            urlsf=url_season[0].a.get("href")
            urlf='https://www.imdb.com'+urlsf
            
            page2 = urllib2.urlopen(urlf)
            soup2 = BeautifulSoup(page2, 'html.parser')
            air_date=soup2.find_all('div',class_="airdate")
            
                                                                                     # Comparing air date with current date and time
            for dates in air_date:
                if(dates==""):
                    count=1
                    break
                  
                new_str1=dates.text.replace(".", "")
                new_str2=new_str1.replace("\n","") 
                new_str3=new_str2.replace(" ","")
                
                if(len(new_str3)==4):                                                 # if length of air date is 4
                    count=3
                    output+= "Tv series name:" + " " + title
                    output+= "  Status: The next season begins in" + " " + new_str3 + "\n"
                    data = "  Status" + " : The next season begins in" + " " + new_str3
                    break
                                                                                      # calling check_date function from date_compare date_compare.py
                elif(date_compare.check_date(new_str3)==True):                        # Check if current date is less then any of the air date
                    DateFormat = "%d%b%Y"
                    a=datetime.datetime.strptime(new_str3 , DateFormat )
                    b=str(a)
                    output+= "Tv series name: " + title
                    output+= "  Status: Next episode airs on" + " " + str(b[0:10]) + "\n"
                    #message1="<b1>" + "Tv series name: " + "</b>",
                    data =  "  Status" +  " : Next episode airs on" + " " + str(b[0:10])
                    count=2
                    break
                    
            if(count==1):                                                             #If No information is available on IMDb.com
                output+= "Tv series name : " + title
                data = "No info available"
                output+= "No info available\n"
            elif(count==0):                                                           #Show has finished streaming all the the episodes
                output+= "Tv series name:" + " " + title
                output+= "  Status:The show has finished streaming all its episodes\n"
                data = "  Status"  + " : The show has finished streaming all its episodes"


            try:                                                                #Try and except for the image available on the website
                image = """<tr>
                      <td width="80" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                      <img src=\"""" + link_img.img.get("src") + """\" width="80" height="120"/>
                      </td>
                      <td width="15"></td>
                      <td valign="top">"""
            except:
                image = """<tr>
                      <td width="80" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                      <img src=\"""" + "https://bit.ly/2CMBIFr" + """\" width="80" height="120"/>
                      </td>
                      <td width="15"></td>
                      <td valign="top">"""
                
            title = """<h3>""" + """<a href=""" + url1 + """>"""+title+"</a><br>" + """</h3>"""
            email_message = """<p><em>""" + data + """</em></p></td></tr>"""
            series_content = image + """<b>""" + "TV series name : " + """</b>""" + title + email_message
            message+=series_content
    except:
        output+= "No details Found for " + xin + "\n"


if output=="":                                                                  # If No output to Print
    print "No results to display"
else:
    print output    
 
if message=="":
    message="No results to display"        
else:
                                                                                                                                 
    try:
        msg = MIMEMultipart()
        SUBJECT = "Schedule of your favourite TV-series"
        TO=email
        FROM=psswrd.from_email()                                                # Get email id from psswrd.py
        email_password=psswrd.password()                                        # Get password from psswrd.py
        msg['From'] = FROM
        msg['To'] = email
        msg['Subject'] = SUBJECT
        SUBJECT = SUBJECT
      
        msg.attach(MIMEText(message, 'html'))
                                                                                # Creating a session    
        server = smtplib.SMTP('smtp.gmail.com')
        server.starttls()
                                                                                # Logging in to the server    
        server.login(FROM,email_password)
                                                                                # Sending email with       
        server.sendmail(FROM, [TO], msg.as_string())
        server.quit()
        print "Email sent successfully"
    except smtplib.SMTPException:
            print("error sending message")   
           
                    

