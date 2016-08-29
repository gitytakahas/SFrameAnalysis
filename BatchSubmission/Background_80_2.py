path2xml="$SFRAME_DIR/../BatchSubmission/xmls"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_StandardID_EleTight_MuTight_LepPairPt_DB"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=1
nFiles=1
hCPU="04:30:00"
hVMEM="6000M"
postFix = ""


'''  
dataSets=[
  
  ["WJetsToLNu_HT-100To200",["WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-1200To2500",["WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-200To400",["WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-2500ToInf",["WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-400To600",["WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-600To800",["WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-800To1200",["WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
 
]
''' 
dataSets=[
  
  
  ["TT",["TT_TuneCUETP8M1_13TeV-powheg-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-100To200",["WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-1200To2500",["WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-200To400",["WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-2500ToInf",["WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-400To600",["WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-600To800",["WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-800To1200",["WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WW",["WW_TuneCUETP8M1_13TeV-pythia8_v2.xml"]],
  ["WZ",["WZ_TuneCUETP8M1_13TeV-pythia8_v2.xml"]],
  ["ZZ",["ZZ_TuneCUETP8M1_13TeV-pythia8_v2.xml"]],
]
'''
 ["TTJets_HT-1200to2500",["TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["TTJets_HT-2500toInf",["TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["TTJets_HT-600to800",["TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["TTJets_HT-800to1200",["TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
'''
userItems = [
   ["IsData","false"],
   ["IsSignal","true"],
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
outputTrees=["analysis","tree_mutau","tree_eletau","tree_tautau" ]

