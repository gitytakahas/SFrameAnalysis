import ROOT
from ROOT import TFile, TH1F, kRed, kBlue, THStack, TCanvas, TLegend, kAzure, kRed, gPad, gROOT, gStyle
ROOT.gROOT.SetBatch(ROOT.kTRUE)

DIR = "/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/"
mylabel = "_ICHEP"




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
    lumi     = 24.5
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
#                     ("TT/", "TT_TuneCUETP8M1",                      "ttbar",              831.76  ),
                    ("DY/", "DYJetsToLL_M-10to50_TuneCUETP8M1",     "Drell-Yan 10-50",  18610.0   ),
#                     ("DY/", "DYJetsToLL_M-50_TuneCUETP8M1",         "Drell-Yan 50",      5765.4   ),
#                     ("WJ/", "WJetsToLNu_TuneCUETP8M1",              "WJ",               61526.7   ),
#                     ("WZ/", "WZ_TuneCUETP8M1",                      "WZ",                  39.9   ), # wrong cross section 
#                     ("ZZ/", "ZZ_TuneCUETP8M1",                      "ZZ",                  10.32  ), # wrong cross section 
               ]


    print "\n>>> integrated luminosity L = %s pb" % lumi
    print ">>> "
    print ">>>    %15s %12s %12s %12s %12s %12s %12s" % ( " ", "cutflow N_1", "cutflow N_6", "tree N", "hist N", "sigma [pb]", "scale" )
    for s, i in zip(samplesB,range(len(samplesB))):

        file1 = TFile( DIR + s[0] + "TauTauAnalysis.%s.root" % s[1] )
        N_1 = file1.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
        N_6 = file1.Get("histogram_mutau/cutflow_mutau").GetBinContent(6)
    
#         file2 = TFile( DIR + s[0] + "%s_mutau.root" % s[1] )
        tree  = file1.Get("tree_mutau")
    
        hist = TH1F("hist","hist",40,-20,20)
        tree.Draw("weight >> hist","( channel == 1 )*weight","goff")
        
        scale = lumi * s[3] * 1000 / N_1
        print ">>>    %-15s %12i %12i %12i %12i %12.5g %12.5g" % ( s[2], N_1, N_6, tree.GetEntries(), hist.Integral(), s[3], scale )





def signalEfficiency():

    # bin 1: no cuts
    # bin 2: JSON / gen weight
    # bin 3: triggers
    # bin 4: MET filters
    # bin 5: lepton selection
    # bin 6: lepton-tau pair selection
    # bin 7: no cuts gen weighted
    
    cuts = [    "no cuts",
                "JSON/weight",
                "triggers",
                "MET filters",
                "lepton",
                "lepton-tau",
                "no cuts (weighted)",
            ]
    
    file = TFile( DIR + "signal/TauTauAnalysis.LowMass_30GeV_DiTauResonance%s.root" % mylabel )
    efficiencies = [ ]
    for i, cut in zip(range(1,len(cuts)+1),cuts):
        N = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(i)
        N_tot = 0
        if i is 1:
            N = 1
            N_tot = 1
        else:
            N_tot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(i-1)
            
        if N and N_tot:
            efficiencies.append(( cut, N / N_tot ))
        else:
            print ">>> Warning: GetBinContent(%i) = %s, GetBinContent(%i) = %s " % (i,N,i-1,N_tot)
    
    for cut, efficiency in efficiencies:
        print ">>> %s: %5.2f%%" % (cut,efficiency*100)





