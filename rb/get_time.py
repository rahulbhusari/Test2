import os.path, time
file = "C:\project\local_repo\push.txt"
print("last modified: %s" % time.ctime(os.path.getmtime(file))) ##needed
print("created: %s" % time.ctime(os.path.getctime(file)))

import os
import datetime as dt

now = dt.datetime.now()
ago = now-dt.timedelta(days=30)
print(now)
print(ago)

for root, dirs,files in os.walk('C:\project\local_repo'):
    for fname in files:
        path = os.path.join(root, fname)
        st = os.stat(path)    
        mtime = dt.datetime.fromtimestamp(st.st_mtime)
        if mtime > ago:
            print('%s modified %s'%(path, mtime))
