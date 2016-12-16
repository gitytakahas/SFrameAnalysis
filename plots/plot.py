# HTT Working TWiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016
from argparse import ArgumentParser
from math import sqrt, pow
import ROOT
from ROOT import TFile, TH1D, gDirectory, kAzure
import os, sys
import PlotTools
from PlotTools import Sample, Samples, Plot, Plot2D, color, warning, error, combineCuts
ROOT.gROOT.SetBatch(ROOT.kTRUE)



argv = sys.argv
description = '''This script make plots.'''
parser = ArgumentParser(description=description,epilog="Succes!")
parser.add_argument( "-c", "--category", dest="category", type=int, default=-1, action='store',
                     metavar="CATEGORY", help="only plot for this category of selection and cuts" )
parser.add_argument( "-l", "--list", dest="list", default=False, action='store_true',
                     help="list all available categories" )
args = parser.parse_args()



# SAMPLES
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_and_data_samples
OUT_DIR = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/")
PLOTS_DIR = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/plots/")
samplesB = [
            ("TT/", "TT_TuneCUETP8M1",                      "ttbar",                    831.76  ),
            ##("DY/", "DYJetsToLL_M-10to50_TuneCUETP8M1",     "Drell-Yan 10-50",        18610.0   ),
            ("DY/", "DYJetsToLL_M-10to50_nlo",              "Drell-Yan 10-50",    18610.0   ), # 18610 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("DY/", "DY1JetsToLL_M-10to50_nlo",             "Drell-Yan 1J 10-50 NLO",   421.5   ), # 421.5 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("DY/", "DY2JetsToLL_M-10to50_nlo",             "Drell-Yan 2J 10-50 NLO",   184.3   ), # 184.3 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("DY/", "DYJetsToLL_M-50_TuneCUETP8M1",         "Drell-Yan 50",            4954.0   ), # LO 4954.0; NLO 5765.4
            ("DY/", "DY1JetsToLL_M-50_TuneCUETP8M1",        "Drell-Yan 1J 50",         1012.5   ), 
            ("DY/", "DY2JetsToLL_M-50_TuneCUETP8M1",        "Drell-Yan 2J 50",          332.8   ), 
            ("DY/", "DY3JetsToLL_M-50_TuneCUETP8M1",        "Drell-Yan 3J 50",          101.8   ), 
            ("DY/", "DY4JetsToLL_M-50_TuneCUETP8M1",        "Drell-Yan 4J 50",           54.8   ), 
            ("WJ/", "WJetsToLNu_TuneCUETP8M1",              "W + jets",               50380.0   ), # LO 50380.0; NLO 61526.7
            ("WJ/", "W1JetsToLNu_TuneCUETP8M1",             "W + 1J",                  9644.5   ), 
            ("WJ/", "W2JetsToLNu_TuneCUETP8M1",             "W + 2J",                  3144.5   ), 
            ("WJ/", "W3JetsToLNu_TuneCUETP8M1",             "W + 3J",                   954.8   ), 
            ("WJ/", "W4JetsToLNu_TuneCUETP8M1",             "W + 4J",                   485.6   ), 
            ("WW/", "WW_TuneCUETP8M1",                      "WW",                        63.21  ), # 63.21  https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWW_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("WZ/", "WZ_TuneCUETP8M1",                      "WZ",                        22.82  ), # 10.71? https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ZZ/", "ZZ_TuneCUETP8M1",                      "ZZ",                        10.32  ), #  3.22? https://cmsweb.cern.ch/das/request?input=dataset%3D%2FZZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_tW_top_5f_inclusiveDecays",         "ST tW",                     35.60  ), #  38.09 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_tW_antitop_5f_inclusiveDecays",     "ST atW",                    35.60  ), #  38.09 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_t-channel_antitop_4f_leptonDecays", "ST t",                      80.95  ), #  80.95 TWiki # 80.95 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_t-channel_top_4f_leptonDecays",     "ST at",                    136.02  ), # 136.02 TWiki # 136.02 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal 
            ##("WW/", "WWTo1L1Nu2Q",                          "WW",                        1.212  ), # 1.212 TWiki # 45.85 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("WW/", "WWTo4Q_4f",                            "WW",                        45.31  ), # 45.31 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWWTo4Q_4f_13TeV_amcatnloFXFX_madspin_pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("ST/", "ST_tW_top_5f_NoFullyHadronicDecays",   "ST",                        38.09  ), # 
            ##("ST/", "ST_tW_antitop_5f_NoFullyHadronicDecays", "ST",                       0.00  ), # 
            ##("ST/", "ST_s-channel_4f_leptonDecays",         "ST",                        10.11  ), # 10.11 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("ST/", "ST_t-channel_antitop_4f_inclusiveDecays", "ST",                     80.95  ), # 80.95 https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM
            ##("ST/", "ST_t-channel_top_4f_inclusiveDecays",  "ST",                         0.00  ), # 
            ]
            
