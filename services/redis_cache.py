import json
import redis
from rediscluster import RedisCluster


class RedisDB:
    def __init__(self, cluster_mode=False, host='127.0.0.1', startup_nodes=[], port=6379):
        
        if cluster_mode:
            self.redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        else:
            self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)

    def save_data(self, request_id, data):
        try:
            print(request_id)
            self.redis_client.rpush(request_id, json.dumps(data))
        except Exception as e:
            print("Exception in save_data: ", e)
    

    def get_data(self, request_id, hist_count=20):
        try:
            raw_data = self.redis_client.lrange(str(request_id), -hist_count, -1)
            data = [json.loads(item) for item in raw_data]
            return data
        except Exception as e:
            return []

