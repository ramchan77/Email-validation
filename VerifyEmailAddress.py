import re
import smtplib
import dns.resolver
import pandas as pd
import time
import glob
import string
import json

csv_files=glob.glob('*.csv')
input_file=string.replace(csv_files[0], '.csv', '')
input_data=pd.read_csv(str(input_file)+'.csv',encoding='utf-8',error_bad_lines=False,sep=';')
count=0
fd = open(str(input_file)+'_output.csv','a')
fd.write('"Given Email";"Response Code";"Domain Status"\n')
fd.close()
fromAddress = 'email'
pwd='pass'
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
for index,Email in input_data.itertuples():
	# Address used for SMTP MAIL FROM command  
	count+=1
	
	# Simple Regex for syntax checking
	# Email address to verify
	#inputAddress = str(email.encode("utf-8"))
	addressToVerify = str(Email.encode("utf-8")).lower()
	print(str(count)+' '+addressToVerify)
	# Syntax check
	match = re.match(regex, addressToVerify)
	if match == None:
		print('Bad Syntax')
		continue
		#raise ValueError('Bad Syntax')

	# Get domain for DNS lookup
	splitAddress = addressToVerify.split('@')
	domain = str(splitAddress[1])
	print('Domain:', domain)

	# MX record lookup
	try:
		records = dns.resolver.query(domain, 'MX')
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)
	except Exception as e:
		print(e)
		fd = open(str(input_file)+'_output.csv','a')
		fd.write('"'+addressToVerify+'";"";"'+str(e)+'"\n')
		fd.close()
		continue	

	# SMTP lib setup (use debug level for full output)
	server = smtplib.SMTP()
	server.set_debuglevel(1)

	# SMTP Conversation
	try:
		server.connect(mxRecord)
		server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
		server.mail(fromAddress)
		code, message = server.rcpt(str(addressToVerify))
		server.quit()
	except Exception as e:
		print(e)
		fd = open(str(input_file)+'_output.csv','a')
		fd.write('"'+addressToVerify+'";"";"'+str(e)+'"\n')
		fd.close()
		continue	

	#print(code)
	#print(message)

	# Assume SMTP response 250 is success
	if code == 250:
		print("success")
		print(message)
		fd = open(str(input_file)+'_output.csv','a')
		fd.write('"'+addressToVerify+'";"'+str(code)+'";"'+str(message)+'"\n')
		fd.close()
	else:
		print("success")
		print(message)
		fd = open(str(input_file)+'_output.csv','a')
		fd.write('"'+addressToVerify+'";"'+str(code)+'";"'+str(message)+'"\n')
		fd.close()
