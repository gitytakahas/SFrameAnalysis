path2xml="$SFRAME_DIR/../BatchSubmission/xmls"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_StandardID_EleTight_MuTight_LepPairPt_DB"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=2
nFiles=4
hCPU="02:30:00"
hVMEM="4000M"
postFix = ""
dataSets=[
  
 
  ["JetHT_Run2016B-PromptReco",[
      "JetHT_Run2016B-PromptReco-v2_V3_2p6fb.xml",
      "JetHT_Run2016B-PromptReco-v2_V3_2p6fb_4fb.xml"
      ]
   ],
 
  ["SingleElectron_Run2016B-PromptReco",
   ["SingleElectron_Run2016B-PromptReco-v2_V3_2p6fb_0.xml",
    "SingleElectron_Run2016B-PromptReco-v2_V3_2p6fb_1.xml",
    "SingleElectron_Run2016B-PromptReco-v2_V3_2p6fb_2.xml",
    "SingleElectron_Run2016B-PromptReco-v2_V3_2p6fb_4fb.xml",
    ]
   ],
  ["SingleMuon_Run2016B",
   ["SingleMuon_Run2016B-PromptReco-v2_V3_2p6fb_0.xml",
    "SingleMuon_Run2016B-PromptReco-v2_V3_2p6fb_1.xml",
    "SingleMuon_Run2016B-PromptReco-v2_V3_2p6fb_4fb.xml"
    ]
   ],


  ]



userItems = [
   ["IsData","true"],
   ["IsSignal","false"],
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

