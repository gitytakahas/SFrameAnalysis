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
DIR_D = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/data/")
PLOTS_DIR = os.path.expandvars("/shome/ineuteli/analysis/SFrameAnalysis/plots/")

# numbers
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_and_data_samples
lumi  = 24.5
sigma_tt = 831.76 * 1000
sigma_DY = 1012.5 * 1000

# cutflow
cutflow = "histogram_mutau/cutflow_mutau"
file_TT = TFile(DIR_TT+"TauTauAnalysis.TT_TuneCUETP8M1.root")
file_DY = TFile(DIR_DY+"TauTauAnalysis.DYJetsToLL_M-50_TuneCUETP8M1.root")
N_TT_tot = file_TT.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
N_DY_tot = file_DY.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
print ">>> total number of ttbar: %i" % N_TT_tot
print ">>> total number of Drell-Yan: %i" % N_DY_tot

# scale
scale_TT = lumi * sigma_tt / N_TT_tot
scale_DY = lumi * sigma_DY / N_DY_tot




    ###############
    # stack plots #
    ###############

def plotStacks(channel):
    print "\n  %s: Stacked plots" % channel
    
    
    file = "%s.root" % channel
    variables = [ ]
    samples = [ Sample( DIR_TT+file, "ttbar",     scale = scale_TT, background = True, cuts = "" ),
                Sample( DIR_DY+file, "Drell-Yan", scale = scale_DY, background = True, cuts = "" ),
#                 Sample( DIR_B+file, "signal",   scale = scale_DY, signal = True, cuts = "" ),
#                 Sample( DIR_S+file, "data",     scale = scale_DY, data = True, cuts = "m_vis < 26 || 32 < m_vis" )
              ]

    
    category = [ ]    
    for cuts in category:
    
        for n in [ "nbtag", "njets" ]:
            variables.append( (n,5,0,5) )
        variables.append( ("m_vis",70,0,70) )

        for var, nBins, a, b in variables:
    
            position = ""
            if "m_" in var: position = "Left"
            
            plot = Plot( samples, var, nBins, a, b, cuts=cuts)
            plot.plot(stack=True,position=position)
            plot.saveAs(PLOTS_DIR+"%s/%s.png" % (channel,var))





    ########
    # main #
    ########

def main():

    for channel in [ "eletau", "mutau", ]:
        
        # make directories    
        if not os.path.exists(PLOTS_DIR+channel):
            os.makedirs(PLOTS_DIR+channel)
            print ">>> made directory " + PLOTS_DIR+channel
        
        plotStacks(channel)

    print "\nDone with this, son.\n"





if __name__ == '__main__':
    main()




