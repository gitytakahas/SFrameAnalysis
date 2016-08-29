import os
# import array
from ROOT import *
import random
import sys
import datetime
# from math import pow,exp,sqrt
topSamples = ["MCATNLO", "ALPGEN", "POWHEGJIMMY", "POWHEGPYTHIA", "ACERMC", "ALPGENPYTHIA"] #already defined in RootStyle.py!

ChargeAsymmetryScaleFactors = []

def SetChargeAsymmetryScaleFactors( SFs ):
  global ChargeAsymmetryScaleFactors
  ChargeAsymmetryScaleFactors = SFs
  return

def LoadAtlasStyle(file):
 # ATLAS Style
  # importing ATLASstyle for ROOT (adjust path to current version)
  ROOT.gROOT.LoadMacro(file)
  atlasStyle = SetAtlasStyle()
  # importing ATLASstyle for ROOT (adjust path to current version)
  ROOT.gROOT.SetStyle("ATLAS") # setting ATLAS style
  ROOT.gROOT.ForceStyle()
  ROOT.gROOT.SetBatch(kTRUE); # switch off any graphical output
  gStyle.SetPalette(1)
  gStyle.SetOptStat(0)
  return


def OpenFiles(inputSamples, inputDir, inputPrefix="", inputPostfix=""):
  print "In OpenFiles"
  files = {}
  for sample in inputSamples:
    for subsample in sample[1]:
      for substring in sample[2]:
        filename = inputDir+"/"+inputPrefix+subsample+substring+inputPostfix
        if os.path.exists(filename):
          file = TFile.Open(filename)
          print "Opening: %s" % (filename)
          files[subsample+substring] = file
        else:
          print "File not found: %s" % (filename)
          sys.exit()
  return files


def GetScales(inputSamples, xsecs, targetLumi, files, weightHist, doIntegral = False, ttbarHist = ""):

  scale = {}
  ttbarSamples = ["105200", "105860", "105861", "105890", "105891", "105892", "105894", "105895", "105896", "117887", "117888", "117889", "117897", "117898", "117899"]

  for sample in inputSamples:
    for subsample in sample[1]:
      for substring in sample[2]:
        sampleId=subsample+substring
        if (sampleId.find("JetHT74X") >= 0):
          continue
        #print "%s - %3.2f - %3.2f" % (sampleId, xsecs[int(sampleId)][0], xsecs[int(sampleId)][1])
        h1fromfile = 0
        h1fromfile = files[sampleId].Get(weightHist)
        if ("%s" %type(h1fromfile)).find("TH1") < 0:
          print "hist %s not found in %s!" %(weightHist, sampleId)
          sys.exit()
        if ((doIntegral) and ((subsample in ttbarSamples) or (weightHist != "Events"))):
          if (h1fromfile.Integral(0, h1fromfile.GetNbinsX()+1) == 0):
            print "Warning: %s has 0 events for normalisation!" %sampleId
            scale[sampleId] = 0
            sys.exit()
          else:
            print "sampleId: %s using integral %f from %s" %(sampleId, h1fromfile.Integral(0, h1fromfile.GetNbinsX()+1), weightHist)
            scale[sampleId] = xsecs[int(subsample)][0] * xsecs[int(subsample)][1] / ( h1fromfile.Integral(0, h1fromfile.GetNbinsX()+1) ) * targetLumi
        else:
          scale[sampleId] = xsecs[sampleId] / h1fromfile.GetBinContent(1) * targetLumi
          print "Sample: %s - xsec: %f - totalEvents: %f - lumi: %f - scale: %f" %(sampleId, xsecs[sampleId], h1fromfile.GetBinContent(1), targetLumi, scale[sampleId])
  
  return scale


def FixNegativeMMBins(h1subsample):

  origevents = h1subsample.Integral(0, h1subsample.GetNbinsX()+1)
  negativeBin = False
  for bin in range(0,h1subsample.GetNbinsX()+1):
    if (h1subsample.GetBinContent(bin) < 0):
      negativeBin = True
      h1subsample.SetBinContent(bin, 0)
  if (negativeBin):
    newevents = h1subsample.Integral(0, h1subsample.GetNbinsX()+1)
    print "Correcting for negative bins in MM sample: %f to %f" %(origevents, newevents)
    h1subsample.Scale(origevents / newevents)
  return h1subsample


