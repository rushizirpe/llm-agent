# agentcreator

A django based LLM agent creator

Uses https://github.com/simonw/llm / https://github.com/simonw/llm-gpt4all

## installation

* create a virtual env:
```
python3 -m venv venv
```
* activate it:
```
source venv/bin/activate
```
* install requirements:
```
pip install -r requirements.txt
```
* run migrations:
```
python manage.py migrate
```

# create a superuser:
```
python manage.py createsuperuser
```

* run server:
```
python manage.py runserver
```
