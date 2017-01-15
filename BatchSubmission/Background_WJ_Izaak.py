path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="WJ"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=4
hCPU="03:30:00"
hVMEM="5000M"
postFix = "_ICHEP" #"_triggerless"
dataSets = [
                
               [ "WJetsToLNu_TuneCUETP8M1",
                [   "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_reHLT_ext_0000_0.xml",
                    "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_reHLT_ext_0000_1.xml" ]],

               [ "W1JetsToLNu_TuneCUETP8M1",
                [   "W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",
                    "W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_2.xml"]],

               [ "W2JetsToLNu_TuneCUETP8M1",
                [   "W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",]],

               [ "W3JetsToLNu_TuneCUETP8M1",
                [   "W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",]],

               [ "W4JetsToLNu_TuneCUETP8M1",
                [   "W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000.xml",]],
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","false"],
                #["doSVFit","true"],
                ["doRecoilCorr","true"],
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

