#!/bin/sh

# Update self and restart chipster toolbox (if present)

# cd to dir where script is
cd `dirname $0`

# sync remote changes
git fetch

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")
TOOLDIR=/opt/chipster/toolbox/tools

CHIPSTER_TOOL_RELOAD=/opt/chipster/toolbox/reload-tools.sh

if [ $LOCAL = $REMOTE ]; then
    : #echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    git pull
    if [ -d $TOOLDIR ]; then
        rsync -a --delete tools/kielipankki $TOOLDIR
    fi
    if [ -x $CHIPSTER_TOOL_RELOAD ]; then
        $CHIPSTER_TOOL_RELOAD
    fi;
elif [ $REMOTE = $BASE ]; then
    echo "Need to push."
    echo "This should not happen."
else
    echo "Diverged"
    echo "This should not happen."
fi

