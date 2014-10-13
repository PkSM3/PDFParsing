import os
import csv

class Scanner:

	def __init__(self):

		#=Type of failures=
		#	0: Folder-name doesn't follow the defined pattern
		#	1: Folder has no pdfs inside!
		self.fails = []



	def convertCommand(self,param,pID,PI,Ag,extension):
		results = []
		import glob
		files = glob.glob(param+'/*.'+extension)
		for i in files:

			seulfile = i.replace(param+"/","")
			if seulfile:
				txtname = seulfile.replace("."+extension,".txt")
				toexecute = 'python pdf2txt.py "'+i+'" > "'+pID+"|"+PI+"|"+Ag+"|||"+txtname+'"'
				results.append(toexecute)

		return results


	def extrMeta(self,dirname):
		rawdir = dirname.split(" -")
		
		if len(rawdir)<3: return [False,rawdir]
		else:
			# print "\t",len(rawdir),rawdir
			projectID = rawdir[0].strip().replace(" ","")
			author = rawdir[1].strip()
			try:
				agency = rawdir[2].strip()					
				output = [ projectID , author , agency ]
				return output
			except:
				return [False,rawdir]


	def Directory(self,dir2scan,items,outputname,outputFolder,write=False):

		if write:
			x = "create csv"
			# c = csv.writer(open(outputname, "wb"),delimiter='\t')
			# c.writerow(items) #write column names

		for dirs in os.walk(dir2scan):

			dirname = dirs[0].replace(dir2scan+"/","")
			dirname = dirname.replace(dir2scan,"")
			
			if dirname!=dir2scan:
				metadata = self.extrMeta(dirname)
				if metadata[0]: 
					if write:
						# print [ dirs[0] , metadata[0] , metadata[1], metadata[2] ]
						pID = metadata[0]
						PI = metadata[1]
						Ag = metadata[2]
						pdfs = self.convertCommand(dirs[0],pID,PI,Ag,"pdf")
						if len(pdfs)>0:

							for p in pdfs:
								pdf2txt = p.replace(" > "," > "+outputFolder+"/")
								# print pdf2txt
								os.system(pdf2txt)
							# print pID,PI,Ag
							# print pdfs
							# print "----------------------\n"
						else:
							self.fails.append([1,dirs[0]])
					else:
						print '"'+dirs[0]+'/"\t',"\t".join(metadata)
				else: 
					if len(metadata[1][0])>1:
						self.fails.append([0,dirs[0]])





dir2scan ='.'

import sys
if len(sys.argv)>1:
	dir2scan = sys.argv[1]
else:
	print '\n\tpls enter grantproposals folder name (e.g):\n\t\tpython extracter.py "foldername"\n'
	sys.exit(0)



columnNames = ["FolderName","ProjectID", "Author", "Agency"]
outputname = "Save.csv"


# import time
# start_time = time.time()
# print start_time

outputFolder = "output"
os.system("rm -R "+outputFolder+"; mkdir "+outputFolder)

scan = Scanner()
print "... Scanning folders inside [",dir2scan,"]..."
scan.Directory(dir2scan,columnNames,outputname,outputFolder,True)#voila



# Folders that weren't processed
if len(scan.fails)>0:
	f = open("FailFolders.txt","w")
	f.write("# Type of failures\n")
	f.write("#	0: Folder-name doesn't follow the defined pattern\n")
	f.write("#	1: Folder has no pdfs inside!\n\n")
	for i in scan.fails:
		f.write(`i[0]`+"\t"+i[1]+"\n")
	f.close()

print "fini"

