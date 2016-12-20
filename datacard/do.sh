#for a in $(seq 1 30)
for a in $(seq 31 50)
do
#    echo $a
#    python draw_tes_scan.py m${a} & 
#    python draw_tes_scan.py ${a} &
    python draw_tes_scan_m_2.py m${a} & 
    python draw_tes_scan_m_2.py ${a} &
done

#python draw_tes_scan.py 0 &
#python draw_tes_scan_m_2.py 0 &