def ptSignalAcceptence():

    cut = 23. 
    file = TFile( DIR + "signal/TauTauAnalysis.LowMass_30GeV_DiTauResonance%s.root" % mylabel )
    pt_taus = file.Get("checks/pt_gentaus")
    pt_tau1 = file.Get("checks/pt_gentau1")
    pt_tau2 = file.Get("checks/pt_gentau2")
    pt_muon = file.Get("checks/pt_muon")
    
    bincut_taus = pt_taus.FindBin(cut)
    bincut_tau1 = pt_tau1.FindBin(cut)
    bincut_tau2 = pt_tau2.FindBin(cut)
    bincut_muon = pt_muon.FindBin(cut)
    N_taus = pt_taus.Integral()
    N_tau1 = pt_tau1.Integral()
    N_tau2 = pt_tau2.Integral()
    N_muon = pt_muon.Integral()
    
    eff_taus = pt_taus.Integral(bincut_taus, pt_taus.GetNbinsX()) / N_taus
    eff_tau1 = pt_tau1.Integral(bincut_tau1, pt_tau1.GetNbinsX()) / N_tau1
    eff_tau2 = pt_tau2.Integral(bincut_tau2, pt_tau2.GetNbinsX()) / N_tau2
    eff_muon = pt_muon.Integral(bincut_muon, pt_muon.GetNbinsX()) / N_muon
    
    print ">>> efficiency of pt cut of %s on signal's gen tau and reco muon:" % cut
    print ">>> gen tau:  %5.2f%%" % (100*eff_taus)
    print ">>> gen tau1: %5.2f%%" % (100*eff_tau1)
    print ">>> gen tau2: %5.2f%%" % (100*eff_tau2)
    print ">>> gen muon: %5.2f%%" % (100*eff_muon)

    print ">>> check: bincut_taus = %3i,  N_taus =%7i" % (bincut_taus,N_taus)
    print ">>> check: bincut_tau2 = %3i,  N_tau1 =%7i" % (bincut_tau1,N_tau1)
    print ">>> check: bincut_tau3 = %3i,  N_tau2 =%7i" % (bincut_tau2,N_tau2)
    print ">>> check: bincut_muon = %3i,  N_muon =%7i" % (bincut_muon,N_muon)
    
    # DRAW
    canvas = TCanvas("canvas","canvas",100,100,600,600)
    canvas.SetBottomMargin(0.12)
    canvas.SetRightMargin(0.05)
    canvas.SetLeftMargin(0.05)
    canvas.SetTopMargin(0.05)
    pt_taus.SetLineWidth(3)
    pt_muon.SetLineWidth(3)
    pt_taus.SetLineColor(kAzure+4)
    pt_muon.SetLineColor(kRed+3)
    pt_taus.Scale(1/N_taus)
    pt_muon.Scale(1/N_muon/3)
    pt_taus.Rebin(2)
    pt_muon.Rebin(2)
    pt_taus.Draw("hist")
    pt_muon.Draw("histsame")
    pt_taus.SetTitle("")
    pt_taus.GetXaxis().SetRangeUser(0,100)
    pt_taus.GetXaxis().SetTitle("p_{T} of generator level particle")
    pt_taus.GetYaxis().SetTitleSize(0)
    pt_taus.GetXaxis().SetTitleSize(0.05)
    pt_taus.GetXaxis().SetTitleOffset(1.15)
    pt_taus.GetXaxis().SetLabelSize(0.045)
    pt_taus.GetYaxis().SetLabelSize(0)
    gStyle.SetOptStat(0)
    canvas.SaveAs("plots_check/pt.png")

    DeltaR_tautau = file.Get("checks/DeltaR_tautau")
    DeltaR_taumu  = file.Get("checks/DeltaR_taumu")
        
    cut = 0.5
    bincut_tautau = DeltaR_tautau.FindBin(cut)
    bincut_taumu  = DeltaR_taumu.FindBin(cut)
    N_tautau = DeltaR_tautau.Integral()
    N_taumu  = DeltaR_taumu.Integral()
    eff_tautau = DeltaR_tautau.Integral(bincut_tautau, DeltaR_tautau.GetNbinsX()) / N_tautau
    eff_taumu  = DeltaR_taumu.Integral( bincut_taumu,  DeltaR_taumu.GetNbinsX())  / N_taumu
    print ">>> efficiency of DeltaR cut of %s on signal's gen tau and reco muon:" % cut
    print ">>> gen tautau:  %5.2f%%" % (100*eff_tautau)
    print ">>> gen taumu:   %5.2f%%" % (100*eff_taumu)
    print ">>> check: bincut_tautau = %3i,  N_tautau =%7i" % (bincut_tautau, N_tautau)
    print ">>> check: bincut_taumu  = %3i,  N_taumu  =%7i" % (bincut_taumu,  N_taumu)
    
    for DR, hist in [ ("DeltaR_tautau",DeltaR_tautau), ("DeltaR_taumu",DeltaR_taumu) ]:
        canvas = TCanvas("canvas","canvas",100,100,800,600)
        canvas.SetBottomMargin(0.12)
        canvas.SetRightMargin(0.05)
        canvas.SetLeftMargin(0.05)
        canvas.SetTopMargin(0.05)
        hist.SetLineWidth(3)
        hist.SetLineColor(kAzure+4)
        hist.Draw("hist")
        hist.Scale(1/hist.Integral())
        hist.SetTitle("")
        #hist.GetXaxis().SetRangeUser(0,100)
        hist.GetXaxis().SetTitle(DR.replace("Delta","#Delta ").replace("_tautau","_{#tau#tau}").replace("_taumu","_{#tau#mu}"))
        hist.GetYaxis().SetTitleSize(0)
        hist.GetXaxis().SetTitleSize(0.05)
        hist.GetXaxis().SetTitleOffset(1.15)
        hist.GetXaxis().SetLabelSize(0.045)
        hist.GetYaxis().SetLabelSize(0)
        gStyle.SetOptStat(0)
        canvas.SaveAs("plots_check/%s.png" % DR)
        
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    canvas.SetBottomMargin(0.12)
    canvas.SetRightMargin(0.05)
    canvas.SetLeftMargin(0.05)
    canvas.SetTopMargin(0.05)
    DeltaR_tautau.SetLineWidth(3)
    DeltaR_taumu.SetLineWidth(3)
    DeltaR_taumu.SetLineColor(kRed+3)
    DeltaR_taumu.SetLineStyle(2)
    DeltaR_tautau.Draw("hist")
    DeltaR_taumu.Draw("histsame")
    DeltaR_tautau.Scale(1/hist.Integral())
    DeltaR_taumu.Scale(1/hist.Integral())
    DeltaR_tautau.SetTitle("")
    #hist.GetXaxis().SetRangeUser(0,100)
    DeltaR_tautau.GetXaxis().SetTitle("#DeltaR")
    DeltaR_tautau.GetYaxis().SetTitleSize(0)
    DeltaR_tautau.GetXaxis().SetTitleSize(0.06)
    DeltaR_tautau.GetXaxis().SetTitleOffset(0.9)
    DeltaR_tautau.GetXaxis().SetLabelSize(0.045)
    DeltaR_tautau.GetYaxis().SetLabelSize(0)
    legend = TLegend(0.8,0.7,0.6,0.5)
    legend.AddEntry(DeltaR_tautau," #DeltaR(#tau,#tau)")
    legend.AddEntry(DeltaR_taumu," #DeltaR(#mu,#tau_{h})")
    legend.SetTextSize(0.055)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.Draw()
    gStyle.SetOptStat(0)
    canvas.SaveAs("plots_check/DeltaR_tautaumu.png")
    
        
    file.Close()



