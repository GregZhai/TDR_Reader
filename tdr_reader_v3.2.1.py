#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tdr_reader_UI_v3 import *
from Show_TDR import *
from Show_Command import *
from Show_Result_NA import *
from Show_Result_APEU import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from realm2OPgenerator import *

from userlogin import *
import sys,os,signal
import re
import paramiko,time
import threading
import csv
import pyperclip


class inputTDRWindow(QMainWindow, Ui_Input_TDR):
	sendtdr=pyqtSignal(object)
	sendcommandtext=pyqtSignal(str,str)
	sendcommandtextmulti_AP=pyqtSignal(str)
	sendcommandtextmulti_EU=pyqtSignal(str)
	sendcommandtextmulti_NA=pyqtSignal(str)
	def __init__(self, parent=None):
		super(inputTDRWindow, self).__init__(parent)
		self.setupUi(self)
		
		self.tableWidget_filterTable.setColumnWidth(0,190)
		self.tableWidget_filterTable.setColumnWidth(1,190)
		self.tableWidget_filterTable.setColumnWidth(2,1)
		
		self.pushButton.clicked.connect(self.sendtext)
		self.pushButton_list_TDR_today.clicked.connect(self.listtdoayTDR)
		self.pushButton_list_TDR_Before.clicked.connect(self.listbeforeTDR)
		self.pushButton_multiServer.clicked.connect(self.multiServer)
		
		self.checkBox_cat.stateChanged.connect(self.setCommandTypeCat)
		self.checkBox_zcat.stateChanged.connect(self.setCommandTypeZcat)
		self.checkBox_tail.stateChanged.connect(self.setCommandTypeTail)
		self.radioButton_TDR_Today.clicked.connect(self.commandF1)
		self.radioButton_TDR_Before.clicked.connect(self.commandF1)
		self.pushButton_FormCommand.clicked.connect(self.formcommand)
		self.lineEdit_filename.textChanged.connect(self.filenamechanged)
		self.checkBox_AddFilter.stateChanged.connect(self.activateSelectOP)
		self.checkBox_AddSort.stateChanged.connect(self.addSort)
		self.checkBox_AddTitle.stateChanged.connect(self.addTitle)
		self.checkBox_grep1.stateChanged.connect(self.addgrep1)
		self.checkBox_grep2.stateChanged.connect(self.addgrep2)
		self.radioButton_ToTMPDirectory.clicked.connect(self.sortTo)
		self.radioButton_ToLocalDirectory.clicked.connect(self.sortTo)
		
		self.comboBox_OpName.activated.connect(self.selectOP)
		self.comboBox_OpName.currentIndexChanged.connect(self.printRealm)
		self.comboBox_realmselection.currentTextChanged.connect(self.copyRealm)
		
		
		
		self.addchooseServer(self.comboBox_chooseServer)
		self.addchooseServer(self.comboBox_chooseServer_2)

		self.comboBox_chooseServer.currentIndexChanged.connect(self.setServer)
		self.comboBox_chooseServer_2.currentIndexChanged.connect(self.setServer_2)
		
		global user,pwd
		loginuser()
		userinfodirectory=os.getcwd()+r'\file\userinfo.txt'
		input=open(userinfodirectory)
		info=input.read().split(' ')
		user= info[0]
		pwd=info[1]
		input.close()
		
		soap_query_mapcache('http://10.166.28.200:8080/DSC_SOAP/query?','REALM_TO_OPERATOR')
		self.genOPName(r'.\file\conf_mapcache_REALM_TO_OPERATOR.csv')

		global DB
		DB = self.csv2dict(r".\file\TDRFILTER.csv")
		rowindex=0
		for row in DB:
			item1=QTableWidgetItem('')
			item2=QTableWidgetItem(row['Format'])

			self.tableWidget_filterTable.setItem(rowindex,1,item1)
			self.tableWidget_filterTable.setItem(rowindex,2,item2)

			palette = QtGui.QPalette()
			brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
			brush.setStyle(QtCore.Qt.SolidPattern)
			palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
			brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
			brush.setStyle(QtCore.Qt.SolidPattern)
			palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
			brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
			brush.setStyle(QtCore.Qt.SolidPattern)
			palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

			font = QtGui.QFont()
			font.setPointSize(8)
			font.setBold(True)
			font.setWeight(75)
			self.chk=QCheckBox(row['Index']+'.'+row['Name'])
			if str(row['Mark'])=='1':
				self.chk.setFont(font)
				self.chk.setPalette(palette)
			self.chk.toggled.connect(lambda:self.toggle())
			self.tableWidget_filterTable.setCellWidget(rowindex,0,self.chk)

			if rowindex== 27:
				self.comboBox_show_OP=QComboBox()
				self.comboBox_show_OP.setEditable(True)
				self.tableWidget_filterTable.setCellWidget(rowindex,1,self.comboBox_show_OP)
				self.comboBox_show_OP.activated.connect(self.printOOP)
			if rowindex== 30:
				self.comboBox_show_OP_2=QComboBox()
				self.comboBox_show_OP_2.setEditable(True)
				self.tableWidget_filterTable.setCellWidget(rowindex,1,self.comboBox_show_OP_2)
				self.comboBox_show_OP_2.activated.connect(self.printDOP)
			rowindex=rowindex+1
		self.tableWidget_filterTable.setRowCount(rowindex)
		self.tableWidget_filterTable.cellChanged.connect(self.build_filter)
	
	
	def addchooseServer(self,combobox):
		combobox.addItem('Select Server')
		combobox.addItem('HKG APP1')
		combobox.addItem('HKG APP2')
		combobox.addItem('HKG APP3')
		combobox.addItem('SNG APP1')
		combobox.addItem('SNG APP2')
		combobox.addItem('SNG APP3')
		combobox.addItem('FRT APP1')
		combobox.addItem('FRT APP2')
		combobox.addItem('FRT APP3')
		combobox.addItem('AMS APP1')
		combobox.addItem('AMS APP2')
		combobox.addItem('AMS APP3')
		combobox.addItem('DAL APP1')
		combobox.addItem('DAL APP2')
		combobox.addItem('DAL APP4')
		combobox.addItem('DAL APP5')
		combobox.addItem('DAL APP6')
		combobox.addItem('CHI APP1')
		combobox.addItem('CHI APP2')
		combobox.addItem('CHI APP3')
		combobox.addItem('CHI APP4')
		combobox.addItem('CHI APP5')

	def genOPName(self,filename):
		OP_raw=[]
		OP_STR=''
		OP=[]
		with open(filename, 'r') as myFile:  
			lines=csv.reader(myFile)  
			for row in lines:
				OP_raw.append(row[1])
				
		for i in OP_raw:
			if i not in OP:
				OP.append(i)

		for i in range(0,len(OP)):
			OP_STR=OP_STR+OP[i]+'\n'
		userinfodirectory1=os.getcwd()+r'\file\OPname.txt'
		output = open(userinfodirectory1, 'w')
		output.write(OP_STR)
		output.close()

	def selectOP(self):
		xxx=self.comboBox_OpName.lineEdit().text()
		self.comboBox_OpName.removeItem(0)
		abc=self.comboBox_OpName.count()
		while abc>0 :
			self.comboBox_OpName.removeItem(0)
			abc=abc-1
		inputrealm2OP=open(r'.\file\OPname.txt')
		fa = inputrealm2OP.readlines()
		
		for item in fa:
			if re.search(xxx, item.lstrip().strip('\n'), re.IGNORECASE)!=None:
				self.comboBox_OpName.addItem(item.lstrip().strip('\n'))
		
	def printRealm(self):
		abc=self.comboBox_realmselection.count()
		while abc>0 :
			self.comboBox_realmselection.removeItem(0)
			abc=abc-1
		
		OPname=self.comboBox_OpName.lineEdit().text()
		realm=[]
		with open(r'.\file\conf_mapcache_REALM_TO_OPERATOR.csv', 'r') as myFile:  
			lines=csv.reader(myFile)
			for row in lines:
				if OPname==row[1]:
					realm.append(row[0])
		for i in realm:
			self.comboBox_realmselection.addItem(i.lstrip().strip('\n'))
			
	def copyRealm(self):
		pyperclip.copy(self.comboBox_realmselection.currentText())
		
	def toggle(self):
		bbb=self.sender()
		index = self.tableWidget_filterTable.indexAt(bbb.pos())
		rowindex=int(index.row())

		bg=self.tableWidget_filterTable.item(rowindex,2).background().color()
		if str(bg.red())!="200":
			self.tableWidget_filterTable.item(rowindex ,2).setBackground(QBrush(QColor(200,200,200)))
		if str(bg.red())=="200":
			self.tableWidget_filterTable.item(rowindex ,2).setBackground(QBrush(QColor(255,255,255)))
		self.build_filter()
	global titlefinal11,titlefinal22,titlefilter
	titlefinal11=''
	titlefinal22=''
	titlefilter=''
	def build_filter(self):
		printf_filter_1=''
		printf_filter_2=''
		tdr_filter=''
		title1=''
		title2=''
		global titlefinal11,titlefinal22,titlefilter
		row_index=0
		for row in range(self.tableWidget_filterTable.rowCount()):
			bg=self.tableWidget_filterTable.item(row_index ,2).background().color()
			if str(bg.red())=="200":
				printf_filter_1=printf_filter_1+DB[row_index]['Format']
				printf_filter_2=printf_filter_2+'$'+DB[row_index]['Index']+","

				titleraw=DB[row_index]['Format']
				Pos1=titleraw.find('%')
				str_list=list(titleraw)
				content1=str_list[:Pos1-1]
				content2=str_list[Pos1:]

				title11="".join(content1)
				title22="".join(content2)
				title11='"'+title11+'"'

				title2=title2+title22+' '
				title1=title1+title11+', '

			if self.tableWidget_filterTable.item(row_index ,1).text()!="":
				tdr_filter=tdr_filter+ "$"+ str(row_index+1)+"~/"+self.tableWidget_filterTable.item(row_index ,1).text()+"/&&"
			if row_index== 27 and self.comboBox_show_OP.currentText()!="":
				tdr_filter=tdr_filter+"$"+ str(row_index+1)+"~/"+self.comboBox_show_OP.currentText()+"/&&"
			if row_index== 30 and self.comboBox_show_OP_2.currentText()!="":
				tdr_filter=tdr_filter+"$"+ str(row_index+1)+"~/"+self.comboBox_show_OP_2.currentText()+"/&&"

			row_index=row_index+1
			
			titlefinal1='''|awk 'BEGIN{printf "'''+r'%-7s '+title2+r'\n","Number",'+title1+r';printf "-------------------------------------------------------------------------------------------------------------------------------------------------\n"}{print $0}'+"'"
			
			titlefinal2='''|awk 'BEGIN{printf "'''+title2+r'\n",'+title1+r';printf "-------------------------------------------------------------------------------------------------------------------------------------------------\n"}{print $0}'+"'"
			titlefinal11=titlefinal1.replace(', ;',';')
			titlefinal22=titlefinal2.replace(', ;',';')
			
			tdr_filter1= tdr_filter.replace('\n',' ')

			titlefilter3="|awk '{if("+ tdr_filter1+') printf"' +title2+r'\n",'+printf_filter_2+"}'"
			titlefilter2=titlefilter3.replace(',}','}')
			titlefilter=titlefilter2.replace('/&&)','/)').replace('if()','')

			
			final_filter_5 = "|awk '{"+ "if("+tdr_filter1 +")"+"printf"+'"'+printf_filter_1+' \\n",'+printf_filter_2+"}'"
			final_filter_4 = final_filter_5.replace(',}','}')
			final_filter_3 = final_filter_4.replace(' /&&','/&&')
			final_filter_2   = final_filter_3.replace('&&)printf',')printf')
			final_filter     = final_filter_2.replace('if()','')

		self.textEdit_test.setText(final_filter)
		self.addSort()
		

		if str(self.checkBox_AddTitle.checkState())=='2' and str(self.checkBox_AddSort.checkState())=='2':
			self.groupBox_Sort.setEnabled(True)
			if self.radioButton_ToTMPDirectory.isChecked()==True:
				self.textEdit_test.setText(titlefilter+'| sort -T /data4/TMP/tsdss | uniq -c | sort -k 1 -rn -T /data4/TMP/tsdss | head -n 15'+titlefinal11)
			if self.radioButton_ToLocalDirectory.isChecked()==True:
				self.textEdit_test.setText(titlefilter+'| sort | uniq -c | sort -k 1 -rn | head -n 15'+titlefinal11)
		if str(self.checkBox_AddTitle.checkState())=='2' and str(self.checkBox_AddSort.checkState())=='0':
			self.groupBox_Sort.setEnabled(False)
			self.textEdit_test.setText(titlefilter+titlefinal22)
			
		if self.textEdit_test.toPlainText()=='|awk'+" '"+r'{printf" \n"}'+"'":
			self.textEdit_test.setText('')
			

	def csv2dict(self,in_file):
		import csv
		new_dict = {}
		with open(in_file, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			fieldnames = next(reader)
			reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
			new_dict = [row for row in reader]
		return new_dict

	def multiServer(self):
		global finalcommand,serverlist,commandtype,filename
		
		if commandtype =='':
			print ('Please select command type first.')
			QMessageBox.warning(self,"Warning","Please select command type first.",QMessageBox.Ok)
			return
		if filename=='':
			print ('Please input TDR file name first.')
			QMessageBox.warning(self,"Warning",'Please input TDR file name first.',QMessageBox.Ok)
			return
			
		if 'zcat' in commandtype:
			str_list=list(filename)
			str_list=str_list[-13:]
			
			filename="".join(str_list)
			filename='*'+filename
			
			
		if str(self.checkBox_AddFilter.checkState())=='2':
			if str(self.checkBox_grep1.checkState())=='2':
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'+ '| grep -a "'+self.lineEdit_grep2.text()+'"'+self.textEdit_test.toPlainText()
				else:
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'+self.textEdit_test.toPlainText()
			else:
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep2.text()+'"'+self.textEdit_test.toPlainText()
				else:
					finalcommand=commandtype+filename+self.textEdit_test.toPlainText()
		else:
			if str(self.checkBox_grep1.checkState())=='2':
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'+ '| grep -a "'+self.lineEdit_grep2.text()+'"'
				else:
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'
			else:
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep2.text()+'"'
				else:
					finalcommand=commandtype+filename
					
		if str(self.checkBox_AP_Servers.checkState())=='2':
			self.sendcommandtextmulti_AP.emit(finalcommand)
		if str(self.checkBox_EU_Servers.checkState())=='2':
			self.sendcommandtextmulti_EU.emit(finalcommand)
		if str(self.checkBox_NA_Servers.checkState())=='2':
			self.sendcommandtextmulti_NA.emit(finalcommand)
		if str(self.checkBox_AP_Servers.checkState())=='0' and str(self.checkBox_EU_Servers.checkState())=='0' and str(self.checkBox_NA_Servers.checkState())=='0':
			print ('Please select server region first.')
			QMessageBox.warning(self,"Warning","Please select server region first.",QMessageBox.Ok)
			return
	
	def addgrep1(self):
		if str(self.checkBox_grep1.checkState())=='2':
			self.lineEdit_grep1.setEnabled(True)
		if str(self.checkBox_grep1.checkState())=='0':
			self.lineEdit_grep1.setEnabled(False)
	def addgrep2(self):
		if str(self.checkBox_grep2.checkState())=='2':
			self.lineEdit_grep2.setEnabled(True)
		if str(self.checkBox_grep2.checkState())=='0':
			self.lineEdit_grep2.setEnabled(False)
		
	def sortTo(self):
		content=self.textEdit_test.toPlainText()
		if self.radioButton_ToTMPDirectory.isChecked()==True:
			content=content.replace('| sort | uniq -c | sort -k 1 -rn | head -n 15','| sort -T /data4/TMP/tsdss | uniq -c | sort -k 1 -rn -T /data4/TMP/tsdss | head -n 15')
			self.textEdit_test.setText(content)
		if self.radioButton_ToLocalDirectory.isChecked()==True:
			content=content.replace('| sort -T /data4/TMP/tsdss | uniq -c | sort -k 1 -rn -T /data4/TMP/tsdss | head -n 15','| sort | uniq -c | sort -k 1 -rn | head -n 15')
			self.textEdit_test.setText(content)
			
	def addTitle(self):
		global titlefinal11,titlefinal22
		if str(self.checkBox_AddTitle.checkState())=='2' and str(self.checkBox_AddSort.checkState())=='2':
			if self.radioButton_ToTMPDirectory.isChecked()==True:
				self.textEdit_test.setText(titlefilter+'| sort -T /data4/TMP/tsdss | uniq -c | sort -k 1 -rn -T /data4/TMP/tsdss | head -n 15'+titlefinal11)
			if self.radioButton_ToLocalDirectory.isChecked()==True:
				self.textEdit_test.setText(titlefilter+'| sort | uniq -c | sort -k 1 -rn | head -n 15'+titlefinal11)
		if str(self.checkBox_AddTitle.checkState())=='2' and str(self.checkBox_AddSort.checkState())=='0':
			self.textEdit_test.setText(titlefilter+titlefinal22)
		if str(self.checkBox_AddTitle.checkState())=='0':
			self.build_filter()
	
	
	def addSort(self):
		if str(self.checkBox_AddSort.checkState())=='2':
			self.groupBox_Sort.setEnabled(True)
			if str(self.checkBox_AddTitle.checkState())=='2':
				self.checkBox_AddTitle.setChecked(False)
				self.checkBox_AddTitle.setChecked(True)
			#self.checkBox_AddTitle.setEnabled(True)
			else:
				content=self.textEdit_test.toPlainText()
				if self.radioButton_ToTMPDirectory.isChecked()==True:
					content=content+'| sort -T /data4/TMP/tsdss | uniq -c | sort -k 1 -rn -T /data4/TMP/tsdss | head -n 15'
				if self.radioButton_ToLocalDirectory.isChecked()==True:
					content=content+'| sort | uniq -c | sort -k 1 -rn | head -n 15'
				self.textEdit_test.setText(content)
			
		if str(self.checkBox_AddSort.checkState())=='0':
			#self.checkBox_AddTitle.setEnabled(False)
			if str(self.checkBox_AddTitle.checkState())=='2':
				self.checkBox_AddTitle.setChecked(False)
				self.checkBox_AddTitle.setChecked(True)
				
			content=self.textEdit_test.toPlainText()
			content=content.replace('| sort | uniq -c | sort -k 1 -rn | head -n 15','')
			content=content.replace('| sort -T /data4/TMP/tsdss | uniq -c | sort -k 1 -rn -T /data4/TMP/tsdss | head -n 15','')
			self.groupBox_Sort.setEnabled(False)
			self.textEdit_test.setText(content)
			
		if self.textEdit_test.toPlainText()=='|awk'+" '"+r'{printf" \n"}'+"'":
			self.textEdit_test.setText('')

	def activateSelectOP(self):
		if str(self.checkBox_AddFilter.checkState())=='2':
			self.tableWidget_filterTable.setEnabled(True)
			self.checkBox_AddSort.setEnabled(True)
			self.checkBox_AddTitle.setEnabled(True)
			self.textEdit_test.setEnabled(True)
			self.checkBox_tail.setChecked(False)
			
		if str(self.checkBox_AddFilter.checkState())=='0':
			self.tableWidget_filterTable.setEnabled(False)
			self.checkBox_AddSort.setEnabled(False)
			self.checkBox_AddTitle.setEnabled(False)
			self.textEdit_test.setEnabled(False)
			

	def filenamechanged(self):
		global filename
		filename=self.lineEdit_filename.text().rstrip().lstrip()

	global commandtype
	commandtype=''
	global filename
	filename=''
	global serverlist
	serverlist=[]
	
	def commandF1(self):
		self.groupBox_listTDR.setEnabled(True)
		
		if self.radioButton_TDR_Today.isChecked()==True:
			self.checkBox_cat.setEnabled(True)
			self.checkBox_tail.setEnabled(True)
			self.groupBox_todaycommand.setEnabled(True)
			self.checkBox_zcat.setEnabled(False)
			self.checkBox_zcat.setChecked(False)

		if self.radioButton_TDR_Before.isChecked()==True:
			self.checkBox_tail.setChecked(False)
			self.checkBox_cat.setChecked(False)
			self.checkBox_cat.setEnabled(False)
			self.checkBox_tail.setEnabled(False)
			self.checkBox_zcat.setEnabled(True)
			self.checkBox_zcat.setChecked(True)
			self.groupBox_todaycommand.setEnabled(False)
	global serverMapDic
	
	serverMapDic={'HKG APP1':'10.162.28.182','HKG APP2':'10.162.28.183','HKG APP3':'10.162.28.184','SNG APP1':'10.163.28.126','SNG APP2':'10.163.28.127','SNG APP3':'10.163.28.128','FRT APP1':'10.161.28.36','FRT APP2':'10.161.28.37','FRT APP3':'10.161.28.248','AMS APP1':'10.160.28.36','AMS APP2':'10.160.28.37','AMS APP3':'10.160.28.217','DAL APP1':'10.164.28.175','DAL APP2':'10.164.28.176','DAL APP4':'10.164.28.253','DAL APP5':'10.164.20.49','DAL APP6':'10.164.20.50','CHI APP1':'10.166.28.189','CHI APP2':'10.166.28.190','CHI APP3':'10.166.29.2','CHI APP4':'10.166.20.54','CHI APP5':'10.166.20.55'}
	def setServer(self):
		global server1
		self.groupBox_commandType.setEnabled(True)

		if self.comboBox_chooseServer.currentText()=='Select Server':
			self.checkBox_cat.setEnabled(False)
			self.checkBox_zcat.setEnabled(False)
			self.pushButton_list_TDR_today.setEnabled(False)
			self.pushButton_list_TDR_Before.setEnabled(False)

		for key in serverMapDic:
			if self.comboBox_chooseServer.currentText()==key:
				server1=serverMapDic[key]
		#print (server1)

	def setServer_2(self):
		global server
		for key in serverMapDic:
			if self.comboBox_chooseServer_2.currentText()==key:
				server=serverMapDic[key]
		#print(server)



	def setCommandTypeTail(self):
		global commandtype

		if str(self.checkBox_tail.checkState())=='2':
			commandtype='tail -f /data3/DSC_APP/tdr/'
			self.pushButton_list_TDR_today.setEnabled(True)
			self.checkBox_cat.setChecked(False)
			self.checkBox_zcat.setChecked(False)
			self.checkBox_AddSort.setChecked(False)
			self.checkBox_AddSort.setEnabled(False)
			self.checkBox_AddTitle.setChecked(False)
			self.checkBox_AddTitle.setEnabled(False)
			self.pushButton_list_TDR_Before.setEnabled(False)
		if str(self.checkBox_tail.checkState())=='0':
			self.checkBox_AddSort.setEnabled(True)
			self.checkBox_AddTitle.setEnabled(True)
		if str(self.checkBox_tail.checkState())=='0' and str(self.checkBox_cat.checkState())=='0' and str(self.checkBox_zcat.checkState())=='0':
			commandtype=''
		#print (commandtype)

	def setCommandTypeCat(self):
		global commandtype
		if str(self.checkBox_cat.checkState())=='2':
			commandtype='cat /data3/DSC_APP/tdr/'
			self.pushButton_list_TDR_today.setEnabled(True)
			self.checkBox_zcat.setChecked(False)
			self.checkBox_tail.setChecked(False)
			self.pushButton_list_TDR_Before.setEnabled(False)
		if str(self.checkBox_tail.checkState())=='0' and str(self.checkBox_cat.checkState())=='0' and str(self.checkBox_zcat.checkState())=='0':
			commandtype=''
		#print (commandtype)

	def setCommandTypeZcat(self):
		global commandtype
		if str(self.checkBox_zcat.checkState())=='2':
			commandtype='zcat /data4/TDR/'
			self.pushButton_list_TDR_Before.setEnabled(True)
			self.checkBox_cat.setChecked(False)
			self.checkBox_tail.setChecked(False)
			self.pushButton_list_TDR_today.setEnabled(False)

		if str(self.checkBox_tail.checkState())=='0' and str(self.checkBox_cat.checkState())=='0' and str(self.checkBox_zcat.checkState())=='0':
			commandtype=''
		#print (commandtype)

	def printOOP(self):
		xxx=self.comboBox_show_OP.lineEdit().text()
		self.comboBox_show_OP.removeItem(0)
		abc=self.comboBox_show_OP.count()
		while abc>0 :
			self.comboBox_show_OP.removeItem(0)
			abc=abc-1
		inputrealm2OP=open(r'.\file\OPname.txt')
		fa = inputrealm2OP.readlines()
		
		for item in fa:
			if re.search(xxx, item.lstrip().strip('\n'), re.IGNORECASE)!=None:
				self.comboBox_show_OP.addItem(item.lstrip().strip('\n'))
		self.build_filter()


	def printDOP(self):
		xxx=self.comboBox_show_OP_2.lineEdit().text()
		self.comboBox_show_OP_2.removeItem(0)
		abc=self.comboBox_show_OP_2.count()
		while abc>0 :
			self.comboBox_show_OP_2.removeItem(0)
			abc=abc-1
		inputrealm2OP=open(r'.\file\OPname.txt')
		fa = inputrealm2OP.readlines()
		
		for item in fa:
			if re.search(xxx, item.lstrip().strip('\n'), re.IGNORECASE)!=None:
				self.comboBox_show_OP_2.addItem(item.lstrip().strip('\n'))
		self.build_filter()

	def showOOP(self):
		self.comboBox_show_OP.currentText()
	def showDOP(self):
		self.comboBox_show_OP_2.currentText()

	def listtdoayTDR(self):
		global server1
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=server1, port=22, username=user, password=pwd)
		stdin, stdout, stderr = ssh.exec_command('hostname;cd /data3/DSC_APP/tdr/; ls -ltr')
		res,err = stdout.read(),stderr.read()
		result = res if res else err
		dirresult=result.decode().rstrip().lstrip()
		self.plainTextEdit_SSHoutput.setPlainText(dirresult)
	def listbeforeTDR(self):
		global server1
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=server1, port=22, username=user, password=pwd)
		stdin, stdout, stderr = ssh.exec_command('hostname;cd /data4/TDR/; ls -ltr')
		res,err = stdout.read(),stderr.read()
		result = res if res else err
		dirresult=result.decode().rstrip().lstrip()
		#print(type(dirresult))
		self.plainTextEdit_SSHoutput.setPlainText(dirresult)

	def sendtext(self):
		rawTDR=self.plainTextEdit_TDR.toPlainText().replace('\n','').rstrip().lstrip()
		self.sendtdr.emit(rawTDR)
	def formcommand(self):
		global finalcommand,filename
		servername=self.comboBox_chooseServer_2.currentText()
		if servername=='Select Server':
			print ('Please select one server first.')
			QMessageBox.warning(self,"Warning","Please select one server first.",QMessageBox.Ok)
			return
		if commandtype =='':
			print ('Please select command type first.')
			QMessageBox.warning(self,"Warning","Please select command type first.",QMessageBox.Ok)
			return
		if filename=='':
			print ('Please tpye TDR file name first.')
			QMessageBox.warning(self,"Warning","Please tpye TDR file name first.",QMessageBox.Ok)
			return
			
		if 'zcat' in commandtype:
			str_list=list(filename)
			str_list=str_list[-13:]
			
			filename="".join(str_list)
			filename='*'+filename
		if str(self.checkBox_AddFilter.checkState())=='2':
			if str(self.checkBox_grep1.checkState())=='2':
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'+ '| grep -a "'+self.lineEdit_grep2.text()+'"'+self.textEdit_test.toPlainText()
				else:
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'+self.textEdit_test.toPlainText()
			else:
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep2.text()+'"'+self.textEdit_test.toPlainText()
				else:
					finalcommand=commandtype+filename+self.textEdit_test.toPlainText()
		else:
			if str(self.checkBox_grep1.checkState())=='2':
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'+ '| grep -a "'+self.lineEdit_grep2.text()+'"'
				else:
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep1.text()+'"'
			else:
				if str(self.checkBox_grep2.checkState())=='2':
					finalcommand=commandtype+filename+'| grep -a "'+self.lineEdit_grep2.text()+'"'
				else:
					finalcommand=commandtype+filename
		self.sendcommandtext.emit(finalcommand,servername)
		

		
