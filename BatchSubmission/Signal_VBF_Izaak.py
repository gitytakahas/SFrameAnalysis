path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="VBFHTT"
outDir="/scratch/ineuteli/SFrameAnalysis/AnalysisOutput/"+jobName #"$SFRAME_DIR/../AnalysisOutput/"+jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=2
hCPU="03:30:00"
hVMEM="5000M"
postFix="_ICHEP" #"_ICHEP" #"_Summer2016"
dataSets = [

#         ["VBFHToTauTau_M125_13TeV_powheg_pythia8",
#          [  "VBFHToTauTau_M125_13TeV_powheg_pythia8_161014_151922_0.xml", 
#             "VBFHToTauTau_M125_13TeV_powheg_pythia8_161014_151922_1.xml", ]],
            
        ["VBFHToTauTau_M125_13TeV_powheg_pythia8",
         [  "VBFHToTauTau_M125_13TeV_powheg_pythia8_reHLT_v7_0000_0.xml", 
            "VBFHToTauTau_M125_13TeV_powheg_pythia8_reHLT_v7_0000_1.xml", ]],
            
            ]
                
if "Summer2016" in postFix: dataSets = [
        ["VBFHToTauTau_M125_13TeV_powheg_pythia8",
         [  "VBFHToTauTau_M125_13TeV_powheg_pythia8_V2_0000_0.xml",
            "VBFHToTauTau_M125_13TeV_powheg_pythia8_V2_0000_1.xml",
            "VBFHToTauTau_M125_13TeV_powheg_pythia8_V2_0000_2.xml", ]],
            ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","true"],
                ["doSVFit","false"],
                ["doRecoilCorr","false"],
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
