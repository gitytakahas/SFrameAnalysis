# get all necessary packages
# check out SFrame
echo "Creating a few directories"
mkdir AnalysisTemp
mkdir AnalysisOut

cd SFrame/
source setup.sh
cd -;

echo "Compiling sub-directories"
for dir in BTaggingTools NtupleVariables PileupReweightingTool SFrame TauTauResonances GoodRunsLists
do
    echo
    echo $dir
    echo
    cd $dir
    make distclean
    make
    cd -
done
