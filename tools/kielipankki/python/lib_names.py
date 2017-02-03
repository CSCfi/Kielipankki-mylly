import os

def output(output_name, dataset_name):
    '''Use this in the tool script together with some method to map
    input_names to a dataset_name. See extend, insert, below.'''
    with open("chipster-outputs.tsv", "a", encoding = "UTF-8") as out:
        print(output_name, dataset_name, sep = '\t', file = out)

def dataset_name(input_name, *, cash = None):
    '''Returns the corresponding dataset_name that the user actually
    selected. On first call, reads and parser the file where chipster
    put the mapping from input names, which occur in the tool header,
    for this run of the tool.'''

    # https://github.com/chipster/chipster/wiki/TechnicalManual#output-file-names

    if cash is None:
        with open("chipster-inputs.tsv", "r", encoding = "UTF-8") as ins:
            cash = dict(rec.strip('\r\n').split('\t')[:2]
                        for rec in ins
                        if not rec.startswith('#'))

    return cash

sensible_extensions = set('''

   .conll09 .csv .doc .docx .htm .html
   .log
   .odf .ods .org .pdf
   .textgrid .tsv .txt
   .wav .xhtml .xml .zip

'''.split())

def extend(input_name, new):
    '''Replace the filename extension of dataset_name with new. If the
    old extension is not sensible, which is decided by the sole
    discretion of this script, append the new extension to the old
    name.'''

    name = dataset_name(input_name)
    base, ext = os.path.splitext(name)

    if ext.lower in sensible_extensions:
        return base + new
    else:
        return name + new

def insert(input_name, new):
    '''Insert new before the filename extension of dataset_name. If
    the old extension is not sensible, which is decided by the sole
    discretion of this script, append the new extension to the old
    name.'''

    name = dataset_name(input_name)
    base, ext = os.path.splitext(name)

    if ext.lower in sensible_extensions:
        return base + new + ext
    else:
        return name + new
