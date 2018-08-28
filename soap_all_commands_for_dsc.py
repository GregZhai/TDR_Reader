"""*******************************************************************************************************

This script provide all soap commands for DSC.
1. soap_reload_rule_engine(dsc_url)
2. soap_add_decide_route(origin_realm,dest_realm,next_hop,dsc_url,description,pop_name)
3. soap_add_list_cache(list_cache_name,realm_to_add,dsc_url)
4. soap_reload_listcaches(dsc_url)
5. soap_check_decide_route(dsc_url,source_host,source_realm,dest_host,dest_realm,adjacent_source_peer,adjacent_source_realm)
5.1 soap_check_decide_route_by_DR(dsc_url,src_realms,dest_realm)
6. soap_add_rule(dsc_url,ruletype,description,pop_name,orighost="*",origrealm="*",desthost="*",destrealm="*",srchost="*",srcrealm="*",priority="10",condition="1",consequence="RET := 0")
7. soap_dump_rule_engine(dsc_url,filename)
8. soap_add_mapcache(dsc_url,mapcachename,imsiprefix,realm)
9. soap_reload_mapcache(dsc_url)
10. soap_add_realm2op(dsc_url,realm,opname)
11. soap_reload_realm2op(dsc_url)
12. soap_get_customer_info(dsc_url,ssid)
13. soap_add_2d_listcache(dsc_url,listcachename,value1,value2)
14. soap_add_2d_mapcache(dsc_url,name,key1,key2,value)
15. soap_query_mapcache(dscurl,mapcachename)

Author: Jason Qin
Version: v4.0 2018.04.27

*******************************************************************************************************"""

#requests libary to trigger http request
import requests
import csv
import copy
import os

#ElementTree to handle xml file
import xml
from xml.etree import ElementTree as ET

#OS to handle any operation related to OS System
import os

#fuction to replace invalid letter in description to _
def replace_invalid_letter(str):
	invalidlist=". ;:,'`~>>{}[]\|&"
	invalidlist=invalidlist+'"'
	for i in range(len(invalidlist)):
		str=str.replace(invalidlist[i],'_')
	return(str)

def SPLIT2LIST(items):
	LIST=[]
	items = items.lower()
	items = items.replace(",",";")
	temp =  items.split(";")
	for item in temp:
		LIST.append(item.strip())
	return(LIST)
	
#function to excute http post and write result to local file
"""add contect-type to show xml content in wireshark"""
def soap_post(SURL,SENV,filename):
	#headers = {'Host': ''}
	headers = {'content-type': 'text/xml'}
	#headers = {'soapAction': ''}
	response = requests.post(SURL,data=SENV,headers=headers)
	with open(filename, 'w') as file_object:
		file_object.write(response.text)
	return response


"""****************************************************************************************************"""
"""***************************        1. reload rule engine          **********************************"""
"""****************************************************************************************************"""
def soap_reload_rule_engine(dsc_url):

	filename="Reload_rule_engine_result.xml"
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
		SENV=("""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"> <soapenv:Header/> <soapenv:Body> <ws:dscReloadRulesClient/> </soapenv:Body> </soapenv:Envelope>""")
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
		os.remove("Reload_rule_engine_result.xml")
		return result_final
#soap_reload_rule_engine("http://10.162.28.186:8080/DSC_SOAP/query?")


