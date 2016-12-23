import os, copy
from ROOT import TFile, TH1F
from DisplayManager import DisplayManager
from DataMCPlot import *

class config(object):

    def __init__(self, basedir, lumi, tes=None):
        
        self.basedir = basedir

        self.lumi = lumi

        self.hists = {}

        self.baseline = 'dilepton_veto == 0 && extraelec_veto == 0 && extramuon_veto == 0 && againstElectronVLooseMVA6_2 == 1 && againstMuonTight3_2 == 1 && iso_1 < 0.15 && iso_2 == 1 && channel==1 && q_1*q_2 < 0'
        
        self.W_lowMT = 50.
        self.W_highMT = 80.


        self.sel_0jet_low = self.baseline + ' && ' + 'pt_2 > 20 && pt_2 < 50 && njets==0 && pfmt_1 < ' + str(self.W_lowMT)
        self.sel_0jet_high = self.baseline + ' && ' + 'pt_2 > 50 && njets==0 && pfmt_1 < ' + str(self.W_lowMT)
        self.sel_1jet_low = self.baseline + ' && ' + '(njets==1 || (njets==2 && vbf_mjj < 500)) && ((pt_2 > 30 && pt_2 < 40) || (pt_2 > 40 && pt_tt < 140)) && pfmt_1 < ' + str(self.W_lowMT)
        self.sel_1jet_high = self.baseline + ' && ' + '(njets==1 || (njets==2 && vbf_mjj < 500)) && pt_2 > 40 && pt_tt > 140 && pfmt_1 < ' + str(self.W_lowMT)
        self.sel_vbf_low = self.baseline + ' && ' + 'njets==2 && pt_2 > 20 && vbf_mjj > 500 && (vbf_mjj < 800 || pt_tt < 100) && pfmt_1 < ' + str(self.W_lowMT)
        self.sel_vbf_high = self.baseline + ' && ' + 'njets==2 && pt_2 > 20 && vbf_mjj > 800 && pt_tt > 100 && pfmt_1 < ' + str(self.W_lowMT)


        self.catdir = {
            '0jet_low':{'name':'0jet_low', 'sel':self.sel_0jet_low, 'os_ss_ratio':1.},    
            '0jet_high':{'name':'0jet_high', 'sel':self.sel_0jet_high, 'os_ss_ratio':1.},
            '1jet_low':{'name':'1jet_low', 'sel':self.sel_1jet_low, 'os_ss_ratio':1.15},
            '1jet_high':{'name':'1jet_hight', 'sel':self.sel_1jet_high, 'os_ss_ratio':1.15},
            'vbf_low':{'name':'vbf_low', 'sel':self.sel_vbf_low, 'os_ss_ratio':1.2},
            'vbf_high':{'name':'vbf_high', 'sel':self.sel_vbf_high, 'os_ss_ratio':1.2}
            }




        self.process = {

            'TTT':{'name':'TTT', 
                   'file':self.basedir + '/TT/TauTauAnalysis.TT_TuneCUETP8M1_ICHEP.root',
                   'additional_cut':'gen_match_2==5',
                   'cross-section':831.76,
                   'isSignal':0, 
                   'order':1},

            'TTJ':{'name':'TTJ', 
                   'file':self.basedir + '/TT/TauTauAnalysis.TT_TuneCUETP8M1_ICHEP.root',
                   'additional_cut':'gen_match_2!=5',
                   'cross-section':831.76,
                   'isSignal':0, 
                   'order':1},

#            'ZTT10to50':{'name':'ZTT10to50', 
#                         'file':self.basedir + '/DY/TauTauAnalysis.DYJetsToLL_M-10to50_TuneCUETP8M1_ICHEP.root', 
#                         'additional_cut':'1',
#                         'cross-section':18610.0,
#                         'isSignal':0, 
#                         'order':2},

            'ZTT':{'name':'ZTT', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DYJetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2==5',
                   'isSignal':0, 
                   'order':3},

            'ZTT1':{'name':'ZTT1', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DY1JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2==5',
                   'isSignal':0, 
                   'order':3},

            'ZTT2':{'name':'ZTT2', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DY2JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2==5',
                   'isSignal':0, 
                   'order':3},

            'ZTT3':{'name':'ZTT3', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DY3JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2==5',
                   'isSignal':0, 
                   'order':3},

            'ZTT4':{'name':'ZTT4', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DY4JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2==5',
                   'isSignal':0, 
                   'order':3},

            'ZL':{'name':'ZL', 
                  'file':self.basedir + '/DY/TauTauAnalysis.DYJetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                  'cross-section':1.,
                  'additional_cut':'gen_match_2<5',
                  'isSignal':0, 
                  'order':3},

            'ZL1':{'name':'ZL1', 
                  'file':self.basedir + '/DY/TauTauAnalysis.DY1JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                  'cross-section':1.,
                  'additional_cut':'gen_match_2<5',
                  'isSignal':0, 
                  'order':3},

            'ZL2':{'name':'ZL2', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DY2JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2<5',
                   'isSignal':0, 
                   'order':3},

            'ZL3':{'name':'ZL3', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DY3JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2<5',
                   'isSignal':0, 
                   'order':3},

            'ZL4':{'name':'ZL4', 
                   'file':self.basedir + '/DY/TauTauAnalysis.DY4JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                   'cross-section':1.,
                   'additional_cut':'gen_match_2<5',
                   'isSignal':0, 
                   'order':3},


            'ZJ':{'name':'ZJ', 
                  'file':self.basedir + '/DY/TauTauAnalysis.DYJetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                  'additional_cut':'gen_match_2==6',
                  'cross-section':1.,
                  'isSignal':0, 
                  'order':3},

            'ZJ1':{'name':'ZJ1', 
                  'file':self.basedir + '/DY/TauTauAnalysis.DY1JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                  'additional_cut':'gen_match_2==6',
                  'cross-section':1.,
                  'isSignal':0, 
                  'order':3},

            'ZJ2':{'name':'ZJ2', 
                  'file':self.basedir + '/DY/TauTauAnalysis.DY2JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                  'additional_cut':'gen_match_2==6',
                  'cross-section':1.,
                  'isSignal':0, 
                  'order':3},

            'ZJ3':{'name':'ZJ3', 
                  'file':self.basedir + '/DY/TauTauAnalysis.DY3JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                  'additional_cut':'gen_match_2==6',
                  'cross-section':1.,
                  'isSignal':0, 
                  'order':3},

            'ZJ4':{'name':'ZJ4', 
                  'file':self.basedir + '/DY/TauTauAnalysis.DY4JetsToLL_M-50_TuneCUETP8M1_ICHEP.root',
                  'additional_cut':'gen_match_2==6',
                  'cross-section':1.,
                  'isSignal':0, 
                  'order':3},
            
            'WWTo1L1Nu2Q':{'name':'WWTo1L1Nu2Q', 
                           'file':self.basedir + '/WW/TauTauAnalysis.WWTo1L1Nu2Q_ICHEP.root',
                           'cross-section':1.212,
                           'additional_cut':'1',
                           'isSignal':0, 
                           'order':4},
            
            #    'WWTo4Q':{'name':'WWTo4Q', 
            #              'file':self.basedir + '/WW/TauTauAnalysis.WWTo4Q_4f_ICHEP.root', 
            #              'cross-section':22.82,
            #              'additional_cut':'1',
            #              'isSignal':0, 
            #              'order':5},
            
            'WZ':{'name':'WZ', 
                  'file':self.basedir + '/WZ/TauTauAnalysis.WZ_TuneCUETP8M1_ICHEP.root', 
                  'cross-section':10.71,
                  'additional_cut':'1',
                  'isSignal':0, 
                  'order':6},
            
            'ZZ':{'name':'ZZ', 
                  'file':self.basedir + '/ZZ/TauTauAnalysis.ZZ_TuneCUETP8M1_ICHEP.root', 
                  'cross-section':3.22,
                  'additional_cut':'1',
                  'isSignal':0, 
                  'order':7},
            
            'W':{'name':'W', 
                 'file':self.basedir + 'WJ/TauTauAnalysis.WJetsToLNu_TuneCUETP8M1_ICHEP.root', 
                 'cross-section':1.,
                 'additional_cut':'1',
                 'isSignal':0, 
                 'order':8},

            'W1':{'name':'W1', 
                 'file':self.basedir + 'WJ/TauTauAnalysis.W1JetsToLNu_TuneCUETP8M1_ICHEP.root', 
                 'cross-section':1.,
                 'additional_cut':'1',
                 'isSignal':0, 
                 'order':8},

            'W2':{'name':'W2', 
                 'file':self.basedir + 'WJ/TauTauAnalysis.W2JetsToLNu_TuneCUETP8M1_ICHEP.root', 
                 'cross-section':1.,
                 'additional_cut':'1',
                 'isSignal':0, 
                 'order':8},

            'W3':{'name':'W3', 
                 'file':self.basedir + 'WJ/TauTauAnalysis.W3JetsToLNu_TuneCUETP8M1_ICHEP.root', 
                 'cross-section':1.,
                 'additional_cut':'1',
                 'isSignal':0, 
                 'order':8},

            'W4':{'name':'W4', 
                 'file':self.basedir + 'WJ/TauTauAnalysis.W4JetsToLNu_TuneCUETP8M1_ICHEP.root', 
                 'cross-section':1.,
                 'additional_cut':'1',
                 'isSignal':0, 
                 'order':8},
    
            'ST_t_top':{'name':'ST_t_top', 
                        'file':self.basedir + 'ST/TauTauAnalysis.ST_t-channel_top_4f_leptonDecays_ICHEP.root', 
                        'cross-section':136.02,
                        'additional_cut':'1',
                        'isSignal':0, 
                        'order':9},
            
            
            'ST_t_antitop':{'name':'ST_t_antitop', 
                            'file':self.basedir + 'ST/TauTauAnalysis.ST_t-channel_antitop_4f_leptonDecays_ICHEP.root', 
                            'cross-section':80.95,
                            'additional_cut':'1',
                            'isSignal':0, 
                            'order':10},
            
            
            'ST_tw_top':{'name':'ST_tw_top', 
                         'file':self.basedir + 'ST/TauTauAnalysis.ST_tW_top_5f_inclusiveDecays_ICHEP.root', 
                         'cross-section':35.60,
                         'additional_cut':'1',
                         'isSignal':0, 
                         'order':11},
            
            'ST_tw_antitop':{'name':'ST_tw_antitop', 
                             'file':self.basedir + 'ST/TauTauAnalysis.ST_tW_antitop_5f_inclusiveDecays_ICHEP.root', 
                             'cross-section':35.60,
                             'additional_cut':'1',
                             'isSignal':0, 
                             'order':12},
            
            #    'Signal':{'name':'Signal', 
            #              'file':self.basedir + 'signal/TauTauAnalysis.LowMass_30GeV_DiTauResonance_ICHEP.root', 
            #              'cross-section':1.,
            #              'isSignal':1, 
            #              'order':3000},
            
            'data_obs':{'name':'data_obs', 
                        'file':self.basedir + 'SingleMuon/TauTauAnalysis.SingleMuon_Run2016_ICHEP.root',
                        'cross-section':1.,
                        'additional_cut':'1',
                        'isSignal':0, 
                        'order':2999},

            'QCD':{'name':'QCD', 
                   'file':None,
                   'cross-section':None,
                   'additional_cut':'1',
                   'isSignal':0, 
                   'order':0},

            }



        print 'Retrieve normalization'

        for processname, val in self.process.iteritems():
            if processname=='QCD': continue
            
            filename = val['file']
            if tes!=None and processname != 'ZTT10to50':
                filename = filename.replace('DY/', 'DY_tes_' + str(tes) + '/')

