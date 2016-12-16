#python -u submitSFrame.py -j Signal_VBF.py --nosandbox  --useEnv
#python -u submitSFrame.py -j Signal_VBF_new.py --nosandbox  --useEnv
#python -u submitSFrame.py -j Background_DY_Izaak.py --nosandbox  --useEnv
#nohup python -u submitSFrame.py -j Background_DY_Izaak.py --nosandbox --useEnv > nohup/nohup_DY.log &
#nohup python -u submitSFrame.py -j Background_DY_Izaak_3.py --nosandbox --useEnv > nohup/nohup_DY.log &
nohup python -u submitSFrame.py -j Background_DY_Izaak_normal.py --nosandbox --useEnv > nohup/nohup_DY_nominal.log &
#nohup python -u submitSFrame.py -j Background_WJ_Izaak.py --nosandbox --useEnv > nohup/nohup_W.log &