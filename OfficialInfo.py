

from openpyxl import load_workbook

class ExtractCSV:

	def __init__(self,filename):
		self.fn = filename
		self.heads = {}

	def startReading(self, prikey):


		wb = load_workbook(filename = self.fn , use_iterators = True)

		sheetname = wb.get_sheet_names()[0]

		ws = wb.get_sheet_by_name(name = sheetname)

		items = self.heads

		finalregs = []

		for row in ws.iter_rows():
			reg = {}
			for cell in row:
				if cell.row==1:
					items[cell.column] = cell.internal_value
				else: 
					reg[cell.column] = cell.internal_value
			if reg.has_key(prikey) and reg[prikey]!=None and reg[prikey]!="":
				finalregs.append(reg)
			else:
				print reg
				
		return finalregs


	def makeArray(self, results):

		finalarray = {}
		for i in results:
			ACR = i["A"].replace("\n","").replace("\t","") if i["A"]!=None else ""
			PI = i["B"].replace("\n","").replace("\t","") if i["B"]!=None else ""
			ID = i["C"].replace("\n","").replace("\t","")
			AG = i["D"].replace("\n","").replace("\t","") if i["D"]!=None else ""
			TI = i["E"].replace("\n","").replace("\t","") if i["E"]!=None else ""
			finalarray["BPM"+str(ID)] = {"PI":PI,"AG":AG,"ACR":ACR,"TI":TI}

		return finalarray


