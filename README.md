# SDBackend
Create a python3 virtual environment and run following commands after activating the environment. 
Refer - [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html).
```
cd backend

# to install dependencies
pip install -r requirements.txt

# make table in database
python manage.py makemigrations
python manage.py migrate

# to run server
python manage.py runserver
```
* Open a browser and navigate to `localhost:8000`
