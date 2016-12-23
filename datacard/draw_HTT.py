import os, math, copy, sys, collections
from ROOT import gStyle, TCanvas, TLegend, TH1F
from officialStyle import officialStyle
from config import *
from DataMCPlot import *
import MultiDraw


lumi=12.9
#basedir = '/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/'
basedir = '/mnt/t3nfs01/data01/shome/ytakahas/work/TauTau/SFrameAnalysis/AnalysisOutput_SM/'

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

category = None
argList=sys.argv

if len(argList) != 2:
    print 'specify category !'
    sys.exit(1)
else:
    category = argList[1]


print '-'*80
print 'category = ', category
print '-'*80


config = config(basedir, lumi)

process = config.process
W_highMT = config.W_highMT
W_lowMT = config.W_lowMT
catdir = config.catdir

if not catdir.has_key(category):
    print 'choose category among [0jet_low, 0jet_hight, 1jet_low, 1jet_high, vbf_low, vbf_high]'
    sys.exit(1)

var_pfmt_1 = {
    'pfmt_1':{'drawname':'pfmt_1', 'nbins':40, 'min':0, 'max':200, 'label':'PF MET Transverse mass (GeV)'},
    }


vardir = {
    'm_vis':{'drawname':'m_vis', 'nbins':30, 'min':0, 'max':120, 'label':'visible mass (GeV)'},
    'm_sv':{'drawname':'m_sv', 'nbins':26, 'min':0, 'max':350, 'label':'SVfit mass (GeV)'},
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

vardir.update(var_pfmt_1)

###############################################################



##########################################################


catname = 'highMT_ss'
sel_highMT_ss = catdir[category]['sel'].replace('pfmt_1 < ' + str(W_lowMT), 'pfmt_1 > ' + str(W_highMT)).replace('q_1*q_2 < 0', 'q_1*q_2 > 0')

# use PF MET, remove QCD when making histograms
config.createHistograms(catname, sel_highMT_ss, ['QCD'], var_pfmt_1)

# estimate QCD, using pfmt_1 variable
config.extractQCD(catname, ['QCD'], 'pfmt_1', catdir[category]['os_ss_ratio'])


##########################################################

catname = 'highMT_os'
sel_highMT_os = catdir[category]['sel'].replace('pfmt_1 < ' + str(W_lowMT), 'pfmt_1 > ' + str(W_highMT))

config.createHistograms(catname, sel_highMT_os, ['QCD'], var_pfmt_1)

h_W_dd = None
h_W_mc = None

for processname, val in process.iteritems():
        
    hname = 'hist_' + catname + '_' + processname + '_pfmt_1'

    if processname in ['W', 'W1', 'W2', 'W3', 'W4']:
        if h_W_mc == None:
            h_W_mc = copy.deepcopy(config.hists[hname])
        else:
            h_W_mc.Add(config.hists[hname])
    else:
        addfactor = -1
        if val['name'] == 'data_obs':
            addfactor = 1.
            
        if h_W_dd == None:
            h_W_dd = copy.deepcopy(config.hists[hname])
            h_W_dd.Scale(addfactor)
        else:
            h_W_dd.Add(config.hists[hname], addfactor)

print 'W_yield, measured in data = ', returnIntegral(h_W_dd)
print 'W_yield, measured in mc = ', returnIntegral(h_W_mc)

sf_W = 1.
if returnIntegral(h_W_mc)!=0:
    sf_W = returnIntegral(h_W_dd)/returnIntegral(h_W_mc)

print 'W_yield SF = ', sf_W

###################################################################

catname = 'highMT_os_relaxed'

# TODO : change here !!! 

sel_highMT_os_relaxed = catdir[category]['sel'].replace('pfmt_1 < ' + str(W_lowMT), 'pfmt_1 > ' + str(W_highMT)).replace('iso_1 < 0.15', 'iso_1 > 0.15 && iso_1 < 0.3')

removeList = []
for processname, val in process.iteritems():
    if not processname in ['W', 'W1', 'W2', 'W3', 'W4', 'data_obs']:
        removeList.append(processname)
        
config.createHistograms(catname, sel_highMT_os_relaxed, removeList, var_pfmt_1)


W_highMT_os_yield = 0.

for processname, val in process.iteritems():

    if not processname in ['W', 'W1', 'W2', 'W3', 'W4']: continue
        
    hname = 'hist_' + catname + '_' + processname + '_pfmt_1'
    W_highMT_os_yield += returnIntegral(config.hists[hname])

###################################################################

catname = 'lowMT_os_relaxed'
sel_lowMT_os_relaxed = catdir[category]['sel'].replace('iso_1 < 0.15', 'iso_1 > 0.15 && iso_1 < 0.3')

config.createHistograms(catname, sel_lowMT_os_relaxed, ['QCD'], vardir)

W_lowMT_os_yield = 0.

for processname in ['W', 'W1', 'W2', 'W3', 'W4']:
    hname = 'hist_' + catname + '_' + processname + '_pfmt_1'
    W_lowMT_os_yield += returnIntegral(config.hists[hname])


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

# use PF MET, remove QCD when making histograms
config.createHistograms(catname, sel_lowMT_ss_relaxed, ['QCD'], vardir)

# estimate QCD, for all the variables

for varname, var in vardir.iteritems():        
    config.extractQCD(catname, ['QCD'], var['drawname'], catdir[category]['os_ss_ratio'])


#####################################################################
# QCD yield estimation

catname = 'lowMT_ss'
sel_lowMT_ss = catdir[category]['sel'].replace('q_1*q_2 < 0', 'q_1*q_2 > 0')

config.createHistograms(catname, sel_lowMT_ss, ['QCD'], vardir, sf_W)

for varname, var in vardir.iteritems():        
    config.extractQCD(catname, ['QCD'], var['drawname'], catdir[category]['os_ss_ratio'])



# derive shapes for QCD, W, using relaxed selection


norm_QCD = returnIntegral(config.hists['hist_lowMT_os_QCD_pfmt_1'])
norm_W = W_ext_sf*returnIntegral(h_W_dd)

print 'norm_QCD = ', norm_QCD
print 'norm_W = ', norm_W

# signal region 

catname = 'lowMT_os'
sel_lowMT_os = catdir[category]['sel']

config.createHistograms(catname, sel_lowMT_os, ['QCD'], vardir)

signal_W = 0.
for processname in ['W', 'W1', 'W2', 'W3', 'W4']:
    hname = 'hist_' + catname + '_relaxed_' + processname + '_pfmt_1'
    signal_W += returnIntegral(config.hists[hname])
    
signal_QCD = returnIntegral(config.hists['hist_' + catname + '_relaxed_QCD_pfmt_1'])

print 'total W yield in relaxed region = ', signal_W
print 'total QCD yield in relaxed region = ', signal_QCD
    
#############################################################

print '-'*80
print 'Write to the datacard !'
print '-'*80


ensureDir('fig_' + catname)

for varname, var in vardir.iteritems():        

    stackname = 'stackhist_' + catname + '_' + varname
    hist = DataMCPlot(stackname)
    hist.legendBorders = 0.55, 0.55, 0.88, 0.88

    for processname, val in process.iteritems():

        pname = val['name']

        # if W/QCD, take shape from relaxed region !!

        if category in ['1jet_high', 'vbf_low', 'vbf_high']:

            if pname in ['W', 'W1', 'W2', 'W3', 'W4']:
                hname = 'hist_' + catname + '_relaxed_' + processname + '_' + varname

                if signal_W!=0:
                    config.hists[hname].Scale(norm_W/signal_W)

                hist.AddHistogram(pname, config.hists[hname], val['order'])                
            elif pname == 'QCD':
                hname = 'hist_' + catname + '_relaxed_' + processname + '_' + varname

                if signal_QCD!=0:
                    config.hists[hname].Scale(norm_QCD/signal_QCD)
                hist.AddHistogram(pname, config.hists[hname], val['order'])                
            else:
                hname = 'hist_' + catname + '_' + processname + '_' + varname
                hist.AddHistogram(pname, config.hists[hname], val['order'])                

        else:
            hname = 'hist_' + catname + '_' + processname + '_' + varname
            hist.AddHistogram(pname, config.hists[hname], val['order'])                

#        print 'DBG : ', hname, returnIntegral(config.hists[hname])
        
        if pname in ['data_obs']:
            hist.Hist(pname).stack = False

    hist.Group('VV', ['WZ', 'ZZ', 'WWTo1L1Nu2Q', 'ST_t_top', 'ST_t_antitop', 'ST_tw_top', 'ST_tw_antitop'])
    hist.Group('ZTT', ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4'])
    hist.Group('ZL', ['ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4'])
    hist.Group('ZJ', ['ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4'])
    hist.Group('W', ['W', 'W1', 'W2', 'W3', 'W4'])
    
    config.comparisonPlots(hist, 'fig_' + catname + '/' + stackname + '.pdf')


    if varname=='m_sv' and catname=='lowMT_os':
        print hist
        hist.WriteDataCard(filename='datacard_{}_{}.root'.format(varname, category), dir='mt_' + catname, mode='recreate')

        # put ttbar combine here, as in the datacard level, we want to have it in split
        # while for the drawing, we want to have it combined
            
    hist.Group('TT', ['TTT', 'TTJ'])
    config.comparisonPlots(hist, 'fig_' + catname + '/' + stackname + '.pdf')