def countEvent():
    vetos   = "dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1"
    isocuts = "iso_1 < 0.15 && iso_2 == 1"
    cuts    = [ ("category 1", "channel==1 && %s && %s && q_1*q_2<0 && ncbtag > 0 && ncjets == 1 && nfjets  > 0" % (isocuts, vetos)),
                ("category 2", "channel==1 && %s && %s && q_1*q_2<0 && ncbtag > 0 && ncjets  > 1 && nfjets == 0 && dphi_ll_bj > 2 && met < 50" % (isocuts, vetos)),
               ]

    file = TFile( DIR + "signal/TauTauAnalysis.LowMass_30GeV_DiTauResonance%s.root" % mylabel )    
    tree = file.Get("tree_mutau")
    
    for label, cut in cuts:
        hist = TH1F("hist", "hist", 35, 0, 70)
        canvas = TCanvas("canvas","canvas",100,100,400,300)
        tree.Draw("m_vis >> hist", cut)
        print ">>> %s: signal MC sample has %3i events" % (label,hist.Integral())
        canvas.SaveAs("plots_check/%s.png" % label.replace(" ","_"))
        ROOT.gDirectory.Delete(hist.GetName())
        canvas.Close()





def main():
    print ""
        
    #simplePlot()
    #numbers()
    #signalEfficiency()
    ptSignalAcceptence()
#     countEvent()
    
    print ">>>\n>>> done\n"





if __name__ == '__main__':
    main()


