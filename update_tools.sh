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

CHIPSTER_TOOL_RELOAD=/opt/chipster/toolbox/reload-tools.sh

if [ $LOCAL = $REMOTE ]; then
    : #echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    git pull
elif [ $REMOTE = $BASE ]; then
    echo "Need to push."
    echo "This should not happen."
else
    echo "Diverged"
    echo "This should not happen."
fi

if [ -x $CHIPSTER_TOOL_RELOAD ]; then
  $CHIPSTER_TOOL_RELOAD
fi;
