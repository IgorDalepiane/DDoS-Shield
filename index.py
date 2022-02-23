import subprocess
import time



count = 0
while True:
    process = subprocess.run(['ss', '-ntu'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    row_lists = []
    if process.returncode is not None:
        rows = process.stdout.strip().split("\n")
        for row in rows:
            row_lists.append(row.split())
        
        print(row_lists)
        row_lists.remove(row_lists[0])
        print("IP" + " --> " + "Packages sent")
        
        for row in row_lists:
            count = count + int(row[2])
            print(row[5] + " --> " + row[2])
            print(count)

        time.sleep(2)