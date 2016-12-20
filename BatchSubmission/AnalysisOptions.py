loadLibs=[
    #"libGenVector",
    "libNtupleVariables",
    "libGoodRunsLists",
    "libPileupReweightingTool",
    "libBTaggingTools",
    "libTauTauResonances",
    "libSVFitTool",
    "libScaleFactorTool",
    "libRecoilCorrector",

  ]


loadPacks=[
    "SFrameCore.par",
    "NtupleVariables.par",
    "GoodRunsLists.par",
    "PileupReweightingTool.par",
    "BTaggingTools.par",
    "TauTauResonances.par",
    "SVFitTool.par",
    "ScaleFactorTool.par",
    "RecoilCorrector.par",
	   ]

compilePacks=[
    "../NtupleVariables",
    "../GoodRunsLists",
    "../PileupReweightingTool",
    "../BTaggingTools",
    "../SVFitTool",
    "../TauTauResonances",
    "../LepEff2016",
    "../RecoilCorrections",
  ]

AddUserItems = [
    #general settings
    ["RecoTreeName","tree"], 
    ["doSVFit","true"],
  ]

#End