def GetFiducialHists(HistName, Samples, inputSamples, files, scales, jetbin, channel, scaleToLumi = True, doChargeAsymmetry = True, fiducial = [], fidScale = [], WScale = {}, WScaleSyst = 0, WScaleUncert = {}):
  
  tagged = False
  if (HistName.find("BJet") >=0):
    tagged = True
  myHistName = HistName.replace("njetfid/f_", "njet/")
  dummyhist = (files[inputSamples[0][1][0]+inputSamples[0][2][0]].Get(myHistName)).Clone("dummyhist") # simply take the first sample (usually ttbar)
  dummyhist.Reset()
  
  h1subsamples = {}
  for x in range(len(inputSamples)+len(fiducial)-1): # loop over input samples + fiducial ones
    k = x-len(fiducial)+1
    if (x < len(fiducial)):
      k = 0
    #print "k: %i, x: %i"%(k,x)
    #print "looking at %i %s" %(k,inputSamples[k][0])
    h1subsample = 0
    for l in range(len(inputSamples[k][1])): #loop over files
      #print "Working on '%s'" %inputSamples[k][1][l]
      h1extension = 0
      for m in range(len(inputSamples[k][2])): #loop over hist extensions
        sampleId = inputSamples[k][1][l]+inputSamples[k][2][m]
        #print "Working on extension %s" % (inputSamples[k][2][m])
        h1fromfile = 0
        if (x < len(fiducial)):
          fidHistName = (HistName+fiducial[x]).replace("offline/h_","fiducial/f_")
          fidHistName = fidHistName.replace("f_Jet_N_1jincl_nj","f_Jet_N_1jinclnj")
          fidHistName = fidHistName.replace("_el_BJet_2jexcl","2jexcl_el_BJet")
          fidHistName = fidHistName.replace("_el_BJet_3jexcl","3jexcl_el_BJet")
          fidHistName = fidHistName.replace("_el_BJet_4jexcl","4jexcl_el_BJet")
          fidHistName = fidHistName.replace("_el_BJet_5jincl","5jincl_el_BJet")
          fidHistName = fidHistName.replace("_mu_BJet_2jexcl","2jexcl_mu_BJet")
          fidHistName = fidHistName.replace("_mu_BJet_3jexcl","3jexcl_mu_BJet")
          fidHistName = fidHistName.replace("_mu_BJet_4jexcl","4jexcl_mu_BJet")
          fidHistName = fidHistName.replace("_mu_BJet_5jincl","5jincl_mu_BJet")
          fidHistName = fidHistName.replace("_el_TwoBJets_2jexcl","2jexcl_el_TwoBJets")
          fidHistName = fidHistName.replace("_el_TwoBJets_3jexcl","3jexcl_el_TwoBJets")
          fidHistName = fidHistName.replace("_el_TwoBJets_4jexcl","4jexcl_el_TwoBJets")
          fidHistName = fidHistName.replace("_el_TwoBJets_5jincl","5jincl_el_TwoBJets")
          fidHistName = fidHistName.replace("_mu_TwoBJets_2jexcl","2jexcl_mu_TwoBJets")
          fidHistName = fidHistName.replace("_mu_TwoBJets_3jexcl","3jexcl_mu_TwoBJets")
          fidHistName = fidHistName.replace("_mu_TwoBJets_4jexcl","4jexcl_mu_TwoBJets")
          fidHistName = fidHistName.replace("_mu_TwoBJets_5jincl","5jincl_mu_TwoBJets")

          print "Getting %s"%(fidHistName)
          h1fromfile = files[sampleId].Get(fidHistName)
          print h1fromfile
          print h1fromfile.Integral()
        else:
          #print "Getting %s"%myHistName
          h1fromfile = files[sampleId].Get(myHistName)
        #h1fromfile.SetDirectory(0)
        h1 = 0
        if ("%s" %type(h1fromfile)).find("TH1") < 0:
          h1 = dummyhist.Clone("%s-%5i"% ( inputSamples[k][1], random.randint(0,10000) ))
          if (inputSamples[k][0].find("DATA") >= 0) or (inputSamples[k][0].find("QCD") >= 0):
            print "Hist: %s not found for %s" % (HistName,sampleId)
        else:
          #print "*****  %s - %5.1f" % ( HistName, h1fromfile.GetEntries() )
          if (x < len(fiducial)):
            h1 = h1fromfile.Clone("%s%s-%05i"% ( inputSamples[k][0], fiducial[x], random.randint(0,10000)))
          else:
            h1 = h1fromfile.Clone("%s-%05i"% ( inputSamples[k][0], random.randint(0,10000)))
        if (inputSamples[k][0].find("DATA") < 0) and (inputSamples[k][0].find("QCD") < 0) and scaleToLumi:
          if (h1.Integral(0,h1.GetNbinsX()+1) > 0):
            if (inputSamples[k][0][0]=="W" and inputSamples[k][0].find("JETS") >= 0):
              # BEGIN: Top group charge asymmetry values
                if (doChargeAsymmetry):
                  if (HistName.find("Jet_N_1jincl") < 0):
                    wScaleUncertainty = 1
                    if (WScaleSyst > 0):
                      wScaleUncertainty = WScaleUncert[jetbin+channel][0]
                    elif (WScaleSyst < 0):
                      wScaleUncertainty = WScaleUncert[jetbin+channel][1]
                    h1.Scale(scales[sampleId]*WScale[jetbin+channel]*wScaleUncertainty)
                  else:
                    jbinDict = {}
                    jbinDict[2] = "1jexcl"; jbinDict[3] = "2jexcl"; jbinDict[4] = "3jexcl";
                    jbinDict[5] = "4jexcl"; jbinDict[6] = "5jincl"
                    for jbin in range(2,7):
                      content = h1.GetBinContent(jbin)
                      wScaleUncertainty = 1
                      if (WScaleSyst > 0):
                        wScaleUncertainty = WScaleUncert[jbinDict[jbin]+channel][0]
                      elif (WScaleSyst < 0):
                        wScaleUncertainty = WScaleUncert[jbinDict[jbin]+channel][1]
                      content *= scales[sampleId]*WScale[jbinDict[jbin]+channel]*wScaleUncertainty
                      h1.SetBinContent(jbin, content)
                else:
                  h1.Scale(scales[sampleId]) # no charge asymm.
                # W scaling
            else:
              h1.Scale(scales[sampleId])
        if (("%s" %type(h1extension)).find("TH1") < 0):
          h1extension = h1
        else:
          h1extension.Add(h1)
          #print "h1extension: %s - %f - %s" %( inputSamples[i][0], h1extension.Integral(0, h1extension.GetNbinsX()+1), inputSamples[k][3][m] )
      if (("%s" %type(h1subsample)).find("TH1") < 0):
        h1subsample = h1extension
      else:
        h1subsample.Add(h1extension)
    #print "h1subsample: %s - %f" %( inputSamples[i][0], h1subsample.Integral() )
    if (x < len(fiducial)):
      #print "saving as %s"%(inputSamples[k][0]+fiducial[x])
      if (len(fidScale) > x):
        h1subsample.Scale(fidScale[x])
      h1subsamples[inputSamples[k][0]+fiducial[x]] = h1subsample
    else:
      #print "saving as %s"%(inputSamples[k][0])
      if (inputSamples[k][0].find("QCDMM") >= 0):
        h1subsample = FixNegativeMMBins(h1subsample)
      h1subsamples[inputSamples[k][0]] = h1subsample
  print h1subsamples
  return h1subsamples



