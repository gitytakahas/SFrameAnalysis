
ALL=1

# multiple files
PATTERN="lhe_files/LowMass*.lhe"

# one file
FILE="lhe_files/LowMassDiTau.lhe"
OUTFILE="HTT.root"

if [[ $ALL == 1 ]]; then
  FILES=`ls $PATTERN` #  | xargs -n 1 basename
  PARSE="gROOT->ProcessLine(\".L ./parselhe.C+g\");"
  
  for f in $FILES; do
    OUTFILE=`echo $f | sed "s/.lhe/.root/" | sed "s/lhe_/root_/"`
    PARSE=$PARSE"
          parselhe(\"$f\",\"$OUTFILE\");"
  done
  
  echo ${PARSE}
  root -l -b <<EOF
    ${PARSE}
    .q
EOF
else
  root -l -b <<EOF
    gROOT->ProcessLine(".L ./parselhe.C+g");
    parselhe("$FILE","$OUTFILE")
    .q
EOF
fi