samplesS = [
                ("signal/", "LowMass_30GeV_DiTauResonance",     "signal",            400000.0  ),
            ]

samplesD = {
                "mutau"  :  [( "SingleMuon/",     "SingleMuon_Run2016",     "single muon"     )],
                #"eletau" :  [( "SingleElectron/", "SingleElectron_Run2016", "single electron" )],
            }
samples = [ ]


# LUMI
lumi = 12.9 #24.5
PlotTools.lumi = lumi


# LABELS
mylabel   = "_ICHEP" # extra label for opening file, saving plots to dir
plotlabel = "" #"_noWJrenomalization" #_DY_check" # extra label for png file


# PLOTS OPTIONS
stack       = True # COMPARE: set to false
normalizeWJ = len(samplesD) and stack and True
doQCD       = len(samplesD) and stack and True
doSigma     = True and False


# BLIND REGION
S_exp = 2.3 # expected number of signal events per category
blindlimits = { "m_vis":      (   0,  30),
                "m_sv" :      (  20,  36),
                "dR_ll" :     (   0, 1.2),
                #"pt_tt":     (  80, 200),
                #"pt_tt_sv":  (  80, 200),
                "R_pt_m_vis": ( 2.5,  10),
                "R_pt_m_sv":  ( 2.0,  10),  }
blindcuts   = { "m_vis":      "( m_vis < %i || %i < m_vis )"           % blindlimits["m_vis"],
                "m_sv" :      "( m_sv  < %i || %i < m_sv  )"           % blindlimits["m_sv" ],
                "dR_ll":      "%i < dR_ll"                             % blindlimits["dR_ll"][1],
                #"pt_tt"   :   "( pt_tt < %i || %i < pt_tt )"     % blindlimits["pt_tt"   ],
                #"pt_tt_sv":   "( pt_tt_sv < %i || %i < pt_tt_sv )"     % blindlimits["pt_tt_sv"],
                "R_pt_m_vis": "( R_pt_m_vis < %i || %i < R_pt_m_vis )" % blindlimits["R_pt_m_vis"],
                "R_pt_m_sv" : "( R_pt_m_sv  < %i || %i < R_pt_m_sv  )" % blindlimits["R_pt_m_sv" ], }


# CATEGORIES / SELECTIONS
isocuts     = "iso_1 < 0.15 && iso_2 == 1"
vetos       = "dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0 && " +\
                    "againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1"
