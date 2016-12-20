import os, numpy, math, copy, math, sys, collections
from array import array
from ROOT import gStyle, TCanvas, TLegend, TH1F
from officialStyle import officialStyle
from DisplayManager import DisplayManager
from config import config
from DataMCPlot import *
import MultiDraw


lumi=12.9
basedir = '/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/'


normalizeWusinghighMT = True
WsidebandMTvalue = 80.
WriteDataCard = True


gROOT.SetBatch(True)
#gROOT.SetBatch(False)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

def comparisonPlots(hist, pname='sync.pdf', isRatio=True):

    display = DisplayManager(pname, isRatio, lumi, 0.42, 0.65)
    display.Draw(hist)


def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



config = config(basedir, lumi)
process = config.process

# currently, for mu-tau channel only

baseselection = 'dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1 && iso_1 < 0.15 && iso_2 == 1 && channel==1'


################################################################################
### First, evaluate W SF


wcategories = collections.OrderedDict()
wcategories['w_os'] = {'sel':baseselection + '&& q_1*q_2<0'}
wcategories['w_ss'] = {'sel':wcategories['w_os']['sel'].replace('q_1*q_2<0', 'q_1*q_2>0')}

wvardir = {
    'pfmt_1':{'drawname':'pfmt_1', 'nbins':40, 'min':0, 'max':200, 'label':'PF MET Transverse mass (GeV)'},
#    'mt_1':{'drawname':'mt_1', 'nbins':40, 'min':0, 'max':200, 'label':'MVA MET Transverse mass (GeV)'},
    }


whists = {}

for catname, cat in wcategories.iteritems():

    for processname, val in process.iteritems():
        if processname=='QCD': continue
        
        tree = val['file'].Get('tree_mutau')

        print        
        print '[INFO] : Process = ', processname
        
        var_tuples = []

        for varname, var in wvardir.iteritems():        
            hname = 'whist_' + catname + '_' + processname + '_' + varname

            hist_register = TH1F(hname, hname, var['nbins'], var['min'], var['max'])
            hist_register.GetXaxis().SetTitle(var['label'])
            hist_register.Sumw2()
            hist_register.GetXaxis().SetLabelSize(0)
            
            if val['name'] in ['data_obs']:
                hist_register.SetMarkerStyle(20)
                hist_register.SetMarkerSize(0.5)


            whists[hname] = hist_register

            var_tuples.append('{var} >> {hist}'.format(var=var['drawname'], hist=hname))

        weight = 'weight*' + str(val['cross-section']*config.lumi*1000/val['ntot'])  + '*(gen_match_2==5 ? 0.9 : 1)'

        if val['name'] in ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4',
                           'ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4',
                           'ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4']:            
            weight = 'weight*' + config.dy_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

        elif val['name'] in ['W', 'W1', 'W2', 'W3', 'W4']:
            weight = 'weight*' + config.w_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

        elif val['name'] in ['data_obs']:        
            weight = '1'


        cutstr = cat['sel'] + ' && ' + val['additional_cut']
        cut = '({c}) * {we}'.format(c=cutstr, we=weight)
        tree.MultiDraw(var_tuples, cut)


print 'Estimating QCD using SS region'

for varname, var in wvardir.iteritems():        

    h_QCD = None

    for processname, val in process.iteritems():
        if processname=='QCD': continue

        hname = 'whist_w_ss_' + processname + '_' + varname
            
        addfactor = -1
        if val['name'] == 'data_obs':
            addfactor = 1.
            
        if h_QCD == None:
            h_QCD = copy.deepcopy(whists[hname])
        else:
            h_QCD.Add(whists[hname], addfactor)


    h_QCD_ss = copy.deepcopy(h_QCD)
    h_QCD_os = copy.deepcopy(h_QCD)
    h_QCD_os.Scale(1.06)

    osname = 'whist_w_os_QCD_' + varname
    ssname = 'whist_w_ss_QCD_' + varname

    h_QCD_os.SetName(osname)
    h_QCD_ss.SetName(ssname)
    
    whists[osname] = h_QCD_os
    whists[ssname] = h_QCD_ss


SFforW = 1.

if normalizeWusinghighMT:

    data = 0
    totalmc = 0
    wyield = 0

    for processname, val in process.iteritems():
        hname = 'whist_w_os_' + processname + '_pfmt_1'
        bin_min = whists[hname].GetXaxis().FindBin(WsidebandMTvalue)
        bin_max = whists[hname].GetXaxis().FindBin(whists[hname].GetXaxis().GetXmax())

        pname = val['name']

        if pname in ['W', 'W1', 'W2', 'W3', 'W4']:
            wyield += whists[hname].Integral(bin_min, bin_max)
        elif pname == 'data_obs':
            data = whists[hname].Integral(bin_min, bin_max)
