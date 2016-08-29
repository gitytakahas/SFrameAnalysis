import os, sys, random
from ROOT import *

firstCanvas = True

def main():

  # ROOT.gROOT.SetBatch(True)
  sys.path.insert(0, '~/CMSstyle/')
  import tdrstyle
  tdrstyle.setTDRStyle()

  # ROOT.LoadMacro("~/bbH/atlasstyle-00-03-05/AtlasStyle.C")
  # SetAtlasStyle()

  gStyle.SetStatColor(0)
  gStyle.SetCanvasColor(0)
  gStyle.SetPadColor(0)
  gStyle.SetPadBorderMode(0)
  gStyle.SetCanvasBorderMode(0)
  gStyle.SetFrameBorderMode(0)
  #gStyle.SetOptStat(1110)
  gStyle.SetOptStat(0)
  gStyle.SetStatH(0.2)
  gStyle.SetStatW(0.2)
  gStyle.SetStatX(0.99)
  gStyle.SetTitleColor(1)
  gStyle.SetTitleFillColor(0)
  # gStyle.SetTitleY(1.)
  # gStyle.SetTitleX(.15)
  gStyle.SetTitleBorderSize(0)
  gStyle.SetPadTickX(1)
  gStyle.SetPadTickY(1)
  gStyle.SetPalette(1)
#   gStyle.SetMarkerStyle(20);
  # gStyle.SetMarkerSize(2);
  # gStyle.SetLineWidth(2);
#   gStyle.SetLineStyleString(2,"[12 12]"); # postscript dashes

  v_samples = ["7_4_6.patch1", "7_5_0.pre6"]
  prefix = "ExoVVAnalysis."
  
  directories = ["AK4_low", "AK4_high", "AK8_low", "AK8_high"]
  histNames = ["Jet_pt", "Jet_eta", "Jet_m", "Jet_phi", "Jet_e",
               "Jet_muf", "Jet_phf", "Jet_emf", "Jet_nhf", "Jet_chf",
               "Jet_area", "Jet_cm", "Jet_nm",
              ]
  histNamesAK8 = ["Jet_tau1", "Jet_tau2", "Jet_tau3",
                  "Jet_tau21", "Jet_tau32", "Jet_tau31",
                  "Jet_pruned_m", "Jet_softdrop_m",
                  "Jet_pruned_Wwindow_m", "Jet_softdrop_Wwindow_m",
                 ]

  _files = {}
  for sample in v_samples:

    inFile = "%s%s.root" %(prefix,sample)
    
    print "Opening "+inFile
    _files[sample]=TFile.Open(inFile,"READ")
  

  canvasList = []

  for i in range(len(histNames)):
    for direct in directories:
      hists = {}
      for sample in v_samples:
        hist = _files[sample].Get("%s/%s" %(direct,histNames[i]) )
        print "names: %s" %("%s/%s" %(direct,histNames[i]))
        hists["%s_%s_%s" %(sample, direct, histNames[i])] = hist.Clone("%s_%s_%s" %(sample, direct, histNames[i]))
        hist.Delete()
      
        # scale to unity
        hists["%s_%s_%s" %(sample, direct, histNames[i])].Scale(1./(hists["%s_%s_%s" %(sample, direct, histNames[i])].Integral(0, hists["%s_%s_%s" %(sample, direct, histNames[i])].GetNbinsX()+1)))
      MakeRatioPlot(hists["%s_%s_%s" %(v_samples[0], direct, histNames[i])], hists["%s_%s_%s" %(v_samples[1], direct, histNames[i])], "ratio_%s_%s" %(direct, histNames[i]))
      for sample in v_samples:
        hists["%s_%s_%s" %(sample, direct, histNames[i])].Delete()

  for i in range(len(histNamesAK8)):
    for direct in directories:
      if (direct.find("AK8") >= 0):
        hists = {}
        for sample in v_samples:
          hist = _files[sample].Get("%s/%s" %(direct,histNamesAK8[i]) )
          print "names: %s" %("%s/%s" %(direct,histNamesAK8[i]))
          hists["%s_%s_%s" %(sample, direct, histNamesAK8[i])] = hist.Clone("%s_%s_%s" %(sample, direct, histNamesAK8[i]))
          hist.Delete()
      
          # scale to unity
          hists["%s_%s_%s" %(sample, direct, histNamesAK8[i])].Scale(1./(hists["%s_%s_%s" %(sample, direct, histNamesAK8[i])].Integral(0, hists["%s_%s_%s" %(sample, direct, histNamesAK8[i])].GetNbinsX()+1)))
        canvasList.append(MakeRatioPlot(hists["%s_%s_%s" %(v_samples[0], direct, histNamesAK8[i])], hists["%s_%s_%s" %(v_samples[1], direct, histNamesAK8[i])], "ratio_%s_%s" %(direct, histNamesAK8[i])))
        for sample in v_samples:
          hists["%s_%s_%s" %(sample, direct, histNamesAK8[i])].Delete()

  # print "Filling summary canvas"
  # print canvasList
  # counter = 0
  # for canvas in canvasList:
  #   if (counter == 0):
  #     canvas.Print("plots/all.pdf[")
  #   elif (counter == len(canvasList)-1):
  #     canvas.Print("plots/all.pdf]")
  #     print "last"
  #   else:
  #     canvas.Print("plots/all.pdf")
  #   counter += 1
  c2 = TCanvas("empty", "empty", 500, 600)
  c2.Print("plots/all.pdf]")