"""****************************************************************************************************"""
"""***************************           2. add decide route         **********************************"""
"""****************************************************************************************************"""
def soap_add_decide_route(origin_realm,dest_realm,next_hop,dsc_url,description,pop_name):
	description=replace_invalid_letter(description)
	filename="Add_decide_route_result.xml"
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
		
		if dsc_name=="HKG_DSC" or dsc_name=="SNG_DSC":
			pop_name="AP PoP"
		elif dsc_name=="AMS_DSC" or dsc_name=="FRT_DSC":
			pop_name="EU POP"
		elif dsc_name=="CHI_DSC" or dsc_name=="DAL_DSC":
			pop_name="NA POP"
	except KeyError:
		print("Wrong DSC Name, it must be one of HKG_DSC,SNG_DSC,AMS_DSC,FRT_DSC,CHI_DSC,DAL_DSC.")
		key=0"""

	if key==1:
		SENV=("""
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/">
		<soapenv:Header/>
		<soapenv:Body>
		<ws:dscAddRuleClient>
		<!--Optional:-->
		<arg0>*</arg0>
		<!--Optional:-->
		<arg1>"""+ origin_realm +"""</arg1>
		<!--Optional:-->
		<arg2>*</arg2>
		<!--Optional:-->
		<arg3>"""+ dest_realm +"""</arg3>
		<!--Optional:-->
		<arg4>*</arg4>
		<!--Optional:-->
		<arg5>*</arg5>
		<!--Optional:-->
		<arg6>16777251</arg6>
		<!--Optional:-->
		<arg7>DECIDE_ROUTE</arg7>
		<!--Optional:-->
		<arg8>10</arg8>
		<!--Optional:-->
		<arg9>1</arg9>
		<!--Optional:-->
		<arg10>""" + next_hop + """</arg10>
		<!--Optional:-->
		<arg11>""" + description +"""</arg11>
		<!--Optional:-->
		<arg12>""" + pop_name +"""</arg12>
		</ws:dscAddRuleClient>
		</soapenv:Body>
		</soapenv:Envelope>
		""")
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
		os.remove("Add_decide_route_result.xml")
		return result_final

#soap_add_decide_route("test.origin.com","test.dest.com",'DEST_REALM:="test.com"',"http://10.162.28.186:8080/DSC_SOAP/query?","test_soap_add_decide_route_python","AP POP")


"""****************************************************************************************************"""
"""***************************         3. add list cache             **********************************"""
"""****************************************************************************************************"""
def soap_add_list_cache(list_cache_name,realm_to_add,dsc_url):

	filename="Add_list_cache_result.xml"
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
		SENV=("""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscAddListCacheEntryClient><!--Optional:--><arg0>""" + list_cache_name + """</arg0><!--Optional:--><arg1>""" + realm_to_add + """</arg1></ws:dscAddListCacheEntryClient></soapenv:Body></soapenv:Envelope>""")
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
		os.remove("Add_list_cache_result.xml")
		return result_final
		
#soap_add_list_cache("LIST_6668_VIBO","test1.com","http://10.162.28.186:8080/DSC_SOAP/query?")



"""****************************************************************************************************"""
"""***************************         4. reload list caches         **********************************"""
"""****************************************************************************************************"""
def soap_reload_listcaches(dsc_url):

	filename="reload_listcaches_result.xml"
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
		SENV=("""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscReloadListCachesClient/></soapenv:Body></soapenv:Envelope>""")

		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
		os.remove("reload_listcaches_result.xml")
		return result_final
		
#soap_reload_listcaches("HKG_DSC")


"""****************************************************************************************************"""
"""***************************         5. check decide route         **********************************"""
"""****************************************************************************************************"""
def soap_check_decide_route(dsc_url,source_host,source_realm,dest_host,dest_realm,adjacent_source_peer,adjacent_source_realm):

	filename="Check_decide_route_result.xml"
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
		results=[]
		SENV=("""
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/">
		   <soapenv:Header/>
		   <soapenv:Body>
		      <ws:dscQueryClient>
		         <!--Optional:-->
		         <arg0>"""+source_host+"""</arg0>
		         <!--Optional:-->
		         <arg1>"""+source_realm+"""</arg1>
		         <!--Optional:-->
		         <arg2>"""+dest_host+"""</arg2>
		         <!--Optional:-->
		         <arg3>"""+dest_realm+"""</arg3>
		         <!--Optional:-->
		         <arg4>"""+adjacent_source_peer+"""</arg4>
		         <!--Optional:-->
		         <arg5>"""+adjacent_source_realm+"""</arg5>
		      </ws:dscQueryClient>
		   </soapenv:Body>
		</soapenv:Envelope>
		""")
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			results.append('xml.etree.ElementTree.ParseError')
			return results
			
		#for result in tree.iter("consequence"):
			#result_origin=result.text
			#print(result_origin)
			
		queriedRules= tree.findall('.//queriedRules')
		results=[]
		for queriedRule in queriedRules:
			rule=[]
			for decide_route in queriedRule:
				if decide_route.tag=="priority":
					rule.insert(0,decide_route.text)
				elif decide_route.tag=="condition":
					rule.insert(1,decide_route.text)
				elif decide_route.tag=="consequence":
					rule.insert(2,decide_route.text)
				elif decide_route.tag=="ruleType":
					rule.insert(3,decide_route.text)
			if "DECIDE_ROUTE" in rule:
				rule.remove("DECIDE_ROUTE")
				result=rule[0]+" "+rule[1]+" " +rule[2]
				results.append(result)
		os.remove("Check_decide_route_result.xml")
		return results

#print(soap_check_decide_route("http://10.160.28.32:8080/DSC_SOAP/query?","*","*","*","epc.mnc010.mcc202.3gppnetwork.org","*","*"))

"""****************************************************************************************************"""
"""***************************         5.1 check decide route by DR       **********************************"""
"""****************************************************************************************************"""
def soap_check_decide_route_by_DR(dsc_url,src_realms,dest_realm):

	filename="Check_decide_route_result.xml"
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
		results=[]
		SENV=("""
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/">
		   <soapenv:Header/>
		   <soapenv:Body>
		      <ws:dscQueryClient>
		         <!--Optional:-->
		         <arg3>"""+dest_realm+"""</arg3>
		      </ws:dscQueryClient>
		   </soapenv:Body>
		</soapenv:Envelope>
		""")
		src_realm_list=[]
		src_realm_list=SPLIT2LIST(src_realms)
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			results.append('xml.etree.ElementTree.ParseError')
			return results
			
		#for result in tree.iter("consequence"):
			#result_origin=result.text
			#print(result_origin)
			
		queriedRules= tree.findall('.//queriedRules')
		results=[]
		for queriedRule in queriedRules:
			rule=[]
			for item in queriedRule:
				if item.tag=="priority":
					rule.insert(0,item.text)
				elif item.tag=="srcRealm":
					rule.insert(1,item.text)
				elif item.tag=="destRealm":
					rule.insert(2,item.text)
				elif item.tag=="condition":
					rule.insert(3,item.text)
				elif item.tag=="consequence":
					rule.insert(4,item.text)
				elif item.tag=="ruleType":
					rule.insert(5,item.text)
			if "DECIDE_ROUTE" in rule:
				rule.remove("DECIDE_ROUTE")
				result=rule[0]+" "+rule[1]+" > "+dest_realm+"\ncond:" +rule[3]+" cons:" +rule[4]
				results.append(result)
		os.remove("Check_decide_route_result.xml")
		#make src=* and src=src_realm to the head
		arranged_results=[]
		for item in results:
			for orig_realm in src_realm_list:
				if orig_realm in item and orig_realm!="":
					arranged_results.insert(0,item)
					print("item insert"+item)
					results.remove(item)
		for item in results:
			if "*" in item:
				arranged_results.insert(0,item)
				results.remove(item)
		arranged_results.append("\nFrom other operator realm to dest_realm")
		for item in results:
			arranged_results.append(item)
		return arranged_results

#r=soap_check_decide_route_by_DR("http://10.160.28.32:8080/DSC_SOAP/query?","","epc.mnc010.mcc202.3gppnetwork.org")
#for row in r:
#	print(row)

"""****************************************************************************************************"""
"""***************************              6. add rule              **********************************"""
"""****************************************************************************************************"""
def soap_add_rule(dsc_url,ruletype,description,pop_name,orighost="*",origrealm="*",desthost="*",destrealm="*",srchost="*",srcrealm="*",priority="10",condition="1",consequence="RET := 0"):
	filename="Add_rule_result.xml"
	description=replace_invalid_letter(description)
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
		
		if dsc_name=="HKG_DSC" or dsc_name=="SNG_DSC":
			pop_name="AP PoP"
		elif dsc_name=="AMS_DSC" or dsc_name=="FRT_DSC":
			pop_name="EU POP"
		elif dsc_name=="CHI_DSC" or dsc_name=="DAL_DSC":
			pop_name="NA POP"
	except KeyError:
		print("Wrong DSC Name, it must be one of HKG_DSC,SNG_DSC,AMS_DSC,FRT_DSC,CHI_DSC,DAL_DSC.")
		key=0"""

	if key==1:
		SENV=("""
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/">
		<soapenv:Header/>
		<soapenv:Body>
		<ws:dscAddRuleClient>
		<!--Optional:-->
		<arg0>"""+orighost+"""</arg0>
		<!--Optional:-->
		<arg1>"""+ origrealm +"""</arg1>
		<!--Optional:-->
		<arg2>"""+desthost+"""</arg2>
		<!--Optional:-->
		<arg3>"""+ destrealm +"""</arg3>
		<!--Optional:-->
		<arg4>"""+srchost+"""</arg4>
		<!--Optional:-->
		<arg5>"""+srcrealm+"""</arg5>
		<!--Optional:-->
		<arg6>16777251</arg6>
		<!--Optional:-->
		<arg7>"""+ruletype+"""</arg7>
		<!--Optional:-->
		<arg8>"""+priority+"""</arg8>
		<!--Optional:-->
		<arg9>"""+condition+"""</arg9>
		<!--Optional:-->
		<arg10>""" + consequence + """</arg10>
		<!--Optional:-->
		<arg11>""" + description +"""</arg11>
		<!--Optional:-->
		<arg12>""" + pop_name +"""</arg12>
		</ws:dscAddRuleClient>
		</soapenv:Body>
		</soapenv:Envelope>
		""")
		
		soap_post(dsc_url,SENV,filename)

		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		
		F=open(filename)
		result_final=F.read()
		F.close
		
		for result in tree.iter("result"):
			result_origin=result.text
			#when fail,result will contain mutiple ':'
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]

		return result_final
		os.remove("Add_rule_result.xml")
