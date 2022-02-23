import subprocess

process = subprocess.Popen(['ss', '-ntu'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    output = process.stdout.readline()
    print(output.strip())