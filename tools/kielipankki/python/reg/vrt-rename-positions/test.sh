# Bash this

TOOL=vrt-rename-positions.py

set -e

# The great-grandparent is chipster_module_path, this being
# .../tools/kielipankki/python/reg/*/test.sh (sane ..., *)

THIS="$(dirname $(readlink -e $0))"
MODS="$(dirname $(dirname $(dirname $THIS)))"

# Sanity clause: given set -e, halts with a message on fail.
readlink -ev "$MODS/python/$TOOL" > /dev/null

cd "$THIS"

rm -fr tmp-*

# First test: no previous names

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
	</sentence>
	</text>
EOF

{
    sed "s:MODS:$MODS:" <<-EOF
	chipster_module_path='MODS'

	old1 = 'V2'
	new1 = 'bar'
	old2 = 'V3'
	new2 = 'baz'
	old3 = ''
	new3 = ''
	old4 = ''
	new4 = ''

	EOF

    cat "$MODS/python/$TOOL"
} | python3

diff chipster-outputs.tsv - <<-EOF
	output.vrt	sorsa.vrt.txt
EOF

diff output.vrt - <<-EOF
	<!-- Positional attributes: V1 bar baz -->
	<text>
	<sentence>
	Foo	foo	V
	!	!	PUNK
	</sentence>
	</text>
EOF

popd > /dev/null

# Second test: has previous names

mkdir tmp-2
pushd tmp-2 > /dev/null

cat > chipster-inputs.tsv <<-EOF
	input.vrt	sorsa.vrt.txt
EOF

cat > input.vrt <<-EOF
	<text>
	<!-- Positional attributes: one two tre -->
	<sentence>
	Foo	foo	V
	!	!	PUNK
	</sentence>
	</text>
EOF

{
    sed "s:MODS:$MODS:" <<-EOF
	chipster_module_path='MODS'

	old1 = ''
	new1 = ''
	old2 = 'tre'
	new2 = 'three'
	old3 = ''
	new3 = ''
	old4 = ''
	new4 = ''

	EOF

    cat "$MODS/python/$TOOL"
} | python3

diff chipster-outputs.tsv - <<-EOF
	output.vrt	sorsa.vrt.txt
EOF

diff output.vrt - <<-EOF
	<!-- Positional attributes: one two three -->
	<text>
	<sentence>
	Foo	foo	V
	!	!	PUNK
	</sentence>
	</text>
EOF

popd > /dev/null

# Should test some error paths and a large number of other possible
# configurations but there are many other things that one should.
