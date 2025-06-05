# bookbasedcollection
above i have uploaded pdf , it has steps and other database postman related photos<br>

# git clone the project
Git clone the project <br> 
<pre>https://github.com/varshithaga/bookbasedcollection1.git</pre>

# create django project
<pre>
django-admin stratproject myproject
cd myproject 
python manage.py startapp pdfsplitter
</pre>


# environment
<pre>
cd ..
python -m vev venv
.\venv\Scripts\activate
pip install -r requirements.txt
</pre>


# Postgresql
install postgresql <br>
create a database named bookbasedcollection<br>
in settings.py <br>
and enter your  username and password in DATABASES


# Hugging face api
HUGGINGFACE_API -You can generate one(Access Token) and  paste in .env file

# next
run in terminal
<pre>python manage.py runserver
</pre>

# storing
generated images are stored in in media whose path is stored in database<br>
uploaded pdf are stored in media , its path are also stored in database
