
"""
Redis
"""
import json
import redis
from sanitize import sanitize_message


class RedisDB:
    """
    Redis
    """
    def __init__(self, host='127.0.0.1', port=6379):
    # def __init__(self, host='10.36.65.15', port=6381):
        
        self.redis_client = redis.Redis(host=host, port=port, db=0)
        # Define the nodes of your Redis Cluster
        # startup_nodes = [{"host": "10.26.65.41", "port": 7000}]

        # Create a Redis Cluster client
        # self.redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    def save_data(self, user_id, data):
        """save_data"""
        try:
            for item in data:
                if isinstance(item, dict):
                    item = sanitize_message(item)
                self.redis_client.rpush(str(user_id) + '_main', json.dumps(item))
            # data_with_timestamp = {'data': data, 'time': int(time.time())}
            # self.redis_client.rpush(str(user_id) + '_main', json.dumps(data_with_timestamp))
        except Exception as e:
            raise e
    
    def get_data(self, user_id, hist_count=20):
        """get_data"""
        try:
            raw_data = self.redis_client.lrange(str(user_id) + '_main', -hist_count, -1)
            data = [json.loads(item) for item in raw_data]
            return data
        except Exception as e:
            return []

