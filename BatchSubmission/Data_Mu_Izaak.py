path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="SingleMuon_v2"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=1
hCPU="05:00:00"
hVMEM="5000M"
postFix = ""
label = "_ICHEP" #"_triggerless"
dataSets = [
               ["SingleMuon_1_Run2016"+label,
                [   "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0000_0.xml",
                    "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0000_1.xml",
                    "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0000_2.xml",
                    "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0001_0.xml",
                    "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0001_1.xml",
                    "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0001_2.xml",
                    "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0002_0.xml", ]],
                    
               ["SingleMuon_2_Run2016"+label,
                [   "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0002_1.xml",
                    "SingleMuon_Run2016C-PromptReco-v2_24p47fb_v2_0000_0.xml",
                    "SingleMuon_Run2016C-PromptReco-v2_24p47fb_v2_0000_1.xml",
                    "SingleMuon_Run2016C-PromptReco-v2_24p47fb_v2_0000_2.xml",
                    "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0000_0.xml",
                    "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0000_1.xml", ]],
                    
               ["SingleMuon_3_Run2016"+label,
                [   "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0000_2.xml",
                    "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0001_0.xml",
                    "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0001_1.xml",
                    "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_0.xml",
                    "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_1.xml",
                    "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_2.xml",
                    "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0001.xml",   ]],
                    
               ["SingleMuon_4_Run2016"+label,
                [   "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_0.xml",
                    "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_1.xml",
                    "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_2.xml",
                    "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_0.xml",
                    "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_1.xml",
                    "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_2.xml",
                    "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0001.xml",   ]],
                     
#                ["SingleMuon_Run2016"+label+"_1",
#                 [    "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0000_0.xml",
#                      "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0000_1.xml",
#                      "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0001_0.xml",
#                      "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0001_1.xml",
#                      "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0002_0.xml",
#                      "SingleMuon_Run2016B-PromptReco-v2_24p47fb_v2_0002_1.xml",
#                      "SingleMuon_Run2016C-PromptReco-v2_24p47fb_v2_0000_0.xml",
#                      "SingleMuon_Run2016C-PromptReco-v2_24p47fb_v2_0000_1.xml",
#                      "SingleMuon_Run2016C-PromptReco-v2_24p47fb_v2_0000_2.xml",
#                      "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0000_0.xml",
#                      "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0000_1.xml",
#                      "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0000_2.xml",
#                      "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0000_3.xml",
#                      "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0001_0.xml", ]],
#                      
#                ["SingleMuon_Run2016"+label+"_2",
#                 [   "SingleMuon_Run2016D-PromptReco-v2_24p47fb_v2_0001_1.xml",
#                      "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_0.xml",
#                      "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_1.xml",
#                      "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_2.xml",
#                      "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_3.xml",
#                      "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0000_4.xml",
#                      "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0001_0.xml",
#                      "SingleMuon_Run2016E-PromptReco-v2_24p47fb_v2_0001_1.xml",
#                      "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_0.xml",
#                      "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_1.xml",
#                      "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_2.xml",
#                      "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_3.xml",
#                      "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_4.xml",
#                      "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_5.xml", ]],
#                      
#                ["SingleMuon_Run2016"+label+"_3",
#                 [   "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_6.xml",
#                      "SingleMuon_Run2016F-PromptReco-v1_24p47fb_v2_0000_7.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_0.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_1.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_2.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_3.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_4.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_5.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_6.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_7.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0000_8.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0001_0.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0001_1.xml",
#                      "SingleMuon_Run2016G-PromptReco-v1_24p47fb_v2_0001_2.xml", ]],
           ]

userItems = [ 
                ["IsData","true"],
                ["IsSignal","false"],
                ["doSVFit","false"],
                ["OutputTreeName_mutau", "tree_mutau" ],
                ["OutputTreeName_eletau","tree_eletau"],
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
outputTrees=["tree_mutau","tree_eletau"]
