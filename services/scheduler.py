import schedule
import time
from your_module import transfer_logs

def job():
    transfer_logs(redis_client, 'mystream', mongo_collection)

# Schedule the job every 2 minutes
schedule.every(2).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
