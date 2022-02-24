import subprocess
import time
import sys

ip_bytes_count = {}
ips_blocked = []
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
            

            for ip in ip_count.keys():
                print(ip + " --> Connections: " + str(ip_count[ip]), end="\n")
            time.sleep(1)

        elif sys.argv[1] == '-b':
            subprocess.run(['clear'])
            print("IP" + " --> " + "Bytes sent")
            for row in tcp_cons:
                print(row,end="\n");
                ip = row[5].split(":")[0]
                ip_bytes = ip+":"+row[2]+":"+row[4].split(":")[1]

                if int(row[2]) != 0:
                    if ip_bytes in ip_bytes_count:
                        ip_bytes_count[ip_bytes] += 1
                    else:
                        ip_bytes_count[ip_bytes] = 1

                    if ip in ip_count:
                        ip_count[ip] += 1
                    else:
                        ip_count[ip] = 1
            for ip in ip_count.keys():
                print("Number of Connections:", end='\n')
                print(ip + " --> " + str(ip_count[ip]), end="\n")

            temp_block=[]
            for key in ip_bytes_count.keys():
                ip = key.split(":")[0]
                ip_bytes = key.split(":")[1]
                
                if ip_bytes_count[key] > 50:
                    ips_blocked.append(key)
                    
                    subprocess.run(['sudo','iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', key.split(":")[2], '-s', ip, '-j', 'DROP'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
                    temp_block.append(key)

                print(ip + ":" + key.split(":")[2] + " --> Bytes: " + ip_bytes + " Count: " + str(ip_bytes_count[key]), end="\n")
            
            for ip in temp_block:
                ip_bytes_count.pop(ip)

            print("IPs Blocked:",end="\n")
            for ipblocked in ips_blocked:
                ipstring = ipblocked.split(":")[0] + ":" + ipblocked.split(":")[2]
                print("BLOCKED: "+ipblocked, end="\n")
            
            time.sleep(0.04)