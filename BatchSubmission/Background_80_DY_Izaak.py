path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="DY"
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
               ["DYJetsToLL_M-50_TuneCUETP8M1",
               ["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_reHLT_ext_0000.xml"]],
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
