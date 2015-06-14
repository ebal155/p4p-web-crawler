dump = "dailydump.txt"

#TV
#Applications
#Movies

def get_movies(newfile):
	with open(dump) as f:
		for line in f:
			list_line = line.split("|")	

			if len(list_line) == 11:
				if 'Movies' in list_line[2]:
					with open(newfile, "a") as myfile:
						myfile.write(line)

def main():
	get_movies("moviedump.txt")
	print(file_len("appdump.txt"))


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == "__main__": main()