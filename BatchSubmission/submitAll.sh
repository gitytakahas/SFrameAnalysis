# -u option to avoid output buffering
#rm -r nohup/nohup_*.log
nohup python -u submitSFrame.py -j Data_Mu_Izaak.py --nosandbox --useEnv > nohup/nohup_Mu.log &
#nohup python -u submitSFrame.py -j Signal_Izaak.py --nosandbox --useEnv > nohup/nohup_Signal.log &
#nohup python -u submitSFrame.py -j Background_TT_Izaak.py --nosandbox --useEnv > nohup/nohup_TT.log &
#nohup python -u submitSFrame.py -j Background_DY_Izaak.py --nosandbox --useEnv > nohup/nohup_DY.log &
#nohup python -u submitSFrame.py -j Background_WW_Izaak.py --nosandbox --useEnv > nohup/nohup_WW.log &
#nohup python -u submitSFrame.py -j Background_WJ_Izaak.py --nosandbox --useEnv > nohup/nohup_WJ.log &
#nohup python -u submitSFrame.py -j Background_WZ_Izaak.py --nosandbox --useEnv > nohup/nohup_WZ.log &
#nohup python -u submitSFrame.py -j Background_ZZ_Izaak.py --nosandbox --useEnv > nohup/nohup_ZZ.log &
#nohup python -u submitSFrame.py -j Background_ST_Izaak.py --nosandbox --useEnv > nohup/nohup_ZZ.log &

#BG="TT DY WW WJ WZ ZZ"
#date > nohup/nohup_PID.log
#for b in $BG; do
#
#  echo ">>> \
#  nohup python -u submitSFrame.py -j "Background_${b}_Izaak.py" --nosandbox --useEnv > "nohup/nohup_${b}".log &"
#  nohup python -u submitSFrame.py -j "Background_${b}_Izaak.py" --nosandbox --useEnv > "nohup/nohup_${b}".log &
#  echo ">>> ${b}\'s nohup PID: ${!}" >> nohup/nohup_PID.log
#
#done


