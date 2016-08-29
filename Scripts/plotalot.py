import os, array
from ROOT import *
import random
import sys
import optparse
import glob
# from math import pow,exp,sqrt
from PlotHelper import *

# global variables
currentSample=""
default_color = {}
samples = {}
files = {}
sampleDict = {}
plotFolder = "plots"
fullTeXTable = []
fullTeXTable_isFirstColumn = True

def MakeRatioPlot(hists, samples, default_Color, default_Latex, titleprefix, titlepostfix, histOutName, outputDir, cutName, currentCategory, default_extension, scaleToUnity = False, ratioRange = 0):

  ratiohistos = {}
  c1 = TCanvas(histOutName, "plot", 500, 600)
  c1.Range(0,0,1,1)

  # ratio pad
  c1_1 = GetRatioPad()
  if (histOutName.find("Jet_N") >=0) or (histOutName.find("jet1_pt") >=0):
    c1_1.SetGrid(0,0)
  c1.cd()

  #main pad
  c1_2 = GetMainPad()
  if (histOutName.find("Jet_N") >=0):
    c1_2.SetGrid(0,0)
  y_max = 0

  for i in range(len(hists)): # loop over samples
    #if (histOutName.find("eta") >=0) or (histOutName.find("jet1_pt") >=0):
    #  hists[i].Rebin(2)
    hists[i].SetMarkerColor(default_Color[samples[i]])
    hists[i].SetFillColor(0)
    hists[i].SetLineColor(default_Color[samples[i]])
    hists[i].SetLineStyle(i+1)
    hists[i].SetLabelSize(0.0)
    hists[i].SetTitleSize(0.00)
    if (scaleToUnity == True):
      if (i==0):
        print "Scaling to Unity"
      hists[i].Scale(1/hists[i].Integral(0, hists[i].GetNbinsX()+1))
    c1_2.cd()
    if (i == 0):
      #hists[i].Draw("e")
      hists[i].Draw("HIST")
      if not (scaleToUnity):
        hists[i].GetYaxis().SetTitle("Events / 4.7 fb^{-1}")
      y_max = hists[i].GetMaximum()
      y_min = hists[i].GetMinimum()
      if (histOutName.find("Jet_N") >=0) and not scaleToUnity:
        c1_2.SetLogy()
    else:
      #if (histOutName.find("Jet_N") <0):
      #  hists[i].Smooth()
      hists[i].Draw("HIST same")
      KS = hists[i].KolmogorovTest(hists[0])
      TextBox = TLatex()
      #TextBox.SetNDC()
      TextBox.SetTextSize(0.03)
      c1.cd()
      #TextBox.SetTextAngle(90)
      #TextBox.DrawLatex(0.52,0.93-float(i/27.),"%s KS: %3.2f" %(samples[i], KS))
      if (hists[i].GetMaximum() > y_max):
        y_max = hists[i].GetMaximum()
      if (hists[i].GetMinimum() < y_min):
        y_min = hists[i].GetMinimum()
    if (histOutName.find("eta") >=0):
      hists[0].GetYaxis().SetRangeUser(0.001,y_max*1.3)
    else:
      hists[0].GetYaxis().SetRangeUser(0.001,y_max*1.2) # fix for Logy #change for N Jet logscale
    if (histOutName.find("Jet_N") >=0):
      hists[0].GetXaxis().SetRangeUser(0.5,5.5)
    MeanBox = TLatex()
    MeanBox.SetTextSize(0.03)
    MeanBox.SetTextAngle(90)
    c1.cd()
    #MeanBox.DrawLatex(0.9+float((i+1)/32.),0.2,"%s Mean: %3.2f (%i entries)" %(samples[i], hists[i].GetMean(), hists[i].GetEntries()))

    if (i != 0):
      ratiohistos[i] = (hists[i]).Clone("ratiohistos%i" %random.randint(0,10000))
      ratiohistos[i].Divide(hists[0])
      ratiohistos[i].SetMarkerColor(default_Color[samples[i]])
      #ratiohistos[i].SetFillColor(default_Color[samples[i]])
      ratiohistos[i].SetLineColor(default_Color[samples[i]])
      hists[i].SetLineStyle(i+1)
      ratiohistos[i].GetXaxis().SetLabelSize(0.14)
      ratiohistos[i].GetXaxis().SetTitleSize(0.14)
      ratiohistos[i].GetXaxis().SetTitleOffset(0.7)
      ratiohistos[i].GetYaxis().SetLabelSize(0.1)
      ratiohistos[i].GetYaxis().SetTitleSize(0.1)
      ratiohistos[i].GetYaxis().SetTitleOffset(0.7)
      ratiohistos[i].GetYaxis().SetTitle("ratio")
      if ratioRange == 0:
        if (scaleToUnity == True):
          ratiohistos[i].GetYaxis().SetRangeUser(0.6,1.4)
        else:
          ratiohistos[i].GetYaxis().SetRangeUser(0,2)
      else:
        ratiohistos[i].GetYaxis().SetRangeUser(ratioRange[0],ratioRange[1])
      #if (histOutName.find("Jet_N") >=0) or (histOutName.find("jet1_pt") >=0):
      #  c1_1.SetLogy()
      #  #c1_2.SetLogy()
      c1_1.cd()
      if (i == 1):
        ratiohistos[i].Draw("e")
        ratiohistos[i].GetXaxis().SetTitleOffset(0.98)
        if (histOutName.find("Jet_N") >=0):
          ratiohistos[i].GetXaxis().SetRangeUser(0.5,5.5)
          for f in range(2,7):
            ratiohistos[i].GetXaxis().SetLabelSize(0.2)
            if (f == 6):
              ratiohistos[i].GetXaxis().SetBinLabel(f, "#geq%i"%(f-1))
            else:
              ratiohistos[i].GetXaxis().SetBinLabel(f, "%i"%(f-1))
      else:
        ratiohistos[i].Draw("same e")
  c1.cd()
  if (len(hists) < 3):
    leg = GetLegend(hists, samples, default_Latex, "two")
  else:
    leg = GetLegend(hists, samples, default_Latex)
  leg.Draw()
  #c1_2.SetLogy(1)

  if (scaleToUnity):
    c1.SaveAs("%s/%s/%s/%s%s%s_unity%s" %(outputDir, cutName, currentCategory, titleprefix, histOutName, titlepostfix, default_extension))
  else:
    c1.SaveAs("%s/%s/%s/%s%s%s%s" %(outputDir, cutName, currentCategory, titleprefix, histOutName, titlepostfix, default_extension))
  c1.Clear()

  return



def MakeSimplePlot(hists, samples, default_Color, default_Latex, titleprefix, titlepostfix, histOutName, outputDir, cutName, currentCategory, default_extension, lumi, scaleToUnity = False):

  ratiohistos = {}
  c1 = TCanvas(histOutName, "plot", 500, 500)
  c1.SetRightMargin(0.05)
  # c1.Range(0,0,1,1)

  y_max = 0
  
  for i in range(len(hists)): # loop over samples
    #if (histOutName.find("eta") >=0) or (histOutName.find("jet1_pt") >=0):
    #  hists[i].Rebin(2)
    hists[i].SetMarkerColor(default_Color[samples[i][0]])
    hists[i].SetFillColor(0)
    hists[i].SetLineColor(default_Color[samples[i][0]])
    hists[i].SetLineStyle(i+1)
    # hists[i].SetLabelSize(0.0)
    # hists[i].SetTitleSize(0.00)
    if (scaleToUnity == True):
      if (i==0):
        print "Scaling to Unity"
      hists[i].Scale(1/hists[i].Integral(0, hists[i].GetNbinsX()+1))
    if (i == 0):
      # hists[i].Draw("p e")
      hists[i].Draw("hist e")
      hists[i].GetXaxis().SetTitleOffset(1.1)
      hists[i].GetYaxis().SetTitleOffset(1.8)
      # if not (scaleToUnity):
        # hists[i].GetYaxis().SetTitle("Events / X fb^{-1}")
      y_max = hists[i].GetMaximum()
      y_min = hists[i].GetMinimum()
      if (histOutName.find("Jet_N") >=0) and not scaleToUnity:
        c1.SetLogy()
    else:
      # hists[i].Draw("p e same")
      hists[i].Draw("hist same")
      # TextBox.SetTextSize(0.03)
      c1.cd()
      if (hists[i].GetMaximum() > y_max):
        y_max = hists[i].GetMaximum()
      if (hists[i].GetMinimum() < y_min):
        y_min = hists[i].GetMinimum()
    # if (histOutName.find("eta") >=0):
      # hists[0].GetYaxis().SetRangeUser(0.001,y_max*1.3)
#     else:
      hists[0].GetYaxis().SetRangeUser(0.001,y_max*1.2) # fix for Logy #change for N Jet logscale
#     if (histOutName.find("Jet_N") >=0):
#       hists[0].GetXaxis().SetRangeUser(0.5,5.5)

  c1.cd()
  if (len(hists) < 3):
    leg = GetLegend(hists, samples, default_Latex, "two")
  else:
    leg = GetLegend(hists, samples, default_Latex, "ratio")
  leg.Draw()
  
  # TextBox = TLatex()