class showTDRWindow(QMainWindow, Ui_Show_TDR):
	
	def __init__(self, parent=None):
		super (showTDRWindow, self).__init__(parent)
		self.setupUi(self)
		
	def showTDRcontent (self, catchrawTDR):
		arrTDR=catchrawTDR.split(' ')
		if len(arrTDR)<60:
			print ('Incomplete TDR content.')
			QMessageBox.warning(self,"Warning","Incomplete TDR content.",QMessageBox.Ok)
			return
		if len(arrTDR)>60:
			print ('Please input Single TDR content.')
			QMessageBox.warning(self,"Warning","Please input Single TDR content.",QMessageBox.Ok)
			return
		slot1.show()
		self.lineEdit_1_log_date.setText(arrTDR[0])
		self.lineEdit_2_log_time.setText(arrTDR[1])
		self.lineEdit_3_start_date.setText(arrTDR[2])
		self.lineEdit_4_start_time.setText(arrTDR[3])
		self.lineEdit_5_request_fwd_date.setText(arrTDR[4])
		self.lineEdit_6_rquest_fwd_time.setText(arrTDR[5])
		self.lineEdit_7_request_dequeue_date.setText(arrTDR[6])
		self.lineEdit_8_request_dequeue_time.setText(arrTDR[7])
		self.lineEdit_9_request_send_date.setText(arrTDR[8])
		self.lineEdit_10_request_send_time.setText(arrTDR[9])
		self.lineEdit_11_answer_rcv_date.setText(arrTDR[10])
		self.lineEdit_12_answer_rcv_time.setText(arrTDR[11])
		self.lineEdit_13_answer_dequeue_date.setText(arrTDR[12])
		self.lineEdit_14_answer_dequeue_time.setText(arrTDR[13])
		self.lineEdit_15_answer_send_date.setText(arrTDR[14])
		self.lineEdit_16_answer_send_Time.setText(arrTDR[15])
		self.lineEdit_17_sender_prot.setText(arrTDR[16])
		self.lineEdit_18_sender_host.setText(arrTDR[17])
		self.lineEdit_19_sender_realm.setText(arrTDR[18])
		self.lineEdit_20_request_source_edge_proxy_IP.setText(arrTDR[19])
		self.lineEdit_21_request_dest_edge_proxy_IP.setText(arrTDR[20])
		self.lineEdit_22_resent.setText(arrTDR[21])
		self.lineEdit_23_session_id.setText(arrTDR[22])
		self.lineEdit_24_appl_id.setText(arrTDR[23])
		self.lineEdit_25_cmd_code.setText(arrTDR[24])
		self.lineEdit_26_origin_host.setText(arrTDR[25])
		self.lineEdit_27_origin_realm.setText(arrTDR[26])
		self.lineEdit_28_origin_Operator.setText(arrTDR[27])
		self.lineEdit_29_dest_host.setText(arrTDR[28])
		self.lineEdit_30_dest_realm.setText(arrTDR[29])
		self.lineEdit_31_dest_operator.setText(arrTDR[30])
		self.lineEdit_32_req_flag.setText(arrTDR[31])
		self.lineEdit_33_req_ete_id.setText(arrTDR[32])
		self.lineEdit_34_req_hbh_id.setText(arrTDR[33])
		self.lineEdit_35_req_payload.setText(arrTDR[34])
		self.lineEdit_36_imsi.setText(arrTDR[35])
		self.lineEdit_37_msisdn.setText(arrTDR[36])
		self.lineEdit_38_vplmn_id.setText(arrTDR[37])
		self.lineEdit_39_req_rules_hit.setText(arrTDR[38])
		self.lineEdit_40_local_action.setText(arrTDR[39])
		self.lineEdit_41_fw_ete_id.setText(arrTDR[40])
		self.lineEdit_42_fw_hbh_id.setText(arrTDR[41])
		self.lineEdit_43_receiver_prot.setText(arrTDR[42])
		self.lineEdit_44_reroute.setText(arrTDR[43])
		self.lineEdit_45_first_attempt_receiver_host.setText(arrTDR[44])
		self.lineEdit_46_actual_receiver_host.setText(arrTDR[45])
		self.lineEdit_47_fw_req_payload.setText(arrTDR[46])
		self.lineEdit_48_ans_origin_host.setText(arrTDR[47])
		self.lineEdit_49_ans_origin_realm.setText(arrTDR[48])
		self.lineEdit_50_ans_flag.setText(arrTDR[49])
		self.lineEdit_51_ans_payload.setText(arrTDR[50])
		self.lineEdit_52_ans_rules_hit.setText(arrTDR[51])
		self.lineEdit_53_ans_result_code.setText(arrTDR[52])
		self.lineEdit_54_ans_experiment_result_code.setText(arrTDR[53])
		self.lineEdit_55_fw_ans_payload.setText(arrTDR[54])
		self.lineEdit_56_fw_ans_rst_code.setText(arrTDR[55])
		self.lineEdit_57_fw_ans_exp_rst_code.setText(arrTDR[56])
		self.lineEdit_58_fw_ans_err_msg.setText(arrTDR[57])
		self.lineEdit_59_reason.setText(arrTDR[58])
		self.lineEdit_60_reason_id.setText(arrTDR[59])


