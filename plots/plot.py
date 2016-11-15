# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016
from argparse import ArgumentParser
import ROOT
from ROOT import TFile, TH1D
import os, sys
import PlotTools
from PlotTools import Sample, Samples, Plot
ROOT.gROOT.SetBatch(ROOT.kTRUE)



argv = sys.argv
usage = '''This script make plots.'''
parser = ArgumentParser(description="Make textfile with hierarchy of subdir for a given dir",usage=usage,epilog="Succes!")
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
#             ("DY/", "DYJetsToLL_M-10to50_TuneCUETP8M1",     "Drell-Yan 10-50",        18610.0   ),
            ("DY/", "DYJetsToLL_M-10to50_nlo",              "Drell-Yan 10-50 NLO",    18610.0   ), # 18610 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
#             ("DY/", "DY1JetsToLL_M-10to50_nlo",             "Drell-Yan 1J 10-50 NLO",   421.5   ), # 421.5 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
#             ("DY/", "DY2JetsToLL_M-10to50_nlo",             "Drell-Yan 2J 10-50 NLO",   184.3   ), # 184.3 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
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
            ("WZ/", "WZ_TuneCUETP8M1",                      "WZ",                        22.82  ), #10.71? # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ZZ/", "ZZ_TuneCUETP8M1",                      "ZZ",                        10.32  ), #3.22? # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FZZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_tW_top_5f_inclusiveDecays",         "ST tW",                     35.60  ), #  38.09 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_tW_antitop_5f_inclusiveDecays",     "ST atW",                    35.60  ), #  38.09 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_t-channel_antitop_4f_leptonDecays", "ST t",                      80.95  ), #  80.95 TWiki # 80.95 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("ST/", "ST_t-channel_top_4f_leptonDecays",     "ST at",                    136.02  ), # 136.02 TWiki # 136.02 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ("WW/", "WW_TuneCUETP8M1",                      "WW",                        63.21  ), # 63.21 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWW_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("WW/", "WWTo1L1Nu2Q",                          "WW",                        1.212  ), #  1.212 TWiki # 45.85 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("WW/", "WWTo4Q_4f",                            "WW",                        45.31  ), # 45.31 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWWTo4Q_4f_13TeV_amcatnloFXFX_madspin_pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("ST/", "ST_tW_top_5f_NoFullyHadronicDecays",   "ST",                        38.09  ), # 
            ##("ST/", "ST_tW_antitop_5f_NoFullyHadronicDecays", "ST",                       0.00  ), # 
            ##("ST/", "ST_s-channel_4f_leptonDecays",         "ST",                        10.11  ), # 10.11 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ##("ST/", "ST_t-channel_antitop_4f_inclusiveDecays", "ST",                     80.95  ), # 80.95 https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM
            ##("ST/", "ST_t-channel_top_4f_inclusiveDecays",  "ST",                         0.00  ), # 
            ]
            
samplesS = [    ("signal/", "LowMass_30GeV_DiTauResonance",     "signal",                400.0  ),
            ]

samplesD = {
                "mutau"  :  [( "SingleMuon/",     "SingleMuon_Run2016",     "single muon"     )],
                #"eletau" :  [( "SingleElectron/", "SingleElectron_Run2016", "single electron" )],
            }

lumi = 12.9 #24.5
PlotTools.lumi = lumi
mylabel = "_ICHEP"  # extra label for opening file, saving plots to dir
plotlabel = ""      # extra label for png file



# CATEGORIES / SELECTIONS
vetos   = "dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1"
isocuts = "iso_1 < 0.15 && iso_2 == 1"
categories = [
#                 ("no cuts",             ""),
                #("isolation",           "%s" % (isocuts)),
                #("lepton vetos",        "%s" % (vetos)),
                #("iso, lepton vetos",   "%s && %s" % (isocuts, vetos)),
                #("lepton vetos, OS",    "%s && q_1*q_2<0" % (vetos)),
                ("iso, vetos, OS",      "%s && %s && q_1*q_2<0" % (isocuts, vetos)),
                #("iso, vetos, SS",      "%s && %s && q_1*q_2>0" % (isocuts, vetos)),
#                 ("category 1",          "%s && %s && q_1*q_2<0 && ncbtag > 0 && ncjets == 1 && nfjets  > 0" % (isocuts, vetos)),
#                 ("category 2",          "%s && %s && q_1*q_2<0 && ncbtag > 0 && ncjets  > 1 && nfjets == 0 && dphi_ll_bj > 2 && met < 50" % (isocuts, vetos)),
              ]





    #############
    # getScales #
    #############

