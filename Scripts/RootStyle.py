# ATLAS Style
# importing ATLASstyle for ROOT (adjust path to current version)
# ROOT.gROOT.LoadMacro(os.environ['SFRAME_DIR']+"/../atlasstyle-00-03-04/AtlasStyle.C")
# atlasStyle = SetAtlasStyle()
# gStyle.SetPalette(1)
# gStyle.SetOptStat(0)

# ROOT.gROOT.SetBatch(True)
sys.path.insert(0, '~/CMSstyle/')
import tdrstyle
tdrstyle.setTDRStyle()

# ROOT.LoadMacro("~/bbH/atlasstyle-00-03-05/AtlasStyle.C")
# SetAtlasStyle()

gStyle.SetStatColor(0)
gStyle.SetCanvasColor(0)
gStyle.SetPadColor(0)
gStyle.SetPadBorderMode(0)
gStyle.SetCanvasBorderMode(0)
gStyle.SetFrameBorderMode(0)
#gStyle.SetOptStat(1110)
gStyle.SetOptStat(0)
gStyle.SetStatH(0.2)
gStyle.SetStatW(0.2)
gStyle.SetStatX(0.99)
gStyle.SetTitleColor(1)
gStyle.SetTitleFillColor(0)
# gStyle.SetTitleY(1.)
# gStyle.SetTitleX(.15)
gStyle.SetTitleBorderSize(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetPalette(1)
#   gStyle.SetMarkerStyle(20);
# gStyle.SetMarkerSize(2);
# gStyle.SetLineWidth(2);
#   gStyle.SetLineStyleString(2,"[12 12]"); # postscript dashes


gROOT.SetBatch(True)

gStyle.SetHistMinimumZero()

# creating canvas, hstack and legend objects
canvas=TCanvas("canvas", "canvas", 600, 600)
hstack=THStack()
legend=TLegend()
title=TLatex()
default_stacktype="bkgsig"
default_histtype=None
default_title=""
default_xlabel=""
default_ylabel=""

# default latex names for given samples
default_Latex={}
default_Latex["TOP"]="t#bar{t}"
default_Latex["TOPCOMP"]="t#bar{t}"
default_Latex["TOP_truth3jexcl_mu"]="t#bar{t} truth #mu + 3j"
default_Latex["TOP_truth4jexcl_mu"]="t#bar{t} truth #mu + 4j"
default_Latex["TOP_truth5jincl_mu"]="t#bar{t} truth #mu + 5j"
default_Latex["TOP_truth3jexcl_el"]="t#bar{t} truth e + 3j"
default_Latex["TOP_truth4jexcl_el"]="t#bar{t} truth e + 4j"
default_Latex["TOP_truth5jincl_el"]="t#bar{t} truth e + 5j"
default_Latex["TOP_none"]="t#bar{t} oops"
default_Latex["TOPOTHER"]="t#bar{t}^{#text{other}}"
default_Latex["STOP"]="single-top"
default_Latex["STOPTCH"]="single-top t-channel"
default_Latex["STOPWT"]="single-top Wt"
default_Latex["STOPSCH"]="single-top s-channel"
default_Latex["QCD"]="QCD"
default_Latex["QCDJE"]="QCD"
default_Latex["WJETS"]="W+Jets"
default_Latex["WJETSCOMP"]="W+Jets"
default_Latex["WBBJETS"]="Wbb+Jets"
default_Latex["WCJETS"]="Wc+Jets"
default_Latex["WCCJETS"]="Wcc+Jets"
default_Latex["ZJETS"]="Z+Jets"
default_Latex["ZBBJETS"]="Zbb+Jets"
default_Latex["DATA"]="data"
default_Latex["PSEUDO"]="pseudo data"
default_Latex["DIBOSON"]="diboson"
default_Latex["ELECTROWEAK"]="electroweak"
default_Latex["WZJETS"]="W/Z+Jets"
default_Latex["RECO"]="reco"
default_Latex["TRUTH"]="truth"
default_Latex["W"]="W"
default_Latex["BJET"]="b jet"
default_Latex["MCATNLO"]="MC@NLO+Herwig"
default_Latex["ALPGEN"]="AlpGEN+Herwig"
default_Latex["ALPGENPYTHIA"]="AlpGEN+Pythia"
default_Latex["POWHEGJIMMY"]="PowHeg+Herwig"
default_Latex["POWHEGPYTHIA"]="PowHeg+Pythia"
default_Latex["WH1000"]="X #rightarrow WH (m = 1 TeV)"
default_Latex["WH2000"]="X #rightarrow WH (m = 2 TeV)"
default_Latex["WH3000"]="X #rightarrow WH (m = 3 TeV)"

# default colors for given samples
default_Color={}
default_Color["TOP"]=2
default_Color["TOPCOMP"]=1
default_Color["TOP_truth3jexcl_mu"]=2
default_Color["TOP_truth4jexcl_mu"]=9
default_Color["TOP_truth5jincl_mu"]=8
default_Color["TOP_truth3jexcl_el"]=2
default_Color["TOP_truth4jexcl_el"]=9
default_Color["TOP_truth5jincl_el"]=8
default_Color["TOP_none"]=7
default_Color["TOPOTHER"]=619
default_Color["STOP"]=62
default_Color["STOPTCH"]=62
default_Color["STOPWT"]=63
default_Color["STOPSCH"]=64
default_Color["QCD"]=51
default_Color["QCDJE"]=51
default_Color["WJETS"]=92
default_Color["WJETSCOMP"]=1
default_Color["WBBJETS"]=93
default_Color["WCJETS"]=94
default_Color["WCCJETS"]=96
default_Color["ZJETS"]=95
default_Color["ZBBJETS"]=96
default_Color["DATA"]=0
default_Color["PSEUDO"]=62
default_Color["DIBOSON"]=3
default_Color["ELECTROWEAK"]=7
default_Color["WZJETS"]=93
default_Color["RECO"]=2
default_Color["TRUTH"]=3
default_Color["W"]=2
default_Color["BJET"]=3
default_Color["MCATNLO"]=4
default_Color["ALPGEN"]=kGreen+1
default_Color["ALPGENPYTHIA"]=kCyan-3
default_Color["POWHEGJIMMY"]=kMagenta-6
default_Color["POWHEGPYTHIA"]=2
default_Color["WH1000"]=2
default_Color["WH2000"]=9
default_Color["WH3000"]=8


default_MarkerStyle = {}
default_MarkerStyle["MCATNLO"]=20
default_MarkerStyle["ALPGEN"]=21
default_MarkerStyle["ALPGENPYTHIA"]=25
default_MarkerStyle["POWHEGJIMMY"]=23
default_MarkerStyle["POWHEGPYTHIA"]=22


topSamples = ["MCATNLO", "ALPGEN", "POWHEGJIMMY", "POWHEGPYTHIA", "ACERMC", "ALPGENPYTHIA"]

# wrapping for fitter input
default_Fitter={}
default_Fitter["TOP"]="tt"
default_Fitter["STOP"]="singletop"
default_Fitter["WJETS"]="W"
default_Fitter["ZJETS"]="Z"
default_Fitter["DIBOSON"]="diboson"
default_Fitter["QCD"]="qcd"
default_Fitter["QCDJE"]="qcd"
default_Fitter["DATA"]="data"
default_Fitter["PSEUDO"]="data"
default_Fitter["2jexcl"]="2j"
default_Fitter["3jexcl"]="3j"
default_Fitter["4jexcl"]="4j"
default_Fitter["5jincl"]="5j"
default_Fitter["none"]="none"
default_Fitter["Egamma"]="e"
default_Fitter["Muons"]="mu"

# default file extension
default_extension=".pdf"

# fraction taken from https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/JetElectronQCDModel for 30 GeV MTW and MET cut
#QCDFractions = { 'Egamma_1jexcl_pretag' : 0.0811, 'Egamma_2jexcl_pretag' : 0.133, 'Egamma_3jexcl_pretag' : 0.165, 'Egamma_4jexcl_pretag' : 0.195, 'Egamma_3jincl_pretag' : 0.0857, 'Egamma_4jincl_pretag' : 0.179, 'Egamma_5jincl_pretag' : 0.0336,
#                 'Egamma_1jexcl_1tag' : 0.107, 'Egamma_2jexcl_1tag' : 0.123, 'Egamma_3jexcl_1tag' : 0.115, 'Egamma_4jexcl_1tag' : 0.125, 'Egamma_3jincl_1tag' : 0.0605, 'Egamma_4jincl_1tag' : 0.122, 'Egamma_5jincl_1tag' : 0.0204,
#                 'Egamma_1jexcl_1tag' : 0.107, 'Egamma_2jexcl_tag' : 0.0605, 'Egamma_3jexcl_tag' : 0.0392, 'Egamma_4jexcl_tag' : 0.0178, 'Egamma_3jincl_tag' : 0.0407, 'Egamma_4jincl_tag' : 0.0146, 'Egamma_5jincl_tag' : 0.0146,
#                 'Muons_1jexcl_pretag' : 0.0214, 'Muons_2jexcl_pretag' : 0.0304, 'Muons_3jexcl_pretag' : 0.0339, 'Muons_4jexcl_pretag' : 0.0278, 'Muons_3jincl_pretag' : 0.0268, 'Muons_4jincl_pretag' : 0.0233, 'Muons_5jincl_pretag' : 0.0146,
#                 'Muons_1jexcl_1tag' : 0.0598, 'Muons_2jexcl_1tag' : 0.0566, 'Muons_3jexcl_1tag' : 0.0392, 'Muons_4jexcl_1tag' : 0.0234, 'Muons_3jincl_1tag' : 0.0299, 'Muons_4jincl_1tag' : 0.0157, 'Muons_5jincl_1tag' : 0.00972,
#                 'Muons_1jexcl_tag' : 0.0598, 'Muons_2jexcl_tag' : 0.055, 'Muons_3jexcl_tag' : 0.0321, 'Muons_4jexcl_tag' : 0.0165, 'Muons_3jincl_tag' : 0.0189, 'Muons_4jincl_tag' : 0.0128, 'Muons_5jincl_tag' : 0.0128 }
#'Muons_3jexcl_tag' : 0.0273,

# MM normalisation
QCDFractions = { 'Egamma_2jexcl_tag' : 0.0748, 'Egamma_3jexcl_tag' : 0.0463, 'Egamma_4jexcl_tag' : 0.0227, 'Egamma_5jincl_tag' : 0.0199,
                 'Muons_2jexcl_tag' : 0.0660, 'Muons_3jexcl_tag' : 0.0382, 'Muons_4jexcl_tag' : 0.0212, 'Muons_5jincl_tag' : 0.0156 }
