#!/usr/bin/python
# filename: cdr3_distro.py

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from pymongo import MongoClient

parser = argparse.ArgumentParser("For a MongoDB collection, plots the germline divergence against the sequence identity to a given 'subject' sequence.")
parser.add_argument('-d', '--database', dest='db', required=True, help="Name of the MongoDB database to query. Required")
parser.add_argument('-c', '--collection', dest='collection', default=None, help="Name of the MongoDB collection to query. If not provided, all collections in the given database will be processed iteratively.")
parser.add_argument('-o', '--output', dest='output', required=True, help="Output directory figure files. The figure file(s) will be 'output/<db>_<collection>_<standard>.pdf'. Required")
parser.add_argument('-i', '--ip', dest='ip', default='localhost', help="The IP address for the MongoDB server.  Defaults to 'localhost'.")
parser.add_argument('-p', '--port', dest='port', default=27017, help="The port for the MongoDB server.  Defaults to '27017'.")
parser.add_argument('-x', '--chain', dest='chain', default='heavy', choices=['heavy', 'light', 'kappa', 'lambda'], help="The chain type of the subject sequence.  Default is 'heavy'.")
args = parser.parse_args()

def get_collections():
	if args.collection:
		return [args.collection,]
	conn = MongoClient(args.ip, args.port)
	db = conn[args.db]
	collections = db.collection_names()
	collections.remove('system.indexes')
	return sorted(collections)

def get_chain():
	if args.chain == 'light':
		return ['kappa', 'lambda']
	else:
		return [args.chain,]

def query(coll, chain):
#	print "\nProcessing {0} chain sequences from {1}...".format(args.chain, coll)
	conn = MongoClient(args.ip, args.port)
	db = conn[args.db]
	c = db[coll]
	tps = ['d0', 'pv1', 'pv2']
	freqs = np.zeros(len(tps))
	for i, tp in enumerate(tps):
		total_count = c.find({'donor': {'$in': ['31', '32', '33', '34']}, 'chain': {'$in': chain}, 'tp': tp, 'cdr3_len': {'$gt': 0}}).count()
		short_count = c.find({'donor': {'$in': ['31', '32', '33', '34']}, 'chain': {'$in': chain}, 'tp': tp, 'cdr3_len': 5}).count()
#		print tp, short_count, total_count
		if total_count > 0:
			freqs[i] = 100.0 * short_count / total_count
	print coll + '\t' + '\t'.join([str(f) for f in freqs])
	return freqs

def make_figure(data):
	sns.boxplot(data, names=['d0', 'pv1', 'pv2'], color='pastel', join_rm=True)
	plt.title("Frequency of short (5 AA) {0} chain CDR3s".format(args.chain));
	sns.axlabel("", "Frequency (% of total repertoire)")
	plt.show()

def main():
	counts = []
	chain = get_chain()
	for collection in get_collections():
		results = query(collection, chain)
		if results != []:
			counts.append(results)
#		counts.append(query(collection, chain))
	zipped_counts = zip(*counts)
	make_figure(zipped_counts)

if __name__ == '__main__':
	main()