Usage:

(1) python extracter.py "Grant proposals"/

This will generate a folder, e.g. "TO-USE/", with lots of txts from GrantProposals' pdfs.
	Log of errors in FailFolders.txt

(2) python processOutput.py

This will read the txts folder, e.g. "TO-USE/", and it will generate a CSV with:

- ID: BPMID
- PI: PI Name according GrantProposalsFolder
- PIfull: PI Name according "extraction BPM.xlsx"
- AG1: Agency according GrantProposalsFolder
- AG2: Agency according "extraction BPM.xlsx"
- ABS: Artifitial abstract using the pdfs extracted-info (for some filtering: blacklist.txt)
- ACR: Acronym according "extraction BPM.xlsx"
- TI: Title according "extraction BPM.xlsx"


This CSV is uploaded to Cortext and then we can generate some bipartite maps.

First testmap:

http://manager.cortext.net/projects/pokesam3_gmail_com/pasteur/data/finalregs-45617-1-finalregs-db~45620/1/maps/maps_output.zip


