import time
from services.redis_cache import RedisDB

class LogExporter:
    def __init__(self, redis_client=None, interval=120):
        """constructor"""
        self.client = redis_client
        self.interval = interval

    def export_logs_to_db(self):
        """method to export logs to database"""
        while True:
            logs = self.client.get_all_logs()
            time.sleep(self.interval)

    def save_to_db(self, log):
        pass

    def run(self):
        self.export_logs_to_db()
