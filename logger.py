from redis_cache import RedisDB

class Logger:
    def __init__(self) -> None:
        self.database_to_export = None
        self.log_file = None
        self.log_color_scheme = None
        self.client = RedisDB()
