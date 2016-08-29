path2xml="$SFRAME_DIR/../BatchSubmission/xmls"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_StandardID_EleTight_MuTigh_LepPairPt"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=2
nFiles=1
hCPU="02:30:00"
hVMEM="2000M"
postFix = ""

  
dataSets=[
  
  
  ["QCD_HT2000toInf",["QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
   ["QCD_HT700to1000",["QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
]


'''
dataSets=[
  
 
  ["DYJetsToLL_M-50_HT-100to200",["DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["DYJetsToLL_M-50_HT-200to400",["DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["DYJetsToLL_M-5to50_HT-100to200",["DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["DYJetsToLL_M-5to50_HT-600toInf",["DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",["DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["QCD_HT1000to1500",["QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["QCD_HT1500to2000",["QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["QCD_HT2000toInf",["QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["QCD_HT200to300",["QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["QCD_HT300to500",["QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["QCD_HT500to700",["QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["QCD_HT700to1000",["QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_v2.xml"]],
  ["ST_t-channel_antitop_4f_inclusiveDecays",["ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_v2.xml"]],
  ["ST_t-channel_antitop_4f_leptonDecays",["ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v2.xml"]],
  ["ST_tW_antitop_5f_inclusiveDecays", ["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v2.xml"]],
  ["ST_tW_top_5f_NoFullyHadronicDecays",["ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1_v2.xml"]],
  ["ST_tW_top_5f_inclusiveDecays",["ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v2.xml"]],
  ["TTJets_HT-1200to2500",["TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["TTJets_HT-2500toInf",["TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["TTJets_HT-600to800",["TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["TTJets_HT-800to1200",["TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["TT",["TT_TuneCUETP8M1_13TeV-powheg-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-100To200",["WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-1200To2500",["WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-200To40",["WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-2500ToInf",["WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-400To600",["WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-600To800",["WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WJetsToLNu_HT-800To1200",["WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v2.xml"]],
  ["WW",["WW_TuneCUETP8M1_13TeV-pythia8_v2.xml"]],
  ["WZ",["WZ_TuneCUETP8M1_13TeV-pythia8_v2.xml"]],
  ["ZZ",["ZZ_TuneCUETP8M1_13TeV-pythia8_v2.xml"]],
]
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

