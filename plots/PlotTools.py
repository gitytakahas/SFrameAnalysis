from ROOT import * #TFile, TCanvas, TH1F, TH2F, THStack, TAxis, TGaxis...
import CMS_lumi, tdrstyle
from math import sqrt, pow

# CMS style
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Preliminary"
CMS_lumi.cmsTextSize  = 0.65
CMS_lumi.lumiTextSize = 0.60
CMS_lumi.relPosX = 0.105
CMS_lumi.outOfFrame = True
tdrstyle.setTDRStyle()

# other
# https://root.cern.ch/doc/master/classTColor.html
legendTextSize = 0.028 #0.036
colors     = [ kRed+3, kAzure+4, kOrange-6, kGreen+3, kMagenta+3, kYellow+2,
               kRed-7, kAzure-4, kOrange+6, kGreen-2, kMagenta-3, kYellow-2 ]
fillcolors = [ kRed-2, kAzure+5, kOrange-5, kGreen-2, kMagenta-3, kYellow-3,
               kRed-7, kAzure-9, kOrange+6, kGreen+3, kMagenta-2, kYellow-2 ]
list = [ ("jpt_1","jet 1 pt"),   ("jpt_2","jet 2 pt"),
         ("bpt_1","b jet 1 pt"), ("bpt_2","b jet 2 pt"),
         ("abs(jeta_1)",  "jet 1 abs(eta)"), ("abs(jeta_2)",  "jet 2 abs(eta)"),
         ("abs(beta_1)","b jet 1 abs(eta)"), ("abs(beta_2)","b jet 1 abs(eta)"),
         ("jeta_1",  "jet 1 eta"), ("jeta_2",  "jet 2 eta"),
         ("beta_1","b jet 1 eta"), ("beta_2","b jet 2 eta"),
         ("dR_ll","#DeltaR_{ll}"), ]
         




def makeLatex(title):
    """Convert patterns in a string to LaTeX format."""

    for a, b in list:
        if a in title:
            title = title.replace(a,b)
            break

    if "p_t" in title or "pt" in title or "Pt" in title:
        if "pt_" in title and "pt_" in title:
            title = title.replace("pt_","p_{T}^{").replace("Pt_","p_{T}^{") + "}"
        else:
            title = title.replace("p_t","p_{T}").replace("pt","p_{T}").replace("Pt","p_{T}")
        title += " [GeV]"
    
    if "m_" in title or "M_" in title:
        title = title.replace("m_","m_{").replace("M_","M_{") + "}" # TODO: split at next space
        title += " [GeV]"
    
    if "mt_" in title or "MT_" in title:
        title = title.replace("mt_","m_{T}^{").replace("M_","M_{T}^{") + "}" # TODO: split at next space
        title += " [GeV]"
    
    if "tau" in title or "Tau" in title:
        title = title.replace("tau","#tau").replace("Tau","#tau")
            
    if "phi" in title or "Phi" in title:
        if "phi_" in title or "Phi_" in title:
            title = title.replace("phi_","#phi_{").replace("Phi_","#phi_{") + "}"
        else:
            title = title.replace("phi","#phi").replace("Phi","#phi")
    
    if "eta" in title or "Eta" in title:
        if "eta_" in title or "Eta_" in title:
            title = title.replace("eta_","#eta_{").replace("Eta_","#eta_{") + "}"
        else:
            title = title.replace("eta","#eta").replace("Eta","#eta")
    
    if "abs(" in title and ")" in title:
        title = title.replace("abs(","|").replace(")","") + "|" # TODO: split at next space
    
    if "muon" in title or "Muon" in title:
        title = title.replace("muon","#muon").replace("Muon","#muon")
    
    if "ttbar" in title or "TTbar" in title:
        title = title.replace("ttbar","t#bar{t}").replace("TTbar","t#bar{t}")
    
    if "npv" in title:
        title = title.replace("npv","number of vertices")
    
    return title
    
    
    
    
    
def makeHistName(label, var):
    """Use label and var to make an unique and valid histogram name."""
    hist_name = "%s_%s" % (label, var)
    hist_name = hist_name.replace(".","_").replace(" ","_").replace("(","_").replace(")","_").replace("[","_").replace("]","_")
    return hist_name
    
    
    
    
    
