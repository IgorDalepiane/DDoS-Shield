import subprocess
import time



ip_count = {}
while True:
    process = subprocess.run(['ss', '-ntu'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    row_lists = []
    if process.returncode is not None:
        rows = process.stdout.strip().split("\n")
        for row in rows:
            row_lists.append(row.split())
        
        row_lists.remove(row_lists[0])
        print("IP" + " --> " + "Packages sent")
        
        for row in row_lists:
            ip_count[row[5]] = ip_count[row[5]] + int(row[2])
            print(row[5] + " --> " + row[2])

        print(ip_count)
        time.sleep(2)