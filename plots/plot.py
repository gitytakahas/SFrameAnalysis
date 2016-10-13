# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016
from argparse import ArgumentParser
import ROOT
from ROOT import TFile, TH1D
import os, sys
from PlotTools import Sample, Plot
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
                ("WZ/", "WZ_TuneCUETP8M1",                      "WZ",                   22.82  ), # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("ZZ/", "ZZ_TuneCUETP8M1",                      "ZZ",                   10.32  ), # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FZZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ]
            
samplesS = [    ("signal/", "LowMass_30GeV_DiTauResonance",     "signal",                50.0  ),
            ]

lumi  = 24.5
samplesD = {
                "mutau"  :  [[ "SingleMuon/",     "SingleMuon_Run2016",     "single muon"     ]],
                #"eletau" :  [[ "SingleElectron/", "SingleElectron_Run2016", "single electron" ]],
            }



# CATEGORIES / SELECTIONS
isocuts = "iso_1 < 0.15 && iso_2 == 1 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1"
vetos   = "dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0"
categories = [
                ("no cuts",        ""),
                ("isolation",      "%s" % (isocuts)),
                ("lepton vetos",      "%s" % (vetos)),
                ("iso, OS, vetos", "%s && q_1*q_2<0 && %s" % (isocuts, vetos)),
                ("iso, SS, vetos", "%s && q_1*q_2>0 && %s" % (isocuts, vetos)),
                #("category 1",    "%s && q_1*q_2<0 && %s && ncbtag > 0 && nfjets > 0" % (isocuts, vetos)),
                #("category 2",    "%s && q_1*q_2>0 && %s && ncbtag > 0 && ncjets > 0" % (isocuts, vetos)),
              ]





    #############
    # getScales #
    #############

def getScales():
    """Calculate the scales and list samples with their cross section."""

    print "\n>>> integrated luminosity L = %s pb" % lumi
    print ">>> "
    for s, i in zip(samplesB,range(len(samplesB))):
        file = TFile( OUT_DIR + s[0] + "TauTauAnalysis.%s.root" % s[1] )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        scale = lumi * s[3] * 1000 / N_tot
        print ">>> %12i  events of  %s %10.2f pb" % (N_tot,s[2].ljust(16),s[3])
        #print ">>> scale %s" % (scale)
        samplesB[i] = ( s[0], s[1], s[2], scale )
        
    for s, i in zip(samplesS,range(len(samplesS))):
        file = TFile( OUT_DIR + s[0] + "TauTauAnalysis.%s.root" % s[1] )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        scale = lumi * s[3] * 1000 / N_tot
        print ">>> %12i  events of  %s %10.2f pb" % (N_tot,s[2].ljust(16),s[3])
        #print ">>> scale %s" % (scale)
        samplesS[i] = ( s[0], s[1], s[2], scale )
    
    for channel, s in samplesD.items():    
        file = TFile( OUT_DIR + s[0][0] + "TauTauAnalysis.%s.root" % s[0][1] )
        N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        print ">>> %12i  events of  %s  L = %5.2f pb" % ( N_tot, s[0][2].ljust(16), lumi )





    ###############
    # stack plots #
    ###############

def plotStacks(channel):
    """Plot stacked histograms with data."""
    print ">>>\n>>>  %s channel: Stacked plots" % channel
    
    variables = [ ]
    samples = [ ]
    treeName = "tree_%s" % channel
    channeli = 0
    if "mutau" in channel:  channeli = 1
    if "eletau" in channel: channeli = 2
    
    for dir, sample, name, scale in samplesB:
        file = OUT_DIR + dir + "TauTauAnalysis.%s.root" % sample
        samples.append(Sample( file, name, scale = scale, background = True, cuts = "", weight = True, treeName="tree_mutau" ))

    for dir, sample, name, scale in samplesS:
        file = OUT_DIR + dir + "TauTauAnalysis.%s.root" % sample
        samples.append(Sample( file, name, scale = scale, signal = True, cuts = "", weight = True, treeName="tree_mutau" ))
    
    for dir, sample, name in samplesD[channel]:
        file = OUT_DIR + dir + "TauTauAnalysis.%s.root" % sample
        samples.append(Sample( file, name, data = True, cuts = "( m_vis < 15 || 30 < m_vis )", treeName="tree_mutau" ))

    variables.append(( "m_vis", 35, 0, 70 ))
    variables.append(( "m_vis", 40, 0, 120 ))
    variables.append(( "mt_1", 40, 0, 120 ))
    variables.append(( "mt_2", 40, 0, 120 ))
    variables.append(( "npu", 50, 0, 50 ))
    variables.append(( "npv", 50, 0, 50 ))
    variables.append(( "met", 35, 0, 70 ))
    variables.append(( "puppimet", 35, 0, 70 ))
    variables.append(( "mvamet", 35, 0, 70 ))
    variables.append(( "dR_ll", 50, 0, 5 ))
    for n in [ "nbtag", "njets" ]:
        variables.append( (n,5,0,5) )
    for n in [ "ncbtag", "nfjets", "ncjets" ]:
        variables.append( (n,10,0,10) )
    for p in [ ("",1), ("",2), ("j",1), ("j",2), ("b",1) ]:
        variables.append(( "%spt_%i"  % p, 50,   0, 100 ))
        #variables.append(( "%sphi_%i" % p,  50,   0,   5 ))
        variables.append(( "abs(%seta_%i)" % p,  25,  0,  4 ))    
    for n in [ "iso_2", "againstElectronVLooseMVA6_2", "againstMuonTight3_2" ]:
        variables.append( (n,2,0,2) )
    variables.append(( "iso_1", 25, 0, 3 ))
    variables.append(( "byIsolationMVA3oldDMwLTraw_2", 25, -1, 1 ))

    
    for label, cuts in categories:
        print "\n>>> %s: %s" % (channel, label)
        if cuts: cuts = "channel==%i && %s" % (channeli, cuts )
        else:    cuts = "channel==%i"       % channeli
        for var, nBins, a, b in variables:
        
            name = PLOTS_DIR+"%s/%s_%s.png" % (channel,var,label)
            if "m_vis" in var:
                name = PLOTS_DIR+"%s/%s_%i_%s.png" % (channel,var,b,label)
            name = name.replace(" and ","-").replace(" ","").replace(",","-")
    
            position = ""
            logy = False
            if "m_" in var or "dR" in var or "against" in var:
                position = "Left"
                if b == 120: position = "LeftLeft"
            if "Iso" in var:
                position = "Center"
            
            # declare, make and save plot
            plot = Plot( samples, var, nBins, a, b, cuts=cuts, QCD=True)
            plot.plot(stack=True, position=position, title=label, errorbars=True, logy=logy)
            plot.saveAs(name)






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
        if not os.path.exists(PLOTS_DIR+channel):
            os.makedirs(PLOTS_DIR+channel)
            print ">>> made directory " + PLOTS_DIR+channel
        
        plotStacks(channel)





if __name__ == '__main__':
    print
    main()
    print ">>>\n>>> Done with this, son.\n"




