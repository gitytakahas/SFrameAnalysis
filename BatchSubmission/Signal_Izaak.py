path2xml="$SFRAME_DIR/../BatchSubmission/xmls_Izaak"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
jobName="signal"
#outDir="$SFRAME_DIR/../AnalysisOutput/" + jobName
outDir="/scratch/$USER/analysis/AnalysisOutput/" + jobName
cycleName="TauTauAnalysis"
nEventsMax=-1
#nEventsMax=200
nProcesses=1
nFiles=1
hCPU="03:00:00"
hVMEM="5000M"
postFix = "_ICHEP" #_onlycrosstrigger" #"_triggerless" # _nocuts
dataSets = [
                ["LowMass_30GeV_DiTauResonance",
                 [  #"LowMass_30GeV_DiTauResonance_RunIISpring16MiniAODv2_asymptotic_miniAODv2.xml",
                    "LowMass_30GeV_DiTauResonance_RunIISpring16MiniAODv2_asymptotic_miniAODv2_short.xml",
                     ]],
           ]

userItems = [ 
                ["IsData","false"],
                ["IsSignal","true"],
                #["doSVFit","true"],
                ["doRecoilCorr","false"],
                ["doTES","false"],
                ["TESshift","0.00"],
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
