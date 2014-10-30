import os
import glob
import re

import langid

from OfficialInfo import ExtractCSV

dacsv = ExtractCSV('extraction BPM.xlsx')
results = dacsv.startReading( prikey = "C" )
OfficialArray = dacsv.makeArray(results)
# # heads = dacsv.heads
# for a in officialarray:
# 	print officialarray[a]


def utf8ify_s(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    else:
        return str(s)


BlackList = {}
f = open("blacklist.txt","r")
for line in f:
	proline = line.replace("\n","")
	if proline!="":
		BlackList[proline] = 1

def isBanned( string , BL):
	for blackword in BL:
		if blackword.lower() in string.lower(): return True
	return False


def makeAbstract(txt):

	fakeabstract = ""

	experiment = txt.split("\n\n")

	for e in experiment:
		if len(e)>20:
			# excludedline = ""
			p = re.compile( "\d+\.\s" )
			m = p.match( e.strip() )
			if m: xxx = ""
			else:
				finaline = e
				arr = e.split("\n")
				finaline = ""
				for a in arr:
					pp = re.compile( "\d+\.\s" )
					mm = pp.match( a )
					if mm: xxx = ""
					else: finaline+=a

				langmatch = langid.classify(finaline)
				if langmatch[0]!="en": xxx=""
				else:
					ppp = re.compile( "\d+-\d+\s" )
					mmm = ppp.match( finaline )
					if mmm: xxx = ""
					else:
						# more cleaning
						if len(finaline)>400:
							if not isBanned(finaline,BlackList):
								pppp = re.compile( "([A-Z-a-z\u00C0-\u017F])+(,)?[ ]{1,2}([A-Z]){1,2}(\.)?,")
								mmmm = pppp.match( finaline )
								if mmmm: xxx = ""
								else: fakeabstract+=finaline
									# print
									# print " [ ==============================================="
									# # print "identified language\t",langmatch
									# print finaline
									# print "=============================================== ] "
									# print


	fakeabstract = fakeabstract.replace("\n"," ")
	fakeabstract = fakeabstract.replace("\t"," ")
	fakeabstract = fakeabstract.replace("'"," ")
	fakeabstract = fakeabstract.replace('"'," ")
	return fakeabstract


foldername = "TO-USE/"
extension = ".txt"

files = glob.glob(foldername+"*"+extension)


globalcounter = 0
IDict = {}
IDictFail = {}


for i in files:
	filesize = os.stat(i).st_size
	if filesize>2048:
		# print filesize,"\t", i
		rawname = i.replace(foldername,"")
		rawname = rawname.replace(extension,"")
		data = rawname.split("|||")
		metadata = data[0]
		fichier = data[1]

		data = metadata.split("|")
		ID = data[0]
		PI = data[1]
		AG = data[2]



		

		f = open(i,"r")
		thebuffer = ""
		for line in f.readlines():
			thebuffer+=line#.replace("\n","")
		ABS = makeAbstract(thebuffer)

		if not IDict.has_key(ID):
			IDict[ID] = { "ID":ID ,"PI":PI ,"AG1":AG ,"ABS":ABS ,"ACR":"" ,"TI":"" ,"PIfull":"" ,"AG2":"" }
		else:
			IDict[ID]["ABS"]+=(" "+ABS)


		if OfficialArray.has_key(ID):
			IDict[ID]["ACR"] = OfficialArray[ID]["ACR"]
			IDict[ID]["TI"] = OfficialArray[ID]["TI"]
			IDict[ID]["AG2"] = OfficialArray[ID]["AG"]
			IDict[ID]["PIfull"] = OfficialArray[ID]["PI"]




print "total",len(IDict.keys())

print "fail",len(IDictFail.keys())


import csv
c = csv.writer(open("finalregs.csv", "wb"),delimiter='\t')
c.writerow(["ID" , "PI" , "PIfull" , "AG1" , "AG2" , "ACR" ,"TI" , "ABS" ])

for i in IDict:
	reg = IDict[i]
	bpmid = utf8ify_s(i)
	PI = utf8ify_s(reg["PI"])#.decode('latin-1').encode("UTF-8")
	AG1 = utf8ify_s(reg["AG1"])#.decode('latin-1').encode("UTF-8")
	ABS = utf8ify_s(reg["ABS"])#.decode('latin-1').encode("UTF-8")
	ABS = re.sub( '\s+', ' ', ABS ).strip()
	ACR = utf8ify_s(reg["ACR"])#.decode('latin-1').encode("UTF-8")
	TI = utf8ify_s(reg["TI"])#.decode('latin-1').encode("UTF-8")
	PI2 = utf8ify_s(reg["PIfull"])#.decode('latin-1').encode("UTF-8")
	AG2 = utf8ify_s(reg["AG2"])#.decode('latin-1').encode("UTF-8")
	c.writerow( [ bpmid, PI, PI2, AG1, AG2 , ACR, TI, ABS ] )