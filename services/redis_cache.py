import json
import redis
from rediscluster import RedisCluster


class RedisDB:
    def __init__(self, cluster_mode=False, host='127.0.0.1', startup_nodes=[], port=6379):
        
        if cluster_mode:
            self.redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        else:
            self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)

    def save_data(self, request_id, data, group_by_id=None):
        try:
            if group_by_id:
                curr_data = self.get_hdata(group_by_id, request_id)
                if curr_data:
                    curr_data.append(data)
                else:
                    curr_data = [data]
                self.redis_client.hset(group_by_id, request_id, json.dumps(curr_data))
            else:
                self.redis_client.rpush(request_id, json.dumps(data))
        except Exception as e:
            print("Exception in save_data: ", e)
            raise e
    

    def get_data(self, request_id, hist_count=20):
        try:
            raw_data = self.redis_client.lrange(str(request_id), -hist_count, -1)
            data = [json.loads(item) for item in raw_data]
            return data
        except Exception as e:
            return []
        
        
    def get_hdata(self, group_by_id, field_id):
        try:
            data = self.redis_client.hget(group_by_id, field_id)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print("Exception in get_hdata: ", e)
            raise e