def GetHists(HistName, Samples, inputSamples, files, scales, jetbin, channel, scaleToLumi = True, doChargeAsymmetry = True, fiducial = [], fidScale = [], addScales = [], WHFsyst = [0, 0, 0], WScaleSyst = 0):
  
  HistName = jetbin + "/" + HistName
  tagged = False
  if (HistName.find("BJet") >=0):
    tagged = True
  myHistName = HistName.replace("njetfid/f_", "njet/")
  print "Getting histograms: %s" %myHistName
  allhists = []
  dummyhist = (files[inputSamples[0][1][0]+inputSamples[0][2][0]].Get(myHistName)).Clone("dummyhist") # simply take the first sample (usually ttbar)
  dummyhist.Reset()
  
  h1subsamples = {}

  if (len(fiducial) == 0):
    for k in range(len(inputSamples)): # loop over input samples
      skippedIntegral = 0 # for W+jets low parton samples
      #print "looking at %i %s" %(k,inputSamples[k][0])
      h1subsample = 0
      for l in range(len(inputSamples[k][1])): #loop over files
        #print "Working on '%s'" %inputSamples[k][1][l]
        h1extension = 0
        for m in range(len(inputSamples[k][2])): #loop over hist extensions
          sampleId = inputSamples[k][1][l]+inputSamples[k][2][m]
          #print "Working on extension %s" % (inputSamples[k][2][m])
          h1fromfile = files[sampleId].Get(HistName)
          #h1fromfile.SetDirectory(0)
          h1 = 0
          if ("%s" %type(h1fromfile)).find("TH1") < 0:
            h1 = dummyhist.Clone("%s-%05i"% ( inputSamples[k][1], random.randint(0,10000) ))
            if (inputSamples[k][0].find("DATA") >= 0):
              print "Hist: %s not found for %s" % (HistName,sampleId)
          else:
            #print "*****  %s - %5.1f" % ( HistName, h1fromfile.GetEntries() )
            h1 = h1fromfile.Clone("%s-%05i"% ( inputSamples[k][0], random.randint(0,10000)))

          if (inputSamples[k][0].find("DATA") < 0) and scaleToLumi:
            if (h1.Integral(0,h1.GetNbinsX()+1) > 0):
              #print "Scaling %s with integral %f using scale %f" %(sampleId, h1.Integral(), scales[sampleId])
              h1.Scale(scales[sampleId])
          if (("%s" %type(h1extension)).find("TH1") < 0):
            h1extension = h1
          else:
            h1extension.Add(h1)
            #print "h1extension: %s - %f - %s" %( inputSamples[i][0], h1extension.Integral(0, h1extension.GetNbinsX()+1), inputSamples[k][3][m] )
        if (("%s" %type(h1subsample)).find("TH1") < 0):
          h1subsample = h1extension
        else:
          h1subsample.Add(h1extension)
      #print "h1subsample: %s - %f" %( inputSamples[i][0], h1subsample.Integral() )
      if (skippedIntegral > 0):
        print "Correcting for low parton samples: %f added to %f" %(skippedIntegral, h1subsample.Integral(0,h1subsample.GetNbinsX()+1))
        h1subsample.Scale( (skippedIntegral+h1subsample.Integral(0,h1subsample.GetNbinsX()+1)) / h1subsample.Integral(0,h1subsample.GetNbinsX()+1))
      if (inputSamples[k][0].find("QCDMM") >= 0):
        h1subsample = FixNegativeMMBins(h1subsample)
      h1subsamples[inputSamples[k][0]] = h1subsample
  else:
    h1subsamples = GetFiducialHists(HistName, Samples, inputSamples, files, scales, jetbin, channel, scaleToLumi, doChargeAsymmetry, fiducial, fidScale, WScale, WScaleSyst, WScaleUncert)

  for addScale in addScales:
    if addScale[0] not in h1subsamples:
      print "ERROR: additionalScale %s unknown!" %addScale[0]
      sys.exit()
    h1subsamples[addScale[0]].Scale(addScale[1])
    
  
  addloop = 0
  if (len(fiducial) > 0):
    addloop = len(fiducial)-1
  for x in range(len(Samples)+addloop): # loop over merging sample containers + fiducial ones
    i = x
    if (len(fiducial) > 0):
      i = x - len(fiducial) + 1
    if (x < len(fiducial)):
      i = 0
    h1sample = 0
    if (x < len(fiducial)):
      h1sample = dummyhist.Clone("%s-%05i"% ( Samples[i][0]+fiducial[x], random.randint(0,10000) ))
    else:
      h1sample = dummyhist.Clone("%s-%05i"% ( Samples[i][0], random.randint(0,10000) ))
    for j in range(len(Samples[i][1])): # loop over subsamples
      #h1subsample = dummyhist.Clone("%s%05i"% ( Samples[i][1][j], random.randint(0,10000) ))
      h1subsample = 0
      if (x < len(fiducial)):
        h1subsample = h1subsamples[Samples[i][1][j]+fiducial[x]]
      else:
        h1subsample = h1subsamples[Samples[i][1][j]]
      h1sample.Add(h1subsample)

    allhists.append(h1sample)

  if (HistName.find("mv1") >= 0):
    for hist in allhists:
      hist.Rebin(5)
  if (HistName.find("met_phi") >= 0):
    for hist in allhists:
      hist.Rebin(3)
  return allhists


