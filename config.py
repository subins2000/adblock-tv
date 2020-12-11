import environ
import os

env = environ.Env()
root = environ.Path(os.getenv('PWD'))
environ.Env.read_env(root('.env'))

dejavu_config = {
    "database": {
        "host": env("DB_HOST"),
        "user": env("DB_USER"),
        "password": env("DB_PASSWORD"),
        "database": env("DB_NAME"),
    },
    "database_type": "postgres"
}

REMOTE_NAME = env("REMOTE_NAME")
REMOTE_KEY_MUTE = env("REMOTE_KEY_MUTE")
