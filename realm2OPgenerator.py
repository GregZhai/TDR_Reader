import requests,xml,copy,csv,os
from xml.etree import ElementTree as ET

def soap_query_mapcache(dsc_url,mapcache_name,csv_name='.\\file\conf_mapcache_REALM_TO_OPERATOR.csv'):
	k=''
	v=''
	m={}
	filename="query_mapcache_result.xml"
	result_final=''
	key=1

	"""try:
		#Define IP address for each DSC server
		dsc_ip_summary= {"HKG_DSC":"http://10.162.28.186:8080/DSC_SOAP/query?",
		"SNG_DSC":"http://10.163.28.131:8080/DSC_SOAP/query?",
		"AMS_DSC":"http://10.160.28.32:8080/DSC_SOAP/query?" ,
		"FRT_DSC":"http://10.161.28.32:8080/DSC_SOAP/query?" ,
		"CHI_DSC":"http://10.166.28.200:8080/DSC_SOAP/query?",
		"DAL_DSC":"http://10.164.28.189:8080/DSC_SOAP/query?",}
		dsc_ip=dsc_ip_summary[dsc_name]

	except KeyError:
		print("Wrong DSC Name, it must be one of HKG_DSC,SNG_DSC,AMS_DSC,FRT_DSC,CHI_DSC,DAL_DSC.")
		key=0"""

	if key==1:
		SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscMapCacheByNameClient>\
		<!--Optional:--><arg0>"""+mapcache_name+"""</arg0>\
		</ws:dscMapCacheByNameClient></soapenv:Body></soapenv:Envelope>"""

		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		entrys= tree.findall('.//entry')
		results=[]
		for entry in entrys:
			for item in entry:
				if item.tag=="key":
					k=item.text
				if item.tag=="value":
					v=item.text
				m['key']=k
				m['value']=v
			results.append(copy.deepcopy(m))
		with open(csv_name, 'w',newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			string=[]
			#for keys in results[1]:
			#	string.append(keys)
			#spamwriter.writerow(string)
			for row in results:
				string=[]
				string.append(row['key'])
				string.append(row['value'])
				spamwriter.writerow(string)

		os.remove("query_mapcache_result.xml")
		return results
		
def soap_post(SURL,SENV,filename):
	#headers = {'Host': ''}
	headers = {'content-type': 'text/xml'}
	#headers = {'soapAction': ''}
	response = requests.post(SURL,data=SENV,headers=headers)
	with open(filename, 'w') as file_object:
		file_object.write(response.text)
	return response

#soap_query_mapcache('http://10.166.28.200:8080/DSC_SOAP/query?','REALM_TO_OPERATOR')
