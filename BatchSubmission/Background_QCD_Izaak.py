path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="TT"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=4
hCPU="03:30:00"
hVMEM="5000M"
postFix = ""
label = "_ICHEP" #"_triggerless"
dataSets = [
               ["QCD_HT100toInf"+label,
                [   "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000.xml",
                    "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000.xml",
                    "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",
                    "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000.xml",
                    "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000.xml",
                    "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000.xml",
                    "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000.xml",
                    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000.xml",
                    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_0.xml",
                    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_1.xml",
                    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_2.xml",
                    "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",
                    "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_0.xml",
                    "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_1.xml",
                    "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_2.xml",
                    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",
                    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_0.xml",
                    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_1.xml",
                    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_2.xml",
                    "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",
                    "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_0.xml",
                    "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_ext_0000_1.xml",   ]],
                 
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","false"],
                #["doSVFit","true"],
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
