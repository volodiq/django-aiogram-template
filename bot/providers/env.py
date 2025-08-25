from environs import env as _env


_env.read_env()

debug = _env.bool("DEBUG")
secret_key = _env.str("SECRET_KEY")
bot_token = _env.str("BOT_TOKEN")

api_base_url = _env.str("API_BASE_URL")

redis_password = _env.str("REDIS_PASSWORD")
redis_fsm_db = 0
redis_fsm_dsn = f"redis://:{redis_password}@redis:6379/{redis_fsm_db}"