def MakeRatioPlot(hist1, hist2, histOutName):

  hists = [hist1, hist2]
  default_Color = [kCyan-3, kRed+2]
  default_Style = [20, 24]
  default_Latex = ["%s" %(hist1.GetName()[0:hist1.GetName().find("_AK")]).replace(".","_"), "%s" %(hist2.GetName()[0:hist2.GetName().find("_AK")]).replace(".","_")]
  ratiohistos = {}
  c1 = TCanvas(histOutName, "plot", 500, 600)
  c1.Range(0,0,1,1)

  # ratio pad
  c1_1 = GetRatioPad()
  c1.cd()

  #main pad
  c1_2 = GetMainPad()
  y_max = 0

  for i in range(len(hists)): # loop over samples
#     hists[i].Scale(1./hists[i].Integral())
#     hists[i].Rebin(2)
    hists[i].SetMarkerColor(default_Color[i])
    hists[i].SetMarkerStyle(default_Style[i])
    hists[i].SetFillColor(0)
    hists[i].SetLineColor(default_Color[i])
    hists[i].SetLineStyle(i+1)
    hists[i].SetLineWidth(2)
    # hists[i].SetMarkerSize(2)
    # print hists[i].GetMarkerSize()
    hists[i].SetLabelSize(0.0)
    hists[i].SetTitleSize(0.00)
    binmin = hists[i].FindBin(-2.2);
    binmax = hists[i].FindBin(2.2);
    # print "Integral %i: %f" %(i, hists[i].Integral())
    c1_2.cd()
    if (i == 0):
      hists[i].Draw("e1")
      print "1st: %f" %hists[i].Integral()
#       hists[i].Draw("HIST")
      hists[i].GetYaxis().SetTitle("events scaled to unity")
      hists[i].GetYaxis().SetLabelSize(0.05)
      hists[i].GetYaxis().SetTitleSize(0.05)
      hists[i].GetYaxis().SetTitleOffset(1.7)
      if (histOutName.find("accep") >=0):
        hists[i].GetYaxis().SetTitle("acceptance")
      y_max = hists[i].GetMaximum()
      y_min = hists[i].GetMinimum()
    else:
