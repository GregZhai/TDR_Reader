str=r'abc  dfdfd  dfdf  ddd \n dffd fdfdf d'

c= str.split(r'\n')
cc=[]
for i in c:
	cc.append(i.lstrip())

ccc='\n'.join(cc)



print (ccc)
