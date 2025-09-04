from environs import env as _env


_env.read_env()

is_run_as_service = _env.bool("IS_RUN_AS_SERVICE", default=False)

debug = _env.bool("DEBUG")
secret_key = _env.str("SECRET_KEY")

if is_run_as_service:
    db_host = _env.str("DB_HOST")
else:
    db_host = "localhost"

db_port = _env.str("DB_PORT")
db_name = _env.str("DB_NAME")
db_user = _env.str("DB_USER")
db_password = _env.str("DB_PASSWORD")
