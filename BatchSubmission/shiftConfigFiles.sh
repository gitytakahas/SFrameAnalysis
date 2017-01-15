#! /bin/bash

BASEDIR="/shome/ineuteli/analysis/SFrameAnalysis/BatchSubmission"
TESFILES="Signal_Izaak.py \
          Signal_HTT_Izaak.py \
          Background_DY_Izaak.py \
          Background_DY_NLO_Izaak.py \
          Background_TT_Izaak.py"
LTFFILES="Background_DY_Izaak.py \
          Background_DY_NLO_Izaak.py"
FILEND="_Izaak.py"
cd $BASEDIR


#######
# TES #
#######

TES_UP="TES1p03"
TES_DOWN="TES0p97"
DOTES_LINE="\[\"doTES\",\"false\"\]"
DOTES_NEWLINE="\[\"doTES\",\"true\"\]"
TESSHIFT="0.03"
TESSHIFT_LINE="\[\"TESshift\",\"0.00\"\],"
TESSHIFT_UP_NEWLINE=`echo $TESSHIFT_LINE | sed "s/0.00/$TESSHIFT/"`
TESSHIFT_DOWN_NEWLINE=`echo $TESSHIFT_LINE | sed "s/0.00/-$TESSHIFT/"`
LABEL_LINE="label = \""
LABEL_TES_UP_NEWLINE="label = \"_${TES_UP}"
LABEL_TES_DOWN_NEWLINE="label = \"_${TES_DOWN}"

echo " "
echo ">>> replacing \"${TESSHIFT_LINE}\" with: "
echo ">>>    \"${TESSHIFT_UP_NEWLINE}\"      "
echo ">>>    \"${TESSHIFT_DOWN_NEWLINE}\"    "
echo ">>> "
echo ">>> replacing \"${DOTES_LINE}\" with: "
echo ">>>    \"${DOTES_NEWLINE}\"           "
echo ">>> "
echo ">>> replacing \"${LABEL_LINE}\" with: "
echo ">>>    \"${LABEL_TES_UP_NEWLINE}\"        "
echo ">>>    \"${LABEL_TES_DOWN_NEWLINE}\"      "

for f in $TESFILES; do
    echo ">>> "
    echo ">>> making TES shifts for $f"
    if grep -q "${DOTES_LINE}" $f; then
        FUP=`  echo $f | sed "s/${FILEND}/_${TES_UP}${FILEND}/"`
        FDOWN=`echo $f | sed "s/${FILEND}/_${TES_DOWN}${FILEND}/"`
        echo ">>> creating file: $FUP"
        echo ">>> creating file: $FDOWN"
        cp $f $FUP
        cp $f $FDOWN
        sed -i "s/${DOTES_LINE}/${DOTES_NEWLINE}/" $FUP
        sed -i "s/${DOTES_LINE}/${DOTES_NEWLINE}/" $FDOWN
        if grep -q "${TESSHIFT_LINE}" $f; then
            sed -i "s/${TESSHIFT_LINE}/${TESSHIFT_UP_NEWLINE}/"   $FUP
            sed -i "s/${TESSHIFT_LINE}/${TESSHIFT_DOWN_NEWLINE}/" $FDOWN
        else echo ">>> WARNING! Could not find \"${TESSHIFT_LINE}\" line"
        fi
        if grep -q "${LABEL_LINE}" $f; then
            sed -i "s/${LABEL_LINE}/${LABEL_TES_UP_NEWLINE}/"   $FUP
            sed -i "s/${LABEL_LINE}/${LABEL_TES_DOWN_NEWLINE}/" $FDOWN          
        else echo ">>> WARNING! Could not find \"${LABEL_LINE}\" line"
        fi
    else echo ">>> WARNING! Could not find \"${DOTES_LINE}\" line"
    fi
done


#######
# LTF #
#######

LTF_UP="LTF1p03"
LTF_DOWN="LTF0p97"
DOLTF_LINE="\[\"doLTF\",\"false\"\]"
DOLTF_NEWLINE="\[\"doLTF\",\"true\"\]"
LTFSHIFT="0.03"
LTFSHIFT_LINE="\[\"LTFshift\",\"0.00\"\],"
LTFSHIFT_UP_NEWLINE=`echo $LTFSHIFT_LINE | sed "s/0.00/$LTFSHIFT/"`
LTFSHIFT_DOWN_NEWLINE=`echo $LTFSHIFT_LINE | sed "s/0.00/-$LTFSHIFT/"`
LABEL_LINE="postFix = \""
LABEL_LTF_UP_NEWLINE="postFix = \"_${LTF_UP}"
LABEL_LTF_DOWN_NEWLINE="postFix = \"_${LTF_DOWN}"

echo ">>> "
echo ">>> "
echo ">>> replacing \"${LTFSHIFT_LINE}\" with: "
echo ">>>    \"${LTFSHIFT_UP_NEWLINE}\"      "
echo ">>>    \"${LTFSHIFT_DOWN_NEWLINE}\"    "
echo ">>> "
echo ">>> replacing \"${DOLTF_LINE}\" with: "
echo ">>>    \"${DOLTF_NEWLINE}\"           "
echo ">>> "
echo ">>> replacing \"${LABEL_LINE}\" with: "
echo ">>>    \"${LABEL_LTF_UP_NEWLINE}\"        "
echo ">>>    \"${LABEL_LTF_DOWN_NEWLINE}\"      "

for f in $LTFFILES; do
    echo ">>> "
    echo ">>> making LTF shifts for $f"
    if grep -q "${DOLTF_LINE}" $f; then
        FUP=`  echo $f | sed "s/${FILEND}/_${LTF_UP}${FILEND}/"`
        FDOWN=`echo $f | sed "s/${FILEND}/_${LTF_DOWN}${FILEND}/"`
        echo ">>> creating file: $FUP"
        echo ">>> creating file: $FDOWN"
        cp $f $FUP
        cp $f $FDOWN
        sed -i "s/${DOLTF_LINE}/${DOLTF_NEWLINE}/" $FUP
        sed -i "s/${DOLTF_LINE}/${DOLTF_NEWLINE}/" $FDOWN
        if grep -q "${LTFSHIFT_LINE}" $f; then
            sed -i "s/${LTFSHIFT_LINE}/${LTFSHIFT_UP_NEWLINE}/"   $FUP
            sed -i "s/${LTFSHIFT_LINE}/${LTFSHIFT_DOWN_NEWLINE}/" $FDOWN
        else echo ">>> WARNING! Could not find \"${LTFSHIFT_LINE}\" line"
        fi
        if grep -q "${LABEL_LINE}" $f; then
            sed -i "s/${LABEL_LINE}/${LABEL_LTF_UP_NEWLINE}/"   $FUP
            sed -i "s/${LABEL_LINE}/${LABEL_LTF_DOWN_NEWLINE}/" $FDOWN          
        else echo ">>> WARNING! Could not find \"${LABEL_LINE}\" line"
        fi
    else echo ">>> WARNING! Could not find \"${DOLTF_LINE}\" line"
    fi
done

echo " "


