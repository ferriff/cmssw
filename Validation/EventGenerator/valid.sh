#!/bin/bash

# working
cmsDriver.py VALID --filein file:gen.root --fileout file:dqm.root --mc --eventcontent DQM --datatier DQMIO --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --step VALIDATION:genvalid_gj --nThreads 1 --geometry DB:Extended --era Run2_2018 --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

DQMIO2histo.py -in dqm.root -o histos.root
