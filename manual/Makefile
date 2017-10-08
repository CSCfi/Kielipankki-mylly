# First make a new it.out.html explicitly:
#
# $ make it.out.html
#
# When out of date, it will be made implicitly:
#
# $ make

all : $(wildcard *.out.html)

%.out.html : %.src.html
	bash nobr.sh "$<" > "$@"
