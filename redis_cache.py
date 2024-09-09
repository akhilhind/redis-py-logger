
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
        
        # self.redis_client = redis.Redis(host='10.26.65.41', port=7000, db=0)
        # self.redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
        # self.redis_client = redis.Redis(host='10.36.65.15', port=6381, db=0)
        self.redis_client = redis.Redis(host=host, port=port, db=0)
        # Define the nodes of your Redis Cluster
        # startup_nodes = [{"host": "10.26.65.41", "port": 7000}]

        # Create a Redis Cluster client
        # self.redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    def set_expiry_key(self,username, access_token, expiry):
        """set_expiry_key"""
        self.redis_client.setex(username, expiry, access_token)

    def get_key(self,current_user):
        """get_key"""
        return self.redis_client.get(current_user)

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

    
    def clear_chat_history(self, curr_user):
        """clear_chat_history"""
        try:
            self.redis_client.delete(str(curr_user) + "_main")
            self.redis_client.set(str(curr_user) + '_active_bot', 'null')
        except Exception as e:
            raise e

