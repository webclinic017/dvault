#!/bin/bash
# create venv if it doesn't exist, call the supplied cmd line args once that
# venv is created and activated
venv_dir=${1}
shift
if [ -z "$venv_dir" ] ; then
    >&2 echo "usage: venv_launch.sh <venv_dir> <program> [arg1] [argN] ..."
    exit 1
fi

deactivate &> /dev/null

set -e

if [ ! -d $venv_dir ] ; then
    python3 -m venv $venv_dir
    rm $venv_dir/.venv_launch_double_init_lock
    pip install pip --upgrade
    pip install wheel
fi

. $venv_dir/bin/activate

# chain to call arguments
echo "venv_launch.sh: Activated '$venv_dir', calling: '$1'"
$@
