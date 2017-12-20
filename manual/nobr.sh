#! /bin/sh

case $# in
    1) xsltproc nobr.xsl "$1" |
       sed 's/class="nobr"/class="\x0a"/g' ;;
    *) echo bash nobr.sh: want one .src.html filename
       echo bash nobr.sh: got: "$@"
       exit 1;;
esac
