import os
import csv

class Scanner:


	def extractPDFs(self,param):
		print param
		import glob
		files = glob.glob(param+'/*.pdf')
		for i in files:
			seulfile = i.replace(param+"/","")
			print i
			print seulfile
			print 


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


	def Directory(self,dir2scan,items,outputname,write=False):

		if write:
			c = csv.writer(open(outputname, "wb"),delimiter='\t')
			c.writerow(items) #write column names

		for dirs in os.walk(dir2scan):

			dirname = dirs[0].replace(dir2scan+"/","")
			dirname = dirname.replace(dir2scan,"")
			
			if dirname!=dir2scan:
				metadata = self.extrMeta(dirname)
				if metadata[0]: 
					if write:
						# print [ dirs[0] , metadata[0] , metadata[1], metadata[2] ]
						self.extractPDFs(dirs[0])
						c.writerow([ dirs[0] , metadata[0] , metadata[1], metadata[2] ])
					else:
						print '"'+dirs[0]+'/"\t',"\t".join(metadata)
				else: 
					if len(metadata[1][0])>1:
						print "error:",metadata[1]





dir2scan ='.'

import sys
if len(sys.argv)>1:
	dir2scan = sys.argv[1]
else:
	print '\n\tpls enter grantproposals folder name (e.g):\n\t\tpython extracter.py "foldername"\n'
	sys.exit(0)



columnNames = ["FolderName","ProjectID", "Author", "Agency"]
outputname = "Save.csv"

scan = Scanner()
print "... Scanning folders inside [",dir2scan,"]..."
scan.Directory(dir2scan,columnNames,outputname,True)#voila
print "fini"

















