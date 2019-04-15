# bash this in xvrt-tools to copy files from another repo assuming you
# have that other repo in place and up to date - - this is a temporary
# setup till (relevant) vrt-tools are properly installed.

other=../../../../../konversio/vrt-tools
files=(
    hrt-from-txt
    hrtlib.py
    hrt-tokenize-finnish-hfst
    hrt-tokenize-udpipe
    outsidelib.py
    vrtargslib.py
    vrtcommentlib.py
    vrtdatalib.py
    vrt-finer
    vrt-finpos
    vrtnamelib.py
    vrt-udpipe
)

for f in "${files[@]}"
do
    if test -f "$other/$f" -a -f "$f"
    then
	if cmp --quiet "$other/$f" "$f"
	then
	    echo ok "$f"
	else
	    echo updating "$f"
	    cp "$other/$f" "$f"
	fi
    elif test -f "$other/$f"
    then
	echo adding "$f"
	cp "$other/$f" "$f"
    elif test -f "$f"
    then
	echo orphan "$f"
    else
	echo unknown "$f"
    fi
done
