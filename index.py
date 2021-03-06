import subprocess
import time
import sys

ip_bytes_count = {}
ips_blocked = []
MAX_CONNECTIONS = 50
MAX_SAME_BYTES_CONNECTIONS = 50

try:
    MAX_CONNECTIONS = sys.argv[1]
    MAX_SAME_BYTES_CONNECTIONS = sys.argv[2]
except:
    print("If you want to specify a number of connections or \nconnections with same number of bytes:")
    print("sudo index.py <MAX_CONNECTIONS> <MAX_SAME_BYTES_CONNECTIONS>")
    print("Using default value (50) for both")
    time.sleep(2)

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

        subprocess.run(['clear'])
        temp_block=[]
        for row in tcp_cons:
            ip = row[5].split(":")[0]
            ip_bytes = ip+":"+row[2]+":"+row[4].split(":")[1]

            if int(row[2]) != 0:
                if ip_bytes in ip_bytes_count:
                    ip_bytes_count[ip_bytes] += 1
                else:
                    ip_bytes_count[ip_bytes] = 1

            if ip in ip_count:
                ip_count[ip] += 1
                if ip_count[ip] > int(MAX_CONNECTIONS):
                    subprocess.run(['sudo','iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', row[4].split(":")[1], '-s', ip, '-j', 'DROP'], 
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
                    subprocess.run(['sudo','ss', '-K', 'dst', ip], 
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
                    ips_blocked.append(ip_bytes)
            else:
                ip_count[ip] = 1
                
        print("Number of Connections:", end='\n')
        for ip in ip_count.keys():
            print(ip + " --> " + str(ip_count[ip]), end="\n")

        print("\nBytes sent" + " --> " + "Counter")
        actualIp = None

        sortedList = sorted(ip_bytes_count.items(), key=lambda x: x[1], reverse=True)
        sortedDict = {}
        for value in sortedList:
            sortedDict[value[0]] = value[1]

        for key in sortedDict.keys():
            ip = key.split(":")[0]
                
            if actualIp != None and ip != actualIp:
                actualIp = ip
                print("\n" + actualIp + ": ")
            elif actualIp == None:
                actualIp = ip
                print(actualIp + ": ")

            ip_bytes = key.split(":")[1]
            if ip_bytes_count[key] > int(MAX_SAME_BYTES_CONNECTIONS):
                ips_blocked.append(key)
                
                subprocess.run(['sudo','iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', key.split(":")[2], '-s', ip, '-j', 'DROP'], 
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
                subprocess.run(['sudo','ss', '-K', 'dst', ip], 
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
                temp_block.append(key)
            print(ip_bytes + " --> " + str(ip_bytes_count[key]), end=" | ")
        
        remove_other_tcp = []
        for ip in temp_block:
            ip_bytes_count.pop(ip)
            for key in ip_bytes_count:
                ipstring_key = key.split(":")[0] + ":" + key.split(":")[2]
                ipstring_blocked = ip.split(":")[0] + ":" + ip.split(":")[2]

                if ipstring_key == ipstring_blocked:
                    remove_other_tcp.append(key)

        for tcp in remove_other_tcp:
            ip_bytes_count.pop(tcp)

        print("\nIPs Blocked:",end="\n")
        for ipblocked in ips_blocked:
            ipstring = ipblocked.split(":")[0] + ":" + ipblocked.split(":")[2]
            print("BLOCKED: "+ipstring, end="\n")
        
        time.sleep(0.04)