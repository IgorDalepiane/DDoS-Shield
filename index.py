import subprocess

process = subprocess.Popen(['ss', '-ntu'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    return_code = process.poll()
    if return_code is not None:
        # Process has finished, read rest of the output 
        for output in process.stdout.readlines():
            print(output.strip())
        break