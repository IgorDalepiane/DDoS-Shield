import subprocess
import time
import sys

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
        if len(sys.argv) == 1 or sys.argv[1] != '-c' and sys.argv[1] != '-p':
            print("Invalid argument, use -c for connections or -p for packages.")
            exit(1)
        elif sys.argv[1] == '-c':
            subprocess.run(['clear'])
            print("IP" + " --> " + "Connections")
            for row in row_lists:
                ip = row[5].split(":")[0]
                if ip in ip_count:
                    ip_count[ip] += 1
                else:
                    ip_count[ip] = 1

            for ip in ip_count.keys():
                print(ip + " --> Connections: " + str(ip_count[ip]), end="\n")
            time.sleep(1)

        elif sys.argv[1] == '-p':
            subprocess.run(['clear'])
            
            print("IP" + " --> " + "Packages")
            for row in row_lists:
                ip = row[5].split(":")[0]
                if ip in ip_count:
                    ip_count[ip] += int(row[2])
                else:
                    ip_count[ip] = int(row[2])
            
            for ip in ip_count.keys():
                if ip in ip_max_count:
                    if int(ip_count[ip]) > ip_max_count[ip]:
                        ip_max_count[ip] = int(ip_count[ip])
                else:
                    ip_max_count[ip] = int(ip_count[ip])
                print(ip + " --> Actual: " + str(ip_count[ip]) + "  Max: " + str(ip_max_count[ip]) +"\n")
            time.sleep(0.01)
        else:
            print("Invalid argument, use -c for connections or -p for packages.")
            exit(1)
