##!/bin/bash/

if [[ $1 == 1 ]]; then
  echo ">>> TT, ST, DY, WW"
  python -u submitSFrame.py -j Background_TT_Izaak.py --nosandbox --useEnv | tee nohup/nohup_TT.log
  python -u submitSFrame.py -j Background_ST_Izaak.py --nosandbox --useEnv | tee nohup/nohup_ST.log
  python -u submitSFrame.py -j Background_DY_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY.log
  python -u submitSFrame.py -j Background_WW_Izaak.py --nosandbox --useEnv | tee nohup/nohup_WW.log
elif [[ $1 == 2 || $1 == 3 ]]; then
  echo ">>> WJ, WZ, ZZ, Signal"
  python -u submitSFrame.py -j Background_WJ_Izaak.py --nosandbox --useEnv | tee nohup/nohup_WJ.log
  python -u submitSFrame.py -j Background_WZ_Izaak.py --nosandbox --useEnv | tee nohup/nohup_WZ.log
  python -u submitSFrame.py -j Background_ZZ_Izaak.py --nosandbox --useEnv | tee nohup/nohup_ZZ.log
  python -u submitSFrame.py -j Signal_Izaak.py        --nosandbox --useEnv | tee nohup/nohup_signal.log
  if [[ $1 == 3 ]]; then
    echo ">>> Data single muon"
    python -u submitSFrame.py -j Data_Mu_Izaak.py     --nosandbox --useEnv | tee nohup/nohup_Mu.log
  fi
else
  echo ">>> Wrong input! Use 1 or 2."
fi
