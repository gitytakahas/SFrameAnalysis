import os, numpy, math, copy, math, sys, collections
#from array import array
from ROOT import gStyle, TCanvas, TLegend, TH1F
from officialStyle import officialStyle
from DisplayManager import DisplayManager
from config import config
from DataMCPlot import *
import MultiDraw


lumi=12.9
#basedir = '/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/'
basedir = '/mnt/t3nfs01/data01/shome/ytakahas/work/TauTau/SFrameAnalysis/AnalysisOutput_SM/'

W_highMT = 80.
W_lowMT = 50.
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

def returnWeight(val, config):
    weight = 'weight*' + str(val['cross-section']*config.lumi*1000/val['ntot'])  + '*(gen_match_2==5 ? 0.9 : 1)'

    if val['name'] in ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4',
                       'ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4',
                       'ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4']:            
        weight = 'weight*' + config.dy_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

    elif val['name'] in ['W', 'W1', 'W2', 'W3', 'W4']:
        weight = 'weight*' + config.w_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

    elif val['name'] in ['data_obs']:        
        weight = '1'

    return weight

baseline = 'dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1 && iso_1 < 0.15 && iso_2 == 1 && channel==1 && q_1*q_2 < 0'

sel_0jet_low = baseline + ' && ' + 'pt_2 > 20 && pt_2 < 50 && njets==0 && pfmt_1 < ' + str(W_lowMT)
sel_0jet_high = baseline + ' && ' + 'pt_2 > 50 && njets==0 && pfmt_1 < ' + str(W_lowMT)
sel_1jet_low = baseline + ' && ' + '(njets==1 || (njets==2 && vbf_mjj < 500)) && ((pt_2 > 30 && pt_2 < 40) || (pt_2 > 40 && pt_tt < 140)) && pfmt_1 < ' + str(W_lowMT)
sel_1jet_high = baseline + ' && ' + '(njets==1 || (njets==2 && vbf_mjj < 500)) && pt_2 > 40 && pt_tt > 140 && pfmt_1 < ' + str(W_lowMT)
sel_vbf_low = baseline + ' && ' + 'njets==2 && pt_2 > 20 && vbf_mjj > 500 && (vbf_mjj < 800 || pt_tt < 100) && pfmt_1 < ' + str(W_lowMT)
sel_vbf_high = baseline + ' && ' + 'njets==2 && pt_2 > 20 && vbf_mjj > 800 && pt_tt > 100 && pfmt_1 < ' + str(W_lowMT)


catdir = {
    '0jet_low':{'name':'0jet_low', 'sel':sel_0jet_low, 'os_ss_ratio':1.},    
    '0jet_high':{'name':'0jet_high', 'sel':sel_0jet_high, 'os_ss_ratio':1.},
    '1jet_low':{'name':'1jet_low', 'sel':sel_1jet_low, 'os_ss_ratio':1.15},
    '1jet_high':{'name':'1jet_hight', 'sel':sel_1jet_high, 'os_ss_ratio':1.15},
    'vbf_low':{'name':'vbf_low', 'sel':sel_vbf_low, 'os_ss_ratio':1.2},
    'vbf_high':{'name':'vbf_high', 'sel':sel_vbf_high, 'os_ss_ratio':1.2}
}



var_pfmt_1 = {
    'drawname':'pfmt_1', 'nbins':40, 'min':0, 'max':200, 'label':'PF MET Transverse mass (GeV)'
    }


