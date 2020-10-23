# import subprocess
# import time

# subprocess.run(["python", "test2.py"])




from subprocess import Popen, PIPE
import time

cmd_list = ["python", "test2.py"]
p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
stdout = p.stdout.read()
stderr = p.stderr.read()

for i in range(100,200):
	print(f"test1: {i}")
	print(stdout)
	time.sleep(0.5)


# if stdout:
# 	print(stdout)
# if stderr:
# 	print(stderr)