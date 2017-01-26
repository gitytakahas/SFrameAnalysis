#! /bin/bash

if [[ $1 == 1 ]]; then
    echo ">>> ST, DY, DY NLO, WW"
    python -u submitSFrame.py -j Background_ST_Izaak.py --nosandbox --useEnv | tee nohup/nohup_ST.log
    python -u submitSFrame.py -j Background_DY_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY.log
    python -u submitSFrame.py -j Background_DY_NLO_Izaak.py     --nosandbox --useEnv | tee nohup/nohup_DY_NLO.log
    python -u submitSFrame.py -j Background_DY_TES1p03_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_TES1p03.log
    python -u submitSFrame.py -j Background_DY_TES0p97_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_TES0p97.log
    python -u submitSFrame.py -j Background_DY_LTF1p03_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_LTF1p03.log
    python -u submitSFrame.py -j Background_DY_LTF0p97_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_LTF0p97.log
    python -u submitSFrame.py -j Background_DY_NLO_TES1p03_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_NLO_TES1p03.log
    python -u submitSFrame.py -j Background_DY_NLO_TES0p97_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_NLO_TES0p97.log
    python -u submitSFrame.py -j Background_DY_NLO_LTF1p03_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_NLO_LTF1p03.log
    python -u submitSFrame.py -j Background_DY_NLO_LTF0p97_Izaak.py --nosandbox --useEnv | tee nohup/nohup_DY_NLO_LTF0p97.log
elif [[ $1 == 2 || $1 == 3 ]]; then
    echo ">>> TT, WJ, WZ, ZZ, Signal, HTT"
    python -u submitSFrame.py -j Background_TT_Izaak.py      --nosandbox --useEnv | tee nohup/nohup_TT.log
    python -u submitSFrame.py -j Background_WJ_Izaak.py      --nosandbox --useEnv | tee nohup/nohup_WJ.log
    python -u submitSFrame.py -j Background_WW_Izaak.py      --nosandbox --useEnv | tee nohup/nohup_WW.log
    python -u submitSFrame.py -j Background_WZ_Izaak.py      --nosandbox --useEnv | tee nohup/nohup_WZ.log
    python -u submitSFrame.py -j Background_ZZ_Izaak.py      --nosandbox --useEnv | tee nohup/nohup_ZZ.log
    python -u submitSFrame.py -j Signal_Izaak.py             --nosandbox --useEnv | tee nohup/nohup_signal.log
#     if [[ $1 == 3 ]]; then
#         echo ">>> Data single muon"
#         python -u submitSFrame.py -j Data_Ele_Izaak.py          --nosandbox --useEnv | tee nohup/nohup_Ele.log
#         python -u submitSFrame.py -j Data_Mu_Izaak.py           --nosandbox --useEnv | tee nohup/nohup_Mu.log
#     fi
    python -u submitSFrame.py -j Background_TT_TES1p03_Izaak.py --nosandbox --useEnv | tee nohup/nohup_TT_TES1p03.log
    python -u submitSFrame.py -j Background_TT_TES0p97_Izaak.py --nosandbox --useEnv | tee nohup/nohup_TT_TES0p97.log
    python -u submitSFrame.py -j Signal_TES1p03_Izaak.py     --nosandbox --useEnv | tee nohup/nohup_signal_TES1p03.log
    python -u submitSFrame.py -j Signal_TES0p97_Izaak.py     --nosandbox --useEnv | tee nohup/nohup_signal_TES0p97.log
    python -u submitSFrame.py -j Signal_HTT_Izaak.py         --nosandbox --useEnv | tee nohup/nohup_HTT.log
    python -u submitSFrame.py -j Signal_HTT_TES1p03_Izaak.py --nosandbox --useEnv | tee nohup/nohup_HTT_TES1p03.log
    python -u submitSFrame.py -j Signal_HTT_TES0p97_Izaak.py --nosandbox --useEnv | tee nohup/nohup_HTT_TES0p97.log
else
    echo ">>> Wrong input! Use 1, 2 or 3."
fi
