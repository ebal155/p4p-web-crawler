class dump_separator():
    """This script extracts all the torrents of a given category out of the full kickass data dump"""
    def __init__(self, filename):
        self.filename = filename

    def separate_dump(self, newfile, category):
        with open(self.filename) as f:
            for line in f:
                list_line = line.split("|")

                if len(list_line) == 11:
                    if category in list_line[2]:
                        with open(newfile, "a") as myfile:
                            myfile.write(line)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if "__main__" == __name__:
    filename = "dailydump.txt"  # This file should be the full data damp taken from the kickass API
    dump_separator = dump_separator(filename)
    dump_separator.separate_dump("moviedump.txt", 'Movies')
