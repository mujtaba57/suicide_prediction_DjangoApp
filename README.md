# Suicide Thought Detection Django Application


## step 1: create a virtual environment
### Steps:
1- Create virtual environment
    $ *For ubuntu*: python3 -m venv venv 
    $ *For ubuntu*: python -m venv venv 
2- Activate virtual environment
    $ *For ubuntu*: source env/bin/activate
    $ *For window*: venv\Scripts\activate

## step2: clone the repository
    $ git clone

## step3: install requirements
    $ *For ubuntu*: pip3 install -r requirements.txt
    $ *For window*: pip install -r requirements.txt

## step4: download models
### steps:
    1- download models file from 
    2- place it in this format *fyp_project/models*

## step5: download and install mysql-workbench
## step6: create mysql-connection into workbench
## step7: create schema with the name of *reg_user*
## step8: create table and add 2 fields with *email* and *password*
## step9: run the commands
### steps:
    1- python/python3 manage.py collectstatic
    2- python/python3 manage.py makemigrations
    3- python/python3 manage.py migrate

## step4: run the app
    $  python/python3 manage.py runserver
