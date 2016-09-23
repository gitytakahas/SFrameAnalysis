# SFrameAnalysis

Repository using submodules for ntuple-based analysis (at PSI T3).

## Getting started

You need ROOT or CMSSW to get started, here CMSSW will be used, and the installation will be done into a new directory:
```
mkdir Analysis
cd Analysis
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_8_0_20
cd CMSSW_8_0_20/src
cmsenv
cd ../..
```
Then get this repository, before fork of it and then:
```
git clone https://github.com/gitytakahas/SFrameAnalysis
git checkout -b my_branch
cd SFrameAnalysis
source init.sh
```
To execute the analysis and get the final tree, 
```
cd TauTauResonances/
sframe_main config/TauTauAnalysis_config_miniAODv2.xml
```
This will give you Myroot_mutau.root and Myroot_eletau.root, which includes all the necessary variables for the analysis
