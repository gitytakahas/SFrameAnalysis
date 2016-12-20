path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="WW"
outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=4
hCPU="03:30:00"
hVMEM="5000M"
postFix = ""
label = "_ICHEP_sorting" #"_triggerless"
dataSets = [
                
#                [ "WWTo1L1Nu2Q"+label,
#                 [   "WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_HLT1_0000.xml", ]],
                    
#                [ "WWTo4Q_4f"+label,
#                 [   "WWTo4Q_4f_13TeV_amcatnloFXFX_madspin_pythia8_HLT1_0000_0.xml",
#                     "WWTo4Q_4f_13TeV_amcatnloFXFX_madspin_pythia8_HLT1_0000_1.xml",
#                     "WWTo4Q_4f_13TeV_amcatnloFXFX_madspin_pythia8_HLT1_0000_2.xml", ]],
                    
               [ "WW_TuneCUETP8M1"+label,
                [   "WW_TuneCUETP8M1_13TeV-pythia8_HLT1_0000.xml", ]],
                    
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","false"],
                #["doSVFit","true"],
                ["doRecoilCorr","false"],
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
