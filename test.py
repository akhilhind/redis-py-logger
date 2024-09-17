from flask import Flask, request
from redis_py_logger import RedisPyLogger

logger = RedisPyLogger({
    "database": {
        "name": "mongo",
        "host": "127.0.0.1",
        "port": 27017
    },
    "log_file": "test",
    "log_level": "DEBUG",
    "use_colors": True,
    "redis_config": {
        "cluster_mode": False,
        "host": "127.0.0.1",
        "port": 6379 
    }
})


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    try:
        name = request.json['name']
        logger.log('this is a simple log')
        logger.log('hahahahahahha ahahahhaha')
        return "thanks", 200
    except Exception as e:
        logger.error("exception occured")
        return "no thanks", 500
        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4321, debug=True)

