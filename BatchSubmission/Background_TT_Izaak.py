path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="TT"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=1
hCPU="03:30:00"
hVMEM="5000M"
postFix = ""
label = "_ICHEP" #"_triggerless" # _nocuts
dataSets = [
               ["TT_TuneCUETP8M1"+label,
                [   "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0000_0.xml",
                    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0000_1.xml",
                    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0001_0.xml",
                    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0001_1.xml",
                    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0002.xml",   ]],
                 
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","false"],
                ["doSVFit","false"],
                ["OutputTreeName_mutau", "tree_mutau" ],
                ["OutputTreeName_eletau","tree_eletau"],
             ]

jobOptionsFile2=open("AnalysisOptions.py", 'r')
command2=""
for i in [o for o in jobOptionsFile2.readlines()]:
    if ("#E" + "nd") in i : break
    command2+=i
jobOptionsFile2.close()
exec command2
userItems += AddUserItems

inputTrees=["ntuplizer/tree"]
outputTrees=["tree_mutau","tree_eletau"]
