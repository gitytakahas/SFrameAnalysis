# -u option to avoid output buffering
nohup python -u submitSFrame.py -j QCDHT.py --nosandbox --useEnv > QCDHT.log &
nohup python -u submitSFrame.py -j JetHT74X.py --nosandbox --useEnv > JetHT74X.log &
nohup python -u submitSFrame.py -j WprimeWHqqbb.py --nosandbox --useEnv > WprimeWHqqbb.log &
nohup python -u submitSFrame.py -j ZprimeZHqqbb.py --nosandbox --useEnv > ZprimeZHqqbb.log &
