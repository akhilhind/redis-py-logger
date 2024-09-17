import uuid
from services.redis_cache import RedisDB

class RedisPyLogger:
    def __init__(self, config=None) -> None:
        self.db_config = {
            'db_name': None,
            'db_host': None,
            'db_port': None
        }
        self.log_file = None
        self.log_level = 'INFO'
        self.use_colors = False
        self.redis_config = None

        if config:
            self.log_file = config.get('log_file_path', self.log_file)
            self.log_level = config.get('log_level', self.log_level)
            self.use_colors = config.get('use_colors', self.use_colors)
            
            if 'database' in config:
                db_config = config['database']
                self.db_config['db_name'] = db_config.get('name', self.db_config['db_name'])
                self.db_config['db_host'] = db_config.get('host', self.db_config['db_host'])
                self.db_config['db_port'] = db_config.get('port', self.db_config['db_port'])
                
            if 'redis_config' in config:
                self.redis_config = config['redis_config']
                

        self.client = RedisDB()

        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level not in valid_log_levels:
            raise ValueError(f"Invalid log level: {self.log_level}. Must be one of {valid_log_levels}.")

    def log(self, message: str, level: str = 'INFO') -> None:
        if self.should_log(level):
            log_entry = self.format_log_entry(message, level)
            print('inside log')
            self.output_log(log_entry)

    def error(self, error_message: str) -> None:
        self.log(error_message, level='ERROR')

    def should_log(self, level: str) -> bool:
        log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        return log_levels.index(level) >= log_levels.index(self.log_level)

    def format_log_entry(self, message: str, level: str) -> str:
        log_entry = f"[{level}] {message}"
        if self.use_colors:
            log_entry = self.apply_color_scheme(log_entry, level)
        return log_entry

    def apply_color_scheme(self, log_entry: str, level: str) -> str:
        colors = {
            'ERROR': '\033[91m',
            'WARNING': '\033[93m',
            'INFO': '\033[92m',
            'DEBUG': '\033[94m',
            'CRITICAL': '\033[95m',
            'RESET': '\033[0m'
        }
        color = colors.get(level, colors['RESET'])
        return f"{color}{log_entry}{colors['RESET']}"

    def output_log(self, log_entry: str) -> None:
        print(log_entry)
        print('2222222222222222222')
        if self.log_file:
            with open(self.log_file, 'a') as file:
                file.write(log_entry + '\n')

        if self.client:
            self.client.save_data(self.generate_request_id(), log_entry)

    def generate_request_id(self) -> str:
        return str(uuid.uuid4())
