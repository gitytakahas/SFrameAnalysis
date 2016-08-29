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
  ["WH-1000", ["WprimeToWhToWhadhbb_narrow_M-1000_13TeV-madgraph"]],
  ["WH-1200", ["WprimeToWhToWhadhbb_narrow_M-1200_13TeV-madgraph"]],
  ["WH-1400", ["WprimeToWhToWhadhbb_narrow_M-1400_13TeV-madgraph"]],
  ["WH-1600", ["WprimeToWhToWhadhbb_narrow_M-1600_13TeV-madgraph"]],
  ["WH-1800", ["WprimeToWhToWhadhbb_narrow_M-1800_13TeV-madgraph"]],
  ["WH-2000", ["WprimeToWhToWhadhbb_narrow_M-2000_13TeV-madgraph"]],
  ["WH-2500", ["WprimeToWhToWhadhbb_narrow_M-2500_13TeV-madgraph"]],
  ["WH-3000", ["WprimeToWhToWhadhbb_narrow_M-3000_13TeV-madgraph"]],
  ["WH-3500", ["WprimeToWhToWhadhbb_narrow_M-3500_13TeV-madgraph"]],
  ["WH-4000", ["WprimeToWhToWhadhbb_narrow_M-4000_13TeV-madgraph"]],
  ["WH-4500", ["WprimeToWhToWhadhbb_narrow_M-4500_13TeV-madgraph"]],
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
outputTrees=["analysis"]

