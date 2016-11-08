path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="DY"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=5
hCPU="03:30:00"
hVMEM="5000M"
postFix = ""
label = "_ICHEP" #"_triggerless"
dataSets = [
                
               ["DYJetsToLL_M-50_TuneCUETP8M1"+label,
                [   "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_reHLT_ext_0000.xml", ]],
               
               ["DYJetsToLL_M-10to50_TuneCUETP8M1"+label,
                [   "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml", ]],
                
               ["DY1JetsToLL_M-10to50"+label,
                [   "DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_reHLT_0000.xml", ]],
                
               ["DY2JetsToLL_M-10to50"+label,
                [   "DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_reHLT_0000.xml", ]],
                
               ["DY1JetsToLL_M-50_TuneCUETP8M1"+label,
                [   "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml",
                    "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_2.xml",
                    "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0001_0.xml",
                    "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0001_1.xml", ]],
                
               ["DY2JetsToLL_M-50_TuneCUETP8M1"+label,
                [   "DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_0.xml",
                    "DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000_1.xml", ]],
                
               ["DY3JetsToLL_M-50_TuneCUETP8M1"+label,
                [   "DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000.xml", ]],
                
               ["DY4JetsToLL_M-50_TuneCUETP8M1"+label,
                [   "DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT1_0000.xml", ]],
                
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