def combineCuts(*cuts,**kwargs):
    """Combine cuts and apply weight if needed."""

    cuts = [ cut for cut in cuts if cut and type(cut) == str ]
    weight = kwargs.get('weight', False)
    
    # TODO: take "or" into account with parentheses
    for cut in cuts:
        if "||" in cuts: print ">>> be carefull with those \"or\" statements!"
        # [cut.strip() for i in cut.split('||')]
        
    if cuts:
        cuts = " && ".join(cuts)
        if weight:  cuts = "(%s)*%s" % (cuts, weight)
    elif weight:    cuts = weight
    else:           cuts = ""

    #print cuts
    return cuts





class Ratio(object):
    """Class to make histogram for Plot class."""

    def __init__(self, ratio, **kwargs):
        self.ratio = ratio
        self.staterror = kwargs.get('staterror', None)
        self.line = kwargs.get('line', False)
    

    
    def Draw(self, option, **kwargs):
        a = self.ratio.GetXaxis().GetXmin()
        b = self.ratio.GetXaxis().GetXmax()
        
        self.ratio.Draw("E same")
        
        if self.staterror:
            self.staterror.Draw("E2 same")
            self.staterror.SetLineStyle(1)
            self.staterror.SetMarkerStyle(1)
            self.staterror.SetFillColor(kBlack)
            self.staterror.SetFillStyle(3004)
        
        if self.line:
            self.line = TLine(a,1,b,1)
            self.line.SetLineStyle(2)
            self.line.Draw("same")
        
        self.ratio.Draw("E same")





class Samples(object):
    """Class to combine a set of Sample-objects to make one histogram with the Plot class."""

    def __init__(self, label, **kwargs):
        self.samples = [ ]
        self.label = label
        self.cuts = kwargs.get('cuts', "")
        self.weight = kwargs.get('weight', False)
        self.scale = kwargs.get('scale', 1)
        self.isData = kwargs.get('data', False)
        self.isBackground = kwargs.get('background', False)
        self.isSignal = kwargs.get('signal', False)
    

    
    def add(self, sample, **kwargs):
        self.samples.add(sample)
    

    
    def hist(self, var, nBins, a, b, scale=1, **kwargs):
        name   = kwargs.get('name',  makeHistName(self.label, var))
        title  = kwargs.get('title', self.label)
        
        hist = TH1F(name, title, nBins, a, b)
        for sample in self.samples:
            hist.Add(sample.hist(var, nBins, a, b, scale=scale, **kwargs))
        
        return hist





class Sample(object):
    """Class to make histogram with the Plot class."""

    def __init__(self, filename, label, **kwargs):
        self.filename = filename
        self.file = TFile(filename)
        self.label = label
        self.cuts = kwargs.get('cuts', "")
        self.weight = kwargs.get('weight', False)
        self.scale = kwargs.get('scale', 1)
        self.isData = kwargs.get('data', False)
        self.isBackground = kwargs.get('background', False)
        self.isSignal = kwargs.get('signal', False)
        self.treeName = kwargs.get('treeName', "tree")
    

    
    def hist(self, var, nBins, a, b, scale=1, **kwargs):
        """Make a histogram with a tree."""
        
        tree   = self.file.Get(self.treeName)
        weight = self.weight or kwargs.get('weight', False)
        cuts   = combineCuts(self.cuts, kwargs.get('cuts', ""), weight=weight)
        name   = kwargs.get('name',  makeHistName(self.label, var))
        title  = kwargs.get('title', self.label)
        
        hist = TH1F(name, title, nBins, a, b)
        tree.Draw("%s >> %s" % (var,name), cuts, "gOff")
        if self.scale*scale is not 1:
            hist.Scale(self.scale*scale)
        #print hist.GetEntries()
        #gDirectory.Delete(label)
        return hist
    
    
    
    def scale(self, hist, scale, **kwargs):
        """Make a scale."""
        
        if len(args):
            scale = args[0]
            if I: hist.Scale(scale)
            else: print ">>> could not scale: I = 0"
        else:
            lumi = kwargs.get('lumi', 0)
            sigma = kwargs.get('sigma', 0)
            efficiency = kwargs.get('efficiency', 1)
            acceptance = kwargs.get('acceptance', 1)
            e = kwargs.get('e', 1)
            A = kwargs.get('A', 1)
            N = kwargs.get('N', 1)
            if lumi and sigma:
                scale = lumi * sigma * efficiency * e * acceptance * A / N
                if I: hist.Scale(scale)
                else: print ">>> could not scale: I = 0"


    def norm(self, hist):
        """Normalize histogram."""
        
        I = hist.Integral()
        if I:
            hist.Scale(1/I)





