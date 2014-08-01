#!/usr/bin/python
# filename: batch_add_json_field.py

import os
import glob
import json
import argparse

parser = argparse.ArgumentParser("Iterates through a JSON file and adds a field to each entry.")
parser.add_argument('-in', dest='input_dir',required=True, help="The input JSON file.")
parser.add_argument('-out', dest='output_dir',required=True, help="The output (updated) JSON file.")
args = parser.parse_args()

def list_files(d):
	if os.path.isdir(d):
		expanded_dir = os.path.expanduser(d)
		return sorted(glob.glob(expanded_dir + '/*'))
	else:
		return [d,]

def get_field_contents(in_file):
	info = os.path.basename(in_file).split('_')[0].split('-')
	species = {'h': 'human', 'm': 'mouse'}
	if info[0] in ['male', 'female']:
		donor = ''.join(info[:2])
		timepoint = info[2]
		seq_species = species[info[3][0]]
		chain = info[3][1:3]
	else:
		donor = info[0]
		timepoint = info[1]
		seq_species = species[info[2][0]]
		chain = info[2][1:3]
	return {'donor': donor, 'tp': timepoint, 'species': seq_species}, chain

def add_field(in_file, out_dir):
	print '\nProcessing {0}'.format(os.path.basename(in_file))
	fields, chain = get_field_contents(in_file)
	out_file = os.path.join(out_dir, '{0}_{1}_{2}_{3}.json'.format(fields['donor'], fields['tp'], fields['species'], chain))
	out_handle = open(out_file, 'a')
	open(out_file, 'w').write('')
	count = 0
	for line in open(in_file, 'r'):
		if line == '':
			continue
		else:	
			entry = json.loads(line)
			for f in fields.keys():
				entry[f] = fields[f]
			out_handle.write(json.dumps(entry) + '\n')
			count += 1
	out_handle.close()
	print 'Done. {0} entries were updated.\n'.format(count)

def main():
	for file in list_files(args.input_dir):
		add_field(file, args.output_dir)

if __name__ == '__main__':
	main()