#   TextBox.SetNDC()
#   TextBox.SetTextSize(0.03)
#   TextBox.DrawLatex(0.75,0.96, "%3.1f fb^{-1} (13 TeV)" %(lumi/1000.))
  AddLumi(lumi)
  
  #c1_2.SetLogy(1)

  if (scaleToUnity):
    c1.SaveAs("%s/%s/%s/%s%s%s_unity%s" %(outputDir, cutName, currentCategory, titleprefix, histOutName, titlepostfix, default_extension))
  else:
    c1.SaveAs("%s/%s/%s/%s%s%s%s" %(outputDir, cutName, currentCategory, titleprefix, histOutName, titlepostfix, default_extension))
    if (histOutName.find("dijet_m") >= 0):
      c1.SetLogy(1)
      c1.SaveAs("%s/%s/%s/%s%s%s_log%s" %(outputDir, cutName, currentCategory, titleprefix, histOutName, titlepostfix, default_extension))
  c1.Clear()

  return



def WriteTeXFile(outputDir, cutName, currentCategory, channel, Samples, default_Latex, hists):
  
  global fullTeXTable_isFirstColumn
  #global fullTeXTable #reset
  sumMC = 0
  quadErrMC = 0
  print "Creating LaTeX table:\n"
  texfile = open("%s/%s/%s/yields_%s.tex" %(outputDir, cutName, currentCategory, channel), 'w')
  texfile.write("\\documentclass[a4paper,12pt]{article}\n")
  texfile.write("\\def\MET{\\ensuremath{E_{\\mathrm{T}}^{\\mathrm{miss}}}}\n")
  texfile.write("\\begin{document}\n")
  texfile.write("\\begin{table}[htbp]\n")
  texfile.write("\\begin{center}\n")
  texfile.write("\\caption{Number of expected events after cut %s in %s of %s channel}\n" %(cutName, currentCategory, channel))
  texfile.write("\\begin{tabular}{l|r}\n")
  texfile.write("\\hline\n")
  texfile.write("    Process        & Events \\\\\n")
  texfile.write("    \\hline\n")
  loopmax = len(Samples)
  if (hists[0].GetName().find("truth") >=0): loopmax += 3
  for k in range(0,loopmax):
    interror = Double()
    intvalue = hists[k].IntegralAndError(0,hists[k].GetNbinsX()+1, interror)
    print "%s: \t %5.1f; %5.1f" %(default_Latex[hists[k].GetName().split("-")[0]], intvalue, interror)
    texfile.write("$%s$         & \t $%8.1f \pm %8.1f$ \\\\ \n" %(default_Latex[hists[k].GetName().split("-")[0]].replace("#","\\"),intvalue, interror))
    
    if (fullTeXTable_isFirstColumn):
      fullTeXTable.append("$%s$         & \t %5.0f; %5.0f" %(default_Latex[hists[k].GetName().split("-")[0]].replace("#","\\"),intvalue, interror))
    else:
      if (k < loopmax-1):
        fullTeXTable[k] += ("& \t %5.0f; %5.0f" %(intvalue, interror))
      else:
        fullTeXTable[loopmax] += ("& \t %5.0f; %5.0f" %(intvalue, interror))
    if (k < loopmax):
      sumMC += intvalue
      quadErrMC += interror*interror
    if (k == loopmax-2):
      print "Sum predicted: \t %8.1f" %sumMC
      texfile.write("\\hline\n")
      texfile.write("sum predicted         & \t $%8.1f$ \\\\ \n" %(sumMC))
      if (fullTeXTable_isFirstColumn):
        fullTeXTable.append("sum predicted         & \t %5.0f; %5.0f" %(sumMC,sqrt(quadErrMC)))
      else:
        fullTeXTable[loopmax-1] += ("& \t %5.0f; %5.0f" %(sumMC,sqrt(quadErrMC)))
      texfile.write("\\hline\n")
  texfile.write("\\hline\n")
  texfile.write("\\end{tabular}\n")
  texfile.write("\\end{center}\n")
  texfile.write("\\label{tab:yields}\n") 
  texfile.write("\\end{table}\n")
  texfile.write("\\end{document}\n")
  texfile.close()
  fullTeXTable_isFirstColumn = False
  
  texfile = open("%s/%s/yields_%s.tex" %(outputDir, cutName, channel), 'w')
  texfile.write("\\documentclass[a4paper,12pt]{article}\n")
  texfile.write("\\usepackage{booktabs}\n")
  texfile.write("\\begin{document}\n")
  texfile.write("\\begin{table}[htbp]\n")
  texfile.write("\\begin{center}\n")
  texfile.write("\\caption{Number of expected events after cut %s of %s channel}\n" %(cutName, channel))
  texfile.write("\\begin{tabular}{l|r|r|r|r}\n")
  texfile.write("\\toprule\n")
  texfile.write("    Process        & Events \\\\\n")
  texfile.write("    \\midrule\n")
  for i in range(len(fullTeXTable)):
    texfile.write("%s \\\\\n" %( fullTeXTable[i] ) ) 
  texfile.write("\\bottomrule\n")
  texfile.write("\\end{tabular}\n")
  texfile.write("\\end{center}\n")
  texfile.write("\\label{tab:yields}\n") 
  texfile.write("\\end{table}\n")
  texfile.write("\\end{document}\n")
  texfile.close()  
  
  return


def MakeDataMCPlot(datahist, stackedhists, legend, targetLumi, histOutName, cutName, outputDir, currentCategory, default_extension):
  
  canvas=TCanvas(histOutName, histOutName, 500, 500)
  canvas.SetTopMargin(0.072)
  canvas.SetLeftMargin(0.19)
  canvas.Draw()

  datahist.Draw("")
  datahist.GetYaxis().SetRangeUser(0.,datahist.GetMaximum()*1.4)
  datahist.GetYaxis().SetTitleOffset(2)
  if (histOutName.find("Jet_N") >=0):
    datahist.GetXaxis().SetRangeUser(1.5,5.5)
    datahist.GetYaxis().SetRangeUser(0.001,datahist.GetMaximum()*0.7)
  stackedhists.Draw("histsame")
  datahist.Draw("same")
  legend.Draw()
  gPad.RedrawAxis()
  #AddWatermark()
  AddLumi(targetLumi)
  canvas.SaveAs("%s/%s/%s/%s%s" %(outputDir, cutName, currentCategory, histOutName, default_extension))
  canvas.Clear()

  return


def MakeDataMCRatioPlot(hists, stackedhists, datahist, outputDir, histname, currentCategory, default_extension, default_Latex, Samples, targetLumi):

  ratiohistos = {}
  canvas = TCanvas(histname, "plot", 600, 800)
  canvas.Range(0,0,1,1)

  # ratio pad
  canvas_1 = GetRatioPad()
  canvas.cd()

  #main pad
  canvas_2 = GetMainPad()

  for i in range(len(hists)):
    hists[i].SetLabelSize(0.0)
    hists[i].SetTitleSize(0.00)
  sumhist = GetSum(hists, Samples)

  canvas_2.cd()
  datahist.Draw("")
  datahist.GetYaxis().SetRangeUser(0.001,datahist.GetMaximum()*1.25)
  datahist.GetYaxis().SetTitleOffset(1.75)
  if (histname.find("Jet_N") >=0):
    datahist.GetXaxis().SetRangeUser(1.5,5.5)
    datahist.GetYaxis().SetRangeUser(0.001,datahist.GetMaximum()*0.6)
  stackedhists.Draw("histsame")
  sumhist.Draw("same")
  datahist.Draw("same")
  
  #KS = sumhist.KolmogorovTest(datahist, "X")
  #TextBox = TLatex()
  #TextBox.SetNDC()
  #TextBox.SetTextSize(0.04)
  #canvas.cd()
  #TextBox.DrawLatex(0.15,0.95,"KS: %3.2f" %(KS))
  #MeanBox = TLatex()
  #MeanBox.SetTextSize(0.03)
  #MeanBox.SetTextAngle(90)
  #canvas.cd()
  #MeanBox.DrawLatex(0.93,0.4,"Mean: %3.2f (data) vs. %3.2f (MC+QCD)" %(datahist.GetMean(), sumhist.GetMean()))

  ratiohist = (datahist.Clone("ratiohistos%i" %random.randint(0,10000)))
  ratiohist.Divide(sumhist)
  ratiohist.SetMarkerColor(1)
  ratiohist.SetFillColor(1)
  ratiohist.SetLineColor(1)
  ratiohist.GetXaxis().SetLabelSize(0.14)
  ratiohist.GetXaxis().SetTitleSize(0.14)
  ratiohist.GetXaxis().SetTitleOffset(0.95)
  ratiohist.GetYaxis().SetTitle("data/prediction")
  ratiohist.GetYaxis().SetLabelSize(0.1)
  ratiohist.GetYaxis().SetTitleSize(0.1)
  ratiohist.GetYaxis().CenterTitle()
  ratiohist.GetYaxis().SetTitleOffset(0.8)
  ratiohist.GetYaxis().SetRangeUser(0.601,1.399)
  
  canvas_1.cd()
  ratiohist.Draw("e")

  canvas.cd()
  legend = GetLegend(hists, Samples, default_Latex, "ratio")
  legend.Draw()
  #canvas_2.SetLogy(1)
  #AddWatermark()
  AddLumi(targetLumi)

  # [histOutName, cutName] = histname.rsplit("_",1)
  histOutName = histname
  cutName = ""
  canvas.SaveAs("%s/%s/%s/ratios/%s%s" %(outputDir, cutName, currentCategory, histOutName, default_extension))
  canvas.Clear()

  return


