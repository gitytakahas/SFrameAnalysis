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
  ["QCD_Pt_1000to1400", ["QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_120to170", ["QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_1400to1800", ["QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_170to300", ["QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_1800to2400", ["QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_2400to3200", ["QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_300to470", ["QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_30to50", ["QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_470to600", ["QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_50to80", ["QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_600to800", ["QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_800to1000", ["QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8"]],
  ["QCD_Pt_80to120", ["QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8"]],
  ]

userItems = [
   ["IsData","false"],
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

