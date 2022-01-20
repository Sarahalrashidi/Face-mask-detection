# Documentation
## Installation
### Windows Installation
1. change your directory to the faceMaskDetection project
```
cd faceMaskDetection
``` 
2. Create a Python virtual environment named 'env' and activate it.
```
virtualenv env
```
```
source env/bin/activate
```
3. Now, run the following command in your Terminal/Command Prompt to install the libraries required
```
pip install -r requirements.txt
```
4. Now, run the following command in your Terminal/Command Prompt to migrate main project
```
python manage.py migrate
```
5. Create super user, so you can log in
```
python manage.py createsuperuser
```
6. Run the project 
```
python manage.py runserver
```
7. Open your browser and navigate to `http://127.0.0.1:8000/admin/` 

