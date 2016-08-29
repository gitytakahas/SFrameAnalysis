path2xml="$SFRAME_DIR/../BatchSubmission/xmls"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_StandardID_EleTight_MuTight_LepPairPt_"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=1
nFiles=1
hCPU="03:30:00"
hVMEM="5000M"
postFix = ""
dataSets=[
  
  ["BulkGrav1200",
   ["BulkGravTohhTohtatahbb_narrow_M-1200_13TeV-madgraph_v2.xml"]],
  ["BulkGrav1400",
   ["BulkGravTohhTohtatahbb_narrow_M-1400_13TeV-madgraph_v2.xml"]],
  ["BulkGrav1600",
   ["BulkGravTohhTohtatahbb_narrow_M-1600_13TeV-madgraph_v2.xml"]],
  ["BulkGrav1800",
   ["BulkGravTohhTohtatahbb_narrow_M-1800_13TeV-madgraph_v2.xml"]],
  ["BulkGrav2000",
   ["BulkGravTohhTohtatahbb_narrow_M-2000_13TeV-madgraph_v2.xml"]],
  ["BulkGrav2500",
   ["BulkGravTohhTohtatahbb_narrow_M-2500_13TeV-madgraph_v2.xml"]],
  ["Wprime3000",
   ["BulkGravTohhTohtatahbb_narrow_M-3000_13TeV-madgraph_v2.xml"]],
  ["BulkGrav3500",
   ["BulkGravTohhTohtatahbb_narrow_M-3500_13TeV-madgraph_v2.xml"]],
  ["BulkGrav4000",
   ["BulkGravTohhTohtatahbb_narrow_M-4000_13TeV-madgraph_v2.xml"]],
  ["BulkGrav4500",
   ["BulkGravTohhTohtatahbb_narrow_M-4500_13TeV-madgraph_v2.xml"]],
  ["HH1000",
   ["RadionTohhTohtatahbb_narrow_M-1000_13TeV-madgraph_v2.xml"]],
  ["HH1200",
   ["RadionTohhTohtatahbb_narrow_M-1200_13TeV-madgraph_v2.xml"]],
  ["HH1400",
   ["RadionTohhTohtatahbb_narrow_M-1400_13TeV-madgraph_v2.xml"]],
  
  ["HH1800",
   ["RadionTohhTohtatahbb_narrow_M-1800_13TeV-madgraph_v2.xml"]],
  ["HH2000",
   ["RadionTohhTohtatahbb_narrow_M-2000_13TeV-madgraph_v2.xml"]],
  ["HH2500",
   ["RadionTohhTohtatahbb_narrow_M-2500_13TeV-madgraph_v2.xml"]],
  ["HH3000",
   ["RadionTohhTohtatahbb_narrow_M-3000_13TeV-madgraph_v2.xml"]],
  ["HH3500",
   ["RadionTohhTohtatahbb_narrow_M-3500_13TeV-madgraph_v2.xml"]],
  ["HH4000",
   ["RadionTohhTohtatahbb_narrow_M-4000_13TeV-madgraph_v2.xml"]],
  ["HH4500",
   ["RadionTohhTohtatahbb_narrow_M-4500_13TeV-madgraph_v2.xml"]],

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
outputTrees=["analysis","tree_mutau","tree_eletau","tree_tautau" ]

