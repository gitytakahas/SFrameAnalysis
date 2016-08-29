path2xml="$SFRAME_DIR/../BatchSubmission/xmls_15p9"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_LepPairPt_StandardID_EleTight_MuTight_15p9fb_69p2_PW_filters"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=1
nFiles=5
hCPU="03:30:00"
hVMEM="1500M"
postFix = ""



dataSets=[
  
  

   ["TT",
   ["TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_0.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_1.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_10.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_11.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_12.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_2.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_3.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_4.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_5.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_6.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_7.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_8.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0000_9.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_0.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_1.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_10.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_11.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_12.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_2.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_3.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_4.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_5.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_6.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_7.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_8.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_0001_9.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_0.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_1.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_10.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_11.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_12.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_13.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_2.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_3.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_4.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_5.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_6.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_7.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_8.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0000_9.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_0.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_1.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_10.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_11.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_12.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_13.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_2.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_3.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_4.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_5.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_6.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_7.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_8.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0001_9.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_0.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_1.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_10.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_11.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_12.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_13.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_2.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_3.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_4.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_5.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_6.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_7.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_8.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0002_9.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_0.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_1.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_10.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_11.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_12.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_2.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_3.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_4.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_5.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_6.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_7.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_8.xml",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext_0003_9.xml"]],

 
  ["WJetsToLNu_HT-100To200",[
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_2.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_3.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_4.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_5.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_6.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_7.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_8.xml",
      "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_9.xml"]],
  ["WJetsToLNu_HT-1200To2500",[
      "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
      "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
      "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_2.xml"]],
  ["WJetsToLNu_HT-200To400",[

      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_2.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_2.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_3.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_4.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_5.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_6.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_7.xml",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_8.xml"]],

 ["TTJets_HT-600to800",
   ["TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
    "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
    "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_2.xml"]],
  ["TTJets_HT-800to1200",
   ["TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
    "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
    "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_2.xml"]],
   
  ["WJetsToLNu_HT-2500ToInf",["WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml"]],
  ["WJetsToLNu_HT-400To600",
   ["WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
    "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml"]],
  ["WJetsToLNu_HT-600To800",
   ["WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v4_0000.xml"]],
   
  ["WJetsToLNu_HT-800To1200",[
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_2.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_3.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_4.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_5.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_6.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_7.xml",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_8.xml"]],


  

  ["WW",["WW_TuneCUETP8M1_13TeV-pythia8_0000_0.xml",
         "WW_TuneCUETP8M1_13TeV-pythia8_0000_1.xml"]],
  ["WZ",["WZ_TuneCUETP8M1_13TeV-pythia8_0000_0.xml",
         "WZ_TuneCUETP8M1_13TeV-pythia8_0000_1.xml"]],
  ["ZZ",["ZZ_TuneCUETP8M1_13TeV-pythia8_0000_0.xml",
         "ZZ_TuneCUETP8M1_13TeV-pythia8_0000_2.xml",
         "ZZ_TuneCUETP8M1_13TeV-pythia8_0000_1.xml",  
         "ZZ_TuneCUETP8M1_13TeV-pythia8_0000_3.xml"]],
  
]

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
outputTrees=["tree_mutau","tree_eletau" ]
'''
outputTrees=["analysis","tree_mutau","tree_eletau","tree_tautau" ]
'''
