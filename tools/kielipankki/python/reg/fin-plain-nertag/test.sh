# Bash this in Taito (tool points to /proj/kieli there)

TOOL=fin-plain-nertag.py

set -e

# The great-grandparent is chipster_module_path, this being
# .../tools/kielipankki/python/reg/*/test.sh (sane ..., *)

THIS="$(dirname $(readlink -e $0))"
MODS="$(dirname $(dirname $(dirname $THIS)))"

# Sanity clause: given set -e, halts with a message on fail.
readlink -ev "$MODS/python/$TOOL" > /dev/null

cd "$THIS"

rm -fr tmp-*

# First test: verbose report (error level)

mkdir tmp-1
pushd tmp-1 > /dev/null

cat > chipster-inputs.tsv <<-EOF
	input.txt	sorsa.txt
EOF

cat > input.vrt <<-EOF
	Saksan jalkapalloliiton päävalmentaja Joachim Löw jatkaa
	joukkueen peräsimessä aina vuoteen 2022 asti.
	Saksan jalkapalloliitto tiedotti tiistaina, että se on
	jatkanut päävalmentaja Joachim Löwin sopimusta kahdella
	vuodella. Näin Löwin sopimus päättyy Qatarin MM-kisojen
	jälkeen vuonna 2022.
EOF

{
    sed "s:MODS:$MODS:" <<-EOF
	chipster_module_path='MODS'

	EOF

    cat "$MODS/python/$TOOL"
} | python3

diff chipster-outputs.tsv - <<-EOF
	output.txt	sorsa-ner.txt
	output.tsv	sorsa-ner.rel.tsv
EOF

popd > /dev/null
