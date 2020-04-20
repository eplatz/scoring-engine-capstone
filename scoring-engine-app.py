#Emily Platz
#CNCS Capstone Spring 2020
#Cyberpatriot Practice Scoring Engine

#import statements for necessary modules / libraries 
from flask import Flask, render_template
from packaging.version import parse as parse_version
import os, pwd, grp, subprocess
import configparser

#parses and reads config file
config = configparser.ConfigParser()
config.read('config.ini')

#creating the instance of the web application
app = Flask(__name__)


#score counter to keep track of points
score = 0

#function to check if unauthorized users are removed
def check_users():
	#pulling the global score variable
	global score

	#pulling the global config variable
	global config

	#grabbing all the users and putting them in a list
	user_list = [p.pw_name for p in pwd.getpwall()]

	#grabbing user1 variable from the config file
	user1 = config['check_users']['user1']

	#if unauthorized user was removed, points are given to student
	if user1 not in user_list:
		#message variable used for printing to webpage later
		msg1 = 'Bad user deleted +1 point'
		#score variable updated
		score += 1

	#if it was not removed, students are given a suggestion on where to look
	elif user1 in user_list:
		msg1 = 'Check users on system'
		score -= 1

	#returns variables from inside function
	return msg1,score


#function to check if an authorized user is changed to the proper account type
def check_usergrp():
	global score
	global config

	#grabbing user2 variable from the config file
	user2 = config['check_users']['user2']

	#setting up the variable for the sudo group
	grp_name = 'sudo'

	#setting up the variable to check sudo group
	info = grp.getgrnam(grp_name)

	#if unauthorized admin was removed from the sudoers group, points are given to student
	if user2 not in info.gr_mem:
		msg2 = 'Bad admin user changed to standard +1 point'
		score += 1

	#if unauthorized admin was still located in sudoers group, students are given a suggestion on where to look
	elif user2 in info.gr_mem:
		msg2 = 'Check users on system'
		score -= 1

	return msg2,score


#function to check if authorized service is running/active on the system
def check_service1():
	global score
	global config

	#grabbing service1 variable from the config file
	service1 = config['check_services']['service1']

	#opening a subprocess to run systemctl and capture the output to check if the service is active
	p = subprocess.Popen(['systemctl', 'is-active', service1], stdout=subprocess.PIPE)
	(output, err) = p.communicate()
	output = output.decode('utf-8')

	#if the service is inactive, students are given a suggestion on where to look
	if 'inactive' in output:
		msg3 = 'Check services on system'
		score -= 1

	#if the service is active, points are given to the the student
	elif 'active' in output: 
		msg3 = 'Apache2 service started/running +1 point'
		score += 1

	return msg3,score


#function to check if the firewall is running/active on the system
def check_firewall():
	global score

	#opening a subprocess to check the ufw status and capture the output to check if ufw is active
	fw = subprocess.Popen("sudo ufw status", shell=True, stdout=subprocess.PIPE)
	fw_status = fw.stdout.read()
	fw.stdout.close()
	fw.wait()

	#if the firewall is active, points are given to the student
	if b' active' in fw_status:
		msg4 = 'Firewall is active on the system +1 point'
		score += 1
		#returns variables from inside function

	#if the firewall is not active, students are given a suggestion on where to look
	elif b' inactive' in fw_status:
		msg4 = 'Check firewall on system'
		score -= 1

	return msg4,score


#function similar to check_service1, however this check awards points to the student if the service is stopped/removed 
def check_service2():
	global score
	global config

	#grabbing service2 variable from config file
	service2 = config['check_services']['service2']

	#opening a subprocess to check systemctl status and captures the output
	p = subprocess.Popen(['systemctl', 'is-active', service2], stdout=subprocess.PIPE)
	(output, err) = p.communicate()
	output = output.decode('utf-8')

	#if the service was stopped/removed, points are given to the student
	if 'inactive' in output:
		msg5 = 'Smbd(Samba) service stopped/removed +1 point'
		score += 1

	#if the service is active on the system, students are give a suggestion on where to look
	elif 'active' in output: 
		msg5 = 'Check services on system'
		score -= 1

	return msg5,score


#function to check if unauthorized files were removed from the system
def check_files():
	global score
	global config

	#grabbing the path1 variable from the config file
	path1 = config['check_files']['path1']

	#if path to the file exists, students are given a suggestion on where to look
	if os.path.exists(path1) == True:
		msg6 = 'Check user directories for unecessary files'
		score -= 1

	#if path to the file doesn't exist (was deleted), points are given to the student
	elif os.path.exists(path1) == False:
		msg6 = 'Unecessary file removed +1 point' 
		score += 1

	return msg6,score


