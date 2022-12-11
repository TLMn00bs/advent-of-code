#!/bin/bash
here=$(cd $(dirname $BASH_SOURCE) && pwd)
export PYTHONPATH="$here/:$PYTHONPATH"