def ScaleQCD(hists, HistName, Samples, QCDFractions, jetbin, channel):
  
  tagged = "pretag"
  if (HistName.find("BJet") >=0):
    tagged = "tag"
  qcdIndex = -1
  dataIndex = -1
  for i in range(len(hists)):
    if (hists[i].GetName().find("DATA") >= 0):
      dataIndex = i
    if (hists[i].GetName().find("QCDJE") >= 0):
      qcdIndex = i

  if (qcdIndex == -1):
    print "No QCD in samples!"
    return hists
  if (dataIndex == -1):
    print "No DATA in samples!"
    return hists

  currentJetbin = jetbin
  if (int(currentJetbin[0]) > 5): 
    s = list(currentJetbin)
    s[0] = "5"
    currentJetbin = "".join(s)
  dictstring = "%s_%s_%s" %(channel, currentJetbin, tagged)
  dataYield = hists[dataIndex].Integral(0, hists[dataIndex].GetNbinsX()+1)
  qcdYield = hists[qcdIndex].Integral(0, hists[qcdIndex].GetNbinsX()+1)
  #print "DataYield: %f" % dataYield
  #print "QCDYield: %f" % qcdYield
  if (qcdYield != 0):
    hists[qcdIndex].Scale( QCDFractions[dictstring]*dataYield/qcdYield)
    hists[qcdIndex].Smooth()
    hists[qcdIndex].Smooth()
  else:
    hists[qcdIndex].Scale( 0 )
    print "WARNING: QCD yields zero!"
  #print "QCDYield after scaling: %f" %hists[qcdIndex].Integral(0, hists[qcdIndex].GetNbinsX()+1)
  
  return hists


