from Bio import SeqIO
import argparse
import gzip
import itertools

def cli():
	parser = argparse.ArgumentParser(description='Remove resolved duplex reads from simplex file and merge to create final fastq')
	required = parser.add_argument_group('required arguments')
	required.add_argument('-s',"--simplexreads", type=str, required=True,
						help='simplex reads')
	required.add_argument('-d',"--duplexreads", type=str, required=True,
						help='resolved duplex reads')
	required.add_argument('-p',"--pairedlist", type=str, required=True,
						help='list of paired reads')
	args = parser.parse_args()
	print(args)

	return(
		args.simplexreads,
		args.duplexreads,
		args.pairedlist
		)

if __name__=='__main__':
	(simplex,duplex,pairs) = cli()
	with gzip.open(duplex,"rt") as handle:
		duplex_list=[]
		for record in SeqIO.parse(handle, "fastq"):
			duplex_list.append(record.id)
	handle.close()
	
	# check which duplexes in the list were actually recovered
	with open(pairs) as handle:
		saved_duplexes = []
		counter = 0
		for line in handle:
			p_line = line.strip().split(" ")
			counter += 1
			if (p_line[0] in duplex_list) or (p_line[1] in duplex_list):
				saved_duplexes.append(p_line)
	handle.close()

	print("number of listed pairs in original duplex text file ", counter)
	print("number of duplexes in duplex fastq actually recovered ", len(duplex_list))

	# list of reads to remove from simplex fastq
	to_remove = list(itertools.chain.from_iterable(saved_duplexes))

	with gzip.open(simplex,"rt") as shandle:
		counter=0
		new_fastq = []
		for record in SeqIO.parse(shandle, "fastq"):
			counter+=1
			if counter % 10000 == 0:
				print("reads of simplex file processed: ", counter)
			if record.id in to_remove:
				continue
			else:
				new_fastq.append(record)
	shandle.close()

# append all the duplex reads too
	with gzip.open(duplex,"rt") as handle:
		duplex_records=[]
		for record in SeqIO.parse(handle, "fastq"):
			duplex_records.append(record)
	handle.close()

	final_fastq = new_fastq + duplex_records

	with gzip.open("final.fastq.gz", "wt") as output_handle:
		SeqIO.write(final_fastq, output_handle, "fastq")
	output_handle.close()