#            totalmc += hists['hist_signal_os_QCD_pfmt_1'].Integral(bin_min, bin_max)
        else:
            totalmc += whists[hname].Integral(bin_min, bin_max)



    if wyield!=0:
        SFforW = (data - totalmc)/wyield
        print '*'*80
        print '* W norm. : data ', data, ', other MC : ', totalmc, ', Wyield : ', wyield, ', SF => ', SFforW
        print '*'*80




print 'SF = ', SFforW, 'This is to be compared to 0.962981606496'


###########################################################


vardir = {
    'm_vis':{'drawname':'m_vis', 'nbins':30, 'min':0, 'max':120, 'label':'visible mass (GeV)'},
    'm_sv':{'drawname':'m_sv', 'nbins':35, 'min':0, 'max':350, 'label':'SVfit mass (GeV)'},
    'pfmt_1':{'drawname':'pfmt_1', 'nbins':40, 'min':0, 'max':200, 'label':'PF MET Transverse mass (GeV)'},
    'mt_1':{'drawname':'mt_1', 'nbins':40, 'min':0, 'max':200, 'label':'MVA MET Transverse mass (GeV)'},
    'm_2':{'drawname':'m_2', 'nbins':30, 'min':0, 'max':3, 'label':'Tau mass (GeV)'},
    'pt_1':{'drawname':'pt_1', 'nbins':30, 'min':0, 'max':150, 'label':'muon pT (GeV)'},
    'pt_2':{'drawname':'pt_2', 'nbins':30, 'min':0, 'max':150, 'label':'tau pT (GeV)'},
    'met':{'drawname':'met', 'nbins':30, 'min':0, 'max':200, 'label':'missing E_{T} (GeV)'},
    'dR_ll':{'drawname':'dR_ll', 'nbins':30, 'min':0, 'max':math.pi, 'label':'#Delta R (l, #tau)'},
    'eta_1':{'drawname':'eta_1', 'nbins':30, 'min':-2.5, 'max':2.5, 'label':'muon eta'},
    'eta_2':{'drawname':'eta_2', 'nbins':30, 'min':-2.5, 'max':2.5, 'label':'tau eta'},
    'njets':{'drawname':'njets', 'nbins':10, 'min':0, 'max':10, 'label':'# of jets (pT > 30)'},
    'nfjets':{'drawname':'nfjets', 'nbins':10, 'min':0, 'max':10, 'label':'# of forward jets (pT > 30)'},
    'byIsolationMVA3oldDMwLTraw_2':{'drawname':'byIsolationMVA3oldDMwLTraw_2', 'nbins':30, 'min':-1, 'max':1, 'label':'Tau MVA isolation'},
    'byCombinedIsolationDeltaBetaCorrRaw3Hits_2':{'drawname':'byCombinedIsolationDeltaBetaCorrRaw3Hits_2', 'nbins':30, 'min':0, 'max':200, 'label':'Tau dbeta isolation'},
    'jpt_1':{'drawname':'jpt_1', 'nbins':30, 'min':0, 'max':500, 'label':'leading jet pT (GeV)'},
    'jeta_1':{'drawname':'jeta_1', 'nbins':30, 'min':-5, 'max':5, 'label':'leading jet eta'},
    'jpt_2':{'drawname':'jpt_2', 'nbins':30, 'min':0, 'max':500, 'label':'sub leading jet pT (GeV)'},
    'jeta_2':{'drawname':'jeta_2', 'nbins':30, 'min':-5, 'max':5, 'label':'sub leading jet eta'},
    'gen_match_2':{'drawname':'gen_match_2', 'nbins':7, 'min':0, 'max':7, 'label':'gen_match_2'},
    }

base_cat1 = baseselection + '&& ncbtag > 0 && ncjets == 1 && nfjets  > 0 && met < 60 && pfmt_1 < 60'
base_cat2 = baseselection + '&& ncbtag > 0 && ncjets  > 1 && nfjets == 0 && dphi_ll_bj > 2 && met < 60 && pfmt_1 < 60'

categories = collections.OrderedDict()
categories['signal_cat1_os'] = {'sel':base_cat1 + '&& q_1*q_2<0'}
categories['signal_cat1_ss'] = {'sel':categories['signal_cat1_os']['sel'].replace('q_1*q_2<0', 'q_1*q_2>0')}
categories['signal_cat2_os'] = {'sel':base_cat2 + '&& q_1*q_2<0'}
categories['signal_cat2_ss'] = {'sel':categories['signal_cat2_os']['sel'].replace('q_1*q_2<0', 'q_1*q_2>0')}


