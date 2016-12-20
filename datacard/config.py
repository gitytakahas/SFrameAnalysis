from ROOT import TFile

class config(object):

    def __init__(self, basedir, lumi, tes=None):
        
        self.basedir = basedir

        self.lumi = lumi

        self.process = {

            'TT':{'name':'TT', 
                  'file':self.basedir + '/TT/TauTauAnalysis.TT_TuneCUETP8M1_ICHEP.root',
                  'additional_cut':'1',
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
