path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="signal"
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
               ["SUSYGluGluToHToTauTau_M-160",
               ["SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8.xml"]],
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","true"],
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
