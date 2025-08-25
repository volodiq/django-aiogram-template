from environs import env as _env


_env.read_env()

debug = _env.bool("DEBUG")
secret_key = _env.str("SECRET_KEY")

db_host = _env.str("DB_HOST")
db_port = _env.str("DB_PORT")
db_name = _env.str("DB_NAME")
db_user = _env.str("DB_USER")
db_password = _env.str("DB_PASSWORD")
