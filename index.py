import subprocess
import time
import sys

while True:
    ip_count = {}
    
    process = subprocess.run(['ss', '-ntu'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    tcp_cons = []
    if process.returncode is not None:
        rows = process.stdout.strip().split("\n")
        for row in rows:
            tcp_cons.append(row.split())
        
        tcp_cons.remove(tcp_cons[0])
        if len(sys.argv) == 1 or sys.argv[1] != '-c' and sys.argv[1] != '-b':
            print("Invalid argument, use -c for connections or -b for bytes method.")
            exit(1)
        elif sys.argv[1] == '-c':
            if len(sys.argv) < 3:
                print("Please use '-c <MAX_CONNECTIONS>'")
                exit(1)

            subprocess.run(['clear'])
            print("IP" + " --> " + "Connections")
            for row in tcp_cons:
                ip = row[5].split(":")[0]
                if ip in ip_count:
                    ip_count[ip] += 1
                else:
                    ip_count[ip] = 1

            for ip in ip_count.keys():
                print(ip + " --> Connections: " + str(ip_count[ip]), end="\n")
            time.sleep(1)

        elif sys.argv[1] == '-b':
            subprocess.run(['clear'])
            
            print("IP" + " --> " + "Bytes sent")
            for row in tcp_cons:
                ip = row[5].split(":")[0]
                ip_bytes = ip+":"+row[2]

                if ip_bytes in ip_count:
                    ip_count[ip_bytes] += 1
                else:
                    ip_count[ip_bytes] = 1

            for key in ip_count.keys():
                ip = key.split(":")[0]
                ip_bytes = key.split(":")[1]
                print(ip + " --> Bytes: " + ip_bytes + " Count: " + ip_count[key], end="\n")

            print(ip_count)
            time.sleep(1)