class showCommandWindow(QMainWindow, Ui_Show_Command):
	sendsignal=pyqtSignal(str)
	global result1
	result1=''
	def __init__(self, parent=None):
		super (showCommandWindow, self).__init__(parent)
		self.setupUi(self)
		
		self.pushButton_SendCommand.clicked.connect(self.sendcommand)
		self.pushButton_Close.clicked.connect(self.showcommandclose)
		self.pushButton_ClearOutput.clicked.connect(self.clearoutput)
		self.pushButton_StopCommand.clicked.connect(self.quit1)
		self.pushButton_CopyOutput.clicked.connect(self.copyOutput)
		
		self.sendsignal.connect(self.changestatus)

	def copyOutput(self):
		outputall=self.textEdit_SSHoutput.toPlainText()
		pyperclip.copy(outputall)

	def closeEvent(self, event):
		self.quit1()
		event.accept()

	def clearoutput(self):
		self.textEdit_SSHoutput.setPlainText('')
		self.label_status.setText('Status: Not Started.')
	
	def changestatus(self,catchresult):

		if 'tail -f' in self.textEdit_command.toPlainText():
			c=catchresult.split(r'\n')
			cc=[]
			for i in c:
				cc.append(i.lstrip())
			ccc='\n\n\n'.join(cc)
			ccc=ccc.replace("b'",'').replace("'",'')
			self.textEdit_SSHoutput.append(ccc)
		else:
			self.textEdit_SSHoutput.setPlainText(catchresult)
			self.label_status.setText('Status: Complete!')
		
	def quit1(self):
		global is_sigint_up,ssh,channel,result1
		if 'tail -f' in self.textEdit_command.toPlainText():
			is_sigint_up = True
			self.label_status.setText('Status: Not Started.')
			try:
				ssh.exec_command('killall -u '+user)
				ssh.close()
			except Exception as e:
				print('')
			return
		else:
			#print('You choose to stop command')
			self.label_status.setText('Status: Not Started.')
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=server, port=22, username=user, password=pwd)
			try:
				ssh.exec_command('killall -u '+user)
			except Exception as e:
				print('')
		
	def SSHcommand(self):
		global ssh,channel,result1,is_sigint_up
		is_sigint_up = False
		if 'tail -f' in self.textEdit_command.toPlainText():
			
			result1=''
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=server,port=22,username=user, password=pwd)
			transport=ssh.get_transport()
			channel = transport.open_session()
			com=self.textEdit_command.toPlainText()
			channel.exec_command(com)
			while True:
				data_total=[]
				try:
					data=str(channel.recv(20480))
					if not data: break
					data_total.append(data)
					cc=''.join(data_total)
					#print(cc)
					self.sendsignal.emit(cc)
					if is_sigint_up:
						#print('You choose to stop tail command')
						#result1=''
						break
				except Exception as e:
					print('')

		else:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=server, port=22, username=user, password=pwd)
			com=self.textEdit_command.toPlainText()
			stdin, stdout, stderr = ssh.exec_command(com)
			res,err = stdout.read(),stderr.read()
			result = res if res else err
			dirresult=result.decode().rstrip().lstrip()
			self.sendsignal.emit(dirresult)

	def sendcommand(self):
		self.label_status.setText('Status: In Progress...')
		
		t= threading.Thread(target=self.SSHcommand)
		t.setDaemon(True)
		t.start()

	
	def showcommandclose(self):
		self.close()
		
	def showcommand (self, catchcommand,server):
		self.clearoutput()
		command=catchcommand
		self.label_server.setText(server)
		slot2.show()
		self.textEdit_command.setText(command)
		
		
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		
		palette1 = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		
		self.label_server.setFont(font)
		self.label_server.setPalette(palette)
		if "zcat" in command:
			self.label_caution.setText('Caution: zcat command might cost more than 15 min.')
		else:
			self.label_caution.setText('')
		self.label_status.setText('Status: Not Started.')
		self.label_status.setFont(font)
		self.label_status.setPalette(palette1)