def getScales():
    """Calculate and set the normalization scales and list samples with their respective cross section."""
    
    print "\n>>> integrated luminosity L = %s / fb" % lumi
    print ">>> "
    print ">>> %12s  %26s  %18s  %6s" % ("events", "sample".ljust(20), "cross section (pb)", "norm. scale" )
    
    # BACKGROUND
    for i, s in enumerate(samplesB):
        sigma = s[3]
        file = TFile( OUT_DIR + s[0] + "TauTauAnalysis.%s%s.root" % (s[1],mylabel) )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(7)
        scale = lumi * sigma * 1000 / N_tot        
        print ">>> %12i %26s  %14.2f %12.2f" % (N_tot,s[2].ljust(22),sigma,scale)
        samplesB[i] = ( s[0], s[1], s[2], N_tot, s[3], scale )
        
    # SIGNAL
    for i, s in enumerate(samplesS):
        sigma = s[3]
        file = TFile( OUT_DIR + s[0] + "TauTauAnalysis.%s%s.root" % (s[1],mylabel) )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(7)
        scale = lumi * sigma * 1000 / N_tot
        print ">>> %12i %26s  %14.2f %12.2f" % (N_tot,s[2].ljust(22),sigma,scale)
        samplesS[i] = ( s[0], s[1], s[2], N_tot, s[3], scale )
    
    # DATA
    for channel, s in samplesD.items():
        file = TFile( OUT_DIR + s[0][0] + "TauTauAnalysis.%s%s.root" % (s[0][1],mylabel) )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(7)
        print ">>> %12i %26s %18s" % ( N_tot, s[0][2].ljust(22), "L = %5.2f/fb" % lumi )





    ################
    # mergeSamples #
    ################

def mergeSamples(sample_list,names,**kwargs):
    """Merge samples"""
    print ">>>"
    
    if not isinstance(names,list): names = [names]
    name0       = kwargs.get('name',names[0])
    signal      = kwargs.get('signal',False)
    background  = kwargs.get('background',True) and not signal
    label       = kwargs.get('label',"")
    samples     = Samples(name0, background=background, signal=signal)
    
    # get samples containing names and label
    merge_list = [ ]
    for name in names:
        merge_list += [ s for s in sample_list if s.isPartOf(name,label) ]
    
    # check if sample list of contains to-be-stitched-sample
    if len(merge_list) < 2:
        print ">>> Warning! Could not stitch %s: less than two %s samples" % (name,name)
        return sample_list
    fill = max([ len(s.label) for s in merge_list ])
    
    # add samples with name0 and label
    for sample in merge_list:
        print ">>> merging %s to %s: %s" % (sample.label.ljust(fill),name0,sample.filenameshort)
        samples.add(sample)
    
    # remove merged samples from sample_list
    if samples.samples:
        sample_list.append(samples)
        for sample in samples.samples: sample_list.remove(sample)
    
    return sample_list
    
    
    
    
    
    #################
    # stitchSamples #
    #################

def stitchSamples(sample_list,name0,**kwargs):
    """Stitching samples: merge samples
       and reweight inclusive sample and rescale jet-binned samples"""
    print ">>>\n>>> stiching %s: merge samples and rescale and reweight" % (name0)
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
    print ">>> %s k-factor = %.2f" % (name0, kfactor)
    
    # check if sample list of contains to-be-stitched-sample
    if len(stitch_list) < 2:
        print ">>> Warning! Could not stitch %s: less than two %s samples" % (name0,name0)
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
            print ">>> Warning! Could not stitch %s: N_incl == 0!" % name0
            return sample_list
        else:
            N = N_tot + N_incl*sigma/sigmaLO # effective luminosity
        
        scale = lumi * kfactor * sigma * 1000 / N
        weights.append("(NUP==%i ? %s : 1)" % (len(weights),scale))
        print ">>> stitching %s with scale %5.2f and cross section %7.2f pb" % (sample.label.ljust(fill), scale, sigma)
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
    
        
    
    
    
    
    ###############
    # stack plots #
    ###############

