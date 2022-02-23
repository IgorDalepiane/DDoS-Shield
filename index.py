import subprocess
import time


ip_max_count = {}
flag_to_clear = 0
while True:
    ip_count = {}
    
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
                ip_count[ip] += 1
            else:
                ip_count[ip] = 1

        print(ip + " --> Connections: " + str(ip_count[ip]) +"\n")
        if flag_to_clear == 10:
            flag_to_clear = 0
            subprocess.run(['clear'])
        else:
            flag_to_clear+=1
        # for row in row_lists:
        #     ip = row[5].split(":")[0]
        #     if ip in ip_count:
        #         ip_count[ip] += int(row[2])
        #     else:
        #         ip_count[ip] = int(row[2])
        
        # for ip in ip_count.keys():
        #     if ip in ip_max_count:
        #         if int(ip_count[ip]) > ip_max_count[ip]:
        #             ip_max_count[ip] = int(ip_count[ip])
        #     else:
        #         ip_max_count[ip] = int(ip_count[ip])
        #     print(ip + " --> Actual: " + str(ip_count[ip]) + "  Max: " + str(ip_max_count[ip]) +"\n")
