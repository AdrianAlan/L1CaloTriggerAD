#!/bin/sh
lli=${LLVMINTERP-lli}
exec $lli \
    /afs/cern.ch/work/a/adpol/L1CaloTriggerAD/synthesis/CaloADTrigger/myproject_prj/solution1/.autopilot/db/a.g.bc ${1+"$@"}