def plotStacks(channel, **kwargs):
    """Plot stacked histograms with data."""
    header =  "%s channel: Stacked plots" % channel
    print ">>>\n>>>"
    print ">>>   ###"+'#'*(len(header)+3)
    print ">>>   #  %s  #" % header
    print ">>>   ###"+'#'*(len(header)+3)
    
    DIR = kwargs.get('DIR',"%s/%s" % (PLOTS_DIR,channel))
    label = mylabel
    variables = [ ]
    samples = [ ]
    treeName = "tree_%s" % channel
    channeli = 0
    weight = "weight" #(gen_match_2==5 ? 1.056 : 1.) #puweight*genweight*trigweight_1*idweight_1*isoweight_1
    if "mutau" in channel:  channeli = 1
    if "eletau" in channel: channeli = 2
    
    
    # BACKGROUND
    for dir, sample, name, N_tot, sigma, scale in samplesB:
        file = OUT_DIR + dir + "TauTauAnalysis.%s%s.root" % (sample,label)
        weightB = weight
        #if "DYJetsToLL_M-10to50_nlo" in name: weightB = "%s*%s" % (weightB,"(NUP==0 ? 1 : 0)")
        samples.append(Sample( file, name, sigma=sigma, N=N_tot, scale=scale, background=True, cuts="", weight=weightB, treeName=treeName ))
    
    
    # MERGE
    samples = stitchSamples(samples,"DY",label="M-50")
    samples = stitchSamples(samples,"WJ",name_incl="WJets")
    #samples = mergeSamples(samples,"DY",label="M-10to50_nlo",name="Drell-Yan 10-50 NLO")
    samples = mergeSamples(samples,"ST")
    samples = mergeSamples(samples,["WW","WZ","ZZ"],name="diboson")    
    
    # SIGNAl
    for dir, sample, name, N_tot, sigma, scale in samplesS:
        file = OUT_DIR + dir + "TauTauAnalysis.%s%s.root" % (sample,label)
        samples.append(Sample( file, name, sigma=sigma, N=N_tot, scale=scale, signal=True, cuts="", weight=weight, treeName=treeName ))
    
    
    # DATA
    if channel in samplesD:
        for dir, sample, name in samplesD[channel]:
            file = OUT_DIR + dir + "TauTauAnalysis.%s%s.root" % (sample,label)
            samples.append(Sample( file, name, data=True, treeName=treeName )) #cuts="( m_vis < 15 || 30 < m_vis )"
    
    
    # VARIABLES
    variables.append(( "m_vis", 35, 0, 70 ))
    variables.append(( "m_vis", 35, 0, 140 ))
#     variables.append(( "gen_match_2", 8, 0, 8 ))
#     variables.append(( "NUP", 6, 0, 6 ))
    variables.append(( "pol_2", 25, -1.1, 1.1 ))
#     variables.append(( "mt_1", 40, 0, 200 ))
    variables.append(( "pfmt_1", 30, 0, 150 ))
#     variables.append(( "mt_2", 30, 0, 150 ))
#     variables.append(( "pfmt_1", 30, 0, 150 ))
#     variables.append(( "npu", 50, 0, 50 ))
#     variables.append(( "npv", 50, 0, 50 ))
    variables.append(( "met", 30, 0, 120 ))
    variables.append(( "met_old", 30, 0, 120 ))