class Plot(object):
    """Class to automatically make CMS plot."""

    def __init__(self, samples, var, nBins, a, b, **kwargs):
        self.samples = samples
        self.var = var
        self.nBins = nBins
        self.a = a; self.b = b
        self.cuts = kwargs.get('cuts', "")
        
        self.histsS = [ ]
        self.histsB = [ ]
        self.histsD = [ ]
        self._hists = [ ]
        self._histsMC = [ ]
        self.hist_error = None
        self.ratio = None
        
        for sample in samples:
            if sample.isSignal:
                self.histsS.append(sample.hist(var, nBins, a, b, cuts=self.cuts))
            elif sample.isBackground:
                self.histsB.append(sample.hist(var, nBins, a, b, cuts=self.cuts))
            elif sample.isData:
                self.histsD.append(sample.hist(var, nBins, a, b, cuts=self.cuts))
        if kwargs.get('QCD', False):
            histQCD = self.QCD()
            if histQCD: self.histsB.append(histQCD)
            
        self.stack = None
        self.canvas = None
        self.pads = [ ]
        self.frame = None
        self.legend = None
        self.width = 0.26;  self.height = 0.08 + 0.05 * len(self.histsB)
        self.x2 = 0.95;     self.x1 = self.x2 - self.width
        self.y1 = 0.48;     self.y2 = self.y1 + self.height

    @property
    def hists(self): return ( self.histsB + self.histsS + self.histsD )

    @hists.setter
    def hists(self, value): self._hists = value

    @property
    def histsMC(self): return ( self.histsB + self.histsS )

    @histsMC.setter
    def histsMC(self, value): self._histsMC = value



    def plot(self,*args,**kwargs):
        """Make plot with canvas, axis, error, ratio..."""
    
        # https://root.cern.ch/doc/master/classTHStack.html
        # https://root.cern.ch/doc/master/classTHistPainter.html#HP01e
        stack = kwargs.get('stack', False)
        residue = kwargs.get('residue', False) and self.histsD
        ratio = kwargs.get('ratio', False) and self.histsD
        errorbars = kwargs.get('errorbars', False)
        staterror = kwargs.get('staterror', False)
        option = 'hist'
        if errorbars: option = 'E0 '+option
        
        # CANVAS
        self.makeCanvas(  square=kwargs.get('square', False),
                          residue=residue, ratio=ratio,
                          scaleleftmargin=kwargs.get('scaleleftmargin', 1),
                          scalerightmargin=kwargs.get('scalerightmargin', 1)  )
        
        # MONTE CARLO
        if stack:
            stack = THStack("stack","")
            self.stack = stack
            for hist in self.histsMC: stack.Add(hist)
            stack.Draw(option)
        else:
            for hist in self.histsMC: hist.Draw(option+' same')  
        
        # DATA
        for hist in self.histsD:
            hist.Draw('E same')
        
        # STATISTICAL ERROR
        if staterror:
            self.hist_error = self.makeStatisticalError( self.histsMC, name=makeHistName("stat_error",self.var),
                                                                       title="statistical error" )
            self.hist_error.Draw('E2 same')
        
        # STYLE
        if stack:
            self.setFillStyle(*self.histsMC)
            for hist in self.histsMC: hist.SetMarkerStyle(1)
        else:
            self.setLineStyle(*self.histsMC)
        if self.histsD:
            self.setMarkerStyle(*self.histsD)
        
        # AXES & LEGEND
        self.makeAxes( xlabel=kwargs.get('xlabel', self.var), noxaxis=ratio,
                       logy=kwargs.get('logy',False), logx=kwargs.get('logx',False) )
        if kwargs.get('legend', True):
            self.makeLegend( title=kwargs.get('title', ""), entries=kwargs.get('entries', ),
                                                            position=kwargs.get('position', "") )
        CMS_lumi.CMS_lumi(self.canvas,13,0)
        
        # RATIO
        if ratio:
            self.pads[1].cd()
            self.ratio = self.ratioHistStack( self.histsD[0], self.stack, staterror=self.hist_error,
                                              name=makeHistName("ratio",self.var), title="ratio" )
            self.ratio.Draw("same")
            self.makeAxes( ratio=self.ratio, ylabel="ratio", xlabel=kwargs.get('xlabel', self.var))



    def saveAs(self,filename):
        """Save plot, close canvas and delete the histograms."""
        
        self.canvas.SaveAs(filename)
        self.canvas.Close()
        for hist in self.hists:
            gDirectory.Delete(hist.GetName())



    def makeCanvas(self,**kwargs):
        """Make canvas and pads for ratio plots."""
        
        square = kwargs.get('square', False)
        scaleleftmargin  = kwargs.get('scaleleftmargin', 1)
        scalerightmargin = kwargs.get('scalerightmargin', 1)
        scaletopmargin = kwargs.get('scaletopmargin', 1)
        residue = kwargs.get('residue', False)
        ratio = kwargs.get('ratio', False)
        
        W = 800; H  = 600
        if square:
            W = 800; H  = 800
            self.width = 0.30
            scalerightmargin = 3.5*scalerightmargin
        elif residue or ratio:
            W = 800; H  = 750
            scaleleftmargin  = 1.05*scaleleftmargin
            scalerightmargin = 0.45*scalerightmargin
            scaletopmargin   = 0.80*scaletopmargin
            CMS_lumi.cmsTextSize  = 0.55
            CMS_lumi.lumiTextSize = 0.45
            CMS_lumi.relPosX = 0.08
        
        T = 0.08*H*scaletopmargin
        B = 0.12*H
        L = 0.12*W*scaleleftmargin
        R = 0.04*W*scalerightmargin
        
        canvas = TCanvas("canvas","canvas",100,100,W,H)
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetLeftMargin( L/W )
        canvas.SetRightMargin( R/W )
        canvas.SetTopMargin( T/H )
        canvas.SetBottomMargin( B/H )

        if residue or ratio:
            pads = [ TPad("pad1","pad1", 0, 0.33, 1, 0.95),
                     TPad("pad2","pad2", 0, 0.05, 1, 0.30) ]
            pads[0].SetLeftMargin(0.125)
            #pads[0].SetRightMargin(0.05)
            pads[0].SetTopMargin(0.02)
            pads[0].SetBottomMargin(0.00001)
            pads[0].SetBorderMode(0)
            pads[1].SetTopMargin(0.00001)
            pads[1].SetBottomMargin(0.10)
            pads[1].SetLeftMargin(0.125)
            #pads[1].SetRightMargin(0.05)
            pads[1].SetBorderMode(0)
            pads[0].Draw()
            pads[1].Draw()
            pads[0].cd()
            self.pads = pads

        self.canvas = canvas



    def makeLegend(self,*args,**kwargs):
        """Make legend."""
        
        title = kwargs.get('title', None)
        entries = kwargs.get('entries', [ ])
        position = kwargs.get('position', "")
        transparent = kwargs.get('transparent', False)
        hists = self.hists
        histsD = self.histsD
        x1 = self.x1; x2 = self.x2
        y1 = self.y1; y2 = self.y2
        width = self.width
        height = self.height
        
        styleD  = 'le'
        styleMC = 'l'
        if self.stack: styleMC = 'f'
        
        if position:
            if "LeftLeft" in position:      x1 = 0.15;      x2 =x1 + width
            elif "Left" in position:        x1 = 0.20;      x2 = x1 + width
            elif "RightRight" in position:  x2 = 1 - 0.10;  x1 = x2 - width
            elif "Right" in position:       x2 = 1 - 0.15;  x1 = x2 - width
            elif "Center" in position:      x1 = 0.55 - width/2;  x2 = 0.55 + width/2
            if "BottomBottom" in position:  y1 = 0.15;      y2 = y2 + height
            elif "Bottom" in position:      y1 = 0.20;      y2 = y2 + height
            elif "TopTop" in position:      y2 = 0.95;      y1 = y2 - height
            elif "Top" in position:         y1 = 0.90;      y2 = y1 - height
        legend = TLegend(x1,y1,x2,y2)
        
        if transparent: legend.SetFillStyle(0) # 0 = transparent
        else: legend.SetFillColor(kWhite)
        legend.SetBorderSize(0)
        legend.SetTextSize(legendTextSize)
                       
        if title is None: legend.SetHeader("Title")
        else: legend.SetHeader(title)

        if hists:
            if entries:
                for hist, entry in zip( hists, entries ):
                    style = styleMC
                    if hist in histsD: style = styleD
                    legend.AddEntry(hist,entry,styleMC)
            else:
                for hist in hists:
                    style = styleMC
                    if hist in histsD: style = styleD
                    legend.AddEntry(hist,hist.GetTitle(),style)

            self.legend = legend
            legend.Draw()
            
    
            
    def symmetricYRange(self, frame, **kwargs):
        """Make symmetric Y range around some center value."""
        
        center = kwargs.get('center',0) 
        min = center
        Max = center
        
        for i in range(1,frame.GetNbinsX()+1):
            low = frame.GetBinContent(i) - frame.GetBinError(i)
            up  = frame.GetBinContent(i) + frame.GetBinError(i)
            if low and low < min: min = low
            if         up  > Max: Max = up
        
        width = max(abs(center-min),abs(Max-center))*1.05
        return [ center-width, center+width ]
    



    def makeAxes(self, *args, **kwargs):
        """Make axis."""
        
        frame = None
        ratio = kwargs.get('ratio', None)
        scale = 1
        
        if ratio:
            frame = ratio.ratio
            scale = 2.5
            #width = max(abs(1-frame.GetMinimum(0)),abs(1-frame.GetMaximum()))*1.30
            frame.GetYaxis().SetRangeUser(*self.symmetricYRange(frame,center=1.0))
            frame.GetYaxis().SetNdivisions(505)
        elif self.stack:
            frame = self.stack
            maxs = [ self.stack.GetMaximum() ]
            for hist in self.histsD:
                maxs.append(hist.GetMaximum())
            #frame.SetMinimum(0)
            frame.SetMaximum(max(maxs)*1.12)
        else:
            frame = self.hists[0]
            mins = [ 0 ]
            maxs = [   ]
            for hist in self.hists:
                mins.append(hist.GetMinimum())
                maxs.append(hist.GetMaximum())
            frame.GetYaxis().SetRangeUser(min(mins),max(maxs)*1.12)
        frame.GetXaxis().SetLimits(self.a,self.b)
        
        if kwargs.get('logy',False):
            #frame.SetMinimum(0.1)
            gPad.Update(); gPad.SetLogy()
        if kwargs.get('logx',False):
            #frame.SetMinimum(0.1)
             gPad.Update(); gPad.SetLogx()
        
        xlabel = makeLatex(kwargs.get('xlabel', self.hists[0].GetTitle()))
        ylabel = kwargs.get('ylabel', "")
        if not ylabel:
            ylabel = "Events / %s" % frame.GetXaxis().GetBinWidth(0)
            if "GeV" in xlabel:
                ylabel += " GeV"
        
        if ratio:
            ylabel = "ratio" #"data / M.C."
            frame.GetYaxis().SetTitle(ylabel)
            frame.GetYaxis().SetLabelSize(0.10)
            frame.GetYaxis().SetTitleSize(0.12)
            frame.GetYaxis().CenterTitle(True)
            frame.GetYaxis().SetTitleOffset(0.5)
        else:
            frame.GetYaxis().SetTitle(ylabel)
            frame.GetYaxis().SetLabelSize(0.040)
            frame.GetYaxis().SetTitleSize(0.042)
            frame.GetYaxis().SetTitleOffset(1.45)
        
        frame.GetXaxis().SetTitle(xlabel)
        frame.GetXaxis().SetLabelSize(0.040*scale)
        frame.GetXaxis().SetTitleSize(0.042*scale)
        frame.GetXaxis().SetTitleOffset(1.10)
        if kwargs.get('noxaxis',False):
            frame.GetXaxis().SetLabelSize(0)
            frame.GetXaxis().SetTitleSize(0)  