hists = {}

for catname, cat in categories.iteritems():

    print '-'*80
    print '[INFO]', catname, ':', cat['sel']
    print '-'*80

    for processname, val in process.iteritems():
        if processname=='QCD': continue
        
        tree = val['file'].Get('tree_mutau')

        print        
        print '[INFO] Process = ', processname
        
        var_tuples = []

        for varname, var in vardir.iteritems():        
            hname = 'hist_' + catname + '_' + processname + '_' + varname

            hist_register = TH1F(hname, hname, var['nbins'], var['min'], var['max'])
            hist_register.GetXaxis().SetTitle(var['label'])
            hist_register.Sumw2()
            hist_register.GetXaxis().SetLabelSize(0)
            
            if val['name'] in ['data_obs']:
                hist_register.SetMarkerStyle(20)
                hist_register.SetMarkerSize(0.5)


            hists[hname] = hist_register

            var_tuples.append('{var} >> {hist}'.format(var=var['drawname'], hist=hname))

        weight = 'weight*' + str(val['cross-section']*config.lumi*1000/val['ntot'])  + '*(gen_match_2==5 ? 0.9 : 1)'

        if val['name'] in ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4',
                           'ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4',
                           'ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4']:            
            weight = 'weight*' + config.dy_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

        elif val['name'] in ['W', 'W1', 'W2', 'W3', 'W4']:
            weight = 'weight*' + config.w_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

        elif val['name'] in ['data_obs']:        
            weight = '1'

        cutstr = cat['sel'] + ' && ' + val['additional_cut']
        print '[INFO] cut = ', cutstr, 'weight = ', weight

        cut = '({c}) * {we}'.format(c=cutstr, we=weight)

        tree.MultiDraw(var_tuples, cut)



print 'Estimating QCD using SS region'

for catname, cat in categories.iteritems():

    if catname.find('ss')==-1: continue

    for varname, var in vardir.iteritems():        

        h_QCD = None

        for processname, val in process.iteritems():
            if processname=='QCD': continue

            hname = 'hist_' + catname + '_' + processname + '_' + varname
            
            addfactor = -1
            if val['name'] == 'data_obs':
                addfactor = 1.
            
            if h_QCD == None:
                h_QCD = copy.deepcopy(hists[hname])
            else:
                h_QCD.Add(hists[hname], addfactor)

            
        h_QCD_ss = copy.deepcopy(h_QCD)
        h_QCD_os = copy.deepcopy(h_QCD)
        h_QCD_os.Scale(1.06)

        osname = 'hist_' + catname.replace('ss','os') + '_QCD_' + varname
        ssname = 'hist_' + catname + '_QCD_' + varname

        h_QCD_os.SetName(osname)
        h_QCD_ss.SetName(ssname)
    
        hists[osname] = h_QCD_os
        hists[ssname] = h_QCD_ss





for catname, cat in categories.iteritems():

    ensureDir('fig_' + catname)

    for varname, var in vardir.iteritems():        

        stackname = 'stackhist_' + catname + '_' + varname
        hist = DataMCPlot(stackname)
        hist.legendBorders = 0.55, 0.55, 0.88, 0.88

        for processname, val in process.iteritems():

            hname = 'hist_' + catname + '_' + processname + '_' + varname
            pname = val['name']

            if pname in ['W', 'W1', 'W2', 'W3', 'W4']:
                hists[hname].Scale(SFforW)


            hist.AddHistogram(pname, hists[hname], val['order'])

            if pname in ['data_obs']:
                hist.Hist(pname).stack = False


        hist.Group('VV', ['WZ', 'ZZ', 'WWTo1L1Nu2Q', 'ST_t_top', 'ST_t_antitop', 'ST_tw_top', 'ST_tw_antitop'])
        hist.Group('ZTT', ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4'])
        hist.Group('ZL', ['ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4'])
        hist.Group('ZJ', ['ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4'])
        hist.Group('W', ['W', 'W1', 'W2', 'W3', 'W4'])


        if WriteDataCard == True and varname=='m_sv' and catname in ['signal_cat1_os', 'signal_cat2_os']:
            print hist
            hist.WriteDataCard(filename='datacard_{}_{}.root'.format(varname, catname), dir='mt_' + catname, mode='recreate')
            
        # put ttbar combine here, as in the datacard level, we want to have it in split
        # while for the drawing, we want to have it combined

        hist.Group('TT', ['TTT', 'TTJ'])
        comparisonPlots(hist, 'fig_' + catname + '/' + stackname + '.pdf')
