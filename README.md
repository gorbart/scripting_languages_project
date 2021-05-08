# Scripting languages project
Twitter analyser is my final project for scripting languages
course at 4th semester of Applied Computer Science studies at
the Faculty of Computer Science and Management of Wroclaw
University of Science and Technology. <br>
It's been created in Python with slight mixins of HTML, CSS
and Bootstrap for creating a good-looking graphical user
interface.<br>
Twitter analyser lets its user retrieve data about hashtags,
tweets, and Twitter users and 'follow' them in a way. 
Followed users and hashtags are stored in a database.
Popularity of specific tweets or hashtags is plotted and
displayed to analyser's user. Reports about all this data
can be sent by email to users.<br><br>
Installation instruction:<br>
$ git clone https://github.com/gorbart/scripting_languages_project - 
clone project from GitHub <br>
$ cd scripting_languages_project - enter project directory <br>
$ python3 -m venv my_venv - create virtual environment <br>
$ source my_venv/bin/activate - activate virtual environment <br>
$ pip install -r requirements.txt - install requirements <br>
you also have to create file credentials.py, where you will store
credentials to database, Twitter API and Gmail service
$ python manage.py makemigrations scripting_languages_project <br>
$ python manage.py makemigrations users <br>
$ python manage.py makemigrations twitter_analyser <br>
$ python manage.py migrate - these commands migrate entities
to your database <br>
$ python manage.py runserver - runs whole project