#soap_add_rule("http://10.162.28.186:8080/DSC_SOAP/query?",ruletype="REQUEST_FILTER",description="U Mobile 7019: %request filter% if orig realm in RP LISTCACHE,let pass",pop_name="AP PoP",destrealm="epc.mnc018.mcc502.3gppnetwork.org",condition='(IsExist(#AVP296)&amp;&amp;InList(ToLower(AVP296),"LIST_7019_U_MOBILE"))')


"""****************************************************************************************************"""
"""***************************        7. soap_dump_rule_engine       **********************************"""
"""****************************************************************************************************"""
def soap_dump_rule_engine(dsc_url,filename):

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
		SENV=("""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"> <soapenv:Header/> <soapenv:Body> <ws:dscExportClient/> </soapenv:Body> </soapenv:Envelope>""")
		#SENV=("""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"> <soapenv:Header/> <soapenv:Body> <ws:dscQueryClient> <!--Optional:--> <srcHost>*</srcHost> <!--Optional:--> <srcRealm>*</srcRealm> <!--Optional:--> <destHost>*</destHost> <!--Optional:--> <destRealm>*</destRealm> <!--Optional:--> <adjacentSourcePeer>*</adjacentSourcePeer> <!--Optional:--> <adjacentSourceRealm>*</adjacentSourceRealm> </ws:dscQueryClient> </soapenv:Body> </soapenv:Envelope>