def MakeDataAllMCPlot(datahist, stackedhists, legend, targetLumi, histOutName, cutName, outputDir, currentCategory, default_extension):
  
  canvas=TCanvas(histOutName, histOutName, 800, 600)
  canvas.Draw()

  datahist.Draw("")
  datahist.GetYaxis().SetRangeUser(0.,datahist.GetMaximum()*1.5)
  if (histOutName.find("Jet_N") >=0):
    datahist.GetXaxis().SetRangeUser(1.5,5.5)
  stackedhists[0].Draw("histsame")
  for i in range(1,len(stackedhists)):
    stackedhists[i].Draw("same")
  datahist.Draw("same")
  legend.Draw()
  gPad.RedrawAxis()
  AddWatermark()
  AddLumi(targetLumi)
  canvas.SaveAs("%s/%s/%s/%s%s" %(outputDir, cutName, currentCategory, histOutName, default_extension))
  canvas.Clear()

  return


def MakeDataAllMCRatioPlot(hists, stackedhists, datahist, outputDir, histname, currentCategory, default_extension, default_Latex, Samples, targetLumi):

  ratiohistos = {}
  canvas = TCanvas(histname, "plot", 600, 800)
  canvas.Range(0,0,1,1)

  # ratio pad
  canvas_1 = GetRatioPad()
  canvas.cd()

  #main pad
  canvas_2 = GetMainPad()

  for i in range(len(hists)):
    hists[i].SetLabelSize(0.0)
    hists[i].SetTitleSize(0.00)
    #for bins in range(1,hists[i].GetNbinsX()+1):
    #  print "i = %i - bin %i: %f" %(i, bins, hists[i].GetBinContent(bins))
  sumhist = stackedhists[0].GetStack().Last()

  canvas_2.cd()
  datahist.Draw("")
  datahist.GetYaxis().SetRangeUser(0.001,datahist.GetMaximum()*1.25)
  datahist.GetYaxis().SetTitleOffset(1.75)
  if (histname.find("Jet_N") >=0):
    datahist.GetXaxis().SetRangeUser(1.5,5.5)
    datahist.GetYaxis().SetRangeUser(0.001,datahist.GetMaximum()*0.6)
  stackedhists[0].Draw("histsame")
  #stackedhists[0].SetMarkerSize(0.)
  for i in range(1,len(stackedhists)):
    stackedhists[i].Draw("same")
    stackedhists[i].SetLabelSize(0.0)
    stackedhists[i].SetTitleSize(0.00)
    stackedhists[i].SetMarkerSize(0.2)
  sumhist.Draw("same")
  datahist.Draw("same")
  canvas_2.RedrawAxis()
  
  #KS = sumhist.KolmogorovTest(datahist, "X")
  #TextBox = TLatex()
  #TextBox.SetTextSize(0.04)
  #canvas.cd()
  #TextBox.DrawLatex(0.15,0.95,"KS: %3.2f" %(KS))
  #MeanBox = TLatex()
  #MeanBox.SetTextSize(0.03)
  #MeanBox.SetTextAngle(90)
  #canvas.cd()
  #MeanBox.DrawLatex(0.93,0.4,"Mean: %3.2f (data) vs. %3.2f (MC+QCD)" %(datahist.GetMean(), sumhist.GetMean()))

  canvas_1.cd()
  ratiohists = []
  for i in range(len(stackedhists)):
    ratiohists.append(datahist.Clone("ratiohistos%i" %random.randint(0,10000)))
    if i == 0:
      ratiohists[i].Divide(sumhist)
      ratiohists[i].SetMarkerColor(hists[0].GetMarkerColor())
      ratiohists[i].SetMarkerStyle(hists[0].GetMarkerStyle())
      ratiohists[i].SetFillColor(hists[0].GetFillColor())
      ratiohists[i].SetLineColor(hists[0].GetLineColor())
    else:
      ratiohists[i].Divide(stackedhists[i])
      ratiohists[i].SetMarkerColor(stackedhists[i].GetMarkerColor())
      ratiohists[i].SetMarkerStyle(stackedhists[i].GetMarkerStyle())
      ratiohists[i].SetFillColor(stackedhists[i].GetFillColor())
      ratiohists[i].SetLineColor(stackedhists[i].GetLineColor())
    ratiohists[i].GetXaxis().SetLabelSize(0.14)
    ratiohists[i].GetXaxis().SetTitleSize(0.14)
    ratiohists[i].GetXaxis().SetTitleOffset(0.95)
    ratiohists[i].GetYaxis().SetTitle("data/prediction")
    ratiohists[i].GetYaxis().SetLabelSize(0.1)
    ratiohists[i].GetYaxis().SetTitleSize(0.1)
    ratiohists[i].GetYaxis().CenterTitle()
    ratiohists[i].GetYaxis().SetTitleOffset(0.8)
    ratiohists[i].GetYaxis().SetRangeUser(0.601,1.399)
    if (histname.find("Jet_N") >=0):
      ratiohists[i].GetYaxis().SetRangeUser(0.801,1.199)
    if i == 0:
      ratiohists[i].Draw("e")
    else:
      ratiohists[i].Draw("same")
  canvas.cd()
  gPad.RedrawAxis()
  legend = GetLegend(hists, Samples, default_Latex, "ratio")
  legend.Draw()
  #canvas_2.SetLogy(1)
  #AddWatermark()
  AddLumi(targetLumi)
 

  [histOutName, cutName] = histname.rsplit("_",1)
  canvas.SaveAs("%s/%s/%s/ratios/%s%s" %(outputDir, cutName, currentCategory, histOutName, default_extension))
  canvas.Clear()

  return


def PlotPtEtaPhiE(file, prefix, postfix, titleprefix):

  c1 = TCanvas("c1","Colour Flow",800,600)
  c1.Draw()
  gPad.SetGrid(1)
  plotlist = ["eta", "phi", "pt", "e", "m"]
  for plot in plotlist:
    hist = file.Get("%s_%s%s" %(prefix, plot, postfix) )
    #hist.Sumw2()

    hist = OverflowToLast(hist)
    hist.Draw()
    hist.GetYaxis().SetRangeUser(0.,hist.GetMaximum()*1.2)
    c1.SaveAs(outputFolder+titleprefix+plot+".png")

  return



def PlotPtEtaPhiERatios(files, prefix, postfix, titleprefix):

  plotlist = ["eta", "phi", "pt", "e", "m"]
  for i in range(len(plotlist)):
    hists = []
    for j in range(len(files)):
      hists += [files[j].Get("%s_%s%s" %(prefix, plotlist[i], postfix) )]
      #hists[i].Sumw2()
      hists[j] = OverflowToLast(hists[j])
    MakeRatioPlot(hists, titleprefix, "", plotlist[i])

  return



def PlotPullSampleRatios(files, prefix, postfix, titlepostfix):

  plotlist = ["truthjet_DeltaR", "truthjet_pull_phi", "truthjet_pull_deltaphi", "truthjet_pull_theta", "truthjet_pull_deltatheta", "truthjet_pull_theta_min", "truthjet_pull_omega", "truthjet_pull_omega_variance", "truthjet_pull_variance", "truthjet_conepull_variance", "truthjet_conepull_omega", "truthjet_pull_omega_abs", "truthjet_conepull_omega_abs", "truthjet_pull_deltaomega", "truthjet_pull_omega_min", "truthjet_dipolarity", "truthjet_dipolarity04", "truthjet_slac_dipolarity", "truthjet_slac_orthdipolarity"]
  for i in range(len(plotlist)):
    hists = []
    for j in range(len(files)):
      hists += [files[j].Get("%s_%s%s" %(prefix, plotlist[i], postfix) )]
      if ("%s" %type(hists[j])).find("TH1") < 0:
        print "hist %s_%s%s not found!" %(prefix, plotlist[i], postfix)
        sys.exit()
      #hists[i].Sumw2()
      hists[j] = OverflowToLast(hists[j])
      hists[j].Rebin()
    MakeRatioPlot(hists, "", titlepostfix, plotlist[i])

  return


def PlotSinglePullSampleRatios(files, prefix, postfix, titlepostfix):

  plotlist = ["truthjet_pull_phi", "truthjet_pull_theta", "truthjet_conepull_theta", "truthjet_pull_omega", "truthjet_pull_omega_variance", "truthjet_pull_variance", "truthjet_conepull_variance", "truthjet_conepull_omega", "truthjet_pull_omega_abs", "truthjet_pull_omega_variance_abs", "truthjet_conepull_omega_abs"]
  for i in range(len(plotlist)):
    hists = []
    for j in range(len(files)):
      hists += [files[j].Get("%s_%s%s" %(prefix, plotlist[i], postfix) )]
      #hists[i].Sumw2()
      hists[j] = OverflowToLast(hists[j])
      hists[j].Rebin()
    MakeRatioPlot(hists, "", titlepostfix, plotlist[i])

  return


