import re
import smtplib
import dns.resolver
import pandas as pd
import time
import glob
import string
import json
import requests
import justext

csv_files=glob.glob('*.csv')
input_file=string.replace(csv_files[0], '.csv', '')
input_data=pd.read_csv(str(input_file)+'.csv',encoding='utf-8',error_bad_lines=False,sep=';')
count=0
fd = open(str(input_file)+'_output.csv','a')
fd.write('"Given Email";"Response"\n')
fd.close()
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
for index,Email in input_data.itertuples():
	count+=1
	given_email=str(Email.encode("utf-8")).lower()
	match = re.match(regex, given_email)
	if match == None:
		print('Bad Syntax')
		continue
	try:
		r = requests.post("https://checkeremail.com/smtp_check.php", data={'em': given_email, 'ch': 'nq6md5o7hpz5fd4eqxjs', 'hl': 'checkeremail.com','frm':'example@gmail.com'})
		response=justext.justext(r.content, justext.get_stoplist("English"))
		fd = open(str(input_file)+'_output.csv','a')
		fd.write('"'+given_email+'";"'+response[0].text+'"\n')
		fd.close()
		print(str(count)+' '+given_email+' '+response[0].text)
	except Exception as e:
		print(e)
		fd = open(str(input_file)+'_output.csv','a')
		fd.write('"'+given_email+'";"'+str(e)+'"\n')
		fd.close()
		continue	
		