def OverflowToLast(h1):

  binContent = h1.GetBinContent(h1.GetNbinsX()) + h1.GetBinContent(h1.GetNbinsX()+1)
  binError = sqrt(h1.GetBinError(h1.GetNbinsX())*h1.GetBinError(h1.GetNbinsX()) + h1.GetBinError(h1.GetNbinsX()+1)*h1.GetBinError(h1.GetNbinsX()+1))
  h1.SetBinContent(h1.GetNbinsX(),binContent)
  h1.SetBinContent(h1.GetNbinsX()+1,0.)
  h1.SetBinError(h1.GetNbinsX(),binError)
  h1.SetBinError(h1.GetNbinsX()+1,0.)
  # also add underflow to first bin
  binContent = h1.GetBinContent(0) + h1.GetBinContent(1)
  binError = sqrt(h1.GetBinError(0)*h1.GetBinError(0) + h1.GetBinError(1)*h1.GetBinError(1))
  h1.SetBinContent(1,binContent)
  h1.SetBinContent(0,0.)
  h1.SetBinError(1,binError)
  h1.SetBinError(0,0.)

  return h1


def GetStack(hists, Samples):

  hstack = THStack()
  for i in range(len(hists)-1, -1, -1):
    if (hists[i].GetName().find("DATA") < 0 and hists[i].GetName().find("PSEUDO") < 0):
      hstack.Add(hists[i])

  return hstack


