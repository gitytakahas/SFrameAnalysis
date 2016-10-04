import ROOT
from ROOT import TFile, TH1F, kRed, kBlue, THStack

DIR = "/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/"





def simplePlot():
    
    file1_DY = TFile( DIR + "DY/TauTauAnalysis.DYJetsToLL_M-50_TuneCUETP8M1.root" )
    file1_WJ = TFile( DIR + "WJ/TauTauAnalysis.WJetsToLNu_TuneCUETP8M1.root" )
    N_tot_DY = file1_DY.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
    N_tot_WJ = file1_WJ.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
    N_DY = file1_DY.Get("histogram_mutau/cutflow_mutau").GetBinContent(6)
    N_WJ = file1_WJ.Get("histogram_mutau/cutflow_mutau").GetBinContent(6)

    file2_DY = TFile( DIR + "DY/DYJetsToLL_M-50_TuneCUETP8M1_mutau.root" )
    file2_WJ = TFile( DIR + "WJ/WJetsToLNu_TuneCUETP8M1_mutau.root" )
    tree_DY = file2_DY.Get("tree")
    tree_WJ = file2_WJ.Get("tree")

    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_and_data_samples
    lumi  = 24.5
    sigma_DY =  5765.4
    sigma_WJ = 61526.7
    scale_DY = lumi * sigma_DY * 1000 / N_tot_DY
    scale_WJ = lumi * sigma_WJ * 1000 / N_tot_WJ
    
    print
    print ">>> "
    print ">>>     %15s %15s %15s %15s" % ( "cutflow N_1", "cutflow N_2", "tree N", "scale" )
    print ">>> DY: %15i %15i %15i %15.5g" % ( N_tot_DY, N_DY, tree_DY.GetEntries(), scale_DY )
    print ">>> WJ: %15i %15i %15i %15.5g" % ( N_tot_WJ, N_WJ, tree_WJ.GetEntries(), scale_WJ )
    print ">>> "

    h1 = TH1F("h1","h1",50,0,50)
    h2 = TH1F("h2","h2",50,0,50)
    tree_DY.Draw("npv >> h1","weight","goff")
    tree_WJ.Draw("npv >> h2","weight","goff")
    #tree_DY.Draw("npv >> h1")
    #tree_WJ.Draw("npv >> h2")
    h1.Scale(scale_DY)
    h2.Scale(scale_WJ)

    h1.SetFillColor(kRed)
    h2.SetFillColor(kBlue)

    stack = THStack("stack","stack")
    stack.Add(h1)
    stack.Add(h2)
    stack.Draw('hist')

    wait = raw_input("Press enter to continue")
    print





def numbers():

    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    lumi  = 24.5
    DIR = "/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/"
    samplesB = [
                    ("TT/", "TT_TuneCUETP8M1",                      "ttbar",              831.76  ),
                    ("DY/", "DYJetsToLL_M-10to50_TuneCUETP8M1",     "Drell-Yan 10-50",  18610.0   ),
                    ("DY/", "DYJetsToLL_M-50_TuneCUETP8M1",         "Drell-Yan 50",      5765.4   ),
                    ("WJ/", "WJetsToLNu_TuneCUETP8M1",              "WJ",               61526.7   ),
                    ("WZ/", "WZ_TuneCUETP8M1",                      "WZ",                  39.9   ), # wrong cross section 
                    ("ZZ/", "ZZ_TuneCUETP8M1",                      "ZZ",                  10.32  ), # wrong cross section 
               ]


    print "\n>>> integrated luminosity L = %s pb" % lumi
    print ">>> "
    print ">>>    %15s %12s %12s %12s %12s %12s %12s" % ( " ", "cutflow N_1", "cutflow N_6", "tree N", "hist N", "sigma [pb]", "scale" )
    for s, i in zip(samplesB,range(len(samplesB))):

        file1 = TFile( DIR + s[0] + "TauTauAnalysis.%s.root" % s[1] )
        N_1 = file1.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        N_6 = file1.Get("histogram_mutau/cutflow_mutau").GetBinContent(6)
    
        file2 = TFile( DIR + s[0] + "%s_mutau.root" % s[1] )
        tree  = file2.Get("tree")
    
        hist = TH1F("hist","hist",40,-20,20)
        tree.Draw("weight >> hist","weight","goff")
        
        scale = lumi * s[3] * 1000 / N_1
        print ">>>    %-15s %12i %12i %12i %12i %12.5g %12.5g" % ( s[2], N_1, N_6, tree.GetEntries(), hist.Integral(), s[3], scale )





def main():
        
    #simplePlot()
    numbers()

    print ">>>\n>>> done\n"





if __name__ == '__main__':
    main()


