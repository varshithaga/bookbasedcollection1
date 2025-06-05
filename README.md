# bookbasedcollection
above i have uploaded pdf , it has steps and other database postman related photos

# git clone the project
Git clone the project 

# create django project
django-admin stratproject myproject<br>
cd myproject <br>
python manage.py startapp pdfsplitter<br>

# environment
cd ..
python -m vev venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Hugging face api
HUGGINGFACE_API -You can generate one(Access Token) and  paste in .env file

# next
run in terminal
python manage.py runserver

# storing
generated images are stored in in media whose path is stored in database
uploaded pdf are stored in media , its path are also stored in database
