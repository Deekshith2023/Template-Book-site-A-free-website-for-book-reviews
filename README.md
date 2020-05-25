# Project 1

## Web Programming with Python and JavaScript

### About:  
reviewyourreads is a book review website, where you can have access to the details of many books, including the information from [Goodreads](https://www.goodreads.com/), a popular book review website.  
You can also add reviews to the books and can read the reviews which others have left. But one user cannot add multiple reviews to the same book.  
Also, you can make api reqests to the website in the ```/api/<isbn>``` route, which will return a json object with the details of the book.

To run the application, go inside the project1 directory in the command terminal and run the following commands:
 -  set FLASK_APP=application.py
 -  set DATABASE_URL=postgres://xpeaulqenohknd:e1c341912c325d8813859997c97a1f258f72c8abb3aba782036f24a5eca93d98@ec2-34-194-198-1<span>76.compute-1.amazon</span>aws.com:5432/d436ifs3lnrdui
 -  set FLASK_DEBUG=1
 -  set FLASK_ENV=development
 -  flask run     
And go to the website shown in a web browser. 

### Files:  
#### application.py:
This contains the main flask code of the web application.   
#### import.py:
This is a python program to import the book information from the books.csv file to the database.    
#### login.py:
Just a helper file to authenticate users when they log in.
#### /static:
##### styles.css:
This is the css stylesheet for styling the html pages.
#### /template:
##### bookinfo.html:
To display information about a particular book.
##### dashboard.html:
The dashboard to which the user will be directed when he/she logs in to the application.
##### index.html:
Home page of the application, renders in the default route.
##### layout.html:
For the layout of all the html pages.
##### login.html:
The page where the user logs in to the website.
##### review.html:
The page where the user reviews a book.
##### searchresults.html:
The page displaying the search results when the user searches something about a book.
##### signup.html:
The page where the user registers for the website.



"# reviewyourreads" 