#       hists[i].Draw("HIST same")
      hists[i].Draw("same")
      print "2nd: %f" %hists[i].Integral()
      c1.cd()
      if (hists[i].GetMaximum() > y_max):
        y_max = hists[i].GetMaximum()
      if (hists[i].GetMinimum() < y_min):
        y_min = hists[i].GetMinimum()
    # if ((histOutName.find("Eta") >=0) or (histOutName.find("NJetsPaper") >=0)):
    hists[0].GetYaxis().SetRangeUser(0.00001,y_max*1.5)
    if ((histOutName.find("HiggsMass") >=0)):
      c1_2.SetLogy(1)
    c1.cd()

    if (i != 0):
      ratiohistos[i] = (hists[i]).Clone("ratiohistos%i" %random.randint(0,10000))
      ratiohistos[i].Divide(hists[0])
      ratiohistos[i].SetMarkerColor(default_Color[i])
      ratiohistos[i].SetLineColor(default_Color[i])
      ratiohistos[i].SetMarkerSize(0)
      #hists[i].SetLineStyle(i+1)
      ratiohistos[i].GetXaxis().SetLabelSize(0.14)
      ratiohistos[i].GetXaxis().SetTitleSize(0.14)
      ratiohistos[i].GetXaxis().SetTitleOffset(0.)
      ratiohistos[i].GetYaxis().SetLabelSize(0.12)
      ratiohistos[i].GetYaxis().SetTitleSize(0.12)
      ratiohistos[i].GetYaxis().SetTitleOffset(0.7)
      ratiohistos[i].GetYaxis().SetTitle("ratio")
      ratiohistos[i].GetYaxis().SetRangeUser(0,1.999)
      ratiohistos[i].SetNdivisions(505,"x")
      ratiohistos[i].SetNdivisions(505,"y")
      
      title = "%s" %(hist1.GetName()[hist1.GetName().find("Jet")+4:])
      if (title == "pt"):
        ratiohistos[i].GetXaxis().SetTitle("p_{T} [GeV]")
      elif (title == "e"):
        ratiohistos[i].GetXaxis().SetTitle("E [GeV]")
      elif (title == "eta"):
        ratiohistos[i].GetXaxis().SetTitle("#eta")
      elif (title == "phi"):
        ratiohistos[i].GetXaxis().SetTitle("#phi")
      elif (title == "pruned_m"):
        ratiohistos[i].GetXaxis().SetTitle("pruned m [GeV]")
      elif (title == "softdrop_m"):
        ratiohistos[i].GetXaxis().SetTitle("softdrop m [GeV]")
      elif (title == "pruned_Wwindow_m"):
        ratiohistos[i].GetXaxis().SetTitle("pruned m [GeV]")
      elif (title == "softdrop_Wwindow_m"):
        ratiohistos[i].GetXaxis().SetTitle("softdrop m [GeV]")
      elif (title == "m"):
        ratiohistos[i].GetXaxis().SetTitle("m [GeV]")
      else:
        ratiohistos[i].GetXaxis().SetTitle(title)
      
      c1_1.cd()
      if (i == 1):
        ratiohistos[i].Draw("")
        ratiohistos[i].GetXaxis().SetTitleOffset(0.98)
      else:
        ratiohistos[i].Draw("same")
  c1.cd()
  
  TextBox2 = TLatex()
  TextBox2.SetNDC()
  TextBox2.SetTextSize(0.04)
  akType = hist1.GetName()[hist1.GetName().find("AK"):hist1.GetName().find("AK")+3]  
  TextBox2.DrawLatex(0.22,0.87,"%s Jets" %(akType))
  
  TextBox3 = TLatex()
  TextBox3.SetNDC()
  TextBox3.SetTextSize(0.03)
  cutsApplied = "p_{T} > 500 GeV, |#eta| < 2.4"
  if (histOutName.find("low") >= 0):
    cutsApplied = "p_{T} > 200 GeV, |#eta| < 2.4"
  TextBox3.DrawLatex(0.22,0.83,"%s" %(cutsApplied))
    
  if (len(hists) < 3):
    leg = GetLegend(hists, default_Latex, "two") # "two"
  else:
    leg = GetLegend(hists, default_Latex)
  leg.Draw()
  #c1_2.SetLogy(1)

  c1.SaveAs("plots/%s.pdf" %(histOutName))
  
  global firstCanvas
  if firstCanvas:
    c1.Print("plots/all.pdf[")
    firstCanvas = False
  else:
    c1.Print("plots/all.pdf")
  
  
  c1_2.SetLogy(1)
  c1.SaveAs("plots/%s_log.pdf" %(histOutName))
  c1.Clear()
  # c1_2.SetLogy(0)
  
  return c1


