Usage:

(1) python extracter.py "Grant proposals"/

This will generate a folder, e.g. "TO-USE/", with lots of txts from GrantProposals' pdfs.
	Errors log in FailFolders.txt

(2) python processOutput.py 
- Install http://github.com/saffsd/langid.py
- pip install openpyxl

This will read the txts folder, e.g. "TO-USE/", and it will generate a CSV with:

- ID: BPM-ID
- PI: P.I.-fullname defined by the merge/unification of the names that appear in GrantProposalsFolder and extractionBPM.xlsx 
- AG1: Agency according GrantProposalsFolder
- AG2: Agency according extractionBPM.xlsx
- ABS: Artifitial abstract using the pdfs extracted-info (for some filtering: blacklist.txt)
- ACR: Acronym according extractionBPM.xlsx
- TI: Title according extractionBPM.xlsx


This CSV is uploaded to Cortext.


