import ROOT
from ROOT import TFile, TH1D
import os
from PlotTools import Sample, Plot
ROOT.gROOT.SetBatch(ROOT.kTRUE)
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016

# use os.path.expanduser for "~/" 
DIR_S = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/signal/")
DIR_TT = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/TT/")
DIR_DY = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/DY/")
DIR_MU = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/SingleMuon/")
DIR_EL = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/SingleElectron/")
PLOTS_DIR = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/plots/")

# numbers
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_and_data_samples
lumi  = 24.5
sigma_tt = 831.76 * 1000
sigma_DY = 18610 * 1000
sigma_DY50 = 1012.5 * 1000

# cutflow
cutflow = "histogram_mutau/cutflow_mutau"
file_TT = TFile(DIR_TT+"TauTauAnalysis.TT_TuneCUETP8M1.root")
file_DY = TFile(DIR_DY+"TauTauAnalysis.DYJetsToLL_M-10to50_TuneCUETP8M1.root")
file_DY50 = TFile(DIR_DY+"TauTauAnalysis.DYJetsToLL_M-50_TuneCUETP8M1.root")
N_TT_tot = file_TT.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
N_DY_tot = file_DY.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
N_DY50_tot = file_DY50.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
print ">>> total number of ttbar: %i" % N_TT_tot
print ">>> total number of Drell-Yan: %i" % N_DY_tot
print ">>> total number of Drell-Yan 50: %i" % N_DY50_tot

# scale
scale_TT = lumi * sigma_tt / N_TT_tot
scale_DY = lumi * sigma_DY / N_DY_tot
scale_DY50 = lumi * sigma_DY50 / N_DY50_tot




    ###############
    # stack plots #
    ###############

def plotStacks(channel):
    print "\n  %s: Stacked plots" % channel
    
    
    file = "%s.root" % channel
    variables = [ ]
    samples = [ Sample( DIR_TT+file, "ttbar",     scale = scale_TT, background = True, cuts = "", weight = True ),
                Sample( DIR_DY+"DYJetsToLL_M-10to50_TuneCUETP8M1_%s" % file, "Drell-Yan-low", scale = scale_DY,   background = True, cuts = "", weight = True ),
                Sample( DIR_DY+"DYJetsToLL_M-50_TuneCUETP8M1_%s" % file,     "Drell-Yan-50",  scale = scale_DY50, background = True, cuts = "", weight = True ),
                #Sample( DIR_S+file,  "signal",    scale = scale_DY, signal = True,     cuts = "", weight = True ),
                #Sample( DIR_DY+file, "test data", scale = scale_DY*4, data = True, cuts = "( m_vis < 26 || 32 < m_vis )", weight = True ),
                #Sample( DIR_TT+file, "test data", scale = scale_TT*1.2, data = True, cuts = "( m_vis < 26 || 32 < m_vis )", weight = True ),
               ]
    
    if "mutau" in channel:
        samples.append(Sample( DIR_MU+file,  "single muon",     data = True, cuts = "( m_vis < 26 || 32 < m_vis )" ))
    if "#eletau" in channel:
        samples.append(Sample( DIR_EL+file, "single electron", data = True, cuts = "( m_vis < 26 || 32 < m_vis )" ))


    for n in [ "nbtag", "njets" ]:
        variables.append( (n,5,0,5) )
    for n in [ "ncbtag", "nfjets", "ncjets" ]:
        variables.append( (n,10,0,10) )
    for p in [ ("",1), ("",2), ("j",1), ("j",2), ("b",1) ]:
        variables.append(( "%spt_%i"  % p, 50,   0, 100 ))
        #variables.append(( "%sphi_%i" % p,  50,   0,   5 ))
        variables.append(( "%seta_%i" % p,  50,  -5,   5 ))    
    for n in [ "iso_2", "againstElectronVLooseMVA6_2", "againstMuonTight3_2" ]:
        variables.append( (n,2,0,2) )
    variables.append(( "iso_1", 25, 0, 3 ))
    variables.append(( "byIsolationMVA3oldDMwLTraw_2", 25, -1, 1 ))
    variables.append(( "met", 35, 0, 70 ))
    variables.append(( "m_vis", 35, 0, 70 ))

    
    category = [ ("no cuts",    ""),
                 ("isolation",  "iso_1 < 0.15 && iso_2 == 1 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1"),
                 #("category 1", "ncbtag > 0 && nfjets > 0"),
                 #("category 2", "ncbtag > 0 && ncjets > 0"),
                ]
    #  if(Jet.pt() > 30 && fabs(Jet.eta()) < 2.4 && Jet.csv() > 0.8) ncbtag++;
    #  if(Jet.pt() > 30 && fabs(Jet.eta()) > 2.4 && Jet.csv() > 0.8) nfbtag++;
    #  if(Jet.pt() > 30 && fabs(Jet.eta()) < 2.4) ncjets++;
    #  if(Jet.pt() > 30 && fabs(Jet.eta()) > 2.4) nfjets++;
    
    
    for label, cuts in category:
        for var, nBins, a, b in variables:
            name = PLOTS_DIR+"%s/%s_%s.png" % (channel,var,label)
            name = name.replace(" ","")
    
            position = ""
            if "m_" in var: position = "Left"
            if "jpt_" in var or "bpt_" in var:
                position = "TopLeft"
            
            # delcare, make and save plot
            plot = Plot( samples, var, nBins, a, b, cuts=cuts)
            plot.plot(stack=True,position=position, title=label)
            plot.saveAs(name)





    ########
    # main #
    ########

def main():

    for channel in [ #"eletau",
                     "mutau", ]:
        
        # make directories    
        if not os.path.exists(PLOTS_DIR+channel):
            os.makedirs(PLOTS_DIR+channel)
            print ">>> made directory " + PLOTS_DIR+channel
        
        plotStacks(channel)

    print "\nDone with this, son.\n"





if __name__ == '__main__':
    main()




