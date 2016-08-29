path2xml="$SFRAME_DIR/../BatchSubmission/xmls_15p9"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput/prova_justTauIso_LepPairPt_StandardID_EleTight_MuTight_15p9fb_69p2_PW_filters"
jobName="b2gVHJob"
cycleName="VHTausAnalysis"
nEventsMax=-1
nProcesses=1
nFiles=1
hCPU="03:30:00"
hVMEM="1500M"
postFix = ""
dataSets=[
  ["BulkGrav1000",
   ["BulkGravTohhTohtatahbb_narrow_M-1000_13TeV-madgraph_v3_0000.xml"]],
 
  ["BulkGrav1200",
   ["BulkGravTohhTohtatahbb_narrow_M-1200_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav1400",
   ["BulkGravTohhTohtatahbb_narrow_M-1400_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav1600",
   ["BulkGravTohhTohtatahbb_narrow_M-1600_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav1800",
   ["BulkGravTohhTohtatahbb_narrow_M-1800_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav2000",
   ["BulkGravTohhTohtatahbb_narrow_M-2000_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav2500",
   ["BulkGravTohhTohtatahbb_narrow_M-2500_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav3000",
   ["BulkGravTohhTohtatahbb_narrow_M-3000_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav3500",
   ["BulkGravTohhTohtatahbb_narrow_M-3500_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav4000",
   ["BulkGravTohhTohtatahbb_narrow_M-4000_13TeV-madgraph_v3_0000.xml"]],
  ["BulkGrav4500",
   ["BulkGravTohhTohtatahbb_narrow_M-4500_13TeV-madgraph_v3_0000.xml"]],

  

  ["HH1000",
   ["RadionTohhTohtatahbb_narrow_M-1000_13TeV-madgraph_v3_0000.xml"]],
  ["HH1200",
   ["RadionTohhTohtatahbb_narrow_M-1200_13TeV-madgraph_v3_0000.xml"]],
  ["HH1800",
   ["RadionTohhTohtatahbb_narrow_M-1800_13TeV-madgraph_v3_0000.xml"]],
  ["HH2000",
   ["RadionTohhTohtatahbb_narrow_M-2000_13TeV-madgraph_v3_0000.xml"]],
  ["HH2500",
   ["RadionTohhTohtatahbb_narrow_M-2500_13TeV-madgraph_v3_0000.xml"]],
  ["HH3000",
   ["RadionTohhTohtatahbb_narrow_M-3000_13TeV-madgraph_v3_0000.xml"]],
  ["HH3500",
   ["RadionTohhTohtatahbb_narrow_M-3500_13TeV-madgraph_v3_0000.xml"]],
  ["HH4000",
   ["RadionTohhTohtatahbb_narrow_M-4000_13TeV-madgraph_v3_0000.xml"]],
  ["HH4500",
   ["RadionTohhTohtatahbb_narrow_M-4500_13TeV-madgraph_v3_0000.xml"]],

  ["Wprime1200",
   ["WprimeToWhToWhadhtata_narrow_M-1200_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime1400",
   ["WprimeToWhToWhadhtata_narrow_M-1400_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime1600",
   ["WprimeToWhToWhadhtata_narrow_M-1600_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime2000",
   ["WprimeToWhToWhadhtata_narrow_M-2000_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime2500",
   ["WprimeToWhToWhadhtata_narrow_M-2500_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime3000",
   ["WprimeToWhToWhadhtata_narrow_M-3000_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime3500",
   ["WprimeToWhToWhadhtata_narrow_M-3500_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime4000",
   ["WprimeToWhToWhadhtata_narrow_M-4000_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime600",
   ["WprimeToWhToWhadhtata_narrow_M-600_13TeV-madgraph_v3_0000.xml"]],
  ["Wprime800",
   ["WprimeToWhToWhadhtata_narrow_M-800_13TeV-madgraph_v3_0000.xml"]],

  ["Zprime1200",
   ["ZprimeToZhToZhadhtata_narrow_M-1200_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime1600",
   ["ZprimeToZhToZhadhtata_narrow_M-1600_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime1800",
   ["ZprimeToZhToZhadhtata_narrow_M-1800_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime2000",
   ["ZprimeToZhToZhadhtata_narrow_M-2000_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime2500",
   ["ZprimeToZhToZhadhtata_narrow_M-2500_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime3000",
   ["ZprimeToZhToZhadhtata_narrow_M-3000_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime3500",
   ["ZprimeToZhToZhadhtata_narrow_M-3500_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime4000",
   ["ZprimeToZhToZhadhtata_narrow_M-4000_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime4500",
   ["ZprimeToZhToZhadhtata_narrow_M-4500_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime600",
   ["ZprimeToZhToZhadhtata_narrow_M-600_13TeV-madgraph_v3_0000.xml"]],
  ["Zprime800",
   ["ZprimeToZhToZhadhtata_narrow_M-800_13TeV-madgraph_v3_0000.xml"]],

  ["RSGrav2500",
   ["RSGravTohhTohtatahbb_narrow_M-2500_13TeV-madgraph_v3_0000.xml"]],
  ["RSGrav3500",
   ["RSGravTohhTohtatahbb_narrow_M-3500_13TeV-madgraph_v3_0000.xml"]],

 

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
