## python fastAPI

### project Todos app with authentication

---

#### create Virtual Environment with python venv:

```sh
python -m vevn venv
```

activate venv:

```sh
souce venv/bin/activate
```

### install dependicies using `pip` from requirement.txt

#### create `.env` inside root directory

paste these variables into

```sh
# jwt
SECRET_KEY = '0955f64faf1ff71df5bfe4b659e32873cc68301cd8a969304929cae542ff2105'
ALGORITHM = "HS256"

# if you use postgresql or mysql (not sqlite) get below
# DB configs :
DB_HOST ='postgresql'
HOST_NAME ='localhost'
DB_HOST_PORT=5432
DB_USER ='postgres'
DB_PASSWORD ='user_password'
DB_NAME ='db_name'
```

if you use sqlite then uncomment the SQLALCHEMY_DATABASE_URL from db_config.database.py line:16

#### run project

```sh
uvicorn books:app --reload
```
