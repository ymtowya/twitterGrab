#! /bin/bash
echo "start the job"
cd
cd /home/ubuntu/proj/weiboHotTopGrab
python grab_test.py >> ./logs/runLog20211206.txt
echo "job completed"
