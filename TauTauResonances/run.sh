#make distclean && make && sframe_main config/TauTauAnalysis_config_miniAODv2.xml 2>&1 | tee log
#make distclean && make && sframe_main config/TauTauAnalysis_config_SingleMuon.xml
#make distclean && make && sframe_main config/WJetsToLNu.xml
#make distclean && make && sframe_main config/DYJets_M-10to50.xml
#make distclean && make && sframe_main config/DYJets_M-50.xml
make distclean && make && sframe_main config/Signal.xml
#make distclean && make && sframe_main config/SingleMuon.xml
#make distclean && make && sframe_main config/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1.xml