def GetRatioPad():
  c1_1 = TPad("c1_1", "newpad1",0.,0.,1,0.30)
  c1_1.Draw()
  c1_1.cd()
  c1_1.SetTopMargin(0)
  c1_1.SetBottomMargin(0.3)
  c1_1.SetRightMargin(0.1)
  c1_1.SetFillStyle(0)
  c1_1.SetGrid(1)
  return c1_1


def GetMainPad():
  c1_2 = TPad("c1_2", "newpad2",0.,0.3,1,1)
  c1_2.Draw()
  c1_2.cd()
  c1_2.SetTopMargin(0.1)
  c1_2.SetBottomMargin(0)
  c1_2.SetRightMargin(0.1)
  c1_2.SetFillStyle(0)
  #c1_2.SetGrid(1)
  return c1_2


def GetLegend(hists, default_Latex, option = ""):

  legend = 0
  if option == "top":
    legend = TLegend(.15, .95, .95, 1.)
    legend.SetNColumns(2)
    legend.SetTextSize(0.035)
  elif option == "ratio":
    legend = TLegend(.18, .75, .85, .915)
    legend.SetNColumns(2)
    legend.SetTextSize(0.0325)
  elif option == "datamc":
    legend = TLegend(.22, .735, .85, .905)
    legend.SetNColumns(2)
    legend.SetTextSize(0.035)
  elif option == "two":    
    if (hists[0].GetXaxis().GetTitle().find("exp") >= 0):
      legend = TLegend(.2, .8, .45, .95)
      legend.SetTextSize(0.04)
    else:
      legend = TLegend(.55, .8, .95, .92)
      legend.SetTextSize(0.04)
    
  else:
    legend = TLegend(.75, .55, .9, .95)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)
  legend.SetTextFont(42) #was 72, see http://root.cern.ch/root/html/TAttText.html#T53
  for i in range(len(hists)):
    identifier = i
#     if (("%s" %type(identifier)).find("str") >= 0):
#       if (len(identifier) == 1):
#         identifier = Samples[i]
    if identifier != "DATA":
#       if (i != 0) and (identifier in topSamples):
#         legend.AddEntry(hists[i], default_Latex[identifier], "f")
#       else:
        legend.AddEntry(hists[i], default_Latex[identifier], "pl")
    else:
      legend.AddEntry(hists[i], "%s (%i events)" %(default_Latex[identifier], hists[i].Integral(0, hists[i].GetNbinsX()+1)), "p")

  return legend


def SmoothHistogram(hist):

  smoothBins = 3
  if (smoothBins < 3) or (smoothBins%2 == 0):
    print "WARNING: skipping smoothing - need 3 or more bins and odd number!"
    return hist
  
  nBins = hist.GetNbinsX()
  loopStart = smoothBins%2+1
  loopEnd = nBins-smoothBins%2
  binLimit = smoothBins%2
  
  print "Smoothing %s" %hist.GetName()
  smoothedEntries = [None]*nBins
  for j in range(1,nBins+1):
    if (j < loopStart) or (j > loopEnd):
      smoothedEntries[j-1] = hist.GetBinContent(j)
    else:
      smoothedEntries[j-1] = hist.GetBinContent(j-binLimit)
      for k in range(j-binLimit+1,j+binLimit+1):
        smoothedEntries[j-1] += hist.GetBinContent(k)
      smoothedEntries[j-1] /= float(smoothBins)

  for j in range(1,nBins+1):
    hist.SetBinContent(j, smoothedEntries[j-1])

  return hist


if __name__ == "__main__":
  main()