vardir = {
    'm_vis':{'drawname':'m_vis', 'nbins':30, 'min':0, 'max':120, 'label':'visible mass (GeV)'},
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


category = None
argList=sys.argv

if len(argList) != 2:
    print 'specify category !'
    sys.exit(1)
else:
    category = argList[1]

    if not catdir.has_key(category):
        print 'choose category among [0jet_low, 0jet_hight, 1jet_low, 1jet_high, vbf_low, vbf_high]'
        sys.exit(1)


print '-'*80
print 'category = ', category
print '-'*80

config = config(basedir, lumi)
process = config.process

hists = {}



##########################################################
##########################################################


catname = 'highMT_ss'
sel_highMT_ss = catdir[category]['sel'].replace('pfmt_1 < ' + str(W_lowMT), 'pfmt_1 > ' + str(W_highMT)).replace('q_1*q_2 < 0', 'q_1*q_2 > 0')

print '-'*80
print catname
print sel_highMT_ss
print '-'*80

for processname, val in process.iteritems():
    if processname=='QCD': continue
        
    tree = val['file'].Get('tree_mutau')

    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']
    hist_register = TH1F(hname, hname, var_pfmt_1['nbins'], var_pfmt_1['min'], var_pfmt_1['max'])
    hist_register.GetXaxis().SetTitle(var_pfmt_1['label'])
    hist_register.GetXaxis().SetLabelSize(0)
    hist_register.Sumw2()
    
    if val['name'] in ['data_obs']:
        hist_register.SetMarkerStyle(20)
        hist_register.SetMarkerSize(0.5)
            
    hists[hname] = hist_register

    var_tuples = ['{var} >> {hist}'.format(var=var_pfmt_1['drawname'], hist=hname)]

    weight = returnWeight(val, config)

    cutstr = sel_highMT_ss + ' && ' + val['additional_cut']
    cut = '({c}) * {we}'.format(c=cutstr, we=weight)
    tree.MultiDraw(var_tuples, cut)


h_QCD = None

for processname, val in process.iteritems():
    if processname=='QCD': continue
        
    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']
        
    addfactor = -1
    if val['name'] == 'data_obs':
        addfactor = 1.
            
    if h_QCD == None:
        h_QCD = copy.deepcopy(hists[hname])
    else:
        h_QCD.Add(hists[hname], addfactor)

            
h_QCD_os = copy.deepcopy(h_QCD)
h_QCD_os.Scale(catdir[category]['os_ss_ratio'])

osname = 'hist_' + catname.replace('ss','os') + '_QCD_' + var_pfmt_1['drawname']
h_QCD_os.SetName(osname)

hists[osname] = h_QCD_os


print 'Estimated QCD yield at highMT os = ', h_QCD_os.GetSumOfWeights()


##########################################################
##########################################################

catname = 'highMT_os'
sel_highMT_os = catdir[category]['sel'].replace('pfmt_1 < ' + str(W_lowMT), 'pfmt_1 > ' + str(W_highMT))

print '-'*80
print catname
print sel_highMT_os
print '-'*80

for processname, val in process.iteritems():

    if processname == 'QCD': continue
        
    tree = val['file'].Get('tree_mutau')

    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']
        
    hist_register = TH1F(hname, hname, var_pfmt_1['nbins'], var_pfmt_1['min'], var_pfmt_1['max'])
    hist_register.GetXaxis().SetTitle(var_pfmt_1['label'])
    hist_register.GetXaxis().SetLabelSize(0)
    hist_register.Sumw2()
    
    if val['name'] in ['data_obs']:
        hist_register.SetMarkerStyle(20)
        hist_register.SetMarkerSize(0.5)
        
    hists[hname] = hist_register

    var_tuples = ['{var} >> {hist}'.format(var=var_pfmt_1['drawname'], hist=hname)]

    weight = returnWeight(val, config)

    cutstr = sel_highMT_os + ' && ' + val['additional_cut']
    cut = '({c}) * {we}'.format(c=cutstr, we=weight)
    tree.MultiDraw(var_tuples, cut)


h_W_dd = None
h_W_mc = None

for processname, val in process.iteritems():
        
    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']

    if processname in ['W', 'W1', 'W2', 'W3', 'W4']:
        if h_W_mc == None:
            h_W_mc = copy.deepcopy(hists[hname])
        else:
            h_W_mc.Add(hists[hname])
    else:

        addfactor = -1
        if val['name'] == 'data_obs':
            addfactor = 1.
            
        if h_W_dd == None:
            h_W_dd = copy.deepcopy(hists[hname])
        else:
            h_W_dd.Add(hists[hname], addfactor)

print 'W_yield, measured in data = ', h_W_dd.GetSumOfWeights()
print 'W_yield, measured in mc = ', h_W_mc.GetSumOfWeights()

sf_W = 1.
if h_W_mc.GetSumOfWeights() != 0:
    sf_W = h_W_dd.GetSumOfWeights()/h_W_mc.GetSumOfWeights() 

print 'W_yield SF = ', sf_W


###################################################################
###################################################################

catname = 'highMT_os_relaxed'
sel_highMT_os_relaxed = catdir[category]['sel'].replace('pfmt_1 < ' + str(W_lowMT), 'pfmt_1 > ' + str(W_highMT)).replace('iso_1 < 0.15', 'iso_1 > 0.15 && iso_1 < 0.3')

print '-'*80
print catname
print sel_highMT_os_relaxed
print '-'*80

W_highMT_os_yield = 0.

for processname, val in process.iteritems():

    if not processname in ['W', 'W1', 'W2', 'W3', 'W4']: continue
        
    tree = val['file'].Get('tree_mutau')

    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']

    hist_register = TH1F(hname, hname, var_pfmt_1['nbins'], var_pfmt_1['min'], var_pfmt_1['max'])

    var_tuples = ['{var} >> {hist}'.format(var=var_pfmt_1['drawname'], hist=hname)]

    weight = returnWeight(val, config)

    cutstr = sel_highMT_os_relaxed + ' && ' + val['additional_cut']

    cut = '({c}) * {we}'.format(c=cutstr, we=weight)

    tree.MultiDraw(var_tuples, cut)

    W_highMT_os_yield += hist_register.GetSumOfWeights()





catname = 'lowMT_os_relaxed'
sel_lowMT_os_relaxed = catdir[category]['sel'].replace('iso_1 < 0.15', 'iso_1 > 0.15 && iso_1 < 0.3')

print '-'*80
print catname
print sel_lowMT_os_relaxed
print '-'*80

for processname, val in process.iteritems():

    if processname == 'QCD': continue

    tree = val['file'].Get('tree_mutau')

    var_tuples = []
    
    for varname, var in vardir.iteritems():
        hname = 'hist_' + catname + '_' + processname + '_' + var['drawname']
        
        hist_register = TH1F(hname, hname, var['nbins'], var['min'], var['max'])
        hist_register.GetXaxis().SetTitle(var['label'])
        hist_register.GetXaxis().SetLabelSize(0)
        hist_register.Sumw2()
    
        if val['name'] in ['data_obs']:
            hist_register.SetMarkerStyle(20)
            hist_register.SetMarkerSize(0.5)
        
        hists[hname] = hist_register

        var_tuples.append('{var} >> {hist}'.format(var=var['drawname'], hist=hname))

    weight = returnWeight(val, config)

    cutstr = sel_lowMT_os_relaxed + ' && ' + val['additional_cut']
    cut = '({c}) * {we}'.format(c=cutstr, we=weight)
    tree.MultiDraw(var_tuples, cut)


W_lowMT_os_yield = 0.

for processname in ['W', 'W1', 'W2', 'W3', 'W4']:
    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']
    W_lowMT_os_yield += hists[hname].GetSumOfWeights()



print 'W_yield, high MT = ', W_highMT_os_yield
print 'W_yield, low MT = ', W_lowMT_os_yield

W_ext_sf = 1.
if W_highMT_os_yield!=0:
    W_ext_sf = W_lowMT_os_yield/W_highMT_os_yield

print 'W extrapolation SF = ', W_ext_sf


############################################################################
# derive QCD shapes, too


catname = 'lowMT_ss_relaxed'
sel_lowMT_ss_relaxed = catdir[category]['sel'].replace('iso_1 < 0.15', 'iso_1 > 0.15 && iso_1 < 0.3').replace('q_1*q_2 < 0', 'q_1*q_2 > 0')

print '-'*80
print catname
print sel_lowMT_ss_relaxed
print '-'*80

for processname, val in process.iteritems():

    if processname == 'QCD': continue

    tree = val['file'].Get('tree_mutau')

    var_tuples = []
    
    for varname, var in vardir.iteritems():
        hname = 'hist_' + catname + '_' + processname + '_' + var['drawname']
        
        hist_register = TH1F(hname, hname, var['nbins'], var['min'], var['max'])
        hist_register.GetXaxis().SetTitle(var['label'])
        hist_register.GetXaxis().SetLabelSize(0)
        hist_register.Sumw2()
    
        if val['name'] in ['data_obs']:
            hist_register.SetMarkerStyle(20)
            hist_register.SetMarkerSize(0.5)
        
        hists[hname] = hist_register

        var_tuples.append('{var} >> {hist}'.format(var=var['drawname'], hist=hname))

    weight = returnWeight(val, config)

    cutstr = sel_lowMT_ss_relaxed + ' && ' + val['additional_cut']
    cut = '({c}) * {we}'.format(c=cutstr, we=weight)
    tree.MultiDraw(var_tuples, cut)



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

            
    h_QCD_os = copy.deepcopy(h_QCD)
    h_QCD_os.Scale(catdir[category]['os_ss_ratio'])
    
    osname = 'hist_' + catname.replace('ss','os') + '_QCD_' + varname
    h_QCD_os.SetName(osname)    
    hists[osname] = h_QCD_os
    


#####################################################################
# QCD yield estimation

catname = 'lowMT_ss'
sel_lowMT_ss = catdir[category]['sel'].replace('q_1*q_2 < 0', 'q_1*q_2 > 0')

print '-'*80
print 'Estimate QCD yield using low MT same-sign region'
print 'catname = ', catname
print 'selection = ', sel_lowMT_ss
print '-'*80


for processname, val in process.iteritems():
    if processname=='QCD': continue
        
    tree = val['file'].Get('tree_mutau')

    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']
    hist_register = TH1F(hname, hname, var_pfmt_1['nbins'], var_pfmt_1['min'], var_pfmt_1['max'])
    hist_register.GetXaxis().SetTitle(var_pfmt_1['label'])
    hist_register.GetXaxis().SetLabelSize(0)
    hist_register.Sumw2()
    
    if val['name'] in ['data_obs']:
        hist_register.SetMarkerStyle(20)
        hist_register.SetMarkerSize(0.5)
            
    hists[hname] = hist_register

    var_tuples = ['{var} >> {hist}'.format(var=var_pfmt_1['drawname'], hist=hname)]

    weight = returnWeight(val, config)

    cutstr = sel_lowMT_ss + ' && ' + val['additional_cut']
    cut = '({c}) * {we}'.format(c=cutstr, we=weight)
    tree.MultiDraw(var_tuples, cut)


h_low_QCD = None

for processname, val in process.iteritems():
    if processname=='QCD': continue
        
    hname = 'hist_' + catname + '_' + processname + '_' + var_pfmt_1['drawname']
        
    addfactor = -1
    if val['name'] == 'data_obs':
        addfactor = 1.
            
    if h_low_QCD == None:
        h_low_QCD = copy.deepcopy(hists[hname])
    else:
        h_low_QCD.Add(hists[hname], addfactor)

            
h_low_QCD_os = copy.deepcopy(h_low_QCD)
h_low_QCD_os.Scale(catdir[category]['os_ss_ratio'])

osname = 'hist_' + catname.replace('ss','os') + '_QCD_' + var_pfmt_1['drawname']

h_low_QCD_os.SetName(osname)

hists[osname] = h_low_QCD_os


print 'OS/SS ratio = ', catdir[category]['os_ss_ratio']
print 'Estimated QCD at lowMT os = ', h_low_QCD_os.GetSumOfWeights()


# derive shapes for QCD, W, using relaxed selection


norm_QCD = h_low_QCD_os.GetSumOfWeights()
norm_W = W_ext_sf*h_W_dd.GetSumOfWeights()

print 'norm_QCD = ', norm_QCD
print 'norm_W = ', norm_W

catname = 'lowMT_os'
sel_lowMT_os = catdir[category]['sel']

for processname, val in process.iteritems():

    if processname == 'QCD': continue

    tree = val['file'].Get('tree_mutau')

    var_tuples = []
    
    for varname, var in vardir.iteritems():
        hname = 'hist_' + catname + '_' + processname + '_' + var['drawname']
        
        hist_register = TH1F(hname, hname, var['nbins'], var['min'], var['max'])
        hist_register.GetXaxis().SetTitle(var['label'])
        hist_register.GetXaxis().SetLabelSize(0)
        hist_register.Sumw2()
    
        if val['name'] in ['data_obs']:
            hist_register.SetMarkerStyle(20)
            hist_register.SetMarkerSize(0.5)
        
        hists[hname] = hist_register

        var_tuples.append('{var} >> {hist}'.format(var=var['drawname'], hist=hname))

    weight = returnWeight(val, config)

    cutstr = sel_lowMT_os + ' && ' + val['additional_cut']
    cut = '({c}) * {we}'.format(c=cutstr, we=weight)
    tree.MultiDraw(var_tuples, cut)



print '-'*80
print 'Write to the datacard !'
print hists
print '-'*80


ensureDir('fig_' + catname)

for varname, var in vardir.iteritems():        

    stackname = 'stackhist_' + catname + '_' + varname
    hist = DataMCPlot(stackname)
    hist.legendBorders = 0.55, 0.55, 0.88, 0.88

    signal_W = 0.
    for processname in ['W', 'W1', 'W2', 'W3', 'W4']:
        hname = 'hist_' + catname + '_relaxed_' + processname + '_' + varname
        signal_W += hists[hname].GetSumOfWeights()
        
    print 'total W yield = ', signal_W
    
    for processname, val in process.iteritems():

        pname = val['name']

        # if W, then, take shape from relaxed region, and normalize it to norm_W
        if pname in ['W', 'W1', 'W2', 'W3', 'W4']:
            hname = 'hist_' + catname + '_relaxed_' + processname + '_' + varname

            if signal_W!=0:
                hists[hname].Scale(norm_W/signal_W)

            hist.AddHistogram(pname, hists[hname], val['order'])                
        elif pname == 'QCD':
            pass
            hname = 'hist_' + catname + '_relaxed_' + processname + '_' + varname

            if hists[hname].GetSumOfWeights()!=0:
                hists[hname].Scale(norm_QCD/hists[hname].GetSumOfWeights())
            hist.AddHistogram(pname, hists[hname], val['order'])                
        else:
            hname = 'hist_' + catname + '_' + processname + '_' + varname
            hist.AddHistogram(pname, hists[hname], val['order'])                


        
        if pname in ['data_obs']:
            hist.Hist(pname).stack = False

    hist.Group('VV', ['WZ', 'ZZ', 'WWTo1L1Nu2Q', 'ST_t_top', 'ST_t_antitop', 'ST_tw_top', 'ST_tw_antitop'])
    hist.Group('ZTT', ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4'])
    hist.Group('ZL', ['ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4'])
    hist.Group('ZJ', ['ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4'])
    hist.Group('W', ['W', 'W1', 'W2', 'W3', 'W4'])
    
    comparisonPlots(hist, 'fig_' + catname + '/' + stackname + '.pdf')


    if WriteDataCard == True and varname=='m_sv' and catname=='lowMT_os':
        print hist
        hist.WriteDataCard(filename='datacard_{}.root'.format(varname), dir='mt_' + catname, mode='recreate')

        # put ttbar combine here, as in the datacard level, we want to have it in split
        # while for the drawing, we want to have it combined
            
    hist.Group('TT', ['TTT', 'TTJ'])
    comparisonPlots(hist, 'fig_' + catname + '/' + stackname + '.pdf')
