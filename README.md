### About:  
reviewyourreads is a book review website, where you can have access to the details of many books, including the information from [Goodreads](https://www.goodreads.com/), a popular book review website.  
You can also add reviews to the books and can read the reviews which others have left. But one user cannot add multiple reviews to the same book.  
Also, you can make api reqests to the website in the ```/api/<isbn>``` route, which will return a json object with the details of the book.

To run the application locally, go inside the project1 directory in the command terminal and run the following commands(assuming python has been installed):
 -  pip3 install -r requirements.txt   
 -  set FLASK_APP=application.py
 -  set DATABASE_URL=postgres://xpeaulqenohknd:e1c341912c325d8813859997c97a1f258f72c8abb3aba782036f24a5eca93d98@ec2-34-194-198-1<span>76.compute-1.amazon</span>aws.com:5432/d436ifs3lnrdui
 -  set FLASK_DEBUG=1
 -  set FLASK_ENV=development
 -  flask run     
And go to the website shown in a web browser. 

To visit the site online, visit https://reviewyourreads.herokuapp.com/
