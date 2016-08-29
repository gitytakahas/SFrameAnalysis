path2xml="$SFRAME_DIR/../BatchSubmission/xmls_15p9"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_LepPairPt_StandardID_EleTight_MuTight_15p9fb_69p2_PW_filters"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=1
nFiles=10
hCPU="02:30:00"
hVMEM="1500M"
postFix = ""
dataSets=[
  ["JetHT_Run2016B-PromptReco",[
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0000_0.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0000_1.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0000_2.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0001_0.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0001_1.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0001_2.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0001_3.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0002_0.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0002_1.xml",
      "JetHT_Run2016B-PromptReco-v2_15p9fb_0002_2.xml",
      "JetHT_Run2016C-PromptReco-v2_15p9fb_0000_0.xml",
      "JetHT_Run2016C-PromptReco-v2_15p9fb_0000_1.xml",
      "JetHT_Run2016C-PromptReco-v2_15p9fb_0000_2.xml",
      "JetHT_Run2016C-PromptReco-v2_15p9fb_0000_3.xml",
      "JetHT_Run2016C-PromptReco-v2_15p9fb_0000_4.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0000_0.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0000_1.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0000_2.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0000_3.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0000_4.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0000_5.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0001_0.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0001_1.xml",
      "JetHT_Run2016D-PromptReco-v2_15p9fb_0001_2.xml",
      "JetHT_Run2016E-PromptReco-v2_15p9fb_0000_0.xml",
      "JetHT_Run2016E-PromptReco-v2_15p9fb_0000_1.xml",
      "JetHT_Run2016E-PromptReco-v2_15p9fb_0000_2.xml",
      "JetHT_Run2016E-PromptReco-v2_15p9fb_0000_3.xml",
      "JetHT_Run2016E-PromptReco-v2_15p9fb_0000_4.xml",
      "JetHT_Run2016E-PromptReco-v2_15p9fb_0000_5.xml",
      "JetHT_Run2016E-PromptReco-v2_15p9fb_0000_6.xml"
      ]
   ],
 
  ["SingleElectron_Run2016B-PromptReco",
   [
      
      "SingleElectron_Run2016B-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleElectron_Run2016B-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleElectron_Run2016B-PromptReco-v2_15p9fb_0001_0.xml",
      "SingleElectron_Run2016B-PromptReco-v2_15p9fb_0001_1.xml",
      "SingleElectron_Run2016B-PromptReco-v2_15p9fb_0001_2.xml",
      "SingleElectron_Run2016B-PromptReco-v2_15p9fb_0002_0.xml",
      "SingleElectron_Run2016B-PromptReco-v2_15p9fb_0002_1.xml",
      "SingleElectron_Run2016C-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleElectron_Run2016C-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleElectron_Run2016C-PromptReco-v2_15p9fb_0000_2.xml",
      "SingleElectron_Run2016D-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleElectron_Run2016D-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleElectron_Run2016D-PromptReco-v2_15p9fb_0000_2.xml",
      "SingleElectron_Run2016D-PromptReco-v2_15p9fb_0000_3.xml",
      "SingleElectron_Run2016D-PromptReco-v2_15p9fb_0001_0.xml",
      "SingleElectron_Run2016D-PromptReco-v2_15p9fb_0001_1.xml",
      "SingleElectron_Run2016E-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleElectron_Run2016E-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleElectron_Run2016E-PromptReco-v2_15p9fb_0000_2.xml",
      "SingleElectron_Run2016E-PromptReco-v2_15p9fb_0000_3.xml",
      "SingleElectron_Run2016E-PromptReco-v2_15p9fb_0000_4.xml"
      ]
   ],
  ["SingleMuon_Run2016B",
   [
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0000_2.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0000_3.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0000_4.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0000_5.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0001_0.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0001_1.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0001_2.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0001_3.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0001_4.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0001_5.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0002_0.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0002_1.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0002_2.xml",
      "SingleMuon_Run2016B-PromptReco-v2_15p9fb_0002_3.xml",
      "SingleMuon_Run2016C-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleMuon_Run2016C-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleMuon_Run2016C-PromptReco-v2_15p9fb_0000_2.xml",
      "SingleMuon_Run2016C-PromptReco-v2_15p9fb_0000_3.xml",
      "SingleMuon_Run2016C-PromptReco-v2_15p9fb_0000_4.xml",
      "SingleMuon_Run2016C-PromptReco-v2_15p9fb_0000_5.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0000_2.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0000_3.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0000_4.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0000_5.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0000_6.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0001_0.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0001_1.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0001_2.xml",
      "SingleMuon_Run2016D-PromptReco-v2_15p9fb_0001_3.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_0.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_1.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_2.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_3.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_4.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_5.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_6.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_7.xml",
      "SingleMuon_Run2016E-PromptReco-v2_15p9fb_0000_8.xml"

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
outputTrees=["tree_mutau","tree_eletau" ]

'''
outputTrees=["analysis","tree_mutau","tree_eletau","tree_tautau" ]
'''
