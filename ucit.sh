#!/bin/sh

if [[ $# -eq 0 ]] ; then
    echo 'No arguments provided, to run ucit tool a directory should be given'
    exit 1
fi
cd $1
PROJDIR=$(pwd)
# User file
USER="$PROJDIR/user.lp"
# Coverage Criterion
COV="$PROJDIR/coverage_criterion.lp"
# Testcase
TEST="$PROJDIR/testcase.lp"
# System Model
MODEL="$PROJDIR/system_model.lp"
# Copy the files to original location
cp $USER $COV $MODEL $TEST ~/citlib/
# Open fresh folders
rm -rf ucit_objects
rm -rf scripts
mkdir -p ucit_objects
mkdir -p scripts
# Go to installation dir
cd ~/citlib
# Generate
python3 list_entities.py
mv ~/citlib/generated.lp $PROJDIR/scripts/list_entities_generated.lp
# Cover
python3 cover_entities.py
# Move results and scripts to project dir
mv ~/citlib/generated.lp $PROJDIR/scripts/cover_entities_generated.lp
mv ~/citlib/entities* ~/citlib/testcase_* $PROJDIR/ucit_objects
mv ~/citlib/generated $PROJDIR/scripts
# Clean up the lib
sh ~/citlib/clean_files.sh
rm -rf ~/citlib/user.lp ~/citlib/coverage_criterion.lp ~/citlib/testcase.lp ~/citlib/system_model.lp
# Go back to project directory
cd $PROJDIR

