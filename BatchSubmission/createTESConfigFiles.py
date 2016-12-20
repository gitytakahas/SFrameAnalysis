
BASEDIR="/shome/ineuteli/analysis/SFrameAnalysis/BatchSubmission"
FILES="Signal_Izaak.py Signal_HTT_Izaak.py Background_DY_Izaak.py"
FILEND="_Izaak.py"
cd $BASEDIR

UP="TES0p03"
DOWN="TES0p97"
TESSHIFT="0.03"
TESSHIFTLINE="\[\"TESshift\",\"0.00\"\],"
NEWTESSHIFTUPLINE=`echo $TESSHIFTLINE | sed "s/0.00/$TESSHIFT/"`
NEWTESSHIFTDOWNLINE=`echo $TESSHIFTLINE | sed "s/0.00/-$TESSHIFT/"`

DOTESLINE="\[\"doTES\",\"false\"\]"
NEWDOTESLINE="\[\"doTES\",\"true\"\]"

echo " "
echo ">>> replacing $TESSHIFTLINE with:"
echo ">>>   $NEWTESSHIFTUPLINE"
echo ">>>   $NEWTESSHIFTDOWNLINE"
echo ">>> "
echo ">>> replacing $DOTESLINE with:"
echo ">>>   $NEWDOTESLINE"

for f in $FILES; do
    echo ">>> "
    echo ">>> making TES shifts for $f"
    if grep -q $TESSHIFTLINE $f; then
        FUP=`  echo $f | sed "s/$FILEND/_$UP$FILEND/"`
        FDOWN=`echo $f | sed "s/$FILEND/_$DOWN$FILEND/"`
        echo ">>> creating file: $FUP"
        echo ">>> creating file: $FDOWN"
        cp $f $FUP
        cp $f $FDOWN
        sed -i "s/$TESSHIFTLINE/$NEWTESSHIFTUPLINE/"   $FUP
        sed -i "s/$TESSHIFTLINE/$NEWTESSHIFTDOWNLINE/" $FDOWN
        if grep -q $DOTESLINE $f; then
            sed -i "s/$DOTESLINE/$NEWDOTESLINE/"   $FUP
            sed -i "s/$DOTESLINE/$NEWDOTESLINE/" $FDOWN          
        else
            echo ">>> Warning could not find \"$DOTESLINE\" line"
        fi
    else
        echo ">>> Warning could not find \"$TESSHIFTLINE\" line"
    fi
done

echo " "
