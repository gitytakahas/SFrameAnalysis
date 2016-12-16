#alias sS='source ~/setup_Scripts/setup_SFrame.sh'
#alias cdB='cd ~/analysis/SFrameAnalysis/BatchSubmission' 

tmux new session \;\
  split-window -v \;\
  send-keys 'sS; cdB' C-m \;\
  split-window -h \;\
  send-keys 'sS; cdB' C-m \;\
  #select-pane -t 0 \;\
  #split-window -v \;\
  #send-keys 'sS; cdB' C-m \;\
  #split-window -h \;\
  #send-keys 'sS; cdB' C-m \;\
  select-pane -t 1 \;
