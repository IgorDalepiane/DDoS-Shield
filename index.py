import subprocess

process = subprocess.Popen(['ss', '-ntu'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    row_lists = []

    return_code = process.poll()
    if return_code is not None:
        for output in process.stdout.readlines():
            rows = output.strip().split("\n")
            for row in rows:
                row_lists.append(row)
        print(row_lists)
        break