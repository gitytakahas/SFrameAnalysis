for dir in BTaggingTools GoodRunsLists LepEff2016 NtupleVariables PileupReweightingTool SFrame SVfitStandalone TauTauResonances
do
    echo
    echo $dir
    echo
    cd $dir
    make distclean
    make
    cd -
done
