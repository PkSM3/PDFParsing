import os
import glob
import re

import langid


# == Loading xlsx information in memory ==
from OfficialInfo import ExtractCSV
dacsv = ExtractCSV('extraction BPM.xlsx')
results = dacsv.startReading( prikey = "C" )
OfficialArray = dacsv.makeArray(results)
# == / Loading xlsx information in memory ==

def pr(array):
	import pprint
	pprint.pprint(array)

def utf8ify_s(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    else:
        return str(s)

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

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

def saveCSV(filename , headers , IDict):
	# make more generic pls!
	import csv
	c = csv.writer(open(filename, "wb"),delimiter='\t')
	c.writerow(headers)

	for i in IDict:
		reg = IDict[i]
		bpmid = utf8ify_s(i)
		PI = utf8ify_s(reg["PI"])#.decode('latin-1').encode("UTF-8")
		AG1 = utf8ify_s(reg["AG1"])#.decode('latin-1').encode("UTF-8")

		ABS = utf8ify_s(reg["ABS"])#.decode('latin-1').encode("UTF-8")
		ABS = re.sub( '\s+', ' ', ABS ).strip()

		ACR = utf8ify_s(reg["ACR"])#.decode('latin-1').encode("UTF-8")
		TI = utf8ify_s(reg["TI"])#.decode('latin-1').encode("UTF-8")
		AG2 = utf8ify_s(reg["AG2"])#.decode('latin-1').encode("UTF-8")
		c.writerow( [ bpmid, PI, AG1, AG2 , ACR, TI, ABS ] )

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# == Loading the blacklist in memory ==
BlackList = {}
f = open("blacklist.txt","r")
for line in f:
	proline = line.replace("\n","")
	if proline!="":
		BlackList[proline] = 1
# == / Loading the blacklist in memory ==

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
			IDict[ID] = { "ID":ID ,"PIfolder":PI ,"AG1":AG ,"ABS":ABS ,"ACR":"" ,"TI":"" ,"PIxls":"" ,"AG2":"" }
		else:
			IDict[ID]["ABS"]+=(" "+ABS)


		if OfficialArray.has_key(ID) and ID!="BPM2697" and ID!="BPM2768" and ID!="BPM2613" and ID!="BPM2596":
			IDict[ID]["ACR"] = OfficialArray[ID]["ACR"]
			IDict[ID]["TI"] = OfficialArray[ID]["TI"]
			IDict[ID]["AG2"] = OfficialArray[ID]["AG"]
			IDict[ID]["PIxls"] = OfficialArray[ID]["PI"]

	
print ( "total",len(IDict.keys()) )

print ( "fail",len(IDictFail.keys()) )




# === filter01: searching for similarities between authors ==
pinames = {}
for i in IDict:
	piname = IDict[i]["PIfolder"].lower().replace(". "," ").replace("."," ").replace("-"," ")
	# piname = piname.split(' ', 1)[1]
	if not pinames.has_key(piname):
		# pinames[piname] = {}
		# pinames[piname]["c"] = 1
		pinames[piname] = [i]
	else:
		# pinames[piname]["c"]+=1
		pinames[piname].append(i)
# === / filter01: searching for similarities between authors ==


# === filter02: searching for similarities between authors-names ==
import networkx as nx
G = nx.Graph()
for i in pinames:
	fullname_i = i.split(' ', 1)
	n_i = fullname_i[0]
	ln_i = fullname_i[1]
	for j in pinames:
		fullname_j = j.split(' ', 1)
		n_j = fullname_j[0]
		ln_j = fullname_j[1]
		if ln_i!=ln_j:
			score = similar(ln_i,ln_j)
			if score>0.8:
				# print "ln_i:",ln_i," | ln_j:",ln_j
				if n_i == n_j:
					print "\tequals    word_i:",i," | word_j:",j,"\t",similar(n_i,n_j)
					G.add_edge(i,j)
				# else: 
				# 	if similar(n_i,n_j)>0.6:
				# 		print "\tsimilars    word_i:",i," | word_j:",j,"\t",similar(n_i,n_j)
# === / filter02: searching for similarities between authors-names ==


# === copying|merging homonims-metadata ===
for e in G.edges_iter():
	n1 = e[0]
	n2 = e[1]

	A = sorted(pinames[n1])
	B = sorted(pinames[n2])
	U = sorted(union(A,B))

	# print n1 , ":" , A , "--->" , n2 , ":" , B , "\t=\t" , U
	pinames[n1] = U
	pinames[n2] = U
# === / copying|merging homonims-metadata ===


# === Make inverted-index "i;d;s":[name1,name2,...] ===
finaldict = {}
for i in pinames:
	gps = sorted(pinames[i])
	gps_str = ";".join(gps)
	if not finaldict.has_key(gps_str): finaldict[gps_str] = []
	finaldict[gps_str].append(i)
# === / Make inverted-index "i;d;s":[name1,name2,...] ===


# === Re-assign PI-name to IDict  ===
for i in finaldict:
	auth = finaldict[i]

	gps = i.split(";")

	dictnames = {}
	for gp in gps:
		if IDict[gp].has_key("PIxls") and IDict[gp]["PIxls"]!="": dictnames[IDict[gp]["PIxls"]]=1
		if IDict[gp].has_key("PIfolder") and IDict[gp]["PIfolder"]!="": dictnames[IDict[gp]["PIfolder"]]=1
	
	allpossiblenames = sorted( dictnames.keys() , key=len, reverse=True)
	mostlargename = allpossiblenames[0]
	for ID in gps:
		IDict[ID]["PI"] = mostlargename
# === / Re-assign PI-name to IDict  ===

saveCSV( "finalregs.csv" , ["ID" , "PI" , "AG1" , "AG2" , "ACR" ,"TI" , "ABS" ] , IDict )