#         frame.GetYaxis().CenterTitle(True)
#         frame.GetXaxis().SetNdivisions(508)
#         ROOT.gPad.SetTicks(1,1)
#         ROOT.gPad.SetGrid(1,1)
        TGaxis.SetExponentOffset(-0.058,0.005,'y')



    def setLineStyle(self, *hists, **kwargs):
        """Make line style."""

        if len(hists) is 0: hists = self.hists
        gen = kwargs.get('gen', False)

        if gen:
            colors2 = [kRed+3, kRed-7, kAzure+4, kAzure-4, kMagenta+3, kGreen+3, kOrange+6, kMagenta-3]
            line = [1,3,2,3]
            for i in range(len(hists)):
                hists[i].SetLineColor(colors2[i])
                hists[i].SetLineStyle(line[i%4])
                hists[i].SetLineWidth(3)
        else:
            for i in range(len(hists)):
                hists[i].SetLineColor(colors[i%len(colors)])
                hists[i].SetLineStyle(i%4+1)
                hists[i].SetLineWidth(3)



    def setFillStyle(self, *hists):
        """Make fill style."""
        
        #print ">>> setFillStyle"
        if len(hists) is 0: hists = self.hists
        for i in range(len(hists)):
            #hists[i].SetLineColor(colors[i%len(colors)])
            #hists[i].SetLineStyle(1)
            hists[i].SetFillColor(fillcolors[i%len(colors)])



    def setLineColor(self, *hists):
        """Make line color."""
        
        #print ">>> setLineColor"
        if len(hists) is 0: hists = self.hists
        for i in range(len(hists)):
            hists[i].SetLineColor(colors[i%len(colors)])
            hists[i].SetLineStyle(1)
            hists[i].SetLineWidth(3)



    def setMarkerStyle(self, *hists):
        #print ">>> setMarkerStyle"
        if len(hists) is 0: hists = self.hists
        for hist in hists:
            hist.SetMarkerStyle(20)
            hist.SetMarkerSize(0.8)



    def norm(self,*hists):
        """ Normalize histogram."""
        
        if len(hists) is 0: hists = self.hists
        for hist in hists:
            I = hist.Integral()
            if I:
                hist.Scale(1/I)



    def makeStatisticalError(self,hists,**kwargs):
        """Make statistical error for a set of histograms."""
        
        name = kwargs.get('name', "error_"+hists[0].GetName())
        title = kwargs.get('title', "error")
        color = kwargs.get('color', kBlack)
        N = hists[0].GetNbinsX()
        a = hists[0].GetXaxis().GetXmin()
        b = hists[0].GetXaxis().GetXmax()
        hist_error = TH1F(name,title,N,a,b)
        
        for hist in hists:
            hist_error.Add(hist)
        
        #hist_error.Sumw2()
        hist_error.SetLineStyle(1);
        hist_error.SetMarkerStyle(1);
        hist_error.SetFillColor(color);
        hist_error.SetFillStyle(3004);
        
        return hist_error
        
        
        
    def setStatisticalErrorStyle(self,hist_error,**kwargs):
        color = kwargs.get('color', kBlack)
        hist_error.SetLineStyle(1);
        hist_error.SetMarkerStyle(1);
        hist_error.SetFillColor(color);
        hist_error.SetFillStyle(3004);
        
       
        
    def ratioError(self,a,ea,b,eb):
        """Calculate the error on a ratio a/b given errors ea on a and eb on b"""
        if b == 0:
            print ">>> Warning in ratioError: cannot divide by zero!"
            return ea
        elif a == 0:
            return ea
        return abs(a/b) * sqrt( pow(ea/a,2) + pow(eb/b,2) )
        


    def ratioHistStack(self,hist0,stack,**kwargs):
        """Make a ratio of the data histogram / stacked MC histograms,
           bin by bin."""
        
        name = kwargs.get('name', "ratio_"+hist0.GetName())
        title = kwargs.get('title', "ratio")
        staterror = kwargs.get('staterror',True)
        N = hist0.GetNbinsX()
        a = hist0.GetXaxis().GetXmin()
        b = hist0.GetXaxis().GetXmax()
        hist_ratio = TH1F(name,title,N,a,b)
        hist_staterror = TH1F(name+"_staterror",title+" staterror",N,a,b)
        
        # dummy hist to get error and bin content of the stack
        hist_stack = TH1F("hist_stack","hist_stack",N,a,b)
        for hist in stack.GetStack():
            hist_stack.Add(hist)
        
        for i in range(1,N+1):
            stack_binc = stack.GetStack().Last().GetBinContent(i) #hist_stack.GetBinContent(i)
            hist_binc  = hist0.GetBinContent(i)
            if stack_binc:            
                hist_staterror.SetBinContent(i,1)
                hist_staterror.SetBinError(i,hist_stack.GetBinError(i)/stack_binc)
                if hist_binc and hist_binc / stack_binc < 100:
                    hist_ratio.SetBinContent(i, hist_binc / stack_binc );
                    hist_ratio.SetBinError(i, hist.GetBinError(i) / stack_binc )
        #gDirectory.Delete(hist.GetName())
        
        if not staterror:
            hist_staterror = None
        
        return Ratio( hist_ratio, line=True, staterror=hist_staterror )
        


    def substractStackFromHist(self,stack,hist0,**kwargs):
        """Substract stacked MC histograms from a data histogram,
           bin by bin if the difference is larger than zero."""
        
        name = kwargs.get('name', "diff_"+hist0.GetName())
        title = kwargs.get('title', "difference")
        N = hist0.GetNbinsX()
        a = hist0.GetXaxis().GetXmin()
        b = hist0.GetXaxis().GetXmax()
        hist_diff = TH1F(name,title,N,a,b)
        
        for i in range(1,N+1):
            hist_diff.SetBinContent(i, max(0,hist0.GetBinContent(i)-stack.GetStack().Last().GetBinContent(i)));
            #print ">>> i=%i, diff = %f" % (i, hist.GetBinContent(i)-stack.GetStack().Last().GetBinContent(i))  

        return hist_diff



    def QCD(self,**kwargs):
        """Substract MC from data with same sign (SS) selection of a lepton - tau pair
           and return a histogram of the difference."""
        
        cuts = self.cuts
        var = self.var
        nBins = self.nBins
        a = self.a
        b = self.b
        samples = self.samples
        
        if "q_1 * q_2 < 0" in cuts or "q_1*q_2<0" in cuts or "q_1*q_2 < 0" in cuts:
            cuts = cuts.replace("q_1 * q_2 < 0","q_1 * q_2 > 0").replace("q_1*q_2 < 0","q_1 * q_2 > 0").replace("q_1*q_2<0","q_1 * q_2 > 0")        
        elif cuts:
            cuts = "q_1 * q_2 > 0 && %s" % cuts
        else:
            cuts = "q_1 * q_2 > 0"
            #return None
        
        histsMC_SS = [ ]
        histsD_SS  = [ ]
        for sample in samples:
            name = makeHistName(sample.label+"_SS", var)
            if sample.isBackground or sample.isSignal:
                histsMC_SS.append(sample.hist(var, nBins, a, b, cuts=cuts, name=name))
            elif sample.isData:
                histsD_SS.append(sample.hist(var, nBins, a, b, cuts=cuts, name=name))
        if not histsD_SS:
            print ">>> Warning! No data to make data driven QCD!"
            return None 
        
        stack_SS = THStack("stack_SS","stack_SS")
        for hist in histsMC_SS: stack_SS.Add(hist)
        histQCD = self.substractStackFromHist(stack_SS,histsD_SS[0],name=makeHistName("QCD",var),title="QCD")
        
        for hist in histsMC_SS + histsD_SS: gDirectory.Delete(hist.GetName())
        return histQCD




