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
                ("TT/", "TT_TuneCUETP8M1",                      "ttbar",               831.76  ),
                ("DY/", "DYJetsToLL_M-10to50_TuneCUETP8M1",     "Drell-Yan 10-50",   18610.0   ), 
                ("DY/", "DYJetsToLL_M-50_TuneCUETP8M1",         "Drell-Yan 50",       5765.4   ),
                ("WJ/", "WJetsToLNu_TuneCUETP8M1",              "WJ",                61526.7   ), 
                ("WZ/", "WZ_TuneCUETP8M1",                      "WZ",                   22.82  ), #10.71? # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("ZZ/", "ZZ_TuneCUETP8M1",                      "ZZ",                   10.32  ), #3.22? # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FZZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("ST/", "ST_tW_top_5f_inclusiveDecays",         "ST tW",                35.60  ), #  38.09 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("ST/", "ST_tW_antitop_5f_inclusiveDecays",     "ST atW",               35.60  ), #  38.09 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("ST/", "ST_t-channel_antitop_4f_leptonDecays", "ST t",                 80.95  ), #  80.95 TWiki # 80.95 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("ST/", "ST_t-channel_top_4f_leptonDecays",     "ST at",               136.02  ), # 136.02 TWiki # 136.02 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ##("WW/", "WWTo1L1Nu2Q",                          "WW",                   1.212  ), #  1.212 TWiki # 45.85 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ##("WW/", "WWTo4Q_4f",                            "WW",                   45.31  ), # 45.31 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWWTo4Q_4f_13TeV_amcatnloFXFX_madspin_pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("WW/", "WW_TuneCUETP8M1",                      "WW",                   63.21  ), # 63.21 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWW_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ##("ST/", "ST_tW_top_5f_NoFullyHadronicDecays",   "ST",                   38.09  ), # 
                ##("ST/", "ST_tW_antitop_5f_NoFullyHadronicDecays", "ST",                  0.00  ), # 
                ##("ST/", "ST_s-channel_4f_leptonDecays",         "ST",                   10.11  ), # 10.11 https://cmsweb.cern.ch/das/request?input=dataset%3D%2FST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ##("ST/", "ST_t-channel_antitop_4f_inclusiveDecays", "ST",                80.95  ), # 80.95 https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM
                ##("ST/", "ST_t-channel_top_4f_inclusiveDecays",  "ST",                    0.00  ), # 
            ]
            
samplesS = [    ("signal/", "LowMass_30GeV_DiTauResonance",     "signal",                400.0  ),
            ]

lumi = 12.9 #24.5
PlotTools.lumi = lumi
mylabel = "_ICHEP"
samplesD = {
                "mutau"  :  [[ "SingleMuon/",     "SingleMuon_Run2016",     "single muon"     ]],
                #"eletau" :  [[ "SingleElectron/", "SingleElectron_Run2016", "single electron" ]],
            }



