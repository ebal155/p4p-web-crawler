import os


class block_creator():
    """This script is used to separate the kickass data dump file into smaller blocks"""
    def __init__(self, directory, block_size, current_index, current_num_file):
        self.directory = directory
        self.block_size = block_size
        self.current_index = current_index
        self.current_num_file = current_num_file

    def start(self):
        if not os.path.exists(directory):
            os.mkdir(directory)

        filename = 'moviedump.txt'
        num_lines = file_len(filename)

        print('Number of lines: ' + str(num_lines))

        while(num_lines > self.current_index):  # Keep making blocks until there are no lines left in the main file.
            print("Current Index: " + str(self.current_index))
            print("Current number of files: " + str(self.current_num_file))

            self.separate_blocks(filename)
            self.current_index = self.current_index + self.block_size
            self.current_num_file = self.current_num_file + 1

    def separate_blocks(self, filename):
        """Makes blocks from the dumpfile"""
        count = self.current_index
        newfilename = filename.split(".")[0]  # Name the new block files the same as the current file but with a number added to the end.

        with open(filename) as f:
            lines = f.readlines()

        n = open("./" + self.directory + "/" + newfilename + str(self.current_num_file) + '.txt', 'a')

        for i in range(self.current_index, self.current_index+self.block_size):
            if not i > len(lines):
                if (count > len(lines)):
                    break
                count = count + 1
                if not (i >= len(lines)):
                    n.write(lines[i])
        n.close()


def file_len(fname):
    """Utility method to count number of lines in a file"""
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if "__main__" == __name__:
    directory = 'moviedumpblocks'
    block_creator = block_creator(directory, 250000, 0, 1)
    block_creator.start()