def PlotPullStuffRatios(tree, branchnames, axislabel, cuts, addlabel=""):

  ratiohistos = {}
  hists = []
  c1 = TCanvas(branchnames[0], "plot", 800, 600)
  

  for i in range(len(branchnames)): # loop over samples
    if branchnames[i].find("dipolarity") > 0:
      hists += [TH1D("pullratiohist%i"%i,";%s;a.u."%(axislabel), 40, 0, 20)]
    else:
      hists += [TH1D("pullratiohist%i"%i,";%s;a.u."%(axislabel), 10, 0, 3.1415)]
    hists[i].Sumw2()
    tree.Draw(branchnames[i]+">>pullratiohist%i"%i, cuts[i], "e")
    hists[i] = OverflowToLast(hists[i])

  c1.Clear()
  c1.Range(0,0,1,1)

  # ratio pad
  c1_1 = GetRatioPad()
  c1.cd()

  #main pad
  c1_2 = GetMainPad()

  #stack = THStack("pullstuff", "Pull Ratios")
  for i in range(len(branchnames)): # loop over samples
    hists[i].SetMarkerColor(i+1)
    hists[i].SetFillColor(i+1)
    hists[i].SetLineColor(i+1)
    hists[i].SetLabelSize(0.0)
    hists[i].SetTitleSize(0.00)
    hists[i].Scale(1/hists[i].Integral(0, hists[i].GetNbinsX()+1))
    c1_2.cd()
    if (i == 0):
      hists[i].Draw("e")
    else:
      hists[i].Draw("e same")
      KS = hists[i].KolmogorovTest(hists[0])
      TextBox = TLatex()
      TextBox.SetTextSize(0.03)
      c1.cd()
      TextBox.DrawLatex(0.62,0.93-float(i/27.),"KS: %3.2f" %(KS))
      

    if (i != 0):
      ratiohistos[i] = (hists[i]).Clone("ratiohistos%i" %random.randint(0,10000))
      ratiohistos[i].Divide(hists[0])
      ratiohistos[i].SetMarkerColor(i+1)
      ratiohistos[i].SetFillColor(i+1)
      ratiohistos[i].SetLineColor(i+1)
      ratiohistos[i].GetXaxis().SetLabelSize(0.14)
      ratiohistos[i].GetXaxis().SetTitleSize(0.14)
      ratiohistos[i].GetXaxis().SetTitleOffset(0.7)
      ratiohistos[i].GetYaxis().SetLabelSize(0.1)
      ratiohistos[i].GetYaxis().SetTitleSize(0.1)
      ratiohistos[i].GetYaxis().SetRangeUser(0.,2.)
      c1_1.cd()
      if (i == 1):
        ratiohistos[i].Draw("e")
      else:
        ratiohistos[i].Draw("same e")
  c1.cd()
  leg = GetLegend(hists, branchnames)
  leg.Draw()
  #c1_2.SetLogy(1)
  
  if (branchnames[0] == "truthjet_pull_omega"):
    print "adding bird"
    img = TImage.Open("tucan.jpg");
    img.Scale(76,90)
    pad = TPad("bird","bird", 0.9, 0.9, 1.0, 1.)
    pad.Draw()
    pad.cd()
    img.Draw()
  
  c1.SaveAs(outputFolder+"ratios/"+branchnames[0]+addlabel+".png")
  c1.Clear()

  return


def PlotKinematics(singleDistributions = True):

  global files
  global outputFolder
  dRCuts = ["_dR10", "_dR15", "_dR20"]#, "_dR25", "_dR30", "_dR50"]
  mjjCuts = [10000, 15000, 20000, 25000, 30000, 40000]
  mttCuts = [400000, 500000, 600000, 800000, 1000000]
  ttptCuts = [25000, 50000, 100000, 150000, 200000]

  # single sample distributions
  if (singleDistributions == True):
    for i in range(len(files)):
      outputFolder = plotFolder + "/" + samples[i] + "/"
      #plot single distributions for each sample
      PlotPtEtaPhiE(files[i], "Analysis/top/h_top", "_top", "anytop_")
      PlotPtEtaPhiE(files[i], "Analysis/w/h_w", "_w", "anyW_")
      PlotPtEtaPhiE(files[i], "Analysis/truth/h_truth", "_lepton", "lepton_")
      PlotPtEtaPhiE(files[i], "Analysis/truth/h_truth", "_neutrino", "neutrino_")
      PlotPtEtaPhiE(files[i], "Analysis/truth/h_truth", "_lightquark", "lightquark_")
      PlotPtEtaPhiE(files[i], "Analysis/truth/h_truth", "_bquark", "bquark_")
      #PlotPtEtaPhiE(topTree, "", "truth_interacting_", "", "hadrons_")
      PlotPtEtaPhiE(files[i], "Analysis/jets/h_jet", "_all", "jets_all_")
      PlotPtEtaPhiE(files[i], "Analysis/jets/h_jet", "_jet1", "jets_j1_")
      PlotPtEtaPhiE(files[i], "Analysis/jets/h_jet", "_jet2", "jets_j2_")
      PlotPtEtaPhiE(files[i], "Analysis/jets/h_jet", "_jet3", "jets_j3_")
      PlotPtEtaPhiE(files[i], "Analysis/jets/h_jet", "_jet4", "jets_j4_")
      #loop over cuts, add them to cuts and print cut on plot and save with adjusted filename
      PlotPull(files[i], "Analysis/colourflow/h", "_lightjet", "")
      for cut in dRCuts:
        PlotPull(files[i], "Analysis/colourflow/h", "_lightjet%s" %cut, "%s" %cut)
      #for cut in mjjCuts:
        #PlotPull(files[i], "Analysis/colourflow/h", "_lightjet%s" %cut, "%s" %cut)
      #for cut in mttCuts:
        #PlotPull(files[i], "Analysis/colourflow/h", "_lightjet%s" %cut, "%s" %cut)
    

  # ratios
  print "Plotting ratios"
  gStyle.SetOptStat(0)
  outputFolder = plotFolder + "/"
  PlotPullSampleRatios(files, "Analysis/colourflow/h", "_lightjet", "")
  PlotSinglePullSampleRatios(files, "Analysis/colourflow_single/h", "_single_lightjet_j1", "_j1")
  PlotSinglePullSampleRatios(files, "Analysis/colourflow_single/h", "_single_lightjet_j2", "_j2")
  for cut in dRCuts:
    PlotPullSampleRatios(files, "Analysis/colourflow/h", "_lightjet%s" %cut, "%s" %cut)
    PlotSinglePullSampleRatios(files, "Analysis/colourflow_single/h", "_single_lightjet_j1%s" %cut, "_j1%s" %cut)
    PlotSinglePullSampleRatios(files, "Analysis/colourflow_single/h", "_single_lightjet_j2%s" %cut, "_j2%s" %cut)
  #for cut in mjjCuts:
    #PlotPullSampleRatios(files, "Analysis/colourflow/h", "_lightjet%s" %cut, "%s" %cut)
  #for cut in mttCuts:
    #PlotPullSampleRatios(files, "Analysis/colourflow/h", "_lightjet%s" %cut, "%s" %cut)
  #for cut in ttptCuts:
    #PlotPullSampleRatios(files, "Analysis/colourflow/h", "_lightjet%s" %cut, "%s" %cut)
  PlotPtEtaPhiERatios(files, "Analysis/top/h_top", "_top", "anytop_")
  PlotPtEtaPhiERatios(files, "Analysis/w/h_w", "_w", "anyW_")
  PlotPtEtaPhiERatios(files, "Analysis/truth/h_truth", "_lepton", "lepton_")
  PlotPtEtaPhiERatios(files, "Analysis/truth/h_truth", "_neutrino", "neutrino_")
  PlotPtEtaPhiERatios(files, "Analysis/truth/h_truth", "_lightquark", "lightquark_")
  PlotPtEtaPhiERatios(files, "Analysis/truth/h_truth", "_bquark", "bquark_")
  #PlotPtEtaPhiERatios(files, "", "truth_interacting_", "hadrons_")
  PlotPtEtaPhiERatios(files, "Analysis/jets/h_jet", "_all", "jets_all_")
  PlotPtEtaPhiERatios(files, "Analysis/jets/h_jet", "_jet1", "jets_j1_")
  PlotPtEtaPhiERatios(files, "Analysis/jets/h_jet", "_jet2", "jets_j2_")
  PlotPtEtaPhiERatios(files, "Analysis/jets/h_jet", "_jet3", "jets_j3_")
  PlotPtEtaPhiERatios(files, "Analysis/jets/h_jet", "_jet4", "jets_j4_")
  
  return


def PlotPull(file, prefix, postfix, titlepostfix):

  #difference between b and light jets!!!!!!!
  plotlist = ["truthjet_DeltaR", "truthjet_pull_phi", "truthjet_pull_deltaphi", "truthjet_pull_theta", "truthjet_pull_deltatheta", "truthjet_pull_theta_min", "truthjet_pull_omega", "truthjet_pull_omega_variance", "truthjet_pull_variance", "truthjet_conepull_omega", "truthjet_pull_omega_abs", "truthjet_pull_omega_variance_abs", "truthjet_conepull_omega_abs", "truthjet_pull_deltaomega", "truthjet_pull_omega_min", "truthjet_dipolarity", "truthjet_dipolarity04", "truthjet_slac_dipolarity", "truthjet_slac_orthdipolarity"]
  #pullxaxis = ["#phi", "#Delta #phi", "#theta", "#Delta #theta", "min(#theta)", "#omega", "#omega", "#Delta #omega", "min(#omega)", "dipolarity", "orth. dipolarity"]

  c1 = TCanvas("c1","Colour Flow",800,600)
  c1.Draw()
  gPad.SetGrid(1)
  for plot in plotlist:
    hist = file.Get("%s_%s%s" %(prefix, plot, postfix) )
    if ("%s" %type(hist)).find("TH1") < 0:
      print "hist %s_%s%s not found!" %(prefix, plot, postfix)
      sys.exit()
    #hist.Sumw2()
    hist = OverflowToLast(hist)
    hist.Draw()
    hist.GetYaxis().SetRangeUser(0.,hist.GetMaximum()*1.2)
    c1.SaveAs(outputFolder+plot+titlepostfix+".png")
  return


