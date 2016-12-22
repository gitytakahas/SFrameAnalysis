
BASEDIR="/shome/ineuteli/analysis/SFrameAnalysis/BatchSubmission"
FILES="Signal_Izaak.py Signal_HTT_Izaak.py Background_DY_Izaak.py Background_DY_NLO_Izaak.py Background_TT_Izaak.py"
FILEND="_Izaak.py"
cd $BASEDIR

UP="TES1p03"
DOWN="TES0p97"
TESSHIFT="0.03"
TESSHIFT_LINE="\[\"TESshift\",\"0.00\"\],"
TESSHIFT_UP_NEWLINE=`echo $TESSHIFT_LINE | sed "s/0.00/$TESSHIFT/"`
TESSHIFT_DOWN_NEWLINE=`echo $TESSHIFT_LINE | sed "s/0.00/-$TESSHIFT/"`

DOTES_LINE="\[\"doTES\",\"false\"\]"
DOTES_NEWLINE="\[\"doTES\",\"true\"\]"

LABEL_LINE="label = \""
LABEL_UP_NEWLINE="label = \"_${UP}"
LABEL_DOWN_NEWLINE="label = \"_${DOWN}"

echo " "
echo ">>> replacing \"${TESSHIFT_LINE}\" with: "
echo ">>>    \"\"${TESSHIFT_UP_NEWLINE}\"      "
echo ">>>    \"\"${TESSHIFT_DOWN_NEWLINE}\"    "
echo ">>> "
echo ">>> replacing \"${DOTES_LINE}\" with: "
echo ">>>    \"${DOTES_NEWLINE}\"           "
echo ">>> "
echo ">>> replacing \"${LABEL_LINE}\" with: "
echo ">>>    \"${LABEL_UP_NEWLINE}\"        "
echo ">>>    \"${LABEL_DOWN_NEWLINE}\"      "

for f in $FILES; do
    echo ">>> "
    echo ">>> making TES shifts for $f"
    if grep -q "${TESSHIFT_LINE}" $f; then
        FUP=`  echo $f | sed "s/${FILEND}/_${UP}${FILEND}/"`
        FDOWN=`echo $f | sed "s/${FILEND}/_${DOWN}${FILEND}/"`
        echo ">>> creating file: $FUP"
        echo ">>> creating file: $FDOWN"
        cp $f $FUP
        cp $f $FDOWN
        sed -i "s/${TESSHIFT_LINE}/${TESSHIFT_UP_NEWLINE}/"   $FUP
        sed -i "s/${TESSHIFT_LINE}/${TESSHIFT_DOWN_NEWLINE}/" $FDOWN
        if grep -q "${DOTES_LINE}" $f; then
            sed -i "s/${DOTES_LINE}/${DOTES_NEWLINE}/"   $FUP
            sed -i "s/${DOTES_LINE}/${DOTES_NEWLINE}/" $FDOWN          
        else echo ">>> Warning could not find \"${DOTES_LINE}\" line"
        fi
        if grep -q "${LABEL_LINE}" $f; then
            sed -i "s/${LABEL_LINE}/${LABEL_UP_NEWLINE}/"   $FUP
            sed -i "s/${LABEL_LINE}/${LABEL_DOWN_NEWLINE}/" $FDOWN          
        else echo ">>> Warning could not find \"${LABEL_LINE}\" line"
        fi
    else echo ">>> Warning could not find \"${TESSHIFT_LINE}\" line"
    fi
done

echo " "
