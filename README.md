# bookbasedcollection
above i have uploaded pdf , it has steps and other database postman related photos<br>

# git clone the project
Git clone the project 

# create django project
django-admin stratproject myproject<br>
cd myproject <br>
python manage.py startapp pdfsplitter<br>

# environment
cd ..<br>
python -m vev venv<br>
.\venv\Scripts\activate<br>
pip install -r requirements.txt<br>


# Postgresql
install postgresql <br>
create a database named bookbasedcollection<br>
in settings.py <br>
and enter your  username and password in DATABASES


# Hugging face api
HUGGINGFACE_API -You can generate one(Access Token) and  paste in .env file

# next
run in terminal
python manage.py runserver

# storing
generated images are stored in in media whose path is stored in database<br>
uploaded pdf are stored in media , its path are also stored in database