class showResultWindowAP(QMainWindow, Ui_Show_Result_APEU):
	sendvar=pyqtSignal(list)
	sendstr=pyqtSignal(str)
	def __init__(self, parent=None):
		super (showResultWindowAP, self).__init__(parent)
		self.setupUi(self)
		self.pushButton_SendCommand.clicked.connect(self.sendcommand)
		self.pushButton_Close.clicked.connect(self.showcommandclose)
		self.pushButton_ClearOutput.clicked.connect(self.clearoutput)
		self.pushButton_CopyOutput.clicked.connect(self.copyOutput)
		self.pushButton_StopCommand.clicked.connect(self.quit1)
		
		self.sendvar.connect(self.putresult)
		self.sendstr.connect(self.putresult)
		self.setWindowTitle('AP DSC')
		self.groupBox_DSC1.setTitle('HKG DSC')
		self.groupBox_DSC2.setTitle('SNG DSC')
	
		global user,pwd
		userinfodirectory=os.getcwd()+r'\file\userinfo.txt'
		input=open(userinfodirectory)
		info=input.read().split(' ')
		user= info[0]
		pwd=info[1]
		input.close()
	
	def copyOutput(self):
		outputall=''
		outputwindowlist=[self.textEdit_Server1,self.textEdit_Server3,self.textEdit_Server5,self.textEdit_Server2,self.textEdit_Server4,self.textEdit_Server6]
		
		for i in outputwindowlist:
			outputall=outputall+i.toPlainText()+'\n\n\n'
		pyperclip.copy(outputall)
	
	def closeEvent(self, event):
		self.quit1()
		event.accept()
	
	def clearoutput(self):
		self.textEdit_Server1.setPlainText('')
		self.textEdit_Server2.setPlainText('')
		self.textEdit_Server3.setPlainText('')
		self.textEdit_Server4.setPlainText('')
		self.textEdit_Server5.setPlainText('')
		self.textEdit_Server6.setPlainText('')
		self.label_status.setText('Status: Not Started.')
		
	def quit1(self):
		global is_sigint_up
		if 'tail -f' in self.textEdit_command.toPlainText():
			is_sigint_up = True
			self.label_status.setText('Status: Not Started.')
			serverlist=['10.162.28.182','10.162.28.183','10.162.28.184','10.163.28.126','10.163.28.127','10.163.28.128']
			for i in serverlist:
				time.sleep(0.2)
				t= threading.Thread(target=self.stopmultiserver,args=(i,))
				t.start()
			return
		else:
			serverlist=['10.162.28.182','10.162.28.183','10.162.28.184','10.163.28.126','10.163.28.127','10.163.28.128']
			for i in serverlist:
				time.sleep(0.2)
				t= threading.Thread(target=self.stopmultiserver,args=(i,))
				t.start()
	def stopmultiserver(self,n):
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n, port=22, username=user, password=pwd)
			ssh.exec_command('killall -u '+user)

	def processResult(self,c):
		c=c.split(r'\n')
		cc=[]
		for i in c:
			cc.append(i.lstrip())
		ccc='\n\n\n'.join(cc)
		return(ccc)

	def putresult(self, catchvar):
		if 'tail -f' in self.textEdit_command.toPlainText():
			if '10.162.28.182' in catchvar:
				catchvar=catchvar.replace("10.162.28.182b'",'').replace("'",'')
				self.textEdit_Server1.append(self.processResult(catchvar))
			if '10.162.28.183' in catchvar:
				catchvar=catchvar.replace("10.162.28.183b'",'').replace("'",'')
				self.textEdit_Server3.append(self.processResult(catchvar))
			if '10.162.28.184' in catchvar:
				catchvar=catchvar.replace("10.162.28.184b'",'').replace("'",'')
				self.textEdit_Server5.append(self.processResult(catchvar))
			if '10.163.28.126' in catchvar:
				catchvar=catchvar.replace("10.163.28.126b'",'').replace("'",'')
				self.textEdit_Server2.append(self.processResult(catchvar))
			if '10.163.28.127' in catchvar:
				catchvar=catchvar.replace("10.163.28.127b'",'').replace("'",'')
				self.textEdit_Server4.append(self.processResult(catchvar))
			if '10.163.28.128' in catchvar:
				catchvar=catchvar.replace("10.163.28.128b'",'').replace("'",'')
				self.textEdit_Server6.append(self.processResult(catchvar))
					
		else:

			for i in catchvar:
				if "hk1p-gen-dsc-app001" in i:
					self.textEdit_Server1.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">hk1p-gen-dsc-app001</span></p></body></html>")
					self.textEdit_Server1.append(i.replace('hk1p-gen-dsc-app001\n',''))
				if "hk1p-gen-dsc-app002" in i:
					self.textEdit_Server3.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">hk1p-gen-dsc-app002</span></p></body></html>")
					self.textEdit_Server3.append(i.replace('hk1p-gen-dsc-app002\n',''))
				if "hk1p-gen-dsc-app003" in i:
					self.textEdit_Server5.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">hk1p-gen-dsc-app003</span></p></body></html>")
					self.textEdit_Server5.append(i.replace('hk1p-gen-dsc-app003\n',''))
				if "sg1p-gen-dsc-app001" in i:
					self.textEdit_Server2.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">sg1p-gen-dsc-app001</span></p></body></html>")
					self.textEdit_Server2.append(i.replace('sg1p-gen-dsc-app001\n',''))
				if "sg1p-gen-dsc-app002" in i:
					self.textEdit_Server4.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">sg1p-gen-dsc-app002</span></p></body></html>")
					self.textEdit_Server4.append(i.replace('sg1p-gen-dsc-app002\n',''))
				if "sg1p-gen-dsc-app003" in i:
					self.textEdit_Server6.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">sg1p-gen-dsc-app003</span></p></body></html>")
					self.textEdit_Server6.append(i.replace('sg1p-gen-dsc-app003\n',''))
			self.label_status.setText('Status: Complete!')


	def sendmultiserver(self,n):
		global user,pwd,varAP,is_sigint_up

		if 'tail -f' in self.textEdit_command.toPlainText():
			is_sigint_up = False
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n,port=22,username=user, password=pwd)
			transport=ssh.get_transport()
			channel = transport.open_session()
			com='hostname;'+self.textEdit_command.toPlainText()
			channel.exec_command(com)
			while True:
				data_total=[]
				try:
					data=n+str(channel.recv(20480))
					if not data: break
					data_total.append(data)
					cc=''.join(data_total)
					#print(cc)
					self.sendstr.emit(cc)
					if is_sigint_up:
						#print('You choose to stop tail command')
						try:
							channel.exec_command('exit')
							channel.close()
							ssh.close()
						except Exception as e:
							print ('')
						break
				except Exception as e:
					print('')
		else:
			is_sigint_up = False
			ssh1 = paramiko.SSHClient()
			ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh1.connect(hostname=n, port=22, username=user, password=pwd)

			com='hostname;'+self.textEdit_command.toPlainText()
			stdin, stdout, stderr = ssh1.exec_command(com)

			while True:
				if is_sigint_up:
					#print('You choose to stop command')
					ssh1.exec_command('exit')
					ssh1.close()
					break
				res,err = stdout.read(),stderr.read()
				
				result = res if res else err
				dirresult=result.decode().rstrip().lstrip()
				varAP.append(dirresult)
				break
			if len(varAP)==6:
				self.sendvar.emit(varAP)
					

	def sendcommand(self):
		global varAP
		varAP=[]
		serverlist=['10.162.28.182','10.162.28.183','10.162.28.184','10.163.28.126','10.163.28.127','10.163.28.128']

		for i in serverlist:
			if 'tail -f' in self.textEdit_command.toPlainText():
				time.sleep(0.2)
			t= threading.Thread(target=self.sendmultiserver,args=(i,))
			t.start()
		self.label_status.setText('Status: In Progress...')

	def showcommandclose(self):
		self.close()
	
	def showResultCatchCommand(self, catchcommand):
		self.clearoutput()
		command=catchcommand
		self.label_server.setText('AP DSCs')
		slot3.show()
		self.textEdit_command.setText(command)
		
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		
		palette1 = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		
		self.label_server.setFont(font)
		self.label_server.setPalette(palette)
		
		if "zcat" in command:
			self.label_caution.setText('Caution: zcat command might cost more than 15 min.')
			#self.pushButton_StopCommand.setEnabled(False)
			
		else:
			self.label_caution.setText('')
			#self.pushButton_StopCommand.setEnabled(True)
		self.label_status.setText('Status: Not Started.')
		self.label_status.setFont(font)
		self.label_status.setPalette(palette1)

