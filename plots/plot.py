# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016
import ROOT
from ROOT import TFile, TH1D
import os
from PlotTools import Sample, Plot
ROOT.gROOT.SetBatch(ROOT.kTRUE)

DIR_S  = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/signal/")
OUT_DIR = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/")
DIR_MU = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/SingleMuon/")
DIR_EL = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/SingleElectron/")
PLOTS_DIR = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/plots/")

# sample info (cross section in pb)
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_and_data_samples
samplesB = [
                ("TT/", "TT_TuneCUETP8M1",                      "ttbar",               831.76  ),
                ("DY/", "DYJetsToLL_M-10to50_TuneCUETP8M1",     "Drell-Yan 10-50",   18610.0   ),
                ("DY/", "DYJetsToLL_M-50_TuneCUETP8M1",         "Drell-Yan 50",       5765.4   ),
                ("WJ/", "WJetsToLNu_TuneCUETP8M1",              "WJ",                61526.7   ),
                ("WZ/", "WZ_TuneCUETP8M1",                      "WZ",                   22.82  ), # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FWZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
                ("ZZ/", "ZZ_TuneCUETP8M1",                      "ZZ",                   10.32  ), # https://cmsweb.cern.ch/das/request?input=dataset%3D%2FZZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal
            ]
            
# 61526.7*1000*25/76780000*500000
# 5765.4*1000*25/22190000*3000000
lumi  = 24.5
print "\n>>> integrated luminosity L = %s pb" % lumi
print ">>> "
for s, i in zip(samplesB,range(len(samplesB))):
    file = TFile( OUT_DIR + s[0] + "TauTauAnalysis.%s.root" % s[1] )
    N_tot =  file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
    scale = lumi * s[3] * 1000 / N_tot
    print ">>> %12i  events of  %s (%s pb)" % (N_tot,s[2],s[3])
    #print ">>> scale %s" % (scale)
    samplesB[i] = ( s[0], s[1], s[2], scale )
    
file = TFile( DIR_MU + "TauTauAnalysis.SingleMuon_Run2016.root" )
N_tot =  file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
print ">>> %12i  events of Single Muon (L = %s pb)" % ( N_tot, lumi ) # should be 158188719

scaleMu = 1 #18 #3 * 2 * 158188719 / file.Get("histogram_mutau/cutflow_mutau").GetBinContent(2)
#print scaleMu




    ###############
    # stack plots #
    ###############

def plotStacks(channel):
    print ">>>\n>>>  %s channel: Stacked plots" % channel
    
    variables = [ ]
    samples = [ ]
    
    for dir, sample, name, scale in samplesB:
        file = OUT_DIR + dir + "TauTauAnalysis.%s.root" % sample #(sample, channel)
        samples.append(Sample( file, name, scale = scale, background = True, cuts = "", weight = True, treeName="tree_mutau" ))
    
    channeli = 1
    if "mutau" in channel:
        file = DIR_MU + "TauTauAnalysis.SingleMuon_Run2016.root"
        samples.append(Sample( file, "single muon", data = True, scale = scaleMu, cuts = "( m_vis < 20 || 30 < m_vis )", treeName="tree_mutau" ))
    if "eletau" in channel:
        channeli = 2
        file = DIR_EL + "SingleElectron_Run2016_eletau.root"
        #samples.append(Sample( DIR_EL+file,  "single electron", data = True, cuts = "( m_vis < 26 || 32 < m_vis )" ))

    variables.append(( "m_vis", 35, 0, 70 ))
    variables.append(( "m_vis", 40, 0, 120 ))
    variables.append(( "mt_1", 40, 0, 120 ))
    variables.append(( "mt_2", 40, 0, 120 ))
    variables.append(( "npu", 50, 0, 50 ))
    variables.append(( "npv", 50, 0, 50 ))
    variables.append(( "met", 35, 0, 70 ))
    variables.append(( "puppimet", 35, 0, 70 ))
    variables.append(( "mvamet", 35, 0, 70 ))
    variables.append(( "dR_ll", 32, 0, 3.2 ))
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
    
    isocuts = "iso_1 < 0.15 && iso_2 == 1 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1"
    vetos = "dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0"
    category = [ ("no cuts",    "channel==%i" % channeli),
                 ("isolation",  "channel==%i && %s" % (channeli, isocuts)),
                 ("iso, OS, vetos",  "channel==%i && %s && q_1*q_2<0 && %s" % (channeli, isocuts, vetos)),
                 ("iso, SS, vetos",  "channel==%i && %s && q_1*q_2>0 && %s" % (channeli, isocuts, vetos)),
                 #("category 1", "channel==%i && ncbtag > 0 && nfjets > 0" % channeli),
                 #("category 2", "channel==%i && ncbtag > 0 && ncjets > 0" % channeli),
                ]
    
    for label, cuts in category:
        print "\n>>> %s: %s" % (channel, label)
        for var, nBins, a, b in variables:
        
            name = PLOTS_DIR+"%s/%s_%s.png" % (channel,var,label)
            if "m_vis" in var:
                name = PLOTS_DIR+"%s/%s_%i_%s.png" % (channel,var,b,label)
            name = name.replace(" and ","-").replace(" ","").replace(",","-")
    
            position = ""
            logy = False
            if "m_" in var or "dR" in var or "against" in var:
                position = "Left"
            if "Iso" in var:
                position = "Center"
            
            # declare, make and save plot
            plot = Plot( samples, var, nBins, a, b, cuts=cuts, QCD=True)
            plot.plot(stack=True, position=position, title=label, errorbars=True, logy=logy)
            plot.saveAs(name)





    ########
    # main #
    ########

def main():

    for channel in [ #"eletau",
                     "mutau",
                    ]:
        
        # make directories    
        if not os.path.exists(PLOTS_DIR+channel):
            os.makedirs(PLOTS_DIR+channel)
            print ">>> made directory " + PLOTS_DIR+channel
        
        plotStacks(channel)

    print ">>>\n>>> Done with this, son.\n"





if __name__ == '__main__':
    main()




