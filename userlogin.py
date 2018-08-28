import tkinter
import tkinter.messagebox
import os
import os.path
import sys
import paramiko

user=''
pwd=''

def show_login():

	def login():
		global user, pwd
		user=entryName.get()
		pwd=entryPwd.get()
		root.destroy()

	def cancel():
		root.destroy()
		sys.exit()

	root = tkinter.Tk()
	root.title("Enter gid/pass to login DSC")
	root.geometry('330x170+500+200')

	labelName = tkinter.Label(root,text='Your Gid:',justify=tkinter.RIGHT,width=100)
	labelName.place(x=40, y=20, width=110, height=20)

	varName = tkinter.StringVar(root, value='')
	entryName = tkinter.Entry(root,width=80,textvariable=varName)
	entryName.place(x=170, y=20, width=100, height=20)

	labelPwd = tkinter.Label(root,text='Your Lan Password:',justify=tkinter.RIGHT,width=100)
	labelPwd.place(x=40, y=55, width=110, height=20)

	varPwd = tkinter.StringVar(root, value='')
	entryPwd = tkinter.Entry(root,show='*',width=80,textvariable=varPwd)
	entryPwd.place(x=170, y=55, width=100, height=20)

	buttonOk = tkinter.Button(root,text='Login',command=login)
	buttonOk.place(x=80, y=100, width=80, height=20)

	buttonCancel = tkinter.Button(root,text='Cancel',command=cancel)
	buttonCancel.place(x=180, y=100, width=80, height=20)
	
	root.mainloop()

	userinfodirectory1=os.getcwd()+r'\file\userinfo.txt'
	output = open(userinfodirectory1, 'w')
	output.write(user+' '+pwd)
	output.close()
	#print (user, pwd)


def tryconnect(user1,pwd1):
	
	global cccc
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(hostname='10.162.28.182', port=22, username=user1, password=pwd1)
	except paramiko.AuthenticationException as ddd:
		print("Authentication failed, please login again: "+str(ddd))
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', "Authentication failed, please login again: ")
		root1.destroy()
		cccc=1
		
			
	except paramiko.SSHException as sshException:
		print("Unable to establish SSH connection: %s" % sshException)
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', "Unable to establish SSH connection: %s" % sshException)
		sys.exit()
	except paramiko.BadHostKeyException as badHostKeyException:
		print("Unable to verify server's host key: %s" % badHostKeyException)
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', "Unable to verify server's host key: %s" % badHostKeyException)
		sys.exit()
	except Exception as e:
		print(e.args)
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', e.args)
		sys.exit()

	else:
		print("Login Successfully!")
		#root1=tkinter.Tk()
		#root1.withdraw()
		#tkinter.messagebox.showinfo('Information', "Login Successfully!")
		cccc=2
	


def loginuser():
	global cccc, user, pwd
	
	userinfodirectory=os.getcwd()+r'\file\userinfo.txt'

# if the userinfo.txt exists, if not, write one via show_login()
	if not os.path.exists(userinfodirectory):
		show_login()

# read user and pwd
	input=open(userinfodirectory)
	info=input.read().split(' ')
	input.close()
# decide if the userinfo.txt is empty, if so, write one via show_login()
	if len(info)==1:
		show_login()
		input=open(userinfodirectory)
		info=input.read().split(' ')
	user= info[0]
	pwd=info[1]
	input.close()

	cccc=0
	tryconnect(user,pwd)
	while cccc==1:
		show_login()
		input=open(userinfodirectory)
		info=input.read().split(' ')
		user= info[0]
		pwd=info[1]
		input.close()
		tryconnect(user,pwd)
