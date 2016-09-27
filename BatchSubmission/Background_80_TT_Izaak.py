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
dataSets = [
               ["TT_TuneCUETP8M1",
               ["TT_TuneCUETP8M1_13TeV-powheg-pythia8_1.xml","TT_TuneCUETP8M1_13TeV-powheg-pythia8_2.xml"]],
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","false"],
                ["doSVFit","false"],
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
outputTrees=["tree"]