def GetSum(hists, Samples):

  hsum = hists[0].Clone("SUM-%05i" % random.randint(0,10000))
  hsum.Reset()
  for i in range(len(hists)):
    if (hists[i].GetName().split("-")[0].find("DATA") < 0 and hists[i].GetName().split("-")[0].find("PSEUDO") < 0):
      hsum.Add(hists[i])

  return hsum


def StyleHists(hists, Samples, default_color, default_MarkerStyle):

  for i in range(len(hists)):
    histid = hists[i].GetName().split("-")[0]
    if histid != "DATA":
      hists[i].SetMarkerSize(0.)
      hists[i].SetLineWidth(3)
      hists[i].SetMarkerColor(default_color[histid])
      if histid != "TOP":
        hists[i].SetLineColor(default_color[histid])
      if histid in default_MarkerStyle:
        hists[i].SetMarkerStyle(default_MarkerStyle[histid])
        if (i != 0): hists[i].SetMarkerSize(1.2)
    hists[i].SetFillColor(default_color[histid])
    hists[i].SetNdivisions(505,"x")
    hists[i].SetNdivisions(505,"y")
  return hists


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


def GetLegend(hists, Samples, default_Latex, option = ""):

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
      legend = TLegend(.2, .75, .45, .92)
      legend.SetTextSize(0.04)
    else:
      legend = TLegend(.65, .75, .95, .92)
      legend.SetTextSize(0.04)
    
  else:
    legend = TLegend(.75, .55, .9, .95)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)
  legend.SetTextFont(42) #was 72, see http://root.cern.ch/root/html/TAttText.html#T53
  for i in range(len(hists)):
    identifier = hists[i].GetName().split("-")[0]
    if (("%s" %type(identifier)).find("str") >= 0):
      if (len(identifier) == 1):
        identifier = Samples[i]
    if identifier != "DATA":
      if (i != 0) and (identifier in topSamples):
        legend.AddEntry(hists[i], default_Latex[identifier], "pl")
      else:
        legend.AddEntry(hists[i], default_Latex[identifier], "f")
    else:
      legend.AddEntry(hists[i], "%s (%i events)" %(default_Latex[identifier], hists[i].Integral(0, hists[i].GetNbinsX()+1)), "p")

  return legend


def AddWatermark():

  now = datetime.datetime.now()
  text = "%s - %s" %(os.getenv('USER'), now.strftime("%Y-%m-%d %H:%M"))
  watermark = TLatex()
  watermark.SetNDC()
  watermark.SetTextColor(18)
  watermark.SetTextSize(0.02)
  watermark.SetTextAlign(22)
  watermark.DrawLatex(0.03,0.01,text)
  return


def AddLumi(targetLumi):

  lumi = "%2.1f fb^{-1} (%1.0f TeV)" % (targetLumi/1000.,13)
  LumiBox = TLatex()
  LumiBox.SetNDC()
  LumiBox.SetTextSize(0.03)
  LumiBox.DrawLatex(gStyle.GetPadLeftMargin()+0.58,0.96,lumi)
  return


def SmoothHistograms(hists, Samples, smoothBins):

  if (smoothBins < 3) or (smoothBins%2 == 0):
    print "WARNING: skipping smoothing - need 3 or more bins and odd number!"
    return hists
  
  nBins = hists[0].GetNbinsX()
  loopStart = smoothBins%2+1
  loopEnd = nBins-smoothBins%2
  binLimit = smoothBins%2
  
  for i in range(len(Samples)):
    if (Samples[i][0].find("DATA") >= 0 or Samples[i][0].find("PSEUDO") >= 0):
      continue
    if (Samples[i][0].find("TOP") >= 0):
      continue

    print "Smoothing %s" %Samples[i][0]
    smoothedEntries = [None]*nBins
    for j in range(1,nBins+1):
      if (j < loopStart) or (j > loopEnd):
        smoothedEntries[j-1] = hists[i].GetBinContent(j)
      else:
        smoothedEntries[j-1] = hists[i].GetBinContent(j-binLimit)
        for k in range(j-binLimit+1,j+binLimit+1):
          smoothedEntries[j-1] += hists[i].GetBinContent(k)
        smoothedEntries[j-1] /= float(smoothBins)
  
    for j in range(1,nBins+1):
      hists[i].SetBinContent(j, smoothedEntries[j-1])

    #alternative:
    #hists[i].Smooth()

  return hists