#     variables.append(( "puppimet", 30, 0, 120 ))
#     variables.append(( "mvamet", 30, 0, 120 ))
#     variables.append(( "dR_ll", 45, 0, 7 ))
#     variables.append(( "dphi_ll_bj", 45, 0, 7 ))
#     for n in [ "nbtag", "njets" ]:
#        variables.append( (n,6,0,6) )
#     for n in [ "ncbtag", "nfjets", "ncjets" ]:
#        variables.append( (n,5,0,5) )
#     for p in [ ("j",1), ("b",1), ("",1), ("",2), ("j",1), ("j",2), ("b",1) ]:
#        variables.append(( "%spt_%i"  % p, 50,   0, 150 ))
#        variables.append(( "abs(%seta_%i)" % p,  25,  0,  5 ))
#     for n in [ "iso_2", "againstElectronVLooseMVA6_2", "againstMuonTight3_2" ]:
#        variables.append( (n,2,0,2) )
#     variables.append(( "iso_1", 20, 0, 1.0 ))
#     variables.append(( "byIsolationMVA3oldDMwLTraw_2", 25, -1, 1 ))


    # LOOP over SELECTIONS
    WJnormalized = False # renormalize WJ once!
    for label, cuts in categories:
        
        print ">>>\n>>> %s: %s" % (channel, label)
        
        stack = True # COMPARE: set to false
        if cuts: cuts = "channel==%i && %s" % (channeli, cuts )
        else:    cuts = "channel==%i"       %  channeli
        QCD = False
        if "q_1" in cuts and "q_2" in cuts and stack:
            QCD = True
        
        
        # RENORMALIZE WJ
        if not WJnormalized and not "SS" in label and stack:
           #renormcuts = "channel==%i && %s && %s && q_1*q_2<0" % (channeli, isocuts, vetos)
           plot = Plot( samples, "pfmt_1", 100, 80, 180, cuts=cuts, QCD=QCD )
           plot.renormalizeWJ()
           #WJnormalized = True
        
        
        # RESET
        norm = (not stack) and False # COMPARE: set to false to check normalization; True to check shape
        if not stack and norm:
            for sample in samples: sample.resetScalesAndWeights(weight="genweight")
        
        
        # LOOP over VARIABLES
        for var, nBins, a, b in variables:
        
        
            # NAME
            name = "%s/%s_%s%s.png" % (DIR,var,label,plotlabel)
            if "m_vis" in var:
                name = "%s/%s_%i_%s%s.png" % (DIR,var,b,label,plotlabel)
                for sample in samples:
                    if sample.isData: sample.cuts = "( m_vis < 10 || 25 < m_vis )"
            name = name.replace(" and ","-").replace(" ","").replace(",","-") #.replace("(","").replace(")","")
            
            
            # TITLE
            title = label
    
            
            # WEIGHT
            varweight = ""
            #if "category" not in name and ("btag" in var or "bpt" in var or "beta" in var or "bphi" in var):
            #    varweight = "weightbtag"
            #    title = "%s (btag SF)" % title
            
            
            # BINS
            if "category" in label:
                if "m_vis" in var: nBins = 20
            
            
            # LEGEND POSITION
            position = ""
            logy = False
            if "m_" in var or "iso_" in var or "against" in var:
                position += "Left"
                #if b == 120: position = "LeftLeft"
            if "Iso" in var or "NUP" in var:
                position += "Center"
            if "jeta_" in var or "beta_" in var or "NUP" in var:
                position += "Top"
            if "jpt_1" in var and "category" in label:
                position += "Left"
            if "gen_match" in var:
                position += "Left"
            
            
            # PLOT
            plot = Plot( samples, var, nBins, a, b, cuts=cuts, QCD=QCD) #, weight=varweight)
            plot.plot(stack=stack, position=position, title=title, staterror=stack, logy=logy, ratio=stack, norm=norm)
            if "m_vis" in var and stack: print ">>> integral signal region %s: %s MC events" % (var,plot.integrateStack(15,30))
            plot.saveAs(name)

            if "m_vis" in var:
                for sample in samples:
                    if sample.isData: sample.cuts = ""





    ##################
    # listCategories #
    ##################

def listCategories():
    """List all available categories"""

    print ">>> list of available categories:"
    for name, cuts in categories:
        print ">>>\t%s" % name
    print ">>>\t"





    ##################
    # selectCategory #
    ##################

def selectCategory(category):
    """Only run for this category"""

    global categories
        
    if -1 < category < len(categories) and category == round(category):
        print ">>> select selection category %i" % category
        categories = [categories[category]]
    else:
        print ">>> ERROR: category %i does not exist!" % category
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
        if not os.path.exists(DIR):
            os.makedirs(DIR)
            print ">>>\n>>> made directory " + DIR
        
        plotStacks(channel,DIR=DIR)





if __name__ == '__main__':
    print
    main()
    print ">>>\n>>> Done with this, son.\n"




