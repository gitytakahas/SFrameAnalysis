from ROOT import * #TFile, TCanvas, TH1F, TH2F, THStack, ...
import CMS_lumi, tdrstyle

# CMS style
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Preliminary"
CMS_lumi.cmsTextSize  = 0.65
CMS_lumi.lumiTextSize = 0.6
CMS_lumi.relPosX = 0.105
CMS_lumi.outOfFrame = True
tdrstyle.setTDRStyle()

# other
legendTextSize = 0.04 #0.036
colors = [kRed+3,kAzure+4,kOrange-6,kMagenta+3,kGreen+3,kYellow+2,kRed-7, kAzure-4, kOrange+6, kMagenta-3, kYellow-2]
# TColor, gROOT, ...





def makeLatex(title):

    if "p_t" in title or "pt" in title or "Pt" in title:
        title = title.replace("p_t","p_{T}").replace("pt","p_{T}").replace("Pt","p_{T}")
        
    if "m_" in title or "M_" in title:
        title = title.replace("m_","m_{").replace("M_","M_{") + "}" # TODO: split at next space
    
    if "tau" in title or "Tau" in title:
        title = title.replace("tau","#tau").replace("Tau","#tau")
    
    if "ttbar" in title or "TTbar" in title:
        title = title.replace("ttbar","t#bar{t}").replace("TTbar","t#bar{t}")

    return title
    
    
    
    
    
def combineCuts(*cuts):

    cuts = [ cut for cut in cuts if cut and type(cut) == str ]
    
    # TODO: take "or" into account
    for cut in cuts:
        if "||" in cuts: ">>> be carefull"
    cuts = " && ".join(cuts)

    return cuts





class Sample(object):
    """Class to make histogram for Plot class."""

    def __init__(self, file, label, **kwargs):
        self.file = TFile(file)
        self.label = label
        self.cuts = kwargs.get('cuts', "")
        self.scale = kwargs.get('scale', 1)
        self.isData = kwargs.get('data', False)
        self.isBackground = kwargs.get('background', False)
        self.isSignal = kwargs.get('signal', False)
    

    
    def hist(self, var, nBins, a, b, scale=1, **kwargs):
        tree = self.file.Get("tree")
        cuts = combineCuts(self.cuts, kwargs.get('cuts', ""))
        
        hist = TH1F(self.label, var, nBins, a, b)
        tree.Draw("%s >> %s" % (var,self.label), cuts, "goff")
        if self.scale*scale is not 1:
            hist.Scale(self.scale*scale)
        #print hist.GetEntries()
        #gDirectory.Delete(label)
        return hist
    
    
    
    def scale(self, hist, scale, **kwargs):
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
        I = hist.Integral()
        if I:
            hist.Scale(1/I)





class Plot(object):
    """Class to automatically make CMS plot."""

    def __init__(self, samples, var, nBins, a, b, **kwargs):
