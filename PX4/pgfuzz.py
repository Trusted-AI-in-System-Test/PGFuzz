import time
from subprocess import *
import psutil
import sys, os, getopt

def main(argv):

	# (Start) Parse command line arguments (i.e., input and output file)
	try:
		opts, args = getopt.getopt(argv, "hi:o:f:", ["ifile=","--file"])
		input_file = ""
	except getopt.GetoptError:
		print("pgfuzz.py -i <true: Bounded input mutation / false: Unbounded input mutation>")
		sys.exit(2)

	if opts == []:
		print("pgfuzz.py -i <true/false> [optional] -f <metadata_file>")
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print("pgfuzz.py -i <true: Bounded input mutation / false: Unbounded input mutation>")
			sys.exit()
		elif opt in ("-i", "--ifile"):
			input_type = arg
		
		elif opt in ("-f", "--file"):
			input_file = arg

	open("input_mutation_type.txt", "w").close()

	f_input_type = open("input_mutation_type.txt", "w")
	if input_type == 'true':
		print("User chooses bounded input mutation")
		f_input_type.write('true\n')
	else:
		print("User chooses unbounded input mutation")
		f_input_type.write('false\n')
	
	if input_file == "":
		print("User chooses default options")
		input_file = "./default-metadata.json"
	else:
		print("Running using metadata from " + input_file)
	
	f_input_type.write(input_file)

	f_input_type.close()
	# (End) Parse command line arguments (i.e., input and output file)

	PGFUZZ_HOME = os.getenv("PGFUZZ_HOME")

	if PGFUZZ_HOME is None:
		raise Exception("PGFUZZ_HOME environment variable is not set!")

	PX4_HOME = os.getenv("PX4_HOME")

	if PX4_HOME is None:
		raise Exception("PX4_HOME environment variable is not set!")

	open("restart.txt", "w").close()
	open("iteration.txt", "w").close()
	open("shared_variables.txt", "w").close()

	c = 'gnome-terminal -- python2 ' + PGFUZZ_HOME + 'PX4/fuzzing.py &'
	Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
	
	while True:
		f = open("shared_variables.txt")
		if f.readline() == "build\n":
			lat_lon = f.readline().split(",")
			os.environ["PX4_HOME_LAT"] = lat_lon[0]
			os.environ["PX4_HOME_LON"] = lat_lon[1]
			f.close()
			break
		
		f.close()
		time.sleep(5)
	
	print("Opening simulator")
	c = 'gnome-terminal -- python2 ' + PGFUZZ_HOME + 'PX4/open_simulator.py &'
	handle = Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)

	# Sleep to allow sufficient time for simulator to start
	time.sleep(115)

	# Clear shared variables file telling fuzzing.py to continue running
	f = open("shared_variables.txt", "w")
	f.close()

	print("Running QGroundControl")
	qgc_handle = Popen("/home/pgfuzz/Downloads/QGroundControl.AppImage",stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)

	iteration = 1
	f2 = open("iteration.txt", "w")
	f2.write(str(iteration))
	f2.close()

	while True:
		
		f = open("restart.txt", "r")

		if f.read() != "restart":
			time.sleep(10)
			continue

		print("Restarting fuzzing")
		f.close()
		open("restart.txt", "w").close()

		iteration = iteration + 1
		open("iteration.txt", "w").close()
		f2 = open("iteration.txt", "w")
		f2.write(str(iteration))
		f2.close()

		qgc_handle.kill()
		handle.kill()
		for proc in psutil.process_iter():
			for process_name in ["QGroundControl", "QGroundControl.AppImage"]:
				if process_name in proc.name():
					proc.kill()
			
		c = 'gnome-terminal -- python2 ' + PGFUZZ_HOME + 'PX4/fuzzing.py &'
		Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
		
		while True:
			f = open("shared_variables.txt")
			if f.readline() == "build\n":
				lat_lon = f.readline().split(",")
				os.environ["PX4_HOME_LAT"] = lat_lon[0]
				os.environ["PX4_HOME_LON"] = lat_lon[1]
				f.close()
				break
			
			f.close()
			time.sleep(5)

		print("Opening simulator")
		c = 'gnome-terminal -- python2 ' + PGFUZZ_HOME + 'PX4/open_simulator.py &'
		handle = Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)

		# Sleep to allow sufficient time for simulator to start
		time.sleep(115)

		# Clear shared variables file telling fuzzing.py to continue running
		f = open("shared_variables.txt", "w")
		f.close()

		print("Running QGroundControl")
		qgc_handle = Popen("/home/pgfuzz/Downloads/QGroundControl.AppImage",stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
		


if __name__ == "__main__":
   main(sys.argv[1:])