class showResultWindowEU(QMainWindow, Ui_Show_Result_APEU):
	sendvar=pyqtSignal(list)
	sendstr=pyqtSignal(str)
	def __init__(self, parent=None):
		super (showResultWindowEU, self).__init__(parent)
		self.setupUi(self)
		self.pushButton_SendCommand.clicked.connect(self.sendcommand)
		self.pushButton_Close.clicked.connect(self.showcommandclose)
		self.pushButton_ClearOutput.clicked.connect(self.clearoutput)
		self.pushButton_CopyOutput.clicked.connect(self.copyOutput)
		self.pushButton_StopCommand.clicked.connect(self.quit1)
		
		self.sendvar.connect(self.putresult)
		self.sendstr.connect(self.putresult)
		self.setWindowTitle('EU DSC')
		self.groupBox_DSC1.setTitle('AMS DSC')
		self.groupBox_DSC2.setTitle('FRT DSC')
		global user,pwd
		userinfodirectory=os.getcwd()+r'\file\userinfo.txt'
		input=open(userinfodirectory)
		info=input.read().split(' ')
		user= info[0]
		pwd=info[1]
		input.close()

	def closeEvent(self, event):
		self.quit1()
		event.accept()

	def quit1(self):
		global is_sigint_up
		if 'tail -f' in self.textEdit_command.toPlainText():
			is_sigint_up = True
			self.label_status.setText('Status: Not Started.')
			serverlist=['10.161.28.36','10.161.28.37','10.161.28.248','10.160.28.36','10.160.28.37','10.160.28.217']
			for i in serverlist:
				time.sleep(0.2)
				t= threading.Thread(target=self.stopmultiserver,args=(i,))
				t.start()
			return
		else:
			serverlist=['10.161.28.36','10.161.28.37','10.161.28.248','10.160.28.36','10.160.28.37','10.160.28.217']
			for i in serverlist:
				time.sleep(0.2)
				t= threading.Thread(target=self.stopmultiserver,args=(i,))
				t.start()
	def stopmultiserver(self,n):
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n, port=22, username=user, password=pwd)
			ssh.exec_command('killall -u '+user)
			
	def copyOutput(self):
		outputall=''
		outputwindowlist=[self.textEdit_Server1,self.textEdit_Server3,self.textEdit_Server5,self.textEdit_Server2,self.textEdit_Server4,self.textEdit_Server6]
		
		for i in outputwindowlist:
			outputall=outputall+i.toPlainText()+'\n\n\n'
		pyperclip.copy(outputall)
		
	def clearoutput(self):
		self.textEdit_Server1.setPlainText('')
		self.textEdit_Server2.setPlainText('')
		self.textEdit_Server3.setPlainText('')
		self.textEdit_Server4.setPlainText('')
		self.textEdit_Server5.setPlainText('')
		self.textEdit_Server6.setPlainText('')
		self.label_status.setText('Status: Not Started.')

	def processResult(self,c):
		c=c.split(r'\n')
		cc=[]
		for i in c:
			cc.append(i.lstrip())
		ccc='\n\n\n'.join(cc)
		return(ccc)

	def putresult(self, catchvar):
		
		if 'tail -f' in self.textEdit_command.toPlainText():
			if '10.160.28.36' in catchvar:
				catchvar=catchvar.replace("10.160.28.36b'",'').replace("'",'')
				self.textEdit_Server1.append(self.processResult(catchvar))
			if '10.160.28.37' in catchvar:
				catchvar=catchvar.replace("10.160.28.37b'",'').replace("'",'')
				self.textEdit_Server3.append(self.processResult(catchvar))
			if '10.160.28.217' in catchvar:
				catchvar=catchvar.replace("10.160.28.217b'",'').replace("'",'')
				self.textEdit_Server5.append(self.processResult(catchvar))
			if '10.161.28.36' in catchvar:
				catchvar=catchvar.replace("10.161.28.36b'",'').replace("'",'')
				self.textEdit_Server2.append(self.processResult(catchvar))
			if '10.161.28.37' in catchvar:
				catchvar=catchvar.replace("10.161.28.37b'",'').replace("'",'')
				self.textEdit_Server4.append(self.processResult(catchvar))
			if '10.161.28.248' in catchvar:
				catchvar=catchvar.replace("10.161.28.248b'",'').replace("'",'')
				self.textEdit_Server6.append(self.processResult(catchvar))
					
		else:
			for i in catchvar:
				if "am1p-gen-dsc-app001" in i:
					self.textEdit_Server1.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">am1p-gen-dsc-app001</span></p></body></html>")
					self.textEdit_Server1.append(i.replace('am1p-gen-dsc-app001\n',''))
				if "am1p-gen-dsc-app002" in i:
					self.textEdit_Server3.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">am1p-gen-dsc-app002</span></p></body></html>")
					self.textEdit_Server3.append(i.replace('am1p-gen-dsc-app002\n',''))
				if "am1p-gen-dsc-app003" in i:
					self.textEdit_Server5.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">am1p-gen-dsc-app003</span></p></body></html>")
					self.textEdit_Server5.append(i.replace('am1p-gen-dsc-app003\n',''))
				if "fr4p-gen-dsc-app001" in i:
					self.textEdit_Server2.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">fr4p-gen-dsc-app001</span></p></body></html>")
					self.textEdit_Server2.append(i.replace('fr4p-gen-dsc-app001\n',''))
				if "fr4p-gen-dsc-app002" in i:
					self.textEdit_Server4.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">fr4p-gen-dsc-app002</span></p></body></html>")
					self.textEdit_Server4.append(i.replace('fr4p-gen-dsc-app002\n',''))
				if "fr4p-gen-dsc-app003" in i:
					self.textEdit_Server6.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">fr4p-gen-dsc-app003</span></p></body></html>")
					self.textEdit_Server6.append(i.replace('fr4p-gen-dsc-app003\n',''))
			self.label_status.setText('Status: Complete!')

	def sendmultiserver(self,n):
		global user,pwd,varEU,is_sigint_up
		
		if 'tail -f' in self.textEdit_command.toPlainText():
			is_sigint_up = False
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n,port=22,username=user, password=pwd)
			transport=ssh.get_transport()
			channel = transport.open_session()
			com='hostname;'+self.textEdit_command.toPlainText()
			channel.exec_command(com)
			while True:
				data_total=[]
				try:
					data=n+str(channel.recv(20480))
					if not data: break
					data_total.append(data)
					cc=''.join(data_total)
					#print(cc)
					self.sendstr.emit(cc)
					if is_sigint_up:
						#print('You choose to stop tail command')
						try:
							channel.exec_command('exit')
							channel.close()
							ssh.close()
						except Exception as e:
							print ('')
						break
				except Exception as e:
					print('')
		else:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n, port=22, username=user, password=pwd)
	
			com='hostname;'+self.textEdit_command.toPlainText()
			stdin, stdout, stderr = ssh.exec_command(com)
			res,err = stdout.read(),stderr.read()
			result = res if res else err
			dirresult=result.decode().rstrip().lstrip()
			varEU.append(dirresult)
			if len(varEU)==6:
				self.sendvar.emit(varEU)

	def sendcommand(self):
		global varEU
		varEU=[]
		serverlist=['10.161.28.36','10.161.28.37','10.161.28.248','10.160.28.36','10.160.28.37','10.160.28.217']
		for i in serverlist:
			if 'tail -f' in self.textEdit_command.toPlainText():
				time.sleep(0.2)
			t= threading.Thread(target=self.sendmultiserver,args=(i,))
			t.start()
		self.label_status.setText('Status: In Progress...')

	def showcommandclose(self):
		self.close()
	
	def showResultCatchCommand(self, catchcommand):
		self.clearoutput()
		command=catchcommand
		self.label_server.setText('EU DSCs')
		slot4.show()
		self.textEdit_command.setText(command)
		
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		
		
		palette1 = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		
		self.label_server.setFont(font)
		self.label_server.setPalette(palette)
		if "zcat" in command:
			self.label_caution.setText('Caution: zcat command might cost more than 15 min.')

		else:
			self.label_caution.setText('')

		self.label_status.setText('Status: Not Started.')
		self.label_status.setFont(font)
		self.label_status.setPalette(palette1)

