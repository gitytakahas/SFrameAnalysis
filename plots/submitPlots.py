import os, sys
import subprocess
import time

DIR = "/shome/ineuteli/analysis/SFrameAnalysis/plots"



def getCategories():
    # get list of configs
    header = "list of available categories:"
    tab = "\n>>>\t"
    out = subprocess.check_output("python %s/plot.py -l" % DIR, shell=True, stderr=open(os.devnull, 'w'))
    #print ">>> output from plot.py -l:"
    #print out
    #print ">>> end output"
    if not header in out or not tab in out: sys.exit(1)
    return out.split(header)[1].split(tab)[1:-1]



def main():
    #print
    
    if not os.path.exists("%s/submitPlots" % DIR):
        os.makedirs("%s/submitPlots" % DIR)
        print ">>> made directory %s/submitPlots" % DIR
    
    categories = getCategories()
    
    if len(categories) > 0:
        for category, i in zip(categories, range(len(categories))):
            category = category.replace(" and ","-").replace(" ","").replace(",","-")
            print "\n>>> category %i: %s" % ( i, category )
            command = "qsub -q all.q -N category_%s %s/submitPlots.sh %s" % ( i, DIR, i )
            print ">>> " + command
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            os.system(command)
        #print



if __name__ == '__main__':
    main()
    print "\n>>> done\n"