#            file = TFile(val['file']) 
            print filename
            file = TFile(filename) 
            ntot = file.Get("histogram_mutau/cutflow_mutau").GetBinContent(1)
            self.process[processname]['ntot'] = ntot
            self.process[processname]['file'] = file

            print 'Register', processname.ljust(20), str(self.process[processname]['ntot']).ljust(15), 'SF = ', str(self.process[processname]['cross-section']*self.lumi*1000/self.process[processname]['ntot']).ljust(15)



        # DY stitching

        self.dy_xs = [4954.0, 1012.5, 332.8, 101.8, 54.8]

        self.dy_nlo_xs = 5765.4

        self.dykfactor = self.dy_nlo_xs/self.dy_xs[0]       

        print 'k-factor : DY = ', self.dykfactor, self.dy_nlo_xs, '(NLO) / ', self.dy_xs[0], '(LO)'

        self.dy_efflumi = []

        for ijet, processname in enumerate(['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4']):
            self.dy_efflumi.append(self.process[processname]['ntot']/self.dy_xs[ijet])


        # calculate DY weight 

        self.dy_weight = []
        for ijet, processname in enumerate(['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4']):
            if processname=='ZTT':
                self.dy_weight.append(self.dykfactor*self.lumi*1000/self.dy_efflumi[ijet])
            else:
                self.dy_weight.append(self.dykfactor*self.lumi*1000/(self.dy_efflumi[0] + self.dy_efflumi[ijet]))


        self.dy_weightstr = '('

        for ii, _weight in enumerate(self.dy_weight):
            self.dy_weightstr += '(NUP==' + str(ii) + ' ? ' + str(self.dy_weight[ii]) + ': 1)*'


        self.dy_weightstr += '1)'
        print self.dy_weightstr



        # W stitching 

        self.w_xs = [50380, 9644.5, 3144.5, 954.8, 485.6]

        self.w_nlo_xs = 61526.7

        self.wkfactor = self.w_nlo_xs/self.w_xs[0]       

        print 'k-factor : W = ', self.wkfactor, self.w_nlo_xs, '(NLO) / ', self.w_xs[0], '(LO)'

        self.w_efflumi = []

        for ijet, processname in enumerate(['W', 'W1', 'W2', 'W3', 'W4']):
            self.w_efflumi.append(self.process[processname]['ntot']/self.w_xs[ijet])


        # calculate W weight 

        self.w_weight = []
        for ijet, processname in enumerate(['W', 'W1', 'W2', 'W3', 'W4']):
            if processname=='W':
                self.w_weight.append(self.wkfactor*self.lumi*1000/self.w_efflumi[ijet])
            else:
                self.w_weight.append(self.wkfactor*self.lumi*1000/(self.w_efflumi[0] + self.w_efflumi[ijet]))


        self.w_weightstr = '('

        for ii, _weight in enumerate(self.w_weight):
            self.w_weightstr += '(NUP==' + str(ii) + ' ? ' + str(self.w_weight[ii]) + ': 1)*'


        self.w_weightstr += '1)'
        print self.w_weightstr


    def returnWeight(self, val):
        weight = 'weight*' + str(val['cross-section']*self.lumi*1000/val['ntot'])  + '*(gen_match_2==5 ? 0.9 : 1)'

        if val['name'] in ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4',
                           'ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4',
                           'ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4']:            
            weight = 'weight*' + self.dy_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

        elif val['name'] in ['W', 'W1', 'W2', 'W3', 'W4']:
            weight = 'weight*' + self.w_weightstr + '*(gen_match_2==5 ? 0.9 : 1)'

        elif val['name'] in ['data_obs']:        
            weight = '1'

        return weight


    def createHistograms(self, catname, selection, exceptionList, vardir, sf_W = 1.):

        print '-'*80
        print 'category : ', catname
        print 'selection : ', selection
        print 'exceptionList : ', exceptionList
        print 'vardir = ', vardir
        print 'SF for W = ', sf_W
        print '-'*80    

        for processname, val in self.process.iteritems():
            if processname in exceptionList: 
                print 'Remove', processname
                continue
        
            tree = val['file'].Get('tree_mutau')

            var_tuples = []
    
            for varname, var in vardir.iteritems():