def GetChargeAsymmetryFactors(Samples, inputSamples, files, scales, jetbins, channel, QCDFractions):

  scaleFactors = {}
  pretagHistName = "Analysis/offline/h_lepton_charge_el_WTM"
  if (channel == "Muons"):
    pretagHistName = "Analysis/offline/h_lepton_charge_mu_WTM"
  tagHistName = "Analysis/offline/h_lepton_charge_el_BJet"
  if (channel == "Muons"):
    tagHistName = "Analysis/offline/h_lepton_charge_mu_BJet"

  pretagHists2jexcl = GetHists(pretagHistName, Samples, inputSamples, files, scales, "2jexcl", channel, scaleToLumi = True, doChargeAsymmetry = False)
  tagHists2jexcl = GetHists(tagHistName, Samples, inputSamples, files, scales, "2jexcl", channel, scaleToLumi = True, doChargeAsymmetry = False)
  
  pretagHists2jexcl = ScaleQCD(pretagHists2jexcl, pretagHistName, Samples, QCDFractions, "2jexcl", channel)
  tagHists2jexcl = ScaleQCD(tagHists2jexcl, tagHistName, Samples, QCDFractions, "2jexcl", channel)
  
  DataPre2j = 0 # number of events in data pretag 2j bin
  DataTag2j = 0 # number of events in data tag 2j bin
  SumBkgPre2j = 0 # sum of background events (non-W, non-ttbar MC + QCD) in 2j bin pretag
  SumBkgTag2j = 0 # sum of background events (non-W, non-ttbar MC + QCD) in 2j bin tag
  ttPre2j = 0 # number of ttbar events in 2j bin pretag;
  ttTag2j = 0 # number of ttbar events in 2j bin tag;

  # DETERMINATION of ftag_2j-->ftag_(ith)j factor
  WPre2j = 0 # number of events in W+jets MC pretag 2j bin
  WTag2j = 0 # number of events in W+jets MC tag 2j bin
  
  
  for i in range(len(Samples)):
    if (Samples[i][0].find("DATA") >= 0):
      DataPre2j += pretagHists2jexcl[i].GetBinContent(1)+pretagHists2jexcl[i].GetBinContent(3)
      DataTag2j += tagHists2jexcl[i].GetBinContent(1)+tagHists2jexcl[i].GetBinContent(3)
    elif (Samples[i][0].startswith("W") and (Samples[i][0].find("JETS") >= 0)):
      WPre2j += pretagHists2jexcl[i].GetBinContent(1)+pretagHists2jexcl[i].GetBinContent(3)
      WTag2j += tagHists2jexcl[i].GetBinContent(1)+tagHists2jexcl[i].GetBinContent(3)
    elif (Samples[i][0].startswith("TOP")):
      ttPre2j += pretagHists2jexcl[i].GetBinContent(1)+pretagHists2jexcl[i].GetBinContent(3)
      ttTag2j += tagHists2jexcl[i].GetBinContent(1)+tagHists2jexcl[i].GetBinContent(3)
    else:
      SumBkgPre2j += pretagHists2jexcl[i].GetBinContent(1)+pretagHists2jexcl[i].GetBinContent(3)
      SumBkgTag2j += tagHists2jexcl[i].GetBinContent(1)+tagHists2jexcl[i].GetBinContent(3)

  for currentJetbin in jetbins:
    pretagHists = GetHists(pretagHistName, Samples, inputSamples, files, scales, currentJetbin, channel, scaleToLumi = True, doChargeAsymmetry = False)
    tagHists = GetHists(tagHistName, Samples, inputSamples, files, scales, currentJetbin, channel, scaleToLumi = True, doChargeAsymmetry = False)
    
    pretagHists = ScaleQCD(pretagHists, pretagHistName, Samples, QCDFractions, currentJetbin, channel)
    tagHists = ScaleQCD(tagHists, tagHistName, Samples, QCDFractions, currentJetbin, channel)
  
    DataPlusPre = 0 # number of events in data with a positively charged lepton
    DataPlusTag = 0 # number of events in data with a positively charged lepton
    DataMinusPre = 0 # number of events in data with a negatively charged lepton
    DataMinusTag = 0 # number of events in data with a negatively charged lepton
    SumBkgPlusPre = 0 # sum of background events (non-W, non-ttbar MC + QCD) with a positively charged lepton
    SumBkgPlusTag = 0 # sum of background events (non-W, non-ttbar MC + QCD) with a positively charged lepton
    SumBkgMinusPre = 0 # sum of background events (non-W, non-ttbar MC + QCD) with a negatively charged lepton
    SumBkgMinusTag = 0 # sum of background events (non-W, non-ttbar MC + QCD) with a negatively charged lepton
    WmcPlusPre = 0 # number of MC W+jets events with a positively charged lepton
    WmcPlusTag = 0 # number of MC W+jets events with a positively charged lepton
    WmcMinusPre = 0 # number of MC W+jets events with a negatively charged lepton
    WmcMinusTag = 0 # number of MC W+jets events with a negatively charged lepton
    
    WPreNj = 0 # number of events in W+jets MC pretag i-th bin
    WTagNj = 0 # number of events in W+jets MC tag i-th bin

    for i in range(len(Samples)):
      if (Samples[i][0].find("DATA") >= 0):
        DataMinusPre += pretagHists[i].GetBinContent(1)
        DataPlusPre += pretagHists[i].GetBinContent(3)
        DataMinusTag += tagHists[i].GetBinContent(1)
        DataPlusTag += tagHists[i].GetBinContent(3)
      elif (Samples[i][0].startswith("W") and (Samples[i][0].find("JETS") >= 0)):
        WmcMinusPre += pretagHists[i].GetBinContent(1)
        WmcPlusPre += pretagHists[i].GetBinContent(3)
        WmcMinusTag += tagHists[i].GetBinContent(1)
        WmcPlusTag += tagHists[i].GetBinContent(3)
        WPreNj += pretagHists[i].GetBinContent(1)+pretagHists[i].GetBinContent(3)
        WTagNj += tagHists[i].GetBinContent(1)+tagHists[i].GetBinContent(3)
      else: #if (Samples[i][0].startswith("STOP") >= 0) or (Samples[i][0].startswith("Z") and (Samples[i][0].find("JETS") >= 0)) or (Samples[i][0].find("DIBOSON") >= 0) or (Samples[i][0].startswith("QCD") >= 0):
        SumBkgMinusPre += pretagHists[i].GetBinContent(1)
        SumBkgPlusPre += pretagHists[i].GetBinContent(3)
        SumBkgMinusTag += tagHists[i].GetBinContent(1)
        SumBkgPlusTag += tagHists[i].GetBinContent(3)

    
    scaleFactors[channel+"_"+currentJetbin+"_WTM"] = GetWscaleFactorPretag( int(DataPlusPre), int(DataMinusPre), SumBkgPlusPre, SumBkgMinusPre, WmcPlusPre, WmcMinusPre )
    # the tagged SFs are to be applied to the pretag yields
    taggedSF = GetWscaleFactorTag( int(DataPlusTag), int(DataMinusTag), SumBkgPlusTag, SumBkgMinusTag, WmcPlusTag, WmcMinusTag, int(DataPre2j), int(DataTag2j), SumBkgPre2j, SumBkgTag2j, ttPre2j, ttTag2j, WPre2j, WTag2j, WPreNj, WTagNj)
    #print "WPreNj: %f  - WTagNj: %f  - taggedSF: %f - result: %f" %(WPreNj, WTagNj, taggedSF, WPreNj*taggedSF/WTagNj)
    scaleFactors[channel+"_"+currentJetbin+"_BJet"] = WPreNj*taggedSF/WTagNj
  print "------------> W scale factors <-------------"
  print scaleFactors
  return scaleFactors
