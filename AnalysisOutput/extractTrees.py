import time
start = time.time()
import ROOT
from ROOT import TFile, TTree, TTreeFormula
import numpy # to set branch addres
from math import log, pow, floor

# https://root.cern.ch/root/html/tutorials/tree/copytree.C.html
# https://root.cern.ch/root/html/tutorials/tree/copytree3.C.html
# to get branch channel with string "channel": getattr(oldtree,"channel")


mylabel = "_ICHEP"
DIR = "/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/"





    ############
    # makesCut #
    ############

def makesCut(cuts):
    """Returns boolean weather the event made the selection"""
    return True





    #################
    # makeThreshold #
    #################

def makeThreshold(n):
    """Help function to find a good stepsize for read out when looping over a large number N.
       In a for loop with index i, you could do a print out like:
         if i % threshold == 0: print "some progress message" """
    #                      floor(log(N/10.0,10))        stepsize = (number of digits in N) - 2
    #              max(0.0,floor(log(N/10.0,10)))       make sure it is at least 0
    #        min(6,max(0.0,floor(log(N/10.0,10))))      set maximum step size to 10^6 (otherwise takes too long)
    # pow(10,min(6,max(0.0,floor(log(N/10.0,10)))))     make treshold a power of 10
    return pow(10,min(6,max(0.0,floor(log(n/10.0,10)))))





    ############
    # makeTree #
    ############

def makeTree(treename, filename, **kwargs):
    """Extract tree from file and save in new one."""
    print ">>>\n>>> extracting tree %s from %s" % (treename,filename)
    start_here = time.time()
    
    channel = 0
    if "mutau" in treename: channel = 1
    elif "eltau" in treename: channel = 2
    
    oldfile = TFile(filename)
    oldtree = oldfile.Get(treename)
    newfilename = kwargs.get('newfilename',filename.replace( ".root", "_%s.root" % treename ))
    newfile = TFile(newfilename, 'recreate')
    
    print ">>> cloning tree"
    newtree = oldtree.CloneTree(0) # TTree(treename, treename)
    
    print ">>> selecting and copying entries"
    N = kwargs.get('N',oldtree.GetEntries())
    threshold = makeThreshold(N)
    for i in range(N):
        if i % threshold == 0: print ">>>\t%5.2f%%: copied %i entries of %i" % (100.0*i/N,i,N)
        oldtree.GetEntry(i)
        if oldtree.channel == channel:
            newtree.Fill()

    newN = oldtree.GetEntries()
    print ">>> extraction of %s done: %i of %i entries copied" % (treename,N,newN)
    print ">>> writing and closing new file: %s" % (newfilename)
    newfile.Write()
    newfile.Close()
    oldfile.Close()
    
    print ">>> took %.2f seconds.\n" % (time.time()-start_here)
    print ">>> "





    ############
    # makeTree #
    ############

def makeTreeWithString(treename, filename, **kwargs):
    """Extract tree from file and save in new one."""
    print ">>>\n>>> extracting tree %s from %s" % (treename,filename)
    start_here = time.time()
    # TODO: use TTreeFormula to cut tree
    # TODO: check efficiency
    # https://root.cern.ch/root/roottalk/roottalk04/2010.html
    # https://root.cern.ch/phpBB3/viewtopic.php?t=16775
    
    cut = "channel == 0"
    if "mutau" in cut: "channel == 0"
    elif "eltau" in cut: "channel == 0"
    
    oldfile = TFile(filename)
    oldtree = oldfile.Get(treename)
    newfilename = kwargs.get('newfilename',filename.replace( ".root", "_%s_string.root" % treename ))
    newfile = TFile(newfilename, 'recreate')
    
    print ">>> cloning tree"
    newtree = oldtree.CloneTree(0) # TTree(treename, treename)
    
    print ">>> make TTreeFormula and GetNData"
    cut_form = TTreeFormula( 'channel', cut, oldtree )
    cut_form.GetNdata()
    
    print ">>> selecting and copying entries"
    N = kwargs.get('N',oldtree.GetEntries())
    threshold = makeThreshold(N)
    for i in range(N):
        if i % threshold == 0: print ">>>\t%5.2f%%: copied %i entries of %i" % (100.0*i/N,i,N)
        oldtree.GetEntry(i)
        if cut_form.EvalInstance(i) is not 0:
            newtree.Fill()

    newN = oldtree.GetEntries()
    print ">>> extraction of %s done: %i of %i entries copied" % (treename,N,newN)
    print ">>> writing and closing new file: %s" % (newfilename)
    newfile.Write()
    newfile.Close()
    oldfile.Close()

    print ">>> took %.2f seconds.\n" % (time.time()-start_here)
    print ">>> "





    ########
    # main #
    ########

def main():
    """Main method: list files and which trees to extract."""

    files = [
                "TT/TauTauAnalysis.TT_TuneCUETP8M1%s.root" % mylabel,
#                 "DY/TauTauAnalysis.DYJetsToLL_M-10to50_TuneCUETP8M1.root",
#                 "DY/TauTauAnalysis.DYJetsToLL_M-50_TuneCUETP8M1.root",
             ]

    channels = [    "mutau",
                    #"eletau"
                ]
    
    for file in files:
        file = DIR + file
        for channel in channels:
            treename = "tree_%s" % channel
            makeTreeWithString(treename,file,N=1000000)
            makeTree(treename,file,N=1000000)





if __name__ == '__main__':
    main()
    end = time.time()
    print "\nThis lasted %.2f seconds.\n" % (end-start)
    print ">>> done\n"