category1   = "ncbtag > 0 && ncjets == 1 && nfjets  > 0"
category2   = "ncbtag > 0 && ncjets  > 1 && nfjets == 0 && dphi_ll_bj > 2 && met < 60"
metcut      = "met < 60"
mt1cut      = "pfmt_1 < 60"
signalwindow = "%i < m_sv && m_sv < %i" % blindlimits["m_sv"]
newcuts     = "%s && %s" % (metcut,mt1cut)
categories = [
                #("no cuts",             ""),
                #("isolation",           "%s" % (isocuts)),
                #("lepton vetos",        "%s" % (vetos)),
                #("iso, lepton vetos",   "%s && %s" % (isocuts, vetos)),
#                 ("iso, vetos, OS",      "%s && %s && q_1*q_2<0" % (isocuts, vetos)),
                #("iso, vetos, SS",      "%s && %s && q_1*q_2>0" % (isocuts, vetos)),
#                 ("category 1",          "%s && %s && q_1*q_2<0 && %s" % (isocuts, vetos, category1)),
#                 ("category 2",          "%s && %s && q_1*q_2<0 && %s" % (isocuts, vetos, category2)), # && met < 60
#                 ("category 1 met",      "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category1, metcut)),
#                 ("category 1 mt1",      "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category1, mt1cut)),
#                 ("category 2 mt1",      "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category2, mt1cut)),
#                 ("category 1 SR",       "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category1, signalwindow)),
#                 ("category 2 SR",       "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category2, signalwindow)), # && met < 60
#                 ("category 1 SR met",   "%s && %s && q_1*q_2<0 && %s && %s && %s" % (isocuts, vetos, category1, metcut, signalwindow)),
#                 ("category 1 SR mt1",   "%s && %s && q_1*q_2<0 && %s && %s && %s" % (isocuts, vetos, category1, mt1cut, signalwindow)),
#                 ("category 2 SR mt1",   "%s && %s && q_1*q_2<0 && %s && %s && %s" % (isocuts, vetos, category2, mt1cut, signalwindow)),
                ("category 1.2",        "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category1, newcuts)),
                ("category 2.2",        "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category2, mt1cut)),
              ]

    
# VARIABLES
variables = [
#                 ( "m_vis",         35, 0,  70 ),
                ( "m_sv",          35, 0,  70 ),
#                 ( "m_vis",         35, 0, 150 ),
#                 ( "m_sv",          35, 0, 150 ),
#                 ( "pt_tt",         50, 0, 160 ),
#                 ( "pt_tt_sv",      30, 0, 160 ),
#                 ( "dR_ll",         35, 0,   7 ),
#                 ( "R_pt_m_vis",    50, 0,   7 ),
#                 ( "R_pt_m_sv",     50, 0,   5 ),
#                 ( "pfmt_1",        30, 0, 150 ),
#                 ( "met",           30, 0, 120 ),
#                 ( "pt_1",          30, 0, 150 ),
#                 ( "gen_match_2",    8, 0,   8 ),
#                 ( "nbtag",          6, 0,   6 ),
#                 ( "njets",          6, 0,   6 ),
#                 ( "nfjets",         5, 0,   5 ),
#                 ( "ncjets",         5, 0,   5 ),
#                 ( "ncbtag",         5, 0,   5 ),
#                 ( "NUP",            6, 0,   6 ),
#                 ( "pol_2",         25, -1.1, 1.1 ),
#                 ( "mt_1",          40, 0, 200 ),
#                 ( "npu",           21, 0,  42 ),
#                 ( "npv",           21, 0,  42 ),
#                 ( "met_old",       30, 0, 120 ),
#                 ( "puppimet",      30, 0, 120 ),
#                 ( "mvamet",        30, 0, 120 ),
#                 ( "dphi_ll_bj",    30, 0, 4.5 ),
#                 ( "iso_1",         10, 0, 0.2 ),
#                 ( "byIsolationMVA3oldDMwLTraw_2", 10, 0.4, 1 ),
            ]
# for p in [ ("j",1), ("b",1), ("",1), ("",2), ("j",2), ("b",2) ]:
#     variables.append(( "%spt_%i" % p,       30,  0, 150 ))
#     ##variables.append(( "abs(%seta_%i)" % p, 25,  0,   5 ))
#     variables.append(( "%seta_%i" % p,      30, -3,   3 ))
# for n in [ "iso_2", "againstElectronVLooseMVA6_2", "againstMuonTight3_2" ]:
#     variables.append(( n,             2, 0,   2 ))
    
    
    
    
    
    ###############
    # stack plots #
    ###############

def plotStacks(channel, **kwargs):
    """Plot stacked histograms with data."""
    print header("%s channel: Stacks plots" % channel)
    
    DIR = kwargs.get('DIR',"%s/%s" % (PLOTS_DIR,channel))
    makeDirectory(DIR)
    
    label = mylabel
    treeName = "tree_%s" % channel
    for sample in samples: sample.treeName=treeName


    # LOOP over SELECTIONS
    for label, cuts in categories:
        print ">>>\n>>> " + color("_%s:_%s_" % (channel.replace(' ','_'),label.replace(' ','_')), color = "magenta")
        
        QCD = False
        if "q_1" in cuts and "q_2" in cuts and stack:
            QCD = True and doQCD
        
        
        # REMOVE DY LOW MASS for jet categories
        if "category" in label:
            for sample in samples:
                if ("Drell-Yan" in sample.label or "DY" in sample.label ) and "10-50" in sample.label:
                    samples.remove(sample)
                    if kAzure+5 in PlotTools.fillcolors: PlotTools.fillcolors.remove(kAzure+5)
                    print warning("Removed Drell Yan low mass and kAzure+5.")
        
        
        # RENORMALIZE WJ
        if normalizeWJ and "SS" not in label and "category" not in label:
            #renormcuts = "channel==%i && %s && %s && q_1*q_2<0" % (channeli, isocuts, vetos)
            plot = Plot( samples, "pfmt_1", 100, 80, 180, cuts=cuts, QCD=QCD, reset=True )
            plot.renormalizeWJ()
            plot.close()
        else:
            print warning("Not WJ renormalized! (normalizeWJ=%s, label=\"%s\")" % (normalizeWJ,label))
        
        
        # RESET
        norm = (not stack) and False # COMPARE: set to false to check normalization; True to check shape
        if not stack and norm:
            print warning("Resetting all scales and normalization")
            for sample in samples: sample.resetScalesAndWeights(weight="genweight")
        
        
        # LOOP over VARIABLES
        for var, nBins, a, b in variables:
        
        
            # NAME
            name = "%s/%s_%s%s.png" % (DIR,var,label,plotlabel)
            if "m_vis" == var or "m_sv" == var:
                name = "%s/%s_%i_%s%s.png" % (DIR,var,b,label,plotlabel)
            name = name.replace(" and ","-").replace(" ","").replace(",","-").replace("(","").replace(")","") #.replace("(","").replace(")","")
            
            
            # TITLE
            title = label
    
            
            # WEIGHT
            varweight = ""            
            
            
            # RENORMALIZE Signal
            s = 1
            if   "pt_tt" in var: s = 4
            elif "R_pt_" in var: s = 8
            if   ".2"    in label: s = 0.4
            for sample in samples:
                if sample.isSignal:
                    if "category" in label: sample.scale = sample.scaleBU * s #/ 118.3
                    else:                   sample.scale = sample.scaleBU * 20
            
            
            # BINS
            if "category" in label:
                if "m_vis" == var or "m_sv" == var:
                    a = 0
                    if "m_vis" is var: a = 2
                    if b < 110:
                        b = 76 + a
                        nBins = 19 #100
                    else: nBins = 25
                    print ">>> changed binning to (%i,%i,%i)" % (nBins,a,b)
            elif "m_vis" == var: #or "m_sv" is var:
                if b is 140:
                    a = 2
                    b = 140 + a
                    print ">>> changed binning to (%i,%i,%i)" % (nBins,a,b)
            #nBins = 100
            
            
            # LEGEND POSITION
            position = ""
            logy = False
            if "m_" in var or "iso_" in var or "against" in var:
                position = "Left"
                #if b == 120: position = "LeftLeft"
            if "R_" in var:
                position = "Right"
            if "Iso" in var: # or "NUP" in var:
                position += "Center"
            if "jeta_" in var or "beta_" in var or "NUP" in var:
                position += "Top"
            if "jpt_1" in var and "category" in label:
                position += "Left"
            if "gen_match" in var:
                position = "Left" + position
            
            
            # PLOT
            plot = Plot( samples, var, nBins, a, b, cuts=cuts, QCD=QCD) #, weight=varweight)
            plot.plot(stack=stack, position=position, title=title, staterror=stack, logy=logy, ratio=stack, norm=norm, errorbars=(not stack))
            checkSignal(plot)
            plotSignificance(plot)
            plot.saveAs(name)
            
            # RESET CUTS
#             if "m_vis" in var or "m_sv" in var:
#                 for sample in samples:
#                     if sample.isData: sample.cuts = ""
    
    
    
    
    
    ################
    # Extra checks #
    ################

def checkSignal(plot):
    """Check signal bump, signal region, signal yield, ..."""
    var = plot.var
    if (var in blindlimits or var in blindlimits) and plot.stack != None:
        for signal in plot.histsS:
            (aa,bb) = blindlimits[var]
            mu      = signal.GetMean()
            sd      = signal.GetStdDev()
            N       = signal.GetEntries()
            Sw      = signal.GetSumOfWeights()
            S       = plot.integrateHist(signal,aa,bb)
            B       = plot.integrateStack(aa,bb)
            print ">>> " + color("%.1f expected signal events (sum of weights) and %i MC events"    % (Sw,N), color="grey")
            print ">>> " + color("  signal mean = %.2f, sigma = %.2f"                               % (mu,sd), color="grey")
            print ">>> " + color("  thus 1-sigma signal region should be [ %4.1f, %4.1f ]"          % (mu-1*sd,mu+1*sd), color="grey")
            print ">>> " + color("  thus 2-sigma signal region should be [ %4.1f, %4.1f ]"          % (mu-2*sd,mu+2*sd), color="grey")
            #print ">>> " + color("  %.1f expected signal events (%.1f%%) in signal region %s(%i,%i)" % (S,100*S/Sw,var,aa,bb), color="grey")
            print ">>> " + color("  %.1f expected signal events compared to dimuon analysis"        % (S_exp), color="grey")
            print ">>> " + color("  %.1f expected background events in signal region %s(%i,%i)"     % (B,var,aa,bb), color="grey")
            if B:
                sigma = S_exp/(1+sqrt(B))
                print ">>> " + color("  %.2f expected significance in signal region %s(%i,%i)"          % (sigma,var,aa,bb), color="grey")
    

def plotSignificance(plot):
    """Plot significance."""
    if not doSigma: return
    
    var0 = plot.var
    variables_eff = [
                        ("m_vis",        20,   0, 140, True  ),
                        ("m_sv",         20,   0, 150, False ),
                        ("pfmt_1",       20,   0, 150, True  ),
                        ("mt_1",         20,   0, 150, True  ),
                        ("met",          20,   0, 120, True  ),
                        ("pt_tt",        20,   0, 120, False ),
                        ("pt_tt_sv",     20,   0, 150, False ),
                        ("dR_ll",        20,   0,   7, True  ),
                        ("R_pt_m_vis",   20,   0,   7, False ),
                        ("R_pt_m_sv",    20,   0,   5, False ),
                        ("pt_1",         20,   0, 150, False ),
                        ("pt_2",         20,   0, 150, False ),
                        ("bpt_1",        20,   0, 150, False ),
                        ("bpt_2",        20,   0, 150, False ),
                        ("jpt_1",        20,   0, 150, False ),
                        ("jpt_2",        20,   0, 150, False ),
                        ("dphi_ll_bj",   20,   0, 150, False ),
                    ]
    
    for var, nBins, a, b, upper in variables_eff:
        if var0 == var:
            #print ">>> " + color("making significance vs. cut value", color="grey")
            print ">>> making significance vs. cut value"
            plot.significanceScan(upper=upper)
    
    
    
    
    
    #####################
    # plot2DCorrelation #
    #####################

def plot2DCorrelation(channel, **kwargs):
    """Plot correlation between two variables into a 2D histograms."""
    print header("%s channel: 2D Correlation plots" % channel)
    
    DIR = kwargs.get('DIR',"%s/%s" % (PLOTS_DIR,channel))+"_2D"
    makeDirectory(DIR)
    
    label = mylabel
    variables2D = [ ]
    treeName = "tree_%s" % channel
    for sample in samples: sample.treeName=treeName
    
    
    # VARIABLES
    for s in [ "signal", "ttbar" ]:
        #variables2D.append(( s, "m_vis",    40, 0, 100, "pt_tt",     40, 0, 150 ))
        #variables2D.append(( s, "m_vis",    40, 0, 100, "dR_ll",     40, 0,   5 ))
        #variables2D.append(( s, "dR_ll",    40, 0,   5, "pt_tt",     40, 0, 150 ))
        variables2D.append(( s, "m_sv",     40, 0, 100, "pt_tt_sv",  40, 0, 150 ))
        variables2D.append(( s, "m_sv",     40, 0, 100, "dR_ll",     40, 0,   5 ))
#         variables2D.append(( s, "dR_ll",    40, 0,   5, "pt_tt_sv",  40, 0, 150 ))
#         variables2D.append(( s, "dR_ll",    40, 0,   5, "R_pt_m_sv", 40, 0,   5 ))
#         variables2D.append(( s, "pt_tt_sv", 40, 0, 150, "R_pt_m_sv", 40, 0,   5 ))
#         variables2D.append(( s, "m_sv",     40, 0, 100, "R_pt_m_sv", 40, 0,   5 ))
#         variables2D.append(( s, "met",      40, 0, 150, "pfmt_1",    40, 0, 150 ))
#         variables2D.append(( s, "met",      40, 0, 100, "R_pt_m_sv", 40, 0,   5 ))
#         variables2D.append(( s, "met",      40, 0, 100, "pt_tt_sv",  40, 0, 150 ))
#         variables2D.append(( s, "met",      40, 0, 100, "m_sv",      40, 0, 100 ))
#         variables2D.append(( s, "pfmt_1",   40, 0, 100, "R_pt_m_sv", 40, 0,   5 ))
#         variables2D.append(( s, "pfmt_1",   40, 0, 100, "pt_tt_sv",  40, 0, 150 ))
#         variables2D.append(( s, "pfmt_1",   40, 0, 100, "m_sv",      40, 0, 100 ))
        #variables2D.append(( s, "met",      40, 0, 150, "mvamet",    40, 0, 150 ))
        #variables2D.append(( s, "met",      40, 0, 150, "puppimet",  40, 0, 150 ))
        #variables2D.append(( s, "mvamet",   40, 0, 150, "puppimet",  40, 0, 150 ))
    
    
    # LOOP over SELECTIONS
    for label, cuts in categories:
        print ">>>\n>>> " + color("_%s:_%s_" % (channel.replace(' ','_'),label.replace(' ','_')), color = "magenta")

        # LOOP over VARIABLES
        for samplename, var1, nBins1, a1, b1, var2, nBins2, a2, b2 in variables2D:
            
            # NAME
            name = "%s/%s_vs_%s_%s_%s.png" % (DIR,var1,var2,samplename,label)
            name = name.replace(" and ","-").replace(" ","").replace(",","-").replace("(","").replace(")","")
            
            # GET SAMPLE
            sample = None
            for s in samples:
                if s.label == samplename:
                    sample = s
                    break
            else:
                print warning("Could not make 2D correlation plot: no sample with name \"%s\"!" % (samplename))
                continue

            plot2D = Plot2D(sample, var1, nBins1, a1, b1, var2, nBins2, a2, b2, cuts=cuts)
            plot2D.plot()
            plot2D.saveAs(name)
    
    
    
    
    
    ##########################
    # checkCutflowEfficiency #
    ##########################

def checkCutflowEfficiency(channel, **kwargs):
    """Check cutflow efficiency for a set of samples."""
    print header("%s channel: Checking cutflow" % channel)
    
    categories_dict = { "no cuts":              "",
                        "iso":                  "%s" % (isocuts),
                        "vetos":                "%s" % (vetos),
                        "iso, vetos":           "%s && %s" % (isocuts, vetos),
                        "iso, vetos, OS":       "%s && %s && q_1*q_2<0" % (isocuts, vetos),
                        "b jet":                "%s && %s && q_1*q_2<0 && ncbtag > 0" % (isocuts, vetos),
                        "category 1":           "%s && %s && q_1*q_2<0 && %s" % (isocuts, vetos, category1),
                        "category 2":           "%s && %s && q_1*q_2<0 && %s" % (isocuts, vetos, category2),
                        "category 1 met":       "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category1, metcut),
                        "category 1 mt1":       "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category1, mt1cut),
                        "category 2 met":       "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category2, metcut),
                        "category 2 mt1":       "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category2, mt1cut),
                        "category 1.2":         "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category1, newcuts),
                        "category 2.2":         "%s && %s && q_1*q_2<0 && %s && %s" % (isocuts, vetos, category2, newcuts),
                       }
    cutflows = [
#                     ("no cuts", "iso", "iso, vetos", "iso, vetos, OS", "category 1", "category 1.2"),
#                     ("no cuts", "iso", "iso, vetos", "iso, vetos, OS", "category 2", "category 2.2"),
#                     ("no cuts", "iso", "iso, vetos", "iso, vetos, OS", "b jet", "category 1", "category 1 met", "category 1.2"),
#                     ("no cuts", "iso", "iso, vetos", "iso, vetos, OS", "b jet", "category 2", "category 2 met", "category 2.2"),
#                     ("no cuts", "iso", "iso, vetos", "iso, vetos, OS", "b jet", "category 1", "category 1 mt1", "category 1.2"),
#                     ("no cuts", "iso", "iso, vetos", "iso, vetos, OS", "b jet", "category 2", "category 2 mt1", "category 2.2"),
                    ("category 1", "category 1 mt1", "category 1.2"),
                    ("category 2", "category 2 mt1", "category 2.2"),
                ]
                
    samplenames = [ "signal",
                    #"ttbar"
                  ]
    
    # LOOP over VARIABLES
    for samplename in samplenames:
        print ">>> cutting on %s:" % (samplename)
                                
        # GET SAMPLE
        sample = None
        for s in samples:
            if s.label == samplename:
                sample = s
                break
        else:
            print warning("Could not calculate cutflow efficiency: no sample with name \"%s\"!" % (samplename), prepend="  ")
            continue
            
        # LOOP over dictionary
        yield_dict = { }
        for label in categories_dict:
            cuts = combineCuts("m_vis > 0",categories_dict[label])        
            name    = "m_vis_for_cutflow_eff"
            hist    = sample.hist("m_vis",100,0,250,cuts=cuts,name=name)
            N       = hist.GetSumOfWeights()
            MC      = hist.GetEntries()
            yield_dict[label] = (N,MC)
            gDirectory.Delete(name)
    
        # LOOP over CUTFLOWS and their respective SELECTIONS
        for cutflow in cutflows:
            print ">>>\n>>> %20s %10s %10s %12s %12s" % ("selection".ljust(16),"rel eff","abs eff","yield","MC events")
            N0 = 0
            N_last = 0
            for label in cutflow:
                if label not in yield_dict: warning("Label not found in categories_dict!")
                (N,MC)      = yield_dict[label]
                if not N0 and N:
                    N0      = N
                    N_last  = N
                if N_last and N0:
                    print ">>> %20s %9.2f%% %9.2f%% %12.2f %12.1f" % (label.ljust(18), 100.0*N/N_last, 100.0*N/N0, N, MC)
                if not N:
                    print ">>> zero events left: stop!"
                    break
                N_last = N
        
        print ">>>\n>>> "





    #############
    # getScales #
    #############

def getScales():
    """Calculate and set the normalization scales. Then save and list the samples with their respective cross section."""
    
    print ">>> samples with integrated luminosity L = %s / fb at sqrt(s) = 13 TeV" % lumi
    print ">>> "
    print ">>> %12s  %12s  %26s  %18s  %12s" % ("events", "sum weights", "sample".ljust(22), "cross section (pb)", "norm. scale" )
    global samples
    weight = "weight" #(gen_match_2==5 ? 1.056 : 1.) #puweight*genweight*trigweight_1*idweight_1*isoweight_1
    treeName = "tree_mutau"
    
    # BACKGROUND
    for i, (subdir, sampleName, name, sigma) in enumerate(samplesB):
        filename        = OUT_DIR + subdir + "TauTauAnalysis.%s%s.root" % (sampleName,mylabel)
        file            = TFile( filename )
        N_tot           = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(7)
        N_tot_unweighted = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        scale           = lumi * sigma * 1000 / N_tot
        weightB         = weight
        #if "DYJetsToLL_M-10to50_nlo" in sample: weightB = "%s*%s" % (weightB,"(NUP==1 ? 0 : 1)*(NUP==2 ? 0 : 1)")
        sample = Sample( filename, name, sigma=sigma, N=N_tot, scale=scale, background=True, cuts="channel>0", weight=weightB, treeName=treeName )
        samples.append(sample)
        samplesB[i]     = sample
        print ">>> %12i  %12i  %26s  %18.2f  %12.2f" % (N_tot,N_tot_unweighted,name.ljust(22),sigma,scale)
    
    # BACKGROUND READD for stitch comparison
#     for dir, sample, name, N_tot, sigma, scale in samplesB:
#         if "DYJetsToLL_M-10to50_nlo" not in sample: continue
#         file = OUT_DIR + dir + "TauTauAnalysis.%s%s.root" % (sample,label)
#         weightB = weight
#         name += " incl. only"
#         samples.append(Sample( file, name, sigma=sigma, N=N_tot, scale=scale, background=True, cuts="", weight=weightB, treeName=treeName ))
    
    
    # SIGNAL
    # TODO normalize with expected signal yield, using as selected MC events at category 1 + category 2 stage
    for i, (subdir, sampleName, name, N_exp) in enumerate(samplesS):
        filename        = OUT_DIR + subdir + "TauTauAnalysis.%s%s.root" % (sampleName,mylabel)
        file            = TFile( filename )
        N_tot           = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(7)
        N_tot_unweighted = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        sample = Sample( filename, name, sigma=sigma, N=N_tot, signal=True, cuts="channel>0", weight=weight, treeName=treeName )
        scale           = signalNormalization(sample) * 120 #N_exp / N_tot
        sample.scale    = scale  
        sample.scaleBU  = scale
        samples.append(sample)
        samplesS[i]     = sample
        print ">>> %12i  %12i  %26s  %18.2f  %12.2f" % (N_tot,N_tot_unweighted,name.ljust(22),sigma,scale)
        
        
    # DATA
    for channel, s in samplesD.items():
        (subdir, sampleName, name) = s[0]
        filename        = OUT_DIR + subdir + "TauTauAnalysis.%s%s.root" % (sampleName,mylabel)
        file            = TFile( filename )
        N_tot           = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(7)
        N_tot_unweighted = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        sample = Sample( filename, name, data=True, cuts ="channel>0", treeName=treeName, blind=blindcuts )
        samples.append(sample)
        print ">>> %12i  %12i  %26s  %21s" % ( N_tot, N_tot_unweighted, name.ljust(22), "L = %5.2f/fb" % lumi )
    
    
    # BACKGROUND MERGE
    samples = mergeSamples(samples,"ST")
    samples = mergeSamples(samples,["WW","WZ","ZZ"],name="diboson")
    samples = stitchSamples(samples,"WJ",name_incl="WJets")
    #samples = mergeSamples(samples,"DY",label="M-10to50_nlo",name="Drell-Yan 10-50 NLO")
    samples = stitchSamples(samples,"DY",label="M-50")


def signalNormalization(sample,S_exp=S_exp):
    """Calculates normalization for a given expected signal yield."""
    
    categories_exp = [  ("category 1", "%s && %s && q_1*q_2<0 && %s" % (isocuts, vetos, category1)),
                        ("category 2", "%s && %s && q_1*q_2<0 && %s" % (isocuts, vetos, category2)), ]        
    N  = 0 
    MC = 0
    for label, cuts in categories_exp:
        cuts    = combineCuts("m_vis > 0", cuts)
        name    = "m_vis_for_signal_renormalization"
        hist    = sample.hist("m_vis",100,0,250,cuts=cuts,name=name)
        N       += hist.GetSumOfWeights()
        MC      += hist.GetEntries()
        gDirectory.Delete(name)
    
    #print "S_exp/N = %.2f / %.2f = %.4f" % (S_exp,N,S_exp/N)
    if N: return S_exp / N
    else:
        print warning("Could not find normalization for signal: no MC events in category 1 or 2!")
        return 1
    
    
    
    
    
    
    ######################
    # Stitching & Mergin #
    ######################

def mergeSamples(sample_list,names,**kwargs):
    """Merge samples"""
    
    if not isinstance(names,list): names = [names]
    name0       = kwargs.get('name',names[0]) #+ " merged"
    signal      = kwargs.get('signal',False)
    background  = kwargs.get('background',True) and not signal
    label       = kwargs.get('label',"")
    samples     = Samples(name0, background=background, signal=signal)
    print ">>>\n>>> merging %s: merge samples" % (name0)
    
    # get samples containing names and label
    merge_list = [ ]
    for name in names:
        merge_list += [ s for s in sample_list if s.isPartOf(name,label) ]
    
    # check if sample list of contains to-be-stitched-sample
    if len(merge_list) < 2:
        print warning("Could not stitch %s: less than two %s samples" % (name0,name0))
        return sample_list
    fill = max([ len(s.label) for s in merge_list ])
    
    # add samples with name0 and label
    for sample in merge_list:
        print ">>>   merging %s to %s: %s" % (sample.label.ljust(fill),name0,sample.filenameshort)
        samples.add(sample)
    
    # remove merged samples from sample_list
    if samples.samples:
        sample_list.append(samples)
        for sample in samples.samples: sample_list.remove(sample)
    
    return sample_list
    

def stitchSamples(sample_list,name0,**kwargs):
    """Stitching samples: merge samples
       and reweight inclusive sample and rescale jet-binned samples"""
    print ">>>\n>>> stiching %s: rescale, reweight and merge samples" % (name0)
    # see /shome/ytakahas/work/TauTau/SFrameAnalysis/TauTauResonances/plot/config.py
    # DY cross sections  5765.4 [  4954.0, 1012.5,  332.8, 101.8,  54.8 ]
    # WJ cross sections 61526.7 [ 50380.0, 9644.5, 3144.5, 954.8, 485.6 ]
    
    sigmasLO =  { "DY": { "M-50": 4954.0, "M-10to50_nlo": 18610.0 }, "WJ": { "": 50380.0 } }
    sigmasNLO = { "DY": { "M-50": 5765.4, "M-10to50_nlo": 18610.0 }, "WJ": { "": 61526.7 } }
    
    #name0       = "DY" #"WJ"
    label_incl  = kwargs.get('label_incl',"Jets")
    name_incl   = kwargs.get('name_incl',name0+label_incl)
    label       = kwargs.get('label',"") # extra search term
    sigmaLO     = sigmasLO[name0][label]
    kfactor     = sigmasNLO[name0][label] / sigmaLO
    N_incl      = 0
    weights     = [ ]
    stitch_list = [ s for s in sample_list if s.isPartOf(name0,label) ]
    print ">>>   %s k-factor = %.2f" % (name0, kfactor)
    
    # check if sample list of contains to-be-stitched-sample
    if len(stitch_list) < 2:
        print warning("Could not stitch %s: less than two %s samples" % (name0,name0))
        for s in stitch_list: print ">>>   %s" % s.label
        return sample_list
    fill        = max([ len(s.label) for s in stitch_list ])
    name        = kwargs.get('name',stitch_list[0].label)
    
    # set renormalization scales with effective luminosity
    for sample in stitch_list:
        
        N_tot   = sample.N
        sigma   = sample.sigma
        N       = N_tot
        
        if name_incl in sample.filename:
            N_incl = N_tot
        elif not N_incl:
            print warning("Could not stitch %s: N_incl == 0!" % name0)
            return sample_list
        else:
            N = N_tot + N_incl*sigma/sigmaLO # effective luminosity
        
        scale = lumi * kfactor * sigma * 1000 / N
        weights.append("(NUP==%i ? %s : 1)" % (len(weights),scale))
        print ">>>   stitching %s with scale %5.2f and cross section %7.2f pb" % (sample.label.ljust(fill), scale, sigma)
        #print ">>> weight.append(%s)" % weights[-1]
        
        if name_incl in sample.filename: sample.scale = 1.0   # apply renormalization scale with weights
        else:                            sample.scale = scale # apply renormalization scale
    
    # set weight of inclusive sample
    for sample in stitch_list:
        if sample.isPartOf(name_incl,label):
            sample.scale = 1.0
            sample.addWeight("*".join(weights))
    
    # merge
    return mergeSamples(sample_list,name0,label=label, name=name)
    
    
    
    
    
    ##################
    # Help functions #
    ##################

def header(header):
    """Returns formatted header"""
    
    return ( ">>>\n>>>\n" +
             ">>>   ###%s\n"    % ('#'*(len(header)+3)) +
             ">>>   #  %s  #\n" % (header) +
             ">>>   ###%s\n"    % ('#'*(len(header)+3)) +
             ">>>" )


def makeDirectory(DIR):
    """Make directory if it does not exist."""
    
    if not os.path.exists(DIR):
        os.makedirs(DIR)
        print ">>> made directory " + DIR
    
    
    
    
    
    ##############
    # Categories #
    ##############

def listCategories():
    """List all available categories"""

    print ">>> list of available categories:"
    for name, cuts in categories:
        print ">>>\t%s" % name
    print ">>>\t"
    
    
def selectCategory(category):
    """Only run for this category"""

    global categories
        
    if -1 < category < len(categories) and category == round(category):
        print ">>> select selection category %i" % category
        categories = [categories[category]]
    else:
        print error("Category %i does not exist!" % category)
        sys.exit(1)
    
    
    
    
    
    ########
    # main #
    ########

def main():
    """Main function."""
    
    if args.list:
        listCategories()
        return
    
    getScales()
    
    if args.category > -1:
        selectCategory(args.category)
        
    for channel in [ "mutau",
                     #"eletau",
                    ]:
        
        # make directories
        dirlabel = mylabel #"_69p2mb"#_noSF"
        DIR = PLOTS_DIR+channel+dirlabel
        
        plotStacks(channel,DIR=DIR)
#         plot2DCorrelation(channel,DIR=DIR)
#         checkCutflowEfficiency(channel)




if __name__ == '__main__':
    print
    main()
    print ">>>\n>>> Done with this, son.\n"




