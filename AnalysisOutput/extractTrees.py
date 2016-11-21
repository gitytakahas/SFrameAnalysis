import time
start = time.time()
import ROOT
from ROOT import TFile, TTree
import numpy # to set branch addres
from math import log, pow, floor

# https://root.cern.ch/root/html/tutorials/tree/copytree.C.html
# https://root.cern.ch/root/html/tutorials/tree/copytree3.C.html
# to get branch channel with string "channel": getattr(oldtree,"channel")



DIR = "/shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/"





    ############
    # makesCut #
    ############

def makesCut(cuts):
    """Returns boolean weather the event made the selection"""
    return True





    ############
    # makeTree #
    ############

def makeTree(treename, filename, **kwargs):
    """Extract tree from file and save in new one."""
    print ">>> extracting tree %s from %s" % (treename,filename)
    
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
    N = oldtree.GetEntries()
    threshold = pow(10,min(6,max(0.0,floor(log(N/10.0,10)))))
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
    print ">>> "





    ########
    # main #
    ########

def main():
    """Main method: list files and which trees to extract."""

    files = [
                "TT/TauTauAnalysis.TT_TuneCUETP8M1.root",
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
            makeTree(treename,file)





if __name__ == '__main__':
    main()
    end = time.time()
    print "\nThis lasted",end-start,"seconds.\n"
    print ">>> done\n"