#                print catname, processname, varname, var['drawname']
                hname = 'hist_' + catname + '_' + processname + '_' + var['drawname']
        
                hist_register = TH1F(hname, hname, var['nbins'], var['min'], var['max'])
                hist_register.GetXaxis().SetTitle(var['label'])
                hist_register.GetXaxis().SetLabelSize(0)
                hist_register.Sumw2()
    
                if val['name'] in ['data_obs']:
                    hist_register.SetMarkerStyle(20)
                    hist_register.SetMarkerSize(0.5)
        
                self.hists[hname] = hist_register

                var_tuples.append('{var} >> {hist}'.format(var=var['drawname'], hist=hname))

            weight = self.returnWeight(val)
            if processname in ['W', 'W1', 'W2', 'W3', 'W4']:
                weight += '*' + str(sf_W)

#            print processname, weight



            cutstr = selection + ' && ' + val['additional_cut']
            cut = '({c}) * {we}'.format(c=cutstr, we=weight)
            tree.MultiDraw(var_tuples, cut)



        print 'making plots ...'
        ensureDir('fig_' + catname)

        for varname, var in vardir.iteritems():        

            stackname = 'stackhist_' + catname + '_' + varname
            hist = DataMCPlot(stackname)
            hist.legendBorders = 0.55, 0.55, 0.88, 0.88

            for processname, val in self.process.iteritems():

                hname = 'hist_' + catname + '_' + processname + '_' + varname
                if not self.hists.has_key(hname): continue

                pname = val['name']
                
                hist.AddHistogram(pname, self.hists[hname], val['order'])
                if pname in ['data_obs']:
                    hist.Hist(pname).stack = False

            hist.Group('VV', ['WZ', 'ZZ', 'WWTo1L1Nu2Q', 'ST_t_top', 'ST_t_antitop', 'ST_tw_top', 'ST_tw_antitop'])
            hist.Group('ZTT', ['ZTT', 'ZTT1', 'ZTT2', 'ZTT3', 'ZTT4'])
            hist.Group('ZL', ['ZL', 'ZL1', 'ZL2', 'ZL3', 'ZL4'])
            hist.Group('ZJ', ['ZJ', 'ZJ1', 'ZJ2', 'ZJ3', 'ZJ4'])
            hist.Group('W', ['W', 'W1', 'W2', 'W3', 'W4'])
            hist.Group('TT', ['TTT', 'TTJ'])

            print hist
            self.comparisonPlots(hist, 'fig_' + catname + '/' + stackname + '.gif')
