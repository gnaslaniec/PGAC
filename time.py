from datetime import datetime
import time

fmt = '%Y-%m-%d %H:%M:%S'
date1 = datetime.now()
time.sleep(50)
date2 = datetime.now()

print(date1 - date2)


#minutes_diff = (d1 - d2).total_seconds() / 60.0
