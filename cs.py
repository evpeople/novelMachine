#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def iob():
    htas = open("logg.txt","w")
    htas.write(" qing li ")
    htas.close


sched = BlockingScheduler()
sched.add_job(iob, 'interval', seconds=86400)
sched.start()
