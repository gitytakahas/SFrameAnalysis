path2xml="$SFRAME_DIR/../BatchSubmission/xmls_15p9"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_LepPairPt_StandardID_EleTight_MuTight_15p9fb_69p2_PW_filters"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=1
nFiles=10
hCPU="03:30:00"
hVMEM="2000M"
postFix = ""

dataSets=[
 

  ["QCD_HT1000to1500",[
      "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
      "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml"]],
  ["QCD_HT1500to2000",[
      "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
      "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml"]],
  ["QCD_HT2000toInf",[
      "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
      "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml"]],
  ["QCD_HT200to300",
   ["QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_2.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_10.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_11.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_12.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_13.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_14.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_15.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_16.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_17.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_18.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_19.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_2.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_20.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_21.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_3.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_4.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_5.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_6.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_7.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_8.xml",
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_9.xml"]],
  ["QCD_HT300to500",[
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_2.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_3.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_4.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_5.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_6.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_7.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_8.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_9.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_10.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_11.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_12.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_13.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_14.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_15.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_16.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_17.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_18.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_19.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_2.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_20.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_21.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_22.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_3.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_4.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_5.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_6.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_7.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_8.xml",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_9.xml"]],
  ["QCD_HT500to700",
   ["QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_10.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_11.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_12.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_13.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_14.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_15.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_16.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_17.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_18.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_19.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_2.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_20.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_21.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_22.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_23.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_24.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_3.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_4.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_5.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_6.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_7.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_8.xml",
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_9.xml"]],
  ["QCD_HT700to1000",[
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_0.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_1.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_2.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_3.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_4.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_5.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_6.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_7.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000_8.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_10.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_11.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_12.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_13.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_14.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_15.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_16.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_2.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_3.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_4.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_5.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_6.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_7.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_8.xml",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_9.xml"]],



  ["ST_t-channel_antitop_4f_inclusiveDecays",[
      "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_v3_0000_0.xml",
      "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_v3_0000_1.xml"]],
  ["ST_t-channel_antitop_4f_leptonDecays",
   ["ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v3_0000.xml"]],
  ["ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
   ["ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v3_0000.xml"]],
  ["ST_tW_antitop_5f_inclusiveDecays", 
   ["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v3_0000.xml"]], 
  ["ST_tW_top_5f_inclusiveDecays",
   ["ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v3_0000.xml"]],
  ["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", 
   ["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_v3_0000.xml"]]

  ]

'''
dataSets=[
  
  
  ["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_0.xml",
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000_1.xml",
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0001.xml"]],
  
  ["DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    " DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],
  ["DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],
  ["DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],
  ["DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],

  ["DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml"]],
  ["DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    "DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],
  ["DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    "DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],
  ["DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    "DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],
  ["DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
   ["DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_0000.xml",
    "DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext_0000.xml"]],
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
outputTrees=["tree_mutau","tree_eletau" ]
'''
outputTrees=["analysis","tree_mutau","tree_eletau","tree_tautau" ]
'''
