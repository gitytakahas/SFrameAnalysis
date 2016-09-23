loadLibs=[
  #"libGenVector",
    "libNtupleVariables",
    "libGoodRunsLists",
    "libPileupReweightingTool",
    "libBTaggingTools",
#    "libVHTausResonances",
    "libTauTauResonances",
    "libSVFit",
    "libScaleFactorTool",

  ]


loadPacks=[
    "SFrameCore.par",
    "NtupleVariables.par",
    "GoodRunsLists.par",
    "PileupReweightingTool.par",
    "BTaggingTools.par",
#    "VHTausResonances.par",
    "TauTauResonances.par",
    "SVFit.par",
    "ScaleFactorTool.par",
	   ]

compilePacks=[
  "../NtupleVariables",
  "../GoodRunsLists",
  "../PileupReweightingTool",
  "../BTaggingTools",
  "../SVFit",
#  "../VHTausResonances",
  "../TauTauResonances",
  "../LepEff2016",
  ]

AddUserItems = [
   #general settings
   ["RecoTreeName","tree"], 
#   ["JetPtCut", "120."]
   ]

#End
