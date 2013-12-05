#!/usr/bin/python
# filename: batch_add_json_field.py

import os
import glob
import json
import argparse

parser = argparse.ArgumentParser("Iterates through a JSON file and adds a field to each entry.")
parser.add_argument('-in', dest='input_dir',required=True, help="The input JSON file.")
parser.add_argument('-out', dest='output_dir',required=True, help="The output (updated) JSON file.")
parser.add_argument('-key', dest='key',required=True, help="The key (name) of the new field.")
parser.add_argument('-val', dest='value',required=True, help="The value of the new field.")
args = parser.parse_args()

def list_files(d):
	if os.path.isdir(d):
		expanded_dir = os.path.expanduser(d)
		return sorted(glob.glob(expanded_dir + '/*'))
	else:
		return [d,]

def add_field(in_file, out_dir):
	print '\nProcessing {0}'.format(os.path.basename(in_file))
	out_file = os.path.join(out_dir, os.path.basename(in_file))
	out_handle = open(out_file, 'a')
	open(out_file, 'w').write('')
	count = 0
	for line in open(in_file, 'r'):
		if line == '':
			continue
		else:	
			entry = json.loads(line)
			entry[args.key] = args.value
			out_handle.write(json.dumps(entry) + '\n')
			count += 1
	out_handle.close()
	print 'Done. {0} entries were updated.\n'.format(count)

def main():
	for file in list_files(args.input_dir):
		add_field(file, args.output_dir)

if __name__ == '__main__':
	main()

