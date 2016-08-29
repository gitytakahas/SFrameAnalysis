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
  ["ZH-1000", ["ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-1200", ["ZprimeToZhToZhadhbb_narrow_M-1200_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-1400", ["ZprimeToZhToZhadhbb_narrow_M-1400_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-1600", ["ZprimeToZhToZhadhbb_narrow_M-1600_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-1800", ["ZprimeToZhToZhadhbb_narrow_M-1800_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v2"]],
  ["ZH-2000", ["ZprimeToZhToZhadhbb_narrow_M-2000_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-2500", ["ZprimeToZhToZhadhbb_narrow_M-2500_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-3000", ["ZprimeToZhToZhadhbb_narrow_M-3000_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-3500", ["ZprimeToZhToZhadhbb_narrow_M-3500_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-4000", ["ZprimeToZhToZhadhbb_narrow_M-4000_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
  ["ZH-4500", ["ZprimeToZhToZhadhbb_narrow_M-4500_13TeV-madgraph_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2-v1"]],
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

