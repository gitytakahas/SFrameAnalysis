path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="TT"
outDir="/scratch/$USER/SFrameAnalysis/AnalysisOutput/"+jobName #"$SFRAME_DIR/../AnalysisOutput/"+jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=4
hCPU="03:30:00"
hVMEM="5000M"
postFix="_TES1p03_ICHEP" #"_ICHEP" #"_Summer2016"
dataSets = [
       ["TT_TuneCUETP8M1",
        [   "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0000_0.xml",
            "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0000_1.xml",
            "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0001_0.xml",
            "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0001_1.xml",
            "TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext_0002.xml",   ]],
            ]
                
if "Summer2016" in postFix: dataSets = [
       ["TT_TuneCUETP8M1",
        [   "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_V1_0000_0.xml",
            "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_V1_0000_1.xml",
            "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_V1_0000_2.xml",
            "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_V1_additional_0000_0.xml",
            "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_V1_additional_0000_1.xml",
            "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_V1_additional_0000_2.xml",
            "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_V1_additional_0001.xml",   ]],
            ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","false"],
                ["doRecoilCorr","false"],
                ["doTTpt","true"],
                ["doTES","true"],
                ["TESshift","0.03"],
                ["doTTpt","true"],
             ]

jobOptionsFile2=open("AnalysisOptions.py", 'r')
command2=""
for i in [o for o in jobOptionsFile2.readlines()]:
    if ("#E" + "nd") in i : break
    command2+=i
jobOptionsFile2.close()
exec command2
userItems += AddUserItems
