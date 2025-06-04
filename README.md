# bookbasedcollection
above i have uploaded pdf , it has steps and other database postman realed photos


Git clone the project 
django-admin stratproject myproject
cd myproject 
python manage.py startapp pdfsplitter

to create environment cd ..
python -m vev venv
.\venv\Scripts\activate
pip install -r requirements.txt

I have used HUGGINGFACE_API -You can generate one(Access Token) and  paste in .env file

next
run in terminal
python manage.py runserver

generated images are stored in in media whose path is stored in database
uploaded pdf are stored in media , its path are also stored in database
