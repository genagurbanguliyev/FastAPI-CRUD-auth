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

if you use sqlite then uncomment the SQLALCHEMY_DATABASE_URL from db_config.database.py line:16

paste these variables into

```sh
# jwt
SECRET_KEY = '0955f64faf1ff71df5bfe4b659e32873cc68301cd8a969304929cae542ff2105'
ALGORITHM = "HS256"

# if you use postgresql or mysql (not sqlite) get below
# DB configs :
DB_DIALECT ='postgresql'
DB_HOST ='localhost'
DB_HOST_PORT=5432
DB_USER ='postgres'
DB_PASSWORD ='your_password'
DB_NAME ='test'
```

---

#### BUT if you use Postgresql or MySQL you need some configurations:

run command `alembic init`, after that `alembic.ini` file and `alembic` directory will create
set inside `alembic.ini` file:

```
sqlalchemy.url = postgresql://your_username:your_pass@your_host/db_name
```

and inside `alembic/env.py` file looks like this:

```python
import sys
sys.path.append("...")

from typing import Any

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import models


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
fileConfig(config.config_file_name)
target_metadata = models.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

---

#### run project

```sh
uvicorn books:app --reload
```