#         self.hists = hists
        self.histsS = [ ]
        self.histsB = [ ]
        self.histsD = [ ]
        self._hists = [ ]
        self.cuts = kwargs.get('cuts', "")
        for sample in samples:
            if sample.isSignal:
                self.histsS.append(sample.hist(var, nBins, a, b, cuts=self.cuts))
            elif sample.isBackground:
                self.histsB.append(sample.hist(var, nBins, a, b, cuts=self.cuts))
            elif sample.isData:
                self.histsD.append(sample.hist(var, nBins, a, b, cuts=self.cuts))
        self.var = var
        self.nBins = nBins
        self.a = a; self.b = b
        self.stack = None
        self.canvas = None
        self.frame = None
        self.legend = None
        self.width = 0.24;  self.height = 0.08 + 0.05 * len(self.histsB)
        self.x2 = 0.95;     self.x1 = self.x2 - self.width
        self.y1 = 0.50;     self.y2 = self.y1 + self.height

    @property
    def hists(self): return ( self.histsB + self.histsS + self.histsD )

    @hists.setter
    def hists(self, value): self._hists = value



    def plot(self,*args,**kwargs):
        # https://root.cern.ch/doc/master/classTHStack.html
        stack = kwargs.get('stack', False)
        
        self.makeCanvas(square=kwargs.get('square', False),scaleleftmargin=kwargs.get('scaleleftmargin', 1),scalerightmargin=kwargs.get('scalerightmargin', 1))
        
        if stack:
            stack = THStack("stack","")
            for hist in self.histsB+self.histsS:
                stack.Add(hist)
            self.setFillStyle(*(self.histsB+self.histsS))
            stack.Draw()
            self.stack = stack
        else:
            for hist in self.histsB+self.histsS:
                hist.Draw("same")        
        for hist in self.histsD:
            hist.Draw("Esame")
        
        self.makeAxes(xlabel=kwargs.get('xlabel', ""), ylabel=kwargs.get('ylabel', ""))
        self.makeLegend(title=kwargs.get('title', ""), entries=kwargs.get('entries', [ ]), position=kwargs.get('position', ""))
        CMS_lumi.CMS_lumi(self.canvas,13,0)
        
        if not stack:
            self.setLineStyle(*(self.histsB+self.histsS))
        self.setMarkerStyle(*self.histsD)
        
        #return self.canvas


    def saveAs(self,filename):
        self.canvas.SaveAs(filename)
        self.canvas.Close()
        for hist in self.hists:
            gDirectory.Delete(hist.GetName())


    def makeCanvas(self,square=False, scaleleftmargin=1, scalerightmargin=1):
        W = 800; H  = 600
        if square:
            W = 800; H  = 800
            self.width = 0.30
            scalerightmargin = 3.5*scalerightmargin
        T = 0.08*H
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
#         canvas.SetTickx(0)
#         canvas.SetTicky(0)
#         canvas.cd()
#         self.frame = self.canvas.DrawFrame(0,0,100,10000)
        self.canvas = canvas



    def makeLegend(self,*args,**kwargs):
        title = kwargs.get('title', None)
        entries = kwargs.get('entries', [ ])
        position = kwargs.get('position', "")
        transparent = kwargs.get('transparent', False)
        hists = self.hists
        x1 = self.x1; x2 = self.x2
        y1 = self.y1; y2 = self.y2
        width = self.width
        height = self.height
        
        if position:
            if "LeftLeft" in position:      x1 = 0.15;      x2 =x1 + width
            elif "Left" in position:        x1 = 0.20;      x2 = x1 + width
            elif "RightRight" in position:  x2 = 1 - 0.10;  x1 = x2 - width
            elif "Right" in position:       x2 = 1 - 0.15;  x1 = x2 - width
            if "BottomBottom" in position:  y1 = 0.15;      y2 = y2 + height
            elif "Bottom" in position:      y1 = 0.20;      y2 = y2 + height
            elif "TopTop" in position:      y2 = 0.95;      y1 = y2 - height
            elif "Top" in position:         y1 = 0.90;      y2 = y1 - height
        legend = TLegend(x1,y1,x2,y2)
        
        if transparent: legend.SetFillStyle(0) # 0 = transparent
        else: legend.SetFillColor(kWhite)
        legend.SetBorderSize(0)
        legend.SetTextSize(legendTextSize)
        
        style = 'l'
        if self.stack: style = 'f'
               
        if title is None: legend.SetHeader("Default title")
        if hists:
            if entries:
                for hist, entry in zip( hists, entries ):
                    legend.AddEntry(hist,entry,style)
            else:
                for hist in hists:
                    legend.AddEntry(hist,hist.GetName(),style)

            self.legend = legend
            legend.Draw()



    def makeAxes(self, *args, **kwargs):
        
        frame = None
        if self.stack:
            frame = self.stack
            frame.SetMinimum(0)
            frame.SetMaximum(self.stack.GetMaximum()*1.12)
        else:
            frame = self.hists[0]
            mins = [ 0 ]
            maxs = [   ]
            for hist in self.hists:
                mins.append(hist.GetMinimum())
                maxs.append(hist.GetMaximum())
            frame.GetYaxis().SetRangeUser(min(mins),max(maxs)*1.12)
        frame.GetXaxis().SetLimits(self.a,self.b)
        
        xlabel = kwargs.get('xlabel', "")
        ylabel = ""
        if xlabel:
            frame.GetXaxis().SetTitle(xlabel)
        if kwargs.get('ylabel', ""):
            ylabel = kwargs.get('ylabel', "")
        
        frame.GetYaxis().SetTitle(ylabel)
        frame.GetXaxis().SetLabelSize(0.042)
        frame.GetYaxis().SetLabelSize(0.042)
        frame.GetXaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetTitleOffset(1.45)
#         frame.GetYaxis().CenterTitle(True)
#         frame.GetXaxis().SetNdivisions(508)
#         ROOT.gPad.SetTicks(1,1)
#         ROOT.gPad.SetGrid(1,1)




    def setLineStyle(self, *hists, **kwargs):

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



    def setLineColor(self, *hists):
        if len(hists) is 0: hists = self.hists
        for i in range(len(hists)):
            hists[i].SetLineColor(colors[i%len(colors)])
            hists[i].SetLineStyle(1)
            hists[i].SetLineWidth(3)



    def setMarkerStyle(self, *hists):
        if len(hists) is 0: hists = self.hists
        for hist in hists:
            hist.SetMarkerStyle(20)
            hist.SetMarkerSize(0.8)


    def setFillStyle(self, *hists):
        if len(hists) is 0: hists = self.hists
        for i in range(len(hists)):
#             hists[i].SetLineColor(colors[i%len(colors)])
#             hists[i].SetLineStyle(1)
            hists[i].SetFillColor(colors[i%len(colors)])


    def norm(self,*hists):
        if len(hists) is 0: hists = self.hists
        for hist in hists:
            I = hist.Integral()
            if I:
                hist.Scale(1/I)



