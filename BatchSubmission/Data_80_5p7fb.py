path2xml="$SFRAME_DIR/../BatchSubmission/xmls_5p7"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_LepPairPt_BoostedID_EleLoose_MuLoose_5p7fb"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=2
nFiles=10
hCPU="02:30:00"
hVMEM="4000M"
postFix = ""
dataSets=[
  
 
  ["JetHT_Run2016B-PromptReco",[
      "JetHT_Run2016B-PromptReco-v2_0.xml",
      "JetHT_Run2016B-PromptReco-v2_01.xml",
      "JetHT_Run2016B-PromptReco-v2_1.xml",
      "JetHT_Run2016B-PromptReco-v2_4fb_5p76fb_0.xml",
      "JetHT_Run2016B-PromptReco-v2_4fb_5p76fb_1.xml",
      "JetHT_Run2016C-PromptReco-v2_4fb_5p76fb.xml",
     
       ]
   ],
 
  ["SingleElectron_Run2016B-PromptReco",
   [
      "SingleElectron_Run2016B-PromptReco-v2_0.xml",
      "SingleElectron_Run2016B-PromptReco-v2_01.xml",
      "SingleElectron_Run2016B-PromptReco-v2_1.xml",
      "SingleElectron_Run2016B-PromptReco-v2_2.xml",
      "SingleElectron_Run2016B-PromptReco-v2_3.xml",
      "SingleElectron_Run2016B-PromptReco-v2_4fb_5p76fb_0.xml",
      "SingleElectron_Run2016B-PromptReco-v2_4fb_5p76fb_1.xml",
      "SingleElectron_Run2016B-PromptReco-v2_4fb_5p76fb_2.xml",
      "SingleElectron_Run2016C-PromptReco-v2_4fb_5p76fb.xml",

    ]
   ],
  ["SingleMuon_Run2016B",
   [
      "SingleElectron_Run2016B-PromptReco-v2_0.xml",
      "SingleElectron_Run2016B-PromptReco-v2_01.xml",
      "SingleElectron_Run2016B-PromptReco-v2_1.xml",
      "SingleElectron_Run2016B-PromptReco-v2_2.xml",
      "SingleElectron_Run2016B-PromptReco-v2_3.xml",
      "SingleElectron_Run2016B-PromptReco-v2_4fb_5p76fb_0.xml",
      "SingleElectron_Run2016B-PromptReco-v2_4fb_5p76fb_1.xml",
      "SingleElectron_Run2016B-PromptReco-v2_4fb_5p76fb_2.xml",
      "SingleElectron_Run2016C-PromptReco-v2_4fb_5p76fb.xml",

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

