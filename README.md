### About:  
reviewyourreads is a book review website, where you can have access to the details of many books, including the information from [Goodreads](https://www.goodreads.com/), a popular book review website.  
You can also add reviews to the books and can read the reviews which others have left. But one user cannot add multiple reviews to the same book.  

Also, you can make api reqests to the website in the ```/api/<isbn>``` route, which will return a json object with the details of the book.

### Development:  
To run the application locally, go inside the reviewyourreads directory in the command terminal and run the following commands(assuming python has been installed):
 -  pip3 install -r requirements.txt   
 -  set FLASK_APP=application.py
 -  set DATABASE_URL=your_database_url
 -  set FLASK_DEBUG=1
 -  set FLASK_ENV=development
 -  flask run     
And go to the website shown in a web browser. 

To visit the site online, visit https://reviewyourreads.herokuapp.com/

### Contributing:    
Contributions are always welcome! You can open issues or pull requests for any change or new feature you may need added to the project. Some of the new features/changes I had in mind were:
 - Making the website responsive. It currently looks OK only on desktop screens.
 - Improving the UI
 - Sorting search results in order of the relevance of the book.
 
 Feel free to add/suggest ideas of your own!
