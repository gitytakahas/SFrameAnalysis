path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="ST"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=1
hCPU="03:30:00"
hVMEM="5000M"
postFix = ""
label = "_ICHEP" #"_triggerless"
dataSets = [
                
#                [ "ST_tW_top_5f_NoFullyHadronicDecays"+label,
#                 [   "ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1_HLT1_0000.xml", ]],
               
               [ "ST_tW_top_5f_inclusiveDecays"+label,
                [   "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_HLT1_0000.xml", ]],
               
#                [ "ST_tW_antitop_5f_NoFullyHadronicDecays"+label,
#                 [   "ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1_HLT1_0000.xml", ]],
               
               [ "ST_tW_antitop_5f_inclusiveDecays"+label,
                [   "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_HLT1_0000.xml", ]],
               
               [ "ST_s-channel_4f_leptonDecays"+label,
                [   "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_HLT1_0000.xml", ]],
                    
#                [ "ST_t-channel_antitop_4f_inclusiveDecays"+label,
#                 [   "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_HLT1_0000_0.xml",
#                     "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_HLT1_0000_1.xml", ]],
                    
               [ "ST_t-channel_antitop_4f_leptonDecays"+label,
                [   "ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1_HLT1_0000.xml", ]],
                    
#                [ "ST_t-channel_top_4f_inclusiveDecays"+label,
#                 [   "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_HLT1_0000.xml", ]],
                    
               [ "ST_t-channel_top_4f_leptonDecays"+label,
                [   "ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1_HLT1_0000.xml", ]],
            
           ]

userItems = [ 
                ["IsData","false"],
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
