path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="HTT"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=3
hCPU="03:00:00"
hVMEM="5000M"
postFix = ""
label = "_TES1p03_ICHEP" #_onlycrosstrigger" #"_triggerless" # _nocuts
dataSets = [
                ["GluGluHToTauTau_M125"+label,
                 [  "GluGluHToTauTau_M125_13TeV_powheg_pythia8_reHLT_v7_0000_0.xml",
                    "GluGluHToTauTau_M125_13TeV_powheg_pythia8_reHLT_v7_0000_1.xml",
                    "GluGluHToTauTau_M125_13TeV_powheg_pythia8_reHLT_v7_0000_2.xml", ]],
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","true"],
                ["doRecoilCorr","false"],
                ["doTES","true"],
                ["TESshift","0.03"],
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