class showResultWindowNA(QMainWindow, Ui_Show_Result_NA):
	sendvar=pyqtSignal(list)
	sendstr=pyqtSignal(str)
	def __init__(self, parent=None):
		super (showResultWindowNA, self).__init__(parent)
		self.setupUi(self)
		self.pushButton_SendCommand.clicked.connect(self.sendcommand)
		self.pushButton_Close.clicked.connect(self.showcommandclose)
		self.pushButton_ClearOutput.clicked.connect(self.clearoutput)
		self.pushButton_CopyOutput.clicked.connect(self.copyOutput)
		self.pushButton_StopCommand.clicked.connect(self.quit1)
		
		self.sendvar.connect(self.putresult)
		self.sendstr.connect(self.putresult)
		
		global user,pwd
		userinfodirectory=os.getcwd()+r'\file\userinfo.txt'
		input=open(userinfodirectory)
		info=input.read().split(' ')
		user= info[0]
		pwd=info[1]
		input.close()

	def closeEvent(self, event):
		self.quit1()
		event.accept()

	def quit1(self):
		global is_sigint_up
		if 'tail -f' in self.textEdit_command.toPlainText():
			is_sigint_up = True
			self.label_status.setText('Status: Not Started.')
			serverlist=['10.164.28.175','10.164.28.176','10.164.28.253','10.164.20.49','10.164.20.50','10.166.28.189','10.166.28.190','10.166.29.2','10.166.20.54','10.166.20.55']
			for i in serverlist:
				time.sleep(0.2)
				t= threading.Thread(target=self.stopmultiserver,args=(i,))
				t.start()
			return
		else:
			serverlist=['10.164.28.175','10.164.28.176','10.164.28.253','10.164.20.49','10.164.20.50','10.166.28.189','10.166.28.190','10.166.29.2','10.166.20.54','10.166.20.55']
			for i in serverlist:
				time.sleep(0.2)
				t= threading.Thread(target=self.stopmultiserver,args=(i,))
				t.start()
	def stopmultiserver(self,n):
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n, port=22, username=user, password=pwd)
			ssh.exec_command('killall -u '+user)
			
			
	def copyOutput(self):
		outputall=''
		outputwindowlist=[self.textEdit_Server1,self.textEdit_Server3,self.textEdit_Server5,self.textEdit_Server7,self.textEdit_Server9,self.textEdit_Server2,self.textEdit_Server4,self.textEdit_Server6,self.textEdit_Server8,self.textEdit_Server10]
		
		for i in outputwindowlist:
			outputall=outputall+i.toPlainText()+'\n\n\n'
		pyperclip.copy(outputall)
		
	def clearoutput(self):
		self.textEdit_Server1.setPlainText('')
		self.textEdit_Server2.setPlainText('')
		self.textEdit_Server3.setPlainText('')
		self.textEdit_Server4.setPlainText('')
		self.textEdit_Server5.setPlainText('')
		self.textEdit_Server6.setPlainText('')
		self.textEdit_Server7.setPlainText('')
		self.textEdit_Server8.setPlainText('')
		self.textEdit_Server9.setPlainText('')
		self.textEdit_Server10.setPlainText('')
		self.label_status.setText('Status: Not Started.')

	def processResult(self,c):
		c=c.split(r'\n')
		cc=[]
		for i in c:
			cc.append(i.lstrip())
		ccc='\n\n\n'.join(cc)
		return(ccc)

	def putresult(self, catchvar):
		
		if 'tail -f' in self.textEdit_command.toPlainText():
			if '10.166.28.189' in catchvar:
				catchvar=catchvar.replace("10.166.28.189b'",'').replace("'",'')
				self.textEdit_Server1.append(self.processResult(catchvar))
			if '10.166.28.190' in catchvar:
				catchvar=catchvar.replace("10.166.28.190b'",'').replace("'",'')
				self.textEdit_Server3.append(self.processResult(catchvar))
			if '10.166.29.2' in catchvar:
				catchvar=catchvar.replace("10.166.29.2b'",'').replace("'",'')
				self.textEdit_Server5.append(self.processResult(catchvar))
			if '10.166.20.54' in catchvar:
				catchvar=catchvar.replace("10.166.20.54b'",'').replace("'",'')
				self.textEdit_Server7.append(self.processResult(catchvar))
			if '10.166.20.55' in catchvar:
				catchvar=catchvar.replace("10.166.20.55b'",'').replace("'",'')
				self.textEdit_Server9.append(self.processResult(catchvar))
			if '10.164.28.175' in catchvar:
				catchvar=catchvar.replace("10.164.28.175b'",'').replace("'",'')
				self.textEdit_Server2.append(self.processResult(catchvar))
			if '10.164.28.176' in catchvar:
				catchvar=catchvar.replace("10.164.28.176b'",'').replace("'",'')
				self.textEdit_Server4.append(self.processResult(catchvar))
			if '10.164.28.253' in catchvar:
				catchvar=catchvar.replace("10.164.28.253b'",'').replace("'",'')
				self.textEdit_Server6.append(self.processResult(catchvar))
			if '10.164.20.49' in catchvar:
				catchvar=catchvar.replace("10.164.20.49b'",'').replace("'",'')
				self.textEdit_Server8.append(self.processResult(catchvar))
			if '10.164.20.50' in catchvar:
				catchvar=catchvar.replace("10.164.20.50b'",'').replace("'",'')
				self.textEdit_Server10.append(self.processResult(catchvar))
		
		else:
			for i in catchvar:
				if "mdw01p-gen-dsc-app001" in i:
					self.textEdit_Server1.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">mdw01p-gen-dsc-app001</span></p></body></html>")
					self.textEdit_Server1.append(i.replace('mdw01p-gen-dsc-app001\n',''))
				if "mdw01p-gen-dsc-app002" in i:
					self.textEdit_Server3.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">mdw01p-gen-dsc-app002</span></p></body></html>")
					self.textEdit_Server3.append(i.replace('mdw01p-gen-dsc-app002\n',''))
				if "mdw01p-gen-dsc-app003" in i:
					self.textEdit_Server5.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">mdw01p-gen-dsc-app003</span></p></body></html>")
					self.textEdit_Server5.append(i.replace('mdw01p-gen-dsc-app003\n',''))
				if "mdw01p-gen-dsc-app004" in i:
					self.textEdit_Server7.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">mdw01p-gen-dsc-app004</span></p></body></html>")
					self.textEdit_Server7.append(i.replace('mdw01p-gen-dsc-app004\n',''))
				if "mdw01p-gen-dsc-app005" in i:
					self.textEdit_Server9.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#0055ff;\">mdw01p-gen-dsc-app005</span></p></body></html>")
					self.textEdit_Server9.append(i.replace('mdw01p-gen-dsc-app005\n',''))
				if "dal01p-gen-dsc-app001" in i:
					self.textEdit_Server2.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">dal01p-gen-dsc-app001</span></p></body></html>")
					self.textEdit_Server2.append(i.replace('dal01p-gen-dsc-app001\n',''))
				if "dal01p-gen-dsc-app002" in i:
					self.textEdit_Server4.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">dal01p-gen-dsc-app002</span></p></body></html>")
					self.textEdit_Server4.append(i.replace('dal01p-gen-dsc-app002\n',''))
				if "dal01p-gen-dsc-app004" in i:
					self.textEdit_Server6.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">dal01p-gen-dsc-app004</span></p></body></html>")
					self.textEdit_Server6.append(i.replace('dal01p-gen-dsc-app004\n',''))
				if "dal01p-gen-dsc-app005" in i:
					self.textEdit_Server8.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">dal01p-gen-dsc-app005</span></p></body></html>")
					self.textEdit_Server8.append(i.replace('dal01p-gen-dsc-app005\n',''))
				if "dal01p-gen-dsc-app006" in i:
					self.textEdit_Server10.setHtml("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#00aa00;\">dal01p-gen-dsc-app006</span></p></body></html>")
					self.textEdit_Server10.append(i.replace('dal01p-gen-dsc-app006\n',''))
			self.label_status.setText('Status: Complete!')

	def sendmultiserver(self,n):
		global user,pwd,varNA,is_sigint_up

		if 'tail -f' in self.textEdit_command.toPlainText():
			is_sigint_up = False
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n,port=22,username=user, password=pwd)
			transport=ssh.get_transport()
			channel = transport.open_session()
			com='hostname;'+self.textEdit_command.toPlainText()
			channel.exec_command(com)
			while True:
				data_total=[]
				try:
					data=n+str(channel.recv(20480))
					if not data: break
					data_total.append(data)
					cc=''.join(data_total)
					#print(cc)
					self.sendstr.emit(cc)
					if is_sigint_up:
						#print('You choose to stop tail command')
						try:
							channel.exec_command('exit')
							channel.close()
							ssh.close()
						except Exception as e:
							print ('')
						break
				except Exception as e:
					print('')

		else:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=n, port=22, username=user, password=pwd)
	
			com='hostname;'+self.textEdit_command.toPlainText()
			stdin, stdout, stderr = ssh.exec_command(com)
			res,err = stdout.read(),stderr.read()
			result = res if res else err
			dirresult=result.decode().rstrip().lstrip()
			varNA.append(dirresult)
			if len(varNA)==10:
				self.sendvar.emit(varNA)

	def sendcommand(self):
		global varNA
		varNA=[]
		serverlist=['10.164.28.175','10.164.28.176','10.164.28.253','10.164.20.49','10.164.20.50','10.166.28.189','10.166.28.190','10.166.29.2','10.166.20.54','10.166.20.55']
		for i in serverlist:
			if 'tail -f' in self.textEdit_command.toPlainText():
				time.sleep(0.2)
			t= threading.Thread(target=self.sendmultiserver,args=(i,))
			t.start()
		self.label_status.setText('Status: In Progress...')

	def showcommandclose(self):
		self.close()
	
	def showResultCatchCommand(self, catchcommand):
		self.clearoutput()
		command=catchcommand
		self.label_server.setText('NA DSCs')
		slot5.show()
		self.textEdit_command.setText(command)
		serverlist=['10.164.28.175','10.164.28.176','10.164.28.253','10.164.20.49','10.164.20.50','10.166.28.189','10.166.28.190','10.166.29.2','10.166.20.54','10.166.20.55']
		
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		
		palette1 = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette1.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		
		self.label_server.setFont(font)
		self.label_server.setPalette(palette)
		if "zcat" in command:
			self.label_caution.setText('Caution: zcat command might cost more than 15 min.')
		else:
			self.label_caution.setText('')
		self.label_status.setText('Status: Not Started.')
		self.label_status.setFont(font)
		self.label_status.setPalette(palette1)
		
if __name__=="__main__":  
	app = QApplication(sys.argv)  
	myWin = inputTDRWindow()  
	myWin.show()  

	slot1=showTDRWindow()
	myWin.sendtdr.connect(slot1.showTDRcontent)
	
	slot2=showCommandWindow()
	myWin.sendcommandtext.connect(slot2.showcommand)

	slot3=showResultWindowAP()
	myWin.sendcommandtextmulti_AP.connect(slot3.showResultCatchCommand)
	
	slot4=showResultWindowEU()
	myWin.sendcommandtextmulti_EU.connect(slot4.showResultCatchCommand)
	
	slot5=showResultWindowNA()
	myWin.sendcommandtextmulti_NA.connect(slot5.showResultCatchCommand)
	
	sys.exit(app.exec_())
