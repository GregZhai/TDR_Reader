#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko,signal,sys

#command='tail -f /data3/DSC_APP/tdr/TDR.log | grep -a "Airtel" | grep -a "Rogers"'
command='ls -ltr /data3/DSC_APP/tdr/'

s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect('10.162.28.182',22,'g801781','Xianfeng111')
#transport=s.get_transport()
#channel = transport.open_session()
#channel.exec_command(command)
stdin, stdout, stderr = s.exec_command('killall -u g801781')
#print('1')
res,err = stdout.read(),stderr.read()
result = res if res else err
dirresult=result.decode().rstrip().lstrip()
print (dirresult)

#global is_sigint_up
#is_sigint_up = False



def quit1(signum,frame):
	global is_sigint_up
	is_sigint_up = True
	print(is_sigint_up)
	
	channel.close()
	s.close()
	return
	#sys.exit()
	
#while True:
	#print('a')
	#signal.signal(signal.SIGINT, quit1)
	#signal.signal(signal.SIGTERM, quit1)

#while True:
	#data_total=[]
	#try:
		#data=str(channel.recv(20480))
		#if not data: break
		#data_total.append(data)
		#cc=''.join(data_total)
		#print(cc)
		#if is_sigint_up:
			#print('You choose to stop tail command')
			#break
	#except Exception as e:
		#print(e)
	#signal.signal(signal.SIGINT, quit1)
	#signal.signal(signal.SIGTERM, quit1)
