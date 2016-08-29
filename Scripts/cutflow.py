#! /usr/bin/python
# -*- coding: utf-8 -*-

inputPrefix="WHAnalysis."
inputPostfix=".root"

TargetLumi = 2600.0
weightHist = "Events"
sumWeightHist = "SumWeight"
inputDir = "${SFRAME_DIR}/../AnalysisOutput"
outputDir = "./plotsDataQCD"
systematic = ""


QCDSamples = [
                 "QCD_HT100to200", 
                 "QCD_HT200to300",
                 "QCD_HT300to500",
                 "QCD_HT500to700",
                 "QCD_HT700to1000",
                 "QCD_HT1000to1500",
                 "QCD_HT1500to2000",
                 "QCD_HT2000toInf"
          ]


plotTypes = [
  "dataMC", 
  #"dataMCratio", 
  #"yieldtable"
  ]

inputsamples = [
          #[ "identifier", ["list of input files"], constraint (-1 fixed, 0. free), "hist endings" ],
          [ "WH2000X", ['WH-2000'], [""]],
          [ "ZH2000X", ['ZH-2000'], [""]],
          [ "QCDX", QCDSamples, [""]],
          # [ "WJETSX", WSamples, ["%s_HFOR_isLightFlavor"%systematic] ],
          [ 'DATAX', ['JetHT74X'], [""] ]
          ]

samples = [
         #[ "name", ["list of subsamples"] ],
          [ "WH-2000", ["WH2000X"] ],
          [ "QCD", ["QCDX"] ],
          # [ "WJETS", ["WJETSX"] ],
          [ "DATA", ["DATAX"] ],
]


categories = ["VWindow_NoTau21_SubjetPreTag",
      "VWindow_NoTau21_SubjetNoTag",
      "VWindow_NoTau21_SubjetSingleTagIncl",
      "VWindow_NoTau21_SubjetSingleTagExcl",
      "VWindow_NoTau21_SubjetDoubleTag",
  
      "VWindow_Tau21LP_SubjetPreTag",
      "VWindow_Tau21LP_SubjetNoTag",
      "VWindow_Tau21LP_SubjetSingleTagIncl",
      "VWindow_Tau21LP_SubjetSingleTagExcl",
      "VWindow_Tau21LP_SubjetDoubleTag",
      "WWindow_Tau21LP_SubjetPreTag",
      "WWindow_Tau21LP_SubjetNoTag",
      "WWindow_Tau21LP_SubjetSingleTagIncl",
      "WWindow_Tau21LP_SubjetSingleTagExcl",
      "WWindow_Tau21LP_SubjetDoubleTag",
      "ZWindow_Tau21LP_SubjetPreTag",
      "ZWindow_Tau21LP_SubjetNoTag",
      "ZWindow_Tau21LP_SubjetSingleTagIncl",
      "ZWindow_Tau21LP_SubjetSingleTagExcl",
      "ZWindow_Tau21LP_SubjetDoubleTag",
  
      "VWindow_Tau21HP_SubjetPreTag",
      "VWindow_Tau21HP_SubjetNoTag",
      "VWindow_Tau21HP_SubjetSingleTagIncl",
      "VWindow_Tau21HP_SubjetSingleTagExcl",
      "VWindow_Tau21HP_SubjetDoubleTag",
      "WWindow_Tau21HP_SubjetPreTag",
      "WWindow_Tau21HP_SubjetNoTag",
      "WWindow_Tau21HP_SubjetSingleTagIncl",
      "WWindow_Tau21HP_SubjetSingleTagExcl",
      "WWindow_Tau21HP_SubjetDoubleTag",
      "ZWindow_Tau21HP_SubjetPreTag",
      "ZWindow_Tau21HP_SubjetNoTag",
      "ZWindow_Tau21HP_SubjetSingleTagIncl",
      "ZWindow_Tau21HP_SubjetSingleTagExcl",
      "ZWindow_Tau21HP_SubjetDoubleTag",
      
      # low sideband for V boson
      "VLowSB_NoTau21_SubjetPreTag",
      "VLowSB_NoTau21_SubjetNoTag",
      "VLowSB_NoTau21_SubjetSingleTagIncl",
      "VLowSB_NoTau21_SubjetSingleTagExcl",
      "VLowSB_NoTau21_SubjetDoubleTag",
  
      "VLowSB_Tau21LP_SubjetPreTag",
      "VLowSB_Tau21LP_SubjetNoTag",
      "VLowSB_Tau21LP_SubjetSingleTagIncl",
      "VLowSB_Tau21LP_SubjetSingleTagExcl",
      "VLowSB_Tau21LP_SubjetDoubleTag",
  
      "VLowSB_Tau21HP_SubjetPreTag",
      "VLowSB_Tau21HP_SubjetNoTag",
      "VLowSB_Tau21HP_SubjetSingleTagIncl",
      "VLowSB_Tau21HP_SubjetSingleTagExcl",
      "VLowSB_Tau21HP_SubjetDoubleTag",
  
      # low sideband for Higgs boson
      "VWindow_HLowSB_NoTau21_SubjetPreTag",
      "VWindow_HLowSB_NoTau21_SubjetNoTag",
      "VWindow_HLowSB_NoTau21_SubjetSingleTagIncl",
      "VWindow_HLowSB_NoTau21_SubjetSingleTagExcl",
      "VWindow_HLowSB_NoTau21_SubjetDoubleTag",
  
      "WWindow_HLowSB_Tau21LP_SubjetPreTag",
      "WWindow_HLowSB_Tau21LP_SubjetNoTag",
      "WWindow_HLowSB_Tau21LP_SubjetSingleTagIncl",
      "WWindow_HLowSB_Tau21LP_SubjetSingleTagExcl",
      "WWindow_HLowSB_Tau21LP_SubjetDoubleTag",
  
      "ZWindow_HLowSB_Tau21HP_SubjetPreTag",
      "ZWindow_HLowSB_Tau21HP_SubjetNoTag",
      "ZWindow_HLowSB_Tau21HP_SubjetSingleTagIncl",
      "ZWindow_HLowSB_Tau21HP_SubjetSingleTagExcl",
      "ZWindow_HLowSB_Tau21HP_SubjetDoubleTag",
    
    
    ]

cuts = [
  
  "BeforeCuts",            # C0
  "JSON",                  # C1
  "Trigger",               # C2
  "MetFilters",            # C3
  "TwoFatJets",            # C4
  "FatJetsDeltaEta",       # C5
  "DijetMass",             # C6
  "VWindow",               # C7
  "HiggsWindow",           # C8
  "Tau21",                 # C9
  "SubjetSingleTag",       # C10
  "SubjetDoubleTag"        # C11
  
]


Cutflow = []


MyHistNames = [
    ["cutflow", "cutflow", "cut", "Candidate Events"],
    ]
    
# Histograms += [MyHistNames]
Cutflow += [MyHistNames]
