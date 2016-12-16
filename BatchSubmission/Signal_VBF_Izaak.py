path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="signal_VBF"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=2
hCPU="03:30:00"
hVMEM="5000M"
postFix = ""
label = "" #"_triggerless" # _nocuts
dataSets = [
                ["VBFHToTauTau_M125_13TeV_powheg_pythia8",
                 [  'VBFHToTauTau_M125_13TeV_powheg_pythia8_161014_151922_0.xml', 
                    'VBFHToTauTau_M125_13TeV_powheg_pythia8_161014_151922_1.xml'
                    ]],
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","true"],
                ["doSVFit","false"],
                ["doRecoilCorr","false"],
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