# CATEGORIES / SELECTIONS
vetos   = "dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1"
isocuts = "iso_1 < 0.15 && iso_2 == 1"
categories = [
                #("no cuts",             ""),
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
    print     ">>> %12s  %18s  %18s  %6s" % ("events", "sample".ljust(13), "cross section (pb)", "scale" )
    for s, i in zip(samplesB,range(len(samplesB))):
        file = TFile( OUT_DIR + s[0] + "TauTauAnalysis.%s%s.root" % (s[1],mylabel) )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        scale = lumi * s[3] * 1000 / N_tot
        print ">>> %12i %18s  %14.2f %12.2f" % (N_tot,s[2].ljust(16),s[3],scale)
        #print ">>> scale %s" % (scale)
        samplesB[i] = ( s[0], s[1], s[2], scale )
        
    for s, i in zip(samplesS,range(len(samplesS))):
        file = TFile( OUT_DIR + s[0] + "TauTauAnalysis.%s%s.root" % (s[1],mylabel) )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        scale = lumi * s[3] * 1000 / N_tot
        print ">>> %12i %18s  %14.2f %12.2f" % (N_tot,s[2].ljust(16),s[3],scale)
        #print ">>> scale %s" % (scale)
        samplesS[i] = ( s[0], s[1], s[2], scale )
    
    for channel, s in samplesD.items():    
        file = TFile( OUT_DIR + s[0][0] + "TauTauAnalysis.%s%s.root" % (s[0][1],mylabel) )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        print ">>> %12i %18s %18s" % ( N_tot, s[0][2].ljust(16), "L = %5.2f/fb" % lumi )





    ################
    # mergeSamples #
    ################

def mergeSamples(sample_list,labels,**kwargs):
    """Merge samples"""
    
    signal = kwargs.get('signal',False)
    background = kwargs.get('background',True) and not signal
    if not isinstance(labels,list): labels = [labels]
    label = kwargs.get('label',labels[0])
    samples = Samples(label, background=background, signal=signal)
    
    for sample in sample_list:
        for label in labels:
            if label in sample.label:
                print ">>> merging %s: %s" % (label,sample.filename)
                samples.add(sample)
    
    if samples.samples:
        sample_list.append(samples)
        for sample in samples.samples: sample_list.remove(sample)
    
    return sample_list





    ###############
    # stack plots #
    ###############

def plotStacks(channel, **kwargs):
    """Plot stacked histograms with data."""
    print ">>>\n>>>  %s channel: Stacked plots" % channel
    
    DIR = kwargs.get('DIR',"%s/%s" % (PLOTS_DIR,channel))
    label = mylabel
    variables = [ ]
    samples = [ ]
    treeName = "tree_%s" % channel
    channeli = 0
    weight = "puweight*genweight*trigweight_1*idweight_1*isoweight_1*(gen_match_2==5 ? 1.056 : 1.)" #"weight" #"puweight*genweight" #"puweight*genweight*trigweight_1*idweight_1*isoweight_1"
    if "mutau" in channel:  channeli = 1
    if "eletau" in channel: channeli = 2
    
    
    # BACKGROUND
    for dir, sample, name, scale in samplesB:
        file = OUT_DIR + dir + "TauTauAnalysis.%s%s.root" % (sample,label)
        samples.append(Sample( file, name, scale=scale, background=True, cuts="", weight=weight, treeName=treeName ))
    
    
    # MERGE
    #samples = mergeSamples(samples,"DY")
    samples = mergeSamples(samples,"ST")
    samples = mergeSamples(samples,["WW","WZ","ZZ"],label="diboson")
    
    
    # SIGNAl
    for dir, sample, name, scale in samplesS:
        file = OUT_DIR + dir + "TauTauAnalysis.%s%s.root" % (sample,label)
        samples.append(Sample( file, name, scale=scale, signal=True, cuts="", weight=weight, treeName=treeName ))
    
    
    # DATA
    if channel in samplesD:
        for dir, sample, name in samplesD[channel]:
            file = OUT_DIR + dir + "TauTauAnalysis.%s%s.root" % (sample,label)
            samples.append(Sample( file, name, data=True, treeName=treeName )) #cuts="( m_vis < 15 || 30 < m_vis )"
    
    
    # VARIABLES
#     variables.append(( "m_vis", 35, 5, 75 ))
    variables.append(( "m_vis", 35, 0, 140 ))
    variables.append(( "mt_1", 40, 0, 200 ))
#     variables.append(( "pfmt_1", 30, 0, 150 ))
#     variables.append(( "mt_2", 30, 0, 150 ))
#     variables.append(( "pfmt_1", 30, 0, 150 ))
#     variables.append(( "npu", 50, 0, 50 ))
#     variables.append(( "npv", 50, 0, 50 ))
#     variables.append(( "met", 30, 0, 120 ))
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
#        #variables.append(( "%sphi_%i" % p,  50,   0,   5 ))
#        variables.append(( "abs(%seta_%i)" % p,  25,  0,  5 ))
#     for n in [ "iso_2", "againstElectronVLooseMVA6_2", "againstMuonTight3_2" ]:
#        variables.append( (n,2,0,2) )
#     variables.append(( "iso_1", 20, 0, 1.0 ))
#     variables.append(( "byIsolationMVA3oldDMwLTraw_2", 25, -1, 1 ))


    # LOOP over SELECTIONS
    WJnormalized = False # renormalize WJ once!
    for label, cuts in categories:
        
        print ">>>\n>>> %s: %s" % (channel, label)
        if cuts: cuts = "channel==%i && %s" % (channeli, cuts )
        else:    cuts = "channel==%i"       %  channeli
        QCD = False
        if "q_1" in cuts and "q_2" in cuts:
            QCD = True
        if "category" in label:
            weight = "weight"
        
        
        # RENORMALIZE WJ
        if not WJnormalized and not "SS" in label:
           #renormcuts = "channel==%i && %s && %s && q_1*q_2<0" % (channeli, isocuts, vetos)
           plot = Plot( samples, "pfmt_1", 100, 80, 180, cuts=cuts, QCD=QCD)
           plot.renormalizeWJ()
           #WJnormalized = True
        
        
        # LOOP over VARIABLES
        for var, nBins, a, b in variables:
        
        
            # NAME
            name = "%s/%s_%s.png" % (DIR,var,label)
            if "m_vis" in var:
                name = "%s/%s_%i_%s.png" % (DIR,var,b,label)
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
    
    
            # LEGEND POSITION
            position = ""
            logy = False
            if "m_" in var or "iso_" in var or "against" in var:
                position = "Left"
                #if b == 120: position = "LeftLeft"
            if "Iso" in var:
                position = "Center"
            if "jeta_" in var or "beta_" in var:
                position = "Top"
            if "jpt_1" in var and "category" in label:
                position = "Left"
            
            
            # PLOT
            plot = Plot( samples, var, nBins, a, b, cuts=cuts, QCD=QCD) #, weight=varweight)
            plot.plot(stack=True, position=position, title=title, staterror=True, logy=logy, ratio=True)
            if "m_vis" in var: print ">>> integral signal region %s: %s MC events" % (var,plot.integrateStack(15,30))
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