#function to check if john the ripper was removed from the system
def check_program():
	global score
	global config

	#grabbing the program1 variable from the config file
	program1 = config['check_programs']['program1']

	#opening a subprocess to look for john the ripper on the system and captures the output
	program = subprocess.Popen(program1, shell=True, stdout=subprocess.PIPE)
	program_check = program.stdout.read()
	program.stdout.close()
	program.wait()

	#if the program was not removed, students are given a suggestion on where to look
	if program_check:
		msg7 = 'Check programs installed on system'
		score -= 1

	#if the program was removed, points are given to the student
	else:
		msg7 = 'Program john the ripper removed from system +1 point'
		score += 1

	return msg7,score


#function to check password length complexity
def check_pass_complex():
	global score

	#opening a subprocess to check password complexity settings
	pam = subprocess.Popen("cat /etc/pam.d/common-password", shell=True, stdout=subprocess.PIPE)
	pam_check = pam.stdout.read()
	pam.wait()

	#if the length was changed to be between 8-10 chars, points are given to the student
	if b'minlen=8' or b'minlen=9' or b'minlen=10' in pam_check:
		msg8 = 'Enforced password length complexity [8 - 10 chars] +1 point'
		score += 1

	#if the length was not changed, students are given a suggestion on where to look
	elif b'minlen=8' or b'minlen=9' or b'minlen=10' not in pam_check:
		msg8 = 'Check password complexity'
		score -= 1

	return msg8,score


#function to check if netcat was removed from the system
def check_nc():
	global score
	global config

	#grabbing the program2 variable from the config file
	program2 = config['check_programs']['program2']

	#opening subprocess to check for netcat on the system and capturing the output
	nc = subprocess.Popen("dpkg -l | grep netcat", shell=True, stdout=subprocess.PIPE)
	nc_check = nc.stdout.read()
	nc.stdout.close()
	nc.wait()

	#if netcat was found on the system, students are given a suggestion on where to look
	if nc_check:
		msg9 = 'Check programs installed on system'
		score -= 1

	#if netcat was removed, points are given to the student
	else:
		msg9 = 'Netcat fully removed from system +1 point'
		score += 1

	return msg9,score


#function to check password aging limits on the system
def check_login():
	global score

	#opens subprocess to check login.defs file and password aging limits and capture the output
	login = subprocess.Popen("cat /etc/login.defs", shell=True, stdout=subprocess.PIPE)
	login_check = login.stdout.read()
	login.wait()

	#if the following settings are present in the file, points are given to the student
	if b'PASS_MAX_DAYS ' and b'PASS_MIN_DAYS ' and b'PASS_WARN_AGE ' in login_check:
		msg10 = 'Added password aging limits +1 point'
		score += 1

	#if the following settings are not present in the file, students are given a suggestion on where to look 
	elif b'PASS_MAX_DAYS ' and b'PASS_MIN_DAYS ' and b'PASS_WARN_AGE ' not in login_check:
		msg10 = 'Check login.defs file'
		score -= 1

	return msg10,score


#function to check the version of firefox installed on the system
def check_firefox():
	global score
	global config

	#grabbing the version variable from the config file
	version = config['check_firefox']['version']

	#setting the variable for the most current version of firefox
	current_version = parse_version(version)

	#opening a subprocess to get the version of firefox installed on the system, awk extracts just the version
	firefox = subprocess.Popen("firefox --version | awk '{print $3 }'", shell=True, stdout=subprocess.PIPE)
	firefox_check = firefox.stdout.read()
	
	#the output of a subprocess is a byte object and it needs to be decoded into utf-8 and changed to a string
	firefox_check_string = firefox_check.decode('utf-8')
	firefox.stdout.close()
	firefox.wait()

	#if the installed version is less than the current version, students are given a suggestion on where to look
	if parse_version(firefox_check_string) < current_version:
		msg11 = 'Update firefox'
		score -= 1

	#if the installed version is greater than or equal to the current version, points are given to the student
	elif parse_version(firefox_check_string) >= current_version:
		msg11 = 'Firefox has been updated +1 point'
		score += 1

	return msg11,score


#function to reset the score to 0, this keeps the score from infinitely increasing every time the page is refreshed
def reset_score():
	global score
	score = 0

	return score


#mapping the app function to the URL, the scoring engine will display at the root directory or /home
@app.route('/')
@app.route('/home')

#defining the home function, which is what will be returned to the screen on the webpage
def home():
	#mapping the proper variables to their respective functions
	score = reset_score()
	msg1,score = check_users()
	msg2,score = check_usergrp()
	msg3,score = check_service1()
	msg4,score = check_firewall()
	msg5,score = check_service2()
	msg6,score = check_files()
	msg7,score = check_program()
	msg8,score = check_pass_complex()
	msg9,score = check_nc()
	msg10,score = check_login()
	msg11,score = check_firefox()

	#returns the html template and imports the variables to the jinja 2 variables in home.html
	return render_template('home.html', score=score, msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msg6=msg6, msg7=msg7, msg8=msg8, msg9=msg9, msg10=msg10, msg11=msg11)