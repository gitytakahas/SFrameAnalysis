
DIR=/shome/ineuteli/analysis/SFrameAnalysis/BatchSubmission/ #xmls_Izaak #19-09-16_tris #_Izaak
SAMPLE="LowMass"  #DY2JetsToLL_M-10  #DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_HLT #"DYJetsToLL_M-50*reHLT" #"SingleMuon"
N=0

for f in `ls ${DIR}/${SAMPLE}*.xml`; do
  EVENTS=`grep $f -e 'Total number of events processed: ' | grep -Po '[0-9]*'`
  echo ">>> $EVENTS events"
  N=$(($N+$EVENTS))
done

echo ">>> with a grand total of $N events"


