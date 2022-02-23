import subprocess
import time



ip_count = {}
while True:
    # subprocess.run(['clear'])
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
            ip = row[5].split(":")[0]
            if ip in ip_count:
                ip_count[ip] += int(row[2])
            else:
                ip_count[ip] = int(row[2])

        for ip in ip_count.keys():
            print(ip + " --> " + str(ip_count[ip]) + "\n")
