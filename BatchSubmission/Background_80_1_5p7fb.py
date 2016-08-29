path2xml="$SFRAME_DIR/../BatchSubmission/xmls_15p9"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_LepPairPt_StandardID_EleTight_MuTight_15p9"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=1
nFiles=2
hCPU="02:30:00"
hVMEM="3500M"
postFix = ""

  
dataSets=[
  
  
  ["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml"]],
  ["DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",["DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml"]],
  ["QCD_HT1000to1500",[
      "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml",
      "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext.xml",
      ]
   ],
  ["QCD_HT1500to2000",[
      "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml",
      "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext.xml"
      ]
   ],
  ["QCD_HT2000toInf",[
      "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml",
      "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext.xml"
      ]
   ],
  
  ["QCD_HT300to500",[
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext.xml",
      ]
   ],
  ["QCD_HT500to700",["QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml"]],
  ["QCD_HT700to1000",[
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext.xml"  
      ]
   ],
  ["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.xml"]],
  ["ST_t-channel_antitop_4f_inclusiveDecays",["ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1.xml"]],
  ["ST_t-channel_antitop_4f_leptonDecays",["ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.xml"]],
  ["ST_tW_antitop_5f_inclusiveDecays", ["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.xml"]], 
  ["ST_tW_top_5f_inclusiveDecays",["ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.xml"]],
 
]

'''
["QCD_HT200to300",
   ["QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
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

