#! /usr/bin/python
# -*- coding: utf-8 -*-

path2xml="$SFRAME_DIR/../BatchSubmission/xmls"
path2tmp="$SFRAME_DIR/../AnalysisTemp"
outDir="$SFRAME_DIR/../AnalysisOutput"
jobName="b2gVHJob"
cycleName="VHAnalysis"
nEventsMax=-1
nProcesses=2
nFiles=10
hCPU="00:30:00"
hVMEM="3000M"
postFix = ""

dataSets=[
  ["JetHT74X", ["JetHT_Run2015C_25ns_05Oct2015-v1", "JetHT_Run2015D_05Oct2015-v1", "JetHT_Run2015D_PromptReco-v4"]],
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
outputTrees=["analysis"]

