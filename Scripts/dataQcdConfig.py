#! /usr/bin/python
# -*- coding: utf-8 -*-

inputPrefix="WHAnalysis."
inputPostfix=".root"

TargetLumi = 2470.0
weightHist = "Events"
sumWeightHist = "SumWeight"
inputDir = "${SFRAME_DIR}/../AnalysisOutput"
outputDir = "./plotsDataQCD"
systematic = ""


additionalScales = [
  ["QCDX", 0.7]
]

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
  "dataMCratio",
  #"yieldtable"
  ]

inputsamples = [
          #[ "identifier", ["list of input files"], constraint (-1 fixed, 0. free), "hist endings" ],
          [ "QCDX", QCDSamples, [""]],
          # [ "WJETSX", WSamples, ["%s_HFOR_isLightFlavor"%systematic] ],
          [ 'DATAX', ['JetHT74X'], [""] ]
          ]

samples = [
         #[ "name", ["list of subsamples"] ],
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


Histograms = []


MyHistNames = [
    ["cutflow", "cutflow", "cut", "Candidate Events"],
    ["vjet_pt", "V-jet p_{T}", "V-jet p_{T} [GeV]", "Candidate Events"],
    ["vjet_eta", "V-jet #eta", "V-jet #eta", "Candidate Events"],
    ["vjet_phi", "V-jet #phi", "V-jet #phi", "Candidate Events"],
    ["vjet_m", "V-jet m [GeV]", "V-jet m [GeV]", "Candidate Events"],
    ["vjet_mpruned", "V-jet m_{pruned}", "V-jet m_{pruned} [GeV]", "Candidate Events"],
    ["vjet_tau1", "V-jet #tau_{1}", "V-jet #tau_{1}", "Candidate Events"],
    ["vjet_tau2", "V-jet #tau_{2}", "V-jet #tau_{2}", "Candidate Events"],
    ["vjet_tau3", "V-jet #tau_{3}", "V-jet #tau_{3}", "Candidate Events"],
    ["vjet_tau21", "V-jet #tau_{21}", "V-jet #tau_{21}", "Candidate Events"], 
    ["vjet_tau31", "V-jet #tau_{31}", "V-jet #tau_{31}", "Candidate Events"], 
    ["vjet_tau32", "V-jet #tau_{32}", "V-jet #tau_{32}", "Candidate Events"], 
    ["vjet_nSubjets", "V-jet N subjets", "V-jet N subjets", "Candidate Events"],
    ["vjet_nTaggedSubjets", "V-jet N b-tagged subjets", "V-jet N b-tagged subjets", "Candidate Events"],
    ["vjet_subjet0_csv", "V-jet subjet_{1} CSV", "V-jet subjet_{1} CSV", "Candidate Events"],
    ["vjet_subjet1_csv", "V-jet subjet_{2} CSV", "V-jet subjet_{2} CSV", "Candidate Events"],

    ["hjet_pt", "H-jet p_{T}", "H-jet p_{T} [GeV]", "Candidate Events"],
    ["hjet_eta", "H-jet #eta", "H-jet #eta", "Candidate Events"],
    ["hjet_phi", "H-jet #phi", "H-jet #phi", "Candidate Events"],
    ["hjet_m", "H-jet m [GeV]", "H-jet m [GeV]", "Candidate Events"],
    ["hjet_mpruned", "H-jet m_{pruned}", "H-jet m_{pruned} [GeV]", "Candidate Events"],
    ["hjet_tau1", "H-jet #tau_{1}", "H-jet #tau_{1}", "Candidate Events"],
    ["hjet_tau2", "H-jet #tau_{2}", "H-jet #tau_{2}", "Candidate Events"],
    ["hjet_tau3", "H-jet #tau_{3}", "H-jet #tau_{3}", "Candidate Events"],
    ["hjet_tau21", "H-jet #tau_{21}", "H-jet #tau_{21}", "Candidate Events"], 
    ["hjet_tau31", "H-jet #tau_{31}", "H-jet #tau_{31}", "Candidate Events"], 
    ["hjet_tau32", "H-jet #tau_{32}", "H-jet #tau_{32}", "Candidate Events"], 
    ["hjet_nSubjets", "H-jet N subjets", "H-jet N subjets", "Candidate Events"],
    ["hjet_nTaggedSubjets", "H-jet N b-tagged subjets", "H-jet N b-tagged subjets", "Candidate Events"],
    ["hjet_subjet0_csv", "H-jet subjet_{1} CSV", "H-jet subjet_{1} CSV", "Candidate Events"],
    ["hjet_subjet1_csv", "H-jet subjet_{2} CSV", "H-jet subjet_{2} CSV", "Candidate Events"],

    ["jets_deta", "Jets #Delta #eta", "Jets #Delta #eta", "Candidate Events"],
    ["jets_dphi", "Jets #Delta #phi", "Jets #Delta #phi", "Candidate Events"],
    ["jets_dr", "Jets #Delta R", "Jets #Delta R", "Candidate Events"],

    ["dijet_pt", "dijet p_{T}", "dijet p_{T} [GeV]", "Candidate Events"],
    ["dijet_eta", "dijet #eta", "dijet #eta", "Candidate Events"],
    ["dijet_phi", "dijet #phi", "dijet #phi", "Candidate Events"],
    ["dijet_m", "dijet m", "dijet m [GeV]", "Candidate Events"],
    ["dijet_template_m", "dijet m", "dijet m [GeV]", "Candidate Events"],
    ]
    
# Histograms += [MyHistNames]
Histograms += [MyHistNames]