def SetColours():

  global default_Color
  colourList = [1, 619, 62, 92, 51, 93, 94, 96, 95, 97]
  default_Color={}
  for i in range(len(samples)):
    default_Color[samples[i]]= colourList[i]

  return

def plotAll(theseSamples, thisPlotFolder, singleDistributions = True):
  
  global files
  global plotFolder
  global samples
  global outputFolder
  
  samples = theseSamples
  plotFolder = thisPlotFolder
  files = []
  
  SetColours()

  print "Opening files"
  for sample in samples:
    outputFolder = plotFolder + "/" + sample + "/"
    filename = "ColourFlowAnalysis.Hists." + sample + ".root"
    print "Opening %s" % filename
    file = TFile.Open(filename)
    file.cd()
    files += [file]

  gStyle.SetOptStat(0)
  outputFolder = plotFolder + "/"
  PlotKinematics(singleDistributions)
  
  # close file at the end
  for file in files:  
    file.Close()
  
  return


def ReweightToSample(hist, weightHist, NJetHistName, Samples, inputSamples, files, scales, currentCategory, channel):
  
  print "Before %f" %hist.Integral()
  NJethists = GetHists(NJetHistName, Samples, inputSamples, files, scales, "3jincl", channel, scaleToLumi = True)
  # scaling to lumi, but scale ttbar to fiducial or total or better to sth like 1? important for overall normalisation
  #NJethists[0].Scale(1./NJethists[0].Integral(0,NJethists[0].GetNbinsX()+1))
  #NJethists[len(Samples)-1].Scale(1./NJethists[len(Samples)-1].Integral(0,NJethists[len(Samples)-1].GetNbinsX()+1))
  ratioHist = NJethists[0].Clone("ratioHist%s"%currentCategory)
  ratioHist.Divide(NJethists[len(Samples)-1])
  ratioFactor = ratioHist.GetBinContent(int(currentCategory[0])+1)
  #print "ratioHist %f %i" %(ratioFactor,ratioHist.GetBinCenter(int(currentCategory[0])+1))

  #normalisationNJethists = GetHists(NJetHistName.replace("_TwoBJets","_TruthTwoBJets"), Samples, inputSamples, files, scales, "3jincl", channel, scaleToLumi = True)
  ## overall normalisation change from MC@NLO to Alpgen
  normalisationFactor = 1 #(normalisationNJethists[len(Samples)-1].Integral(0,normalisationNJethists[len(Samples)-1].GetNbinsX()+1)) / (normalisationNJethists[0].Integral(0,normalisationNJethists[0].GetNbinsX()+1))
  #print "normalisationFactor %f" %normalisationFactor

  ## scale with ratio of jetbin and total normalisationFactor
  if (ratioFactor != 0):
    hist.Scale(1./(normalisationFactor * ratioFactor))
  
  #print "After %f" %hist.Integral()
  
  return hist


def MakeMatrixPlots(MatrixHistograms, Samples, inputSamples, files, xsecs, targetLumi, fitfiles, getChargeAsymmetryFactors = False):

  weightHist = "Events"
  #normHisto_mu = MatrixHistograms[0][4]%("mu","3jincl")
  #normHisto_el = MatrixHistograms[0][4]%("el","3jincl")
  scales = GetScales(inputSamples, xsecs, targetLumi, files, weightHist)
  #fidscales_el = GetScales(inputSamples, xsecs, targetLumi, files, normHisto_el, True, "")
  #fidscales_mu = GetScales(inputSamples, xsecs, targetLumi, files, normHisto_mu, True, "")
  recoHists = {}

  for Histogram in MatrixHistograms:
    xbins = len(Histogram[1])*len(Histogram[3])
    ybins = len(Histogram[2])*len(Histogram[3])
    outName = (Histogram[0].rsplit("/",1)[1])%("","","","")
    print outName
    th2List = []
    for sample in Samples:
      th2 = TH2F(outName+sample[0],outName+";reco;truth;", xbins, 0, xbins, ybins, 0, ybins)
      th2.Sumw2()
      th2List.append(th2)
    xbin = 0
    for channel in Histogram[3]:
      elmu = "mu"
      ybin = 3
      if channel == "Egamma":
        elmu = "el"
        ybin = 0
      for recobin in Histogram[1]:
        sumhist = 0
        recoHists[recobin] = 0
        xbin += 1
        for truthbin in Histogram[2]:
          recoHists[recobin+truthbin] = 0
          truthhists = 0
          ybin += 1
          HistName = Histogram[0]%(recobin,elmu,truthbin,elmu)
          if truthbin == "none":
            HistName = HistName.rsplit("_",1)[0].replace("truth","")
            print "none: %s" %HistName
          #fidscales = fidscales_el
          #if (channel == "Muons"):
          #  fidscales = fidscales_mu
          #hists = 0
          #if truthbin == "none": # don't wanna get dirty? change back to == "none"
          hists = GetHists(HistName, Samples, inputSamples, files, scales, "", channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors)
          #else: # not needed anymore
          #  hists = GetHists(HistName, Samples, inputSamples, files, fidscales, "", channel, scaleToLumi = True, doChargeAsymmetry = True) # fiducial normalisation!
          #print "channel: %s - recobin: %s - truthbin: %s - Bin: %10.10f" %(channel, recobin, truthbin, hists[0].GetBinContent(1))
          if ("%s" %type(sumhist)).find("TH1") < 0: sumhist = hists[0].Clone((HistName.rsplit('/',1))[1].replace(recobin,"",1).replace("_el","").replace("_mu","").replace("trafo","").replace("_truth"+truthbin,"").replace("__","_").replace("f_","h_",1)+"_sum")
          else: sumhist.Add(hists[0])
          interror = Double()
          intvalue = hists[0].IntegralAndError(0,hists[0].GetNbinsX()+1, interror)
          th2List[0].SetBinContent(xbin, ybin, intvalue)
          #print "Setting Bin Content x = %i, y = %i, value = %f, error = %f" %(xbin, ybin, intvalue, interror)
          recoHists[recobin+truthbin] = hists[0]
          if ("%s" %type(recoHists[recobin])).find("TH1") < 0:
            recoHists[recobin] = hists[0]
          else:
            recoHists[recobin].Add(hists[0])
          print "%s: %f" %(HistName,hists[0].Integral())
          
          # truth efficiency:
          TruthHistName = Histogram[4]%(elmu,truthbin)
          if truthbin != "none":
            #fidscales = fidscales_el
            #if (channel == "Muons"):
            #  fidscales = fidscales_mu
            truthhists = GetHists(TruthHistName, Samples, inputSamples, files, scales, "", channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors)
            print "Truth Efficiency Hist %s: %f" %(TruthHistName,truthhists[0].Integral())
          #end truth efficiency
          #truth histograms scaled to full phase space
          #NormaHistName = Histogram[4]%(elmu,"3jincl")
          #normahists = GetHists(NormaHistName, Samples, inputSamples, files, scales, "", channel, scaleToLumi = True, doChargeAsymmetry = True)
          #print "Norma Hist %s: %f" %(NormaHistName,normahists[0].Integral())
          #end truth histograms scaled to full phase space
          
          if (len(fitfiles) > 0): #save as templates for fit
            fitfiles[recobin+truthbin+channel][0].cd()
            savename = "%s" %(HistName.rsplit('/',1))[1].replace(recobin,"",1).replace("_el","").replace("_mu","").replace("trafo","").replace("__","_").replace("f_","h_",1).rstrip(truthbin).rstrip("truth").rstrip("_")
            recoHists[recobin+truthbin].SetName(savename)
            recoHists[recobin+truthbin].Scale(1./targetLumi) # 1pb
            recoHists[recobin+truthbin].Write()
            recoHists[recobin].SetName("%s_sum" %savename)
            recoHists[recobin].Scale(1./targetLumi) # 1pb
            recoHists[recobin].Write()
            if truthbin != "none":
              truthhists[0].SetName("%s" %(TruthHistName.rsplit('/',1))[1].replace(recobin,"",1).replace("_el","").replace("_mu","").replace("trafo","").replace("__","_").replace("f_","h_",1).rstrip(truthbin).rstrip("truth").rstrip("_"))
              truthhists[0].Scale(1./targetLumi) # 1pb
              truthhists[0].Write()
            #normahists[0].SetName("%s" %(NormaHistName.rsplit('/',1))[1].replace(recobin,"",1).replace("_el","").replace("_mu","").replace("trafo","").replace("__","_").replace("f_","h_",1).rstrip("truth").rstrip("_"))
            #normahists[0].Scale(1./targetLumi) # 1pb
            #normahists[0].Write()
          #end write templates


          
          ybin -= len(Histogram[2])
        #sumhist.Scale(1./164.57) #for fiducial
        sumhist.Scale(1./targetLumi) # 1pb
        sumhist.Write()
    if (len(fitfiles) > 0): #save matrix
      #print fitfiles
      fitfiles["2jexcl"+"3jexcl"+channel][0].cd()
      th2List[0].Write()
      c1 = TCanvas("plot", "plot", 500, 600)
      th2List[0].SetStats(0)
      th2List[0].GetXaxis().SetLabelOffset(99)
      th2List[0].GetYaxis().SetLabelOffset(99)
      th2List[0].Draw("TEXT BOX")

      # draw labels along X
      recolabels = ["e+2 jets", "e+ 3jets", "e+4 jets", "e+5 jets+","#mu+2 jets", "#mu+3 jets", "#mu+4 jets", "#mu+5 jets+"]
      truthlabels = ["e+ 3jets-", "e+4 jets", "e+5 jets+", "none", "#mu+3 jets-", "#mu+4 jets", "#mu+5 jets+", "none"]
      y = gPad.GetUymin() - 0.2*th2List[0].GetYaxis().GetBinWidth(1)
      t = TLatex()
      t.SetTextAngle(60)
      t.SetTextSize(0.03)
      t.SetTextAlign(33)
      for i in range(0,xbins):
        x = th2List[0].GetXaxis().GetBinCenter(i+1)
        t.DrawLatex(x,y,recolabels[i])
      # draw labels along y
      x = gPad.GetUxmin() - 0.1*th2List[0].GetXaxis().GetBinWidth(1)
      t.SetTextAlign(32);
      t.SetTextAngle(0);
      for i in range(0,ybins):
        y = th2List[0].GetYaxis().GetBinCenter(i+1)
        t.DrawLatex(x,y,truthlabels[i])
      
      c1.SaveAs("test.png")


  return

