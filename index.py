import subprocess
import time

process = subprocess.Popen(['ss', '-ntu'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

count = 0
while True:
    row_lists = []

    return_code = process.poll()
    if return_code is not None:
        for output in process.stdout.readlines():
            rows = output.strip().split("\n")
            for row in rows:
                row_lists.append(row.split())
        
        # row_lists.remove(row_lists[0])
        print("IP" + " --> " + "Packages sent")
        
        for row in row_lists:
            count += int(row[3])
            print(row[5] + " --> " + row[3])
            print(count)
        time.sleep(2)