#""")
		soap_post(dsc_url,SENV,filename)
		
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
			result_final_final=("Dump rule engine result: " + result_final)
			return result_final_final

#soap_dump_rule_engine("http://10.166.28.200:8080/DSC_SOAP/query?","CHI_DSC.xml")


"""****************************************************************************************************"""
"""***************************         8. soap_add_mapcache          **********************************"""
"""****************************************************************************************************"""
def soap_add_mapcache(dsc_url,mapcachename,imsiprefix,realm):

	filename="Add_mapcache_result.xml"
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
		SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscAddMapCacheEntryClient><!--Optional:--><arg0>"""+mapcachename+"""</arg0><!--Optional:--><arg1>"""+imsiprefix+"""</arg1><!--Optional:--><arg2>"""+realm+"""</arg2></ws:dscAddMapCacheEntryClient></soapenv:Body></soapenv:Envelope>"""
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
			result_final_final=("Add mapcache result: " + result_final)
		os.remove("Add_mapcache_result.xml")
		return result_final_final
			#print(result_final_final)


#LAB DSC		
#print(soap_add_mapcache("http://10.166.20.125:8080/DSC_SOAP/query","MAP_TEST","50218","epc.mnc009.mcc295.3gppnetwork.org"))


"""****************************************************************************************************"""
"""***************************          9. soap_reload_mapcache      **********************************"""
"""****************************************************************************************************"""
def soap_reload_mapcache(dsc_url):

	filename="Reload_mapcache_result.xml"
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
		SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscReloadMapCachesClient/></soapenv:Body></soapenv:Envelope>"""
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
			result_final_final=("Reload mapcache result: " + result_final)
		os.remove("Reload_mapcache_result.xml")
		return result_final_final
			#print(result_final_final)


		
#soap_reload_mapcache("http://10.166.28.200:8080/DSC_SOAP/query?")


"""****************************************************************************************************"""
"""***************************         10. soap_add_realm_to_op      **********************************"""
"""****************************************************************************************************"""
def soap_add_realm2op(dsc_url,realm,opname):

	filename="Add_realm2op_result.xml"
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
		SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscAddRealm2OperatorCacheEntryClient><!--Optional:--><arg0>"""+realm+"""</arg0><!--Optional:--><arg1>"""+opname+"""</arg1></ws:dscAddRealm2OperatorCacheEntryClient></soapenv:Body></soapenv:Envelope>"""
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
			result_final_final=("Add result2op result: " + result_final)
		os.remove("Add_realm2op_result.xml")
		return result_final_final
			#print(result_final_final)



#soap_add_realm2op("http://10.166.28.200:8080/DSC_SOAP/query?","epc.mnc018.mcc502.3gppnetwork.org","7019#U-Mobile")


"""****************************************************************************************************"""
"""***************************         11. soap_reload_realm2op      **********************************"""
"""****************************************************************************************************"""
def soap_reload_realm2op(dsc_url):

	filename="Reload_realm2op_result.xml"
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
		SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscReloadRealm2OperatorCacheClient/></soapenv:Body></soapenv:Envelope>"""

		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			#print(len(result_origin.split(":")))
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
			result_final_final=("Reload realm2op result: " + result_final)
		os.remove("Reload_realm2op_result.xml")
		return result_final_final
			#print(result_final_final)
		