# def main():
#
#   LoadAtlasStyle()

def main():

  global Samples
  global inputSamples
  global RangeMin
  global RangeMax
  global default_color
  global default_latex
  global PileUp
  global fitHists
  global verbose
  global nominalMC
  global efficiencyCut
  global eventCountBefore
  global eventCountAfter
  global subtractContamination
  global contaminationPrescale
  global targetLumi
  global fullTeXTable_isFirstColumn
  global fullTeXTable #reset
  
  # parse the command line
  parser=optparse.OptionParser(usage="%prog")
  parser.add_option("-c", "--configfile", action="store",
                     dest="configfile", default="",
                     help="configfile to process")
  parser.add_option("-v", "--verbose", action="store",
                    dest="verbose", default=False,
                    help="verbose on")
  parser.add_option("--comp", action="store_true",
                    dest="comp", default=False,
                    help="compile C++ script")
  parser.add_option("-l", "--linearity", action="store_true",
                    dest="linearity", default=False,
                    help="perform linearity checks")
  parser.add_option("-n", "--nominal", action="store_true",
                    dest="nominalMC", default=False,
                    help="plot nominal MC")
  #save parsing results
  (options, args)=parser.parse_args()
  configfile=options.configfile
  verbose=options.verbose
  comp=options.comp
  doLinearity=options.linearity
  nominalMC=options.nominalMC

  #print configuration
  print "-----------------------------"
  print "|    Welcome to PlotAlot    |"
  print "|           by              |"
  print "|      Clemens Lange        |"
  print "|  <clange@physik.uzh.ch>   |"
  print "-----------------------------"
  print "\n*** Using ConfigFile: %s ***" %(configfile)

  # check for jobOptions file
  if not os.access(configfile,os.R_OK):
    print "FATAL: configfile not accessible!"
    sys.exit()

  # parse jobOptions file
  jobOptionsFile=open(configfile, 'r')
  command=""
  for i in [o for o in jobOptionsFile.readlines()]: #parse
          if "#End" in i : break
          command+=i
  jobOptionsFile.close()
  exec command

  if not "samples" in dir():
    print "Please define Samples!"
    sys.exit()
  else:
    Samples = samples
  print "Using the following Samples:"
  for i in range(len(Samples)):
    sys.stdout.write("  o ")
    print Samples[i]
    
  if not "inputsamples" in dir():
    print "Please define inputsamples!"
    sys.exit()
  else:
    inputSamples = inputsamples
  print "Samples consist of the following input Samples:"
  for i in range(len(inputSamples)):
    sys.stdout.write("  o ")
    print inputSamples[i][0]
    for j in range(len(inputSamples[i][1])):
      sys.stdout.write("    x ")
      print inputSamples[i][1][j]
  
  if not "categories" in dir():
    categories = ["4jincl"]
  sys.stdout.write("Jetbins: ")
  print categories

  if "TargetLumi" in dir():
    targetLumi = TargetLumi
  print "targetLumi: %3.1f" % targetLumi

  if not "getChargeAsymmetryFactors" in dir():
    getChargeAsymmetryFactors = True
  print "getChargeAsymmetryFactors %s" %getChargeAsymmetryFactors

  if not "Histograms" in dir():
    Histograms = []
  print "Histograms:"
  print Histograms

  if not "AllMCHistograms" in dir():
    AllMCHistograms = []
  print "AllMCHistograms:"
  print AllMCHistograms

  if not "IntrinsicHistograms" in dir():
    IntrinsicHistograms = []
  print "IntrinsicHistograms:"
  print IntrinsicHistograms

  if not "ComparisonHistograms" in dir():
    ComparisonHistograms = []
  print "ComparisonHistograms:"
  print ComparisonHistograms
  
  if not "Cutflow" in dir():
    Cutflow = []
  print "Cutflow:"
  print Cutflow
  
  if not "cuts" in dir():
    cuts = [""]
  print "cuts:"
  print cuts
  
  if not "ShapeHistograms" in dir():
    ShapeHistograms = []
  print "ShapeHistograms:"
  print ShapeHistograms

  if not "AllJetHistograms" in dir():
    AllJetHistograms = []
  print "AllJetHistograms:"
  print AllJetHistograms

  if not "FitInput" in dir():
    FitInput = []
  print "FitInput:"
  print FitInput
  
  if not "MatrixHistograms" in dir():
    MatrixHistograms = []
  print "MatrixHistograms:"
  print MatrixHistograms

  if not "fiducialBins" in dir():
    fiducialBins = []
  print "fiducialBins:"
  print fiducialBins

  if not "fiducialScale" in dir():
    fiducialScale = []
  print "fiducialScale:"
  print fiducialScale

  if not "systematic" in dir():
    Systematic = "nominal"
  else:
    Systematic = systematic.lstrip("_")
  print "Systematic: %s" %Systematic
  
  if not "systOutName" in dir():
    systOutName = ""
  else:
    print "systOutName: %s" %systOutName
  
  if not "systematicVariations" in dir():
    systematicVariations = []
  else:
    print systematicVariations

  if not "plotTypes" in dir():
    plotTypes = []
  print "plotTypes:"
  print plotTypes

  if not "ratioLabels" in dir():
    ratioLabels = ["W", "BJET"]
  print "ratioLabels:"
  print ratioLabels
  
  if not "WHFsystematic" in dir():
    WHFsystematic = [0, 0, 0]
  print "WHFsystematic:"
  print WHFsystematic
  
  if not "WScaleSystematic" in dir():
    WScaleSystematic = 0
  print "WScaleSystematic: %i" %WScaleSystematic
  
  if not "additionalScales" in dir():
    additionalScales = []
  else:
    print "additionalScales:"
    print additionalScales

  if not "inputDir" in dir():
    inputDir = "/afs/ifh.de/group/atlas/scratch/topdata/ColourFlowOutput"
  inputDir=os.path.expandvars(inputDir)
  print "Input Directory: %s" % inputDir

  if not "outputDir" in dir():
    outputDir = "plots"
  outputDir=os.path.expandvars(outputDir)
  print "Output Directory: %s" % outputDir
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
  for catName in categories:
    if not os.path.exists(outputDir+"/"+catName):
      os.makedirs(outputDir+"/"+catName)
    if not os.path.exists(outputDir+"/"+catName+'/ratios'):
      os.makedirs(outputDir+"/"+catName+'/ratios')  
  
  if not "templateDir" in dir():
    templateDir = "../templates"
  templateDir=os.path.expandvars(templateDir)
  print "Template Directory: %s" % templateDir
  if not os.path.exists(templateDir):
    os.makedirs(templateDir)

  if not "RootStyleFile" in dir():
    RootStyleFile = "RootStyle.py"
  print "Using RootStyleFile: %s" % RootStyleFile

  if not os.access(RootStyleFile,os.R_OK):
    print "FATAL: RootStyleFile not accessible!"
    sys.exit()

  # parse RootStyle file
  rootStyleFile=open(RootStyleFile, 'r')
  command=""
  for i in [o for o in rootStyleFile.readlines()]: #parse
          if "#End" in i : break
          command+=i
  rootStyleFile.close()
  exec command

  if not "default_Latex" in dir():
    print "Please define default_Latex in %s" %RootStyleFile
    sys.exit()
  else:
    default_latex = default_Latex

  if not "default_Color" in dir():
    print "Please define default_Color in %s" %RootStyleFile
    sys.exit()
  else:
    default_color = default_Color

  if not "QCDFractions" in dir():
    print "Please define QCDFractions"
    sys.exit()

  if not "XSectionDic" in dir():
    XSectionDic = "xsections.py"
  print "Using XSectionDic: %s" % XSectionDic

  if not os.access(XSectionDic,os.R_OK):
    print "FATAL: XSectionDic not accessible!"
    sys.exit()

  # parse RootStyle file
  xSectionDic=open(XSectionDic, 'r')
  command=""
  for i in [o for o in xSectionDic.readlines()]: #parse
          if "#End" in i : break
          command+=i
  xSectionDic.close()
  exec command
  
  comp = False
  if comp:
    print "Compiling root macros"
    ROOT.gSystem.CompileMacro("${SFRAME_DIR}/../Common/WJetsCorrectionsTools/WjetsCorrectionsPackage/Root/Wasymmetry_rel17.cxx")
    ROOT.gSystem.CompileMacro("${SFRAME_DIR}/../Common/WJetsCorrectionsTools/WjetsCorrectionsPackage/Root/HFsys_factor_ttbar_emu.cxx")

  files = OpenFiles(inputSamples, inputDir+"/"+Systematic, inputPrefix, inputPostfix)
  scales = GetScales(inputSamples, xsecs, targetLumi, files, weightHist)

  for variation in systematicVariations:
    print systematicVariations
    varfiles[variation] = OpenFiles(inputSamples, inputDir+"/"+variation.lstrip("_"), inputPrefix, inputPostfix)
  if len(systematicVariations) > 0: sys.exit()

  #if (getChargeAsymmetryFactors):
  #  ChargeAsymmetryScaleFactors = GetChargeAsymmetryFactors(Samples, inputSamples, files, scales, categories, channel, QCDFractions)
  #  SetChargeAsymmetryScaleFactors( ChargeAsymmetryScaleFactors )
