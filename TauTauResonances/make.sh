#make distclean && make && sframe_main config/TauTauAnalysis_config_miniAODv1.xml 2>&1 | tee log
make distclean && make && sframe_main config/TauTauAnalysis_config_miniAODv2.xml 2>&1 | tee log
#sframe_main config/TauTauAnalysis_config_miniAODv2.xml 2>&1 | tee log