#soap_reload_realm2op("http://10.166.28.200:8080/DSC_SOAP/query?")


"""****************************************************************************************************"""
"""***************************       12. soap_get_customer_info      **********************************"""
"""****************************************************************************************************"""
def soap_get_customer_info(dsc_url,ssid):

	filename="soap_get_customer_info.xml"
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
		SENV=("""
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/">
		<soapenv:Header/>
		<soapenv:Body>
		<ws:dscGetCustomerPeeringInfo>
		<!--Optional:-->
		<arg0>"""+ssid+"""</arg0>
		</ws:dscGetCustomerPeeringInfo>
		</soapenv:Body>
		</soapenv:Envelope>
		""")
		
		soap_post(dsc_url,SENV,filename)
		
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'

		realms= tree.findall('.//Realm')
		realm_all=[]
		for realm in realms:
			for name in realm:
				if name.tag=="name":
					realm_all.append(name.text)

		os.remove("soap_get_customer_info.xml")
		return (realm_all)

#soap_get_customer_info('http://10.160.28.32:8080/DSC_SOAP/query?','6357')

def soap_add_2d_listcache(dsc_url,listcachename,value1,value2):
	filename="Add_2d_listcache_result.xml"
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
		SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/">\
		<soapenv:Header/><soapenv:Body><ws:dscAdd2DListCacheEntryClient>\
		<!--Optional:--><arg0>"""+listcachename+"""</arg0>\
		<!--Optional:--><arg1>"""+value1+"""</arg1>\
		<!--Optional:--><arg2>"""+value2+"""</arg2>\
		</ws:dscAdd2DListCacheEntryClient></soapenv:Body></soapenv:Envelope>"""
		
		#SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscAdd2DListCacheEntryClient><!--Optional:--><arg0>"""+listcachename+"""</arg0><!--Optional:--><arg1>"""+value1+"""</arg1><!--Optional:--><arg2>"""+value2+"""</arg2></ws:dscAdd2DListCacheEntryClient></soapenv:Body></soapenv:Envelope>"""

		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
			result_final="Add 2d listcache result: " + result_final
		os.remove(filename)
		return result_final
#soap_add_2d_listcache('http://10.163.28.131:8080/DSC_SOAP/query?','DUALPREFIXLIST_SRC_ORIGIN_REALM_WL','value1','value2')

def soap_add_2d_mapcache(dsc_url,name,key1,key2,value):
	filename="Add_2d_mapcache_result.xml"
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
		SENV="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscAdd2DMapCacheEntryClient>\
		<!--Optional:--><arg0>"""+name+"""</arg0>\
		<!--Optional:--><arg1>"""+key1+"""</arg1>\
		<!--Optional:--><arg2>"""+key2+"""</arg2>\
		<!--Optional:--><arg3>"""+value+"""</arg3>\</ws:dscAdd2DMapCacheEntryClient></soapenv:Body></soapenv:Envelope>"""
		
		soap_post(dsc_url,SENV,filename)
		try: 
			tree=ET.parse(filename)
		except xml.etree.ElementTree.ParseError:
			return 'xml.etree.ElementTree.ParseError'
		for result in tree.iter("result"):
			result_origin=result.text
			result_len=len(result_origin.split(":"))
			if result_len>1:
				result_final=result_origin.split(":")[0]+":"+result_origin.split(":")[1]+","+result_origin.split(":")[2]+"."
			else:
				result_final=result_origin.split(":")[0]
			result_final="Add 2d mapcache result: " + result_final
		os.remove(filename)
		return result_final
#soap_add_2d_mapcache('http://10.166.20.125:8080/DSC_SOAP/query?','DUALPREFIXMAP_TEST','KEY1','KEY2','VALUE')


def soap_query_mapcache(dsc_url,mapcache_name,csv_name='.\\file\conf_mapcache_MAP_IMSITOREALM.csv'):
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

#soap_query_mapcache('http://10.164.28.189:8080/DSC_SOAP/query?','REALM_TO_OPERATOR')
