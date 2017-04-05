# bash this to make a number of similar tools from fiat-omorfi tools;
# omorfi is a best starting point because "omorfi" is distinct enough
# to replace without much reck

while read code lang a Lang
do
    for x in a g
    do
	sed "s/omorfi/$code/g" "fiat-omorfi-$x.py" > "fiat-$lang-$x.py"
	sed -i "s/fiat-$code/fiat-$lang/" "fiat-$lang-$x.py"
	sed -i "s/an Omorfi/$a $Lang/g" "fiat-$lang-$x.py"
	sed -i "s/Omorfi/$Lang/g" "fiat-$lang-$x.py"
    done
done <<EOF
de german a German
en english an English
fi finnish a Finnish
fr french a French
it italian an Italian
sv swedish a Swedish
tr turkish a Turkish
EOF
