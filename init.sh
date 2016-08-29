# get all necessary packages
# check out SFrame
echo "Creating a few directories"
mkdir AnalysisTemp
mkdir AnalysisOut
echo "Checking out SFrame from SVN"
svn co svn://svn.code.sf.net/p/sframe/code/SFrame/trunk SFrame
echo "Getting submodules"
git submodule init
git submodule update
echo "Remember to setup and compile SFrame"