for dir in BTaggingTools GoodRunsLists LepEff2016 NtupleVariables PileupReweightingTool SFrame SVFit SVfitStandalone TauTauResonances VHTausResonances
do
    echo
    echo $dir
    echo
    cd $dir
    make distclean
    make
    cd -
done