#loop over systematics here
  # open fit template files for writing
  fitfiles = {}
  if len(FitInput) > 0:
    systOut = Systematic
    if (systOutName != ""): systOut = systOutName
    if not os.path.exists("%s/default_%s" %(templateDir, systOut)):
      os.makedirs("%s/default_%s" %(templateDir, systOut))
    for bin in categories:
      fitfiles[bin] = []
      for i in range(len(Samples)):
        if (Samples[i][0] != "ALPGEN"):
          fitfiles[bin] += [TFile.Open("%s/default_%s/%s_%s_%s.root" %(templateDir, systOut, default_Fitter[Samples[i][0]], default_Fitter[bin], default_Fitter[channel]), "RECREATE")]

  runScales = False
  channel = ""
  for h in range(len(categories)):
    currentCategory = categories[h]
    for i in range(len(Histograms)):
      HistNameArray = Histograms[i]
      for j in range(len(HistNameArray)):
        hists = 0
        HistName = HistNameArray[j][0]
        hists = GetHists(HistName, Samples, inputSamples, files, scales, currentCategory, channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors, fiducial = fiducialBins, fidScale = fiducialScale, addScales = additionalScales, WHFsyst = WHFsystematic, WScaleSyst = WScaleSystematic)
        # hists = ScaleQCD(hists, HistName, Samples, QCDFractions, currentCategory, channel)
        for k in range(len(hists)):
          hists[k] = OverflowToLast(hists[k])
          hists[k].SetTitle(HistNameArray[j][1])
          hists[k].GetXaxis().SetTitle(HistNameArray[j][2])
          hists[k].GetYaxis().SetTitle(HistNameArray[j][3])
        hists = StyleHists(hists, Samples, default_color, default_MarkerStyle)
        legend = GetLegend(hists, Samples, default_Latex, "datamc")
        stackedhists = GetStack(hists, Samples)
        dataindex = 0
        for k in range(len(hists)):
          if (hists[k].GetName().startswith("DATA") or hists[k].GetName().startswith("PSEUDO")):
            dataindex = k
        datahist = hists[dataindex]
        
        histOutName = HistNameArray[j][0]
        # [histOutName, cutName] = histOutName.rsplit("_",1)
        cutName = ""

        if "dataMC" in plotTypes:
          MakeDataMCPlot(datahist, stackedhists, legend, targetLumi, histOutName, cutName, outputDir, currentCategory, default_extension)
        if "dataMCratio" in plotTypes:
          MakeDataMCRatioPlot(hists, stackedhists, datahist, outputDir, histOutName, currentCategory, default_extension, default_Latex, Samples, targetLumi)
        if (i == 0 and j == 2):
          if "yieldtable" in plotTypes:
            WriteTeXFile(outputDir, cutName, currentCategory, channel, Samples, default_Latex, hists)

  #allMC
  integralList = {}
  for h in range(len(categories)):
    currentCategory = categories[h]
    for i in range(len(AllMCHistograms)):
      HistNameArray = AllMCHistograms[i]
      for j in range(len(HistNameArray)):
        hists = 0
        HistName = HistNameArray[j][0]
        hists = GetHists(HistName, Samples, inputSamples, files, scales, currentCategory, channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors, fiducial = fiducialBins, fidScale = fiducialScale, addScales = additionalScales)
        hists = ScaleQCD(hists, HistName, Samples, QCDFractions, currentCategory, channel)
        for k in range(len(hists)):
          hists[k] = OverflowToLast(hists[k])
          hists[k].SetTitle(HistNameArray[j][1])
          hists[k].GetXaxis().SetTitle(HistNameArray[j][2])
          hists[k].GetYaxis().SetTitle(HistNameArray[j][3])
        hists = StyleHists(hists, Samples, default_color, default_MarkerStyle)
        legend = GetLegend(hists, Samples, default_Latex)
        splithists = []
        splitSamples = []
        stackedhists = []
        topSampleCounter = 0
        for v in range(len(Samples)):
          if Samples[v][0] in topSamples:
            splithists.append([hists[v]])
            splitSamples.append([Samples[v]])
            topSampleCounter += 1
        for v in range(len(Samples)):
          if Samples[v][0] not in topSamples:
            for w in range(0,topSampleCounter):
              splithists[w].append(hists[v])
              splitSamples[w].append(Samples[v])
        
        dataindex = 0
        for v in range(len(splithists)):
          if v == 0:
            stackedhists.append(GetStack(splithists[v], splitSamples[v]))
            for k in range(len(splithists[v])):
              if (splithists[v][k].GetName().startswith("DATA") or splithists[v][k].GetName().startswith("PSEUDO")):
                dataindex = k
            datahist = splithists[v][dataindex]
          else:
            stackedhists.append(GetSum(splithists[v], splitSamples[v]))
        histOutName = HistNameArray[j][0] #HistNameArray[j][0].rsplit("/",1)[1]
        # [histOutName, cutName] = histOutName.rsplit("_",1)
        cutName = ""

        if "dataMC" in plotTypes:
          MakeDataAllMCPlot(datahist, stackedhists, legend, targetLumi, histOutName, cutName, outputDir, currentCategory, default_extension)
        if "dataMCratio" in plotTypes:
          MakeDataAllMCRatioPlot(hists, stackedhists, datahist, outputDir, HistNameArray[j][0].rsplit("/",1)[1], currentCategory, default_extension, default_Latex, Samples, targetLumi)



    # intrinsic histograms
    for i in range(len(IntrinsicHistograms)):
      HistNameArray = IntrinsicHistograms[i]
      allhists = []
      events = []
      for j in range(len(HistNameArray[0])):
        HistName = HistNameArray[0][j]
        print "HistName:", HistName
        hists = GetHists(HistName, Samples, inputSamples, files, scales, currentCategory, channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors, addScales = additionalScales)
        for k in range(len(hists)):
          hists[k] = OverflowToLast(hists[k])
          print "Events: %f" %hists[k].Integral()
          events += [hists[k].Integral()]
        allhists += hists
        histOutName = HistNameArray[j][0]
        # [histOutName, cutName] = histOutName.rsplit("_",1)
        cutName = ""
      #MakeRatioPlot(allhists, ["RECO", "TRUTH"], default_color, default_Latex, titleprefix, titlepostfix, histname, False)
      #MakeRatioPlot(allhists, ["TRUTH", "RECO"], default_Color, default_Latex, "", "", histOutName, outputDir, cutName, currentCategory, default_extension, True)
      for l in range(1,len(events)):
        print "acceptance: %f" %(events[l]/events[0])
      MakeRatioPlot(allhists, ratioLabels, default_Color, default_Latex, "", "", histOutName, outputDir, cutName, currentCategory, default_extension, False)
      MakeRatioPlot(allhists, ratioLabels, default_Color, default_Latex, "", "_unity", histOutName, outputDir, cutName, currentCategory, default_extension, True)


    # comparison histograms
    if len(ComparisonHistograms) > 0:
      for thisCut in cuts:
        for i in range(len(ComparisonHistograms[0])):
          HistNameArray = ComparisonHistograms[0][i]
          hists = 0
          HistName = HistNameArray[0]+thisCut
          currentChannel = "el"
          if channel == "Muons": currentChannel = "mu"
          fixedCut = thisCut
          if fixedCut.find("Truth") < 0: fixedCut = fixedCut.replace("_","_Truth")
          #scales = GetScales(inputSamples, xsecs, targetLumi, files, weightHist, doIntegral = True, ttbarHist="Analysis/offline/h_jet_n_"+currentChannel+fixedCut+"_"+currentCategory) # comment out for full phase space
          hists = GetHists(HistName, Samples, inputSamples, files, scales, currentCategory, channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors, addScales = additionalScales)
          for k in range(len(hists)):
            hists[k] = OverflowToLast(hists[k])
            if (HistNameArray[1] != ""):
              hists[k].SetTitle(HistNameArray[1])
            if (HistNameArray[2] != ""):
              hists[k].GetXaxis().SetTitle(HistNameArray[2])
            if (HistNameArray[3] != ""):
              hists[k].GetYaxis().SetTitle(HistNameArray[3])
            if (HistName == "dijet_m"):
              print hists[k].Integral(0,hists[k].GetNbinsX()+1)
              integralList[currentCategory] = hists[k].Integral(0,hists[k].GetNbinsX()+1)
          hists = StyleHists(hists, Samples, default_color, default_MarkerStyle)
          legend = GetLegend(hists, Samples, default_Latex) #, "ratio"
          histOutName = HistNameArray[0] #.rsplit("/",1)[1]
          #[histOutName, cutName] = histOutName.rsplit("_",1)
          cutName = thisCut.strip("_")
          MakeSimplePlot(hists, Samples, default_Color, default_Latex, "", "", histOutName, outputDir, cutName, currentCategory, default_extension, TargetLumi, False) #[0.001,1.999]
          #MakeRatioPlot(hists, ratioLabels, default_Color, default_Latex, "", "", histOutName, outputDir, cutName, currentCategory, default_extension, True, [0.001,1.999])


    # cutflow histograms
    if len(Cutflow) > 0:
      for i in range(len(Cutflow[0])):
        HistNameArray = Cutflow[0][i]
        hists = 0
        HistName = HistNameArray[0]
        hists = GetHists(HistName, Samples, inputSamples, files, scales, currentCategory, channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors, addScales = additionalScales)
        print "-"*50
        print currentCategory
        sys.stdout.write('{:20s}'.format('cut'))
        for sample in Samples:
          sys.stdout.write('{:25s}{:10s}{:10s}'.format(sample[0], "rel. eff", "abs. eff"))
        sys.stdout.write('\n')
        loopRange = len(cuts)+1
        if (len(cuts) == 0):
          loopRange = hists[0].GetNbinsX()+1
        for bin in range(1, loopRange):
          if (len(cuts) == 0):
            sys.stdout.write('cut {:2d}{:14s}'.format(bin, ''))
          else:
            sys.stdout.write('{:20s}'.format(cuts[bin-1]))
          for k in range(len(hists)):
            sys.stdout.write('{:14.1f}{:11s}'.format(hists[k].GetBinContent(bin),''))
            if (bin > 1):
              relEff = 0
              absEff = 0
              if (hists[k].GetBinContent(bin) != 0):
                relEff = hists[k].GetBinContent(bin)/hists[k].GetBinContent(bin-1)
              if (hists[k].GetBinContent(1) != 0):
                absEff = hists[k].GetBinContent(bin)/hists[k].GetBinContent(1)
              sys.stdout.write('{:7.2f}{:3s}{:7.2f}{:3s}'.format(relEff*100,'',absEff*100,''))
            else:
              sys.stdout.write('{:20s}'.format(''))
          sys.stdout.write('\n')
            
        # MakeSimplePlot(hists, ratioLabels, default_Color, default_Latex, "", "", histOutName, outputDir, cutName, currentCategory, default_extension, TargetLumi, False) #[0.001,1.999]



          
    # shape comparison histograms
    if len(ShapeHistograms) > 0:
      for s in range(len(samples)-1):
        firstSamples = [Samples[s]]
        for t in range(s+1, len(samples)):
          thisSamples = firstSamples+[Samples[t]]
          for h in range(len(categories)):
            currentCategory = categories[h]
            for i in range(len(ShapeHistograms)):
              HistNameArray = ShapeHistograms[i]
              for j in range(len(HistNameArray)):
                hists = 0
                HistName = HistNameArray[j][0]
                print "HistName"
                if runScales == True: #switch back to full phasespace normalisation
                  runScales = False
                  scales = GetScales(inputSamples, xsecs, targetLumi, files, weightHist)
                hists = GetHists(HistName, thisSamples, inputSamples, files, scales, currentCategory, channel, scaleToLumi = True, doChargeAsymmetry = False, addScales = additionalScales)
                #hists = ScaleQCD(hists, HistName, Samples, QCDFractions, currentCategory, channel)
                for k in range(len(hists)):
                  if (len(HistNameArray) > 4):
                    hists[k].Rebin(HistNameArray[4])
                  hists[k] = OverflowToLast(hists[k])
                  hists[k].SetTitle(HistNameArray[j][1])
                  hists[k].GetXaxis().SetTitle(HistNameArray[j][2])
                  hists[k].GetYaxis().SetTitle(HistNameArray[j][3])
                hists = StyleHists(hists, Samples, default_color, default_MarkerStyle)
                legend = GetLegend(hists, Samples, default_Latex)
                histOutName = HistNameArray[j][0]
                # [histOutName, cutName] = histOutName.rsplit("_",1)
                cutName = ""
                histOutName += thisSamples[0][0] + "_" + thisSamples[1][0]
                MakeSimplePlot(hists, ratioLabels, default_Color, default_Latex, "", "", histOutName, outputDir, cutName, currentCategory, default_extension, True, [0.6,1.4])


  for i in range(len(AllJetHistograms)):
    HistNameArray = AllJetHistograms[i]
    for j in range(len(HistNameArray)):
      allhists = 0
      for h in range(len(categories)):
        currentCategory = categories[h]
        hists = 0
        HistName = HistNameArray[j][0]
        if runScales == True: #switch back to full phasespace normalisation
          runScales = False
          scales = GetScales(inputSamples, xsecs, targetLumi, files, weightHist)
        hists = GetHists(HistName, Samples, inputSamples, files, scales, currentCategory, channel, scaleToLumi = True, doChargeAsymmetry = getChargeAsymmetryFactors, fiducial = fiducialBins, fidScale = fiducialScale, addScales = additionalScales)
        hists = ScaleQCD(hists, HistName, Samples, QCDFractions, currentCategory, channel)
        print hists
        #if len(FitInput) > 0:
        #  hists = SmoothHistograms(hists, Samples, 3)
      
        if (allhists==0):
          allhists = hists
        else:
          for k in range(len(hists)):
            allhists[k].Add(hists[k])
      for k in range(len(allhists)):
        print allhists[k].GetName()
        allhists[k] = OverflowToLast(allhists[k])
        allhists[k].SetTitle(HistNameArray[j][1])
        allhists[k].GetXaxis().SetTitle(HistNameArray[j][2])
        allhists[k].GetYaxis().SetTitle(HistNameArray[j][3])
        #if (Samples[k][0].startswith("TOP")):
          #allhists[k].Scale(1./164.57)
          #allhists[k].Scale(targetLumi)

      allhists = StyleHists(allhists, Samples, default_color, default_MarkerStyle)
      legend = GetLegend(allhists, Samples, default_Latex)
      stackedhists = GetStack(allhists, Samples)
      dataindex = 0
      for k in range(len(allhists)):
        if allhists[k].GetName().split("-")[0].startswith("DATA"):
          dataindex = k
      datahist = allhists[dataindex]
      histOutName = HistNameArray[j][0]
      # [histOutName, cutName] = histOutName.rsplit("_",1)
      cutName = ""
      print histOutName
      if "dataMC" in plotTypes:
        MakeDataMCPlot(datahist, stackedhists, legend, targetLumi, histOutName, cutName, outputDir, "all" , default_extension)
      if "dataMCratio" in plotTypes:
        MakeDataMCRatioPlot(allhists, stackedhists, datahist, outputDir, HistNameArray[j][0].rsplit("/",1)[1], "all", default_extension, default_Latex, Samples, targetLumi)


  if (len(fitfiles) > 0):
    for bin in categories:
      for fitfile in fitfiles[bin]:
        fitfile.Close()


  if len(MatrixHistograms) > 0:
    # open fit template files for writing
    fitfiles = {}
    systOut = Systematic
    if (systOutName != ""): systOut = systOutName
    if not os.path.exists("%s/default_%s" %(templateDir, systOut)):
      os.makedirs("%s/default_%s" %(templateDir, systOut))
    for recobin in MatrixHistograms[0][1]:
      for truthbin in MatrixHistograms[0][2]:
        for chan in MatrixHistograms[0][3]:
          fitfiles[recobin+truthbin+chan] = []
          for i in range(len(Samples)):
            if (Samples[i][0] != "ALPGEN"):
              fitfiles[recobin+truthbin+chan] += [TFile.Open("%s/default_%s/%s_truth%s_%s_%s.root" %(templateDir, systOut, default_Fitter[Samples[i][0]], default_Fitter[truthbin], default_Fitter[recobin], default_Fitter[chan]), "RECREATE")]
    #some manipulation to have only the top samples for those plots
    MatrixSamples = []
    for sample in Samples:
      if (sample[0].startswith("TOP")): MatrixSamples += [sample]
    MatrixInputSamples = []
    for sample in MatrixSamples:
      for subsample in sample[1]:
        for inputs in inputSamples:
          if inputs[0] == subsample:
            MatrixInputSamples += [inputs]
    MakeMatrixPlots(MatrixHistograms, MatrixSamples, MatrixInputSamples, files, xsecs, targetLumi, fitfiles)

    for index,filelist in fitfiles.items():
      for file in filelist:
        file.Close()

  print integralList
  
  return

if __name__ == "__main__":
  main()