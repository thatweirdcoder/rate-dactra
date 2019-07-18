# rate-dactra
A ratemyprofessors.com clone for my uni

how to run on windows 

```bat
$ git clone http://github.com/thatweirdcoder/rate-dactra.git
$ cd rate-dactra
$ py -m pip install -r requirements.txt
$ set FLASK_APP=rate-dactra\app.py
$ set FLASK_ENV=development
$ set FLASK_DEBUG=true
$ set SECRET_KEY=not so seceret huh
$ set SQLALCHEMY_DATABASE_URI=sqlite:///%cd%\database.sqlite3
$ set SQLALCHEMY_TRACK_MODIFICATIONS=true
$ py -m flask run
```
