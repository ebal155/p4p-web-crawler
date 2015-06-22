import os

def separate_blocks(block_size, index, num_file):

	count = index

	with open('moviedump.txt') as f:
		lines = f.readlines()

	n = open('./moviedumpblocks/test' + str(num_file) + '.txt','a')

	for i in range (index, index+block_size):
		if not i > len(lines):
			if (count > len(lines)):
				break
			count = count + 1
			if not (i >= len(lines)):
				n.write(lines[i])

	print(count)
	n.close()	

def main():
	directory = 'moviedumpblocks'

	if not os.path.exists(directory):
		os.mkdir(directory)

	block_size = 250000
	current_index = 0
	current_num_file = 1
	num_lines = file_len('moviedump.txt')

	print('Number of lines: ' + str(num_lines))

	while (num_lines > current_index):

		print("Current Index: " + str(current_index))
		print("Current number of files: " + str(current_num_file))

		separate_blocks(block_size, current_index, current_num_file)
		current_index = current_index + block_size
		current_num_file = current_num_file + 1


def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

if __name__ == "__main__": main()	