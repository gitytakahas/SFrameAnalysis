mport os, sys
import datetime

date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
header = \
"""%s
\documentclass[8pt,a4paper]{article}
\usepackage[margin=4mm]{geometry}
\usepackage{graphicx}
\usepackage{float}
\begin{document}
"""
figure = \
"""
\begin{figure}[H]
	\centering
	\includegraphics[width=90mm]{%s}
	\hspace{5mm}
	\includegraphics[width=90mm]{%s}
	\caption{%s}
\end{figure}
"""
footer = \
"""
\end{document}
"""

header = header.replace('\b','\\b') % ("% generated on "+date)
figure = figure.replace('\b','\\b')
footer = footer.replace('\b','\\b')





    ##############
    # writeLaTeX #
    ##############

def writeLaTeXFile(filename, plots):
    """Write LaTeX file."""
    
    file = open(filename, 'w')
    file.write(header)
    for fig1, fig2, caption in plots:
        file.write(figure % (fig1,fig2,caption))
    file.write(footer)
                  
    file.close()

    print "\n>>> written file with %i comparisons" % len(plots)





    ##############
    # includeFig #
    ##############

def includeFig(fig):
    """Return boolean as to whether it should be included or not."""
    
    illegal = [ "abs", "jpt", "bpt", "phi" ]
    
    for flag in illegal:
        if flag in fig: return False
    return True






    ##############
    # includeFig #
    ##############

def makeLaTeX(var):
    """Make nice variables."""

    var = var.replace("_","")

    return var





    ##############
    # getFigures #
    ##############

def getFigures():
    """Get list of all available figures."""
    
    path1 = "plots/mutau_noSF/"
    path2 = "plots/mutau/"
    
    figs1 = os.listdir(path1)
    figs2 = os.listdir(path2)
    plots = [ ]
    
    for fig in figs1:
        if includeFig(fig) and ".png" in fig and fig in figs2:
            caption = "%s without SF vs. with SF" % makeLaTeX(fig.replace(".png",""))
            plots.append((path1+fig,path2+fig,caption))
    
    return plots





    ########
    # main #
    ########

def main():
    """Main function."""

    filename = "test.tex"
    plots = getFigures()
    writeLaTeXFile(filename,plots)





if __name__ == '__main__':
    print
    main()
    print ">>> Done.\n"





