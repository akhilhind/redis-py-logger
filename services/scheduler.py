import schedule
import time
from your_module import transfer_logs

# this scheduler is to run data transfer job. 
# all logs has to be transferred to database of user's choice after every 30s


def job():
    """
    function to run job after every n seconds/minutes
    """
    transfer_logs(redis_client, 'mystream', mongo_collection)

# Schedule the job every 2 minutes
schedule.every(2).minutes.do(job)

while True:
    """
    keep running the function
    """
    schedule.run_pending()
    time.sleep(1)
