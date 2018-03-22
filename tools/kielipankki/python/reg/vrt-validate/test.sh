# Bash this

TOOL=vrt-validate.py

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
	input.vrt	sorsa.vrt.txt
EOF

cat > input.vrt <<-EOF
	<text>
	<sentence>
	Foo	foo	V
	!	!	PUNK
	<sentence>
	</text>
EOF

{
    sed "s:MODS:$MODS:" <<-EOF
	chipster_module_path='MODS'

	level = 'error'
	verbosity = 'verbose'

	EOF

    cat "$MODS/python/$TOOL"
} | python3

diff chipster-outputs.tsv - <<-EOF
	report.tsv	re-sorsa.rel.tsv
EOF

diff report.tsv - <<-EOF
	line	kind	level	issue
	5	nest	error	element already open: sentence
	7	nest	error	element not closed: sentence
EOF

popd > /dev/null

# Second test: summary report (error level)

mkdir tmp-2
pushd tmp-2 > /dev/null

cat > chipster-inputs.tsv <<-EOF
	input.vrt	sorsa.vrt.txt
EOF

cat > input.vrt <<-EOF
	<text>
	<!-- Positional attributes: one two wev -->
	<sentence>
	Foo	foo	V
	!	!	PUNK
	<sentence>
	</text>
EOF

{
    sed "s:MODS:$MODS:" <<-EOF
	chipster_module_path='MODS'

	level = 'error'
	verbosity = 'summary'

	EOF

    cat "$MODS/python/$TOOL"
} | python3

diff chipster-outputs.tsv - <<-EOF
	report.tsv	re-sorsa.rel.tsv
EOF

diff report.tsv - <<-EOF
	count	line	kind	level	issue
	1	6	nest	error	element already open: sentence
	1	8	nest	error	element not closed: sentence
EOF

popd > /dev/null