#            display = DisplayManager('fig_' + catname + '/' + stackname + '.gif', True, self.lumi, 0.42, 0.65)
#            display.Draw(hist)







    def extractQCD(self, catname, exceptionList, var, os_ss_ratio):
        h_QCD = None

        for processname, val in self.process.iteritems():
            if processname in exceptionList: continue
        
            hname = 'hist_' + catname + '_' + processname + '_' + var
        
            addfactor = -1.
            if val['name'] == 'data_obs':
                addfactor = 1.
            
            if h_QCD == None:
                h_QCD = copy.deepcopy(self.hists[hname])
                h_QCD.Scale(addfactor)
#                print 'subtract', hname, self.hists[hname].Integral(0, self.hists[hname].GetNbinsX()+1)
#                print 'subtract_copy', h_QCD.Integral(0, h_QCD.GetNbinsX()+1)
            else:
                h_QCD.Add(self.hists[hname], addfactor)
#                print 'subtract', hname, self.hists[hname].Integral(0, self.hists[hname].GetNbinsX()+1)
#                print 'subtract_copy', h_QCD.Integral(0, h_QCD.GetNbinsX()+1)

            
        h_QCD_os = copy.deepcopy(h_QCD)
        h_QCD_os.Scale(os_ss_ratio)

        osname = 'hist_' + catname.replace('ss','os') + '_QCD_' + var
        h_QCD_os.SetName(osname)

        print '-'*80
        print 'Original yield = ', h_QCD.Integral(0, h_QCD_os.GetNbinsX()+1)
        print 'OS/SS ratio = ', os_ss_ratio
        print 'Estimated QCD yield at ', catname, ' : ', h_QCD_os.Integral(0, h_QCD_os.GetNbinsX()+1)
        print '-'*80

        self.hists[osname] = h_QCD_os



    def comparisonPlots(self, hist, pname='sync.pdf', isRatio=True):
        display = DisplayManager(pname, isRatio, self.lumi, 0.42, 0.65)
        display.Draw(hist)


def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



def returnIntegral(hist):
    return hist.Integral(0, hist.GetNbinsX()+1)
