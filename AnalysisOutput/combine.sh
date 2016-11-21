#!/bin/bash

L="_ICHEP"
ls -l SingleMuon/TauTauAnalysis.SingleMuon*

hadd -f SingleMuon/TauTauAnalysis.SingleMuon_Run2016${L}.root SingleMuon/TauTauAnalysis.SingleMuon_?_Run2016${L}.root
#rm SingleMuon/TauTauAnalysis.SingleMuon_?_Run2016.root

#hadd -f SingleMuon/SingleMuon_Run2016_mutau.root  SingleMuon/SingleMuon_Run2016_?_mutau.root
#hadd -f SingleMuon/SingleMuon_Run2016_eletau.root SingleMuon/SingleMuon_Run2016_?_eletau.root
#rm SingleMuon/SingleMuon_Run2016_?_*.root

#hadd -f SingleMuon/SingleMuon_Run2016_triggerless_mutau.root  SingleMuon/SingleMuon_Run2016_triggerless_?_mutau.root
#hadd -f SingleMuon/SingleMuon_Run2016_triggerless_eletau.root SingleMuon/SingleMuon_Run2016_triggerless_?_eletau.root
#rm SingleMuon/SingleMuon_Run2016_triggerless_?_*.root


