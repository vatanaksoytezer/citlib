SCRIPTDIR=$(pwd)
cd $1 
PROJDIR=$(pwd)
USER="$PROJDIR/user.lp"
# Coverage Criterion
COV="$PROJDIR/coverage_criterion.lp"
# Testcase
TEST="$PROJDIR/testcase.lp"
# System Model
MODEL="$PROJDIR/system_model.lp"
# Go to installation dir
cd ~/citlib
python3 list_entities.py
python3 cover_entities.py
cd $PROJDIR
mkdir scripts
mv ~/citlib/entities* ~/citlib/testcase_* scripts
