## This script requires that FASTA files have first been renamed according to the following format in the header:
# >_genus_species_geneID
# For example, a FASTA header formatted for this script should look like this:
# >_Eschericia_coli_6517891
# Reformatting can be done using the following script available in the Schoeffler Lab GitHub repository:
# name_grabber_jgiformat_public.py
# With a header formatted as above, the script can accept a list of gene IDs and pull out only those sequecnes into a new FASTA file.
# This is useful to partition an alignment into designated subsets.
# Partitioning is a necessary step in the SWiCAM analysis pipeline. 

# The lines below will read in the FASTA format set of sequences and the list of sequences to partition. 

fastafile = open('outputfasta.fa', 'r')
subsetfile = open('subset_list.txt', 'r')

# Be sure your subset list has no "enter" or newline after the last name.

# This function will create a list of lists
def sequence_splitter(seqfiles):
	list_of_seqlists = []
	for line in seqfiles:
		if '>' in line:
			indseqlist = []
			indseqlist.append(line)
		if '>' not in line:
			indseqlist.append(line)
		if '>' in line and indseqlist != []:
			list_of_seqlists.append(indseqlist)
	return list_of_seqlists
		
# This will create a list of organism names
# from the subset file 

subset_list = []
for line in subsetfile:
	stripped_line = line.rstrip('\n')
	subset_list.append(stripped_line)

print(subset_list)

# This function will take each alignment list from the list of lists
# and turn it into a single two-element list.
# The first element will be a string with organism and gene numbers and names.
# The second element will be a list of individual amino acids.

def indseq_list(list_of_seqs, seq_index):

	# grab the desired sequence
	starter_sequence = list_of_seqs[seq_index]

	# turn the lines into a list of amino acids
	number_of_lines = len(starter_sequence)
	counter = 1
	seq_list = []
	while counter < number_of_lines:
		stripped_line = starter_sequence[counter].rstrip('\n')
		line_list = list(stripped_line)
		seq_list = seq_list + line_list
		counter = counter + 1

	name = starter_sequence[0]
	name_and_seq_list = [name, seq_list]	
	return name_and_seq_list

# The command below calls the function to create the list of lists

full_seq_list = sequence_splitter(fastafile)


# The code below creates a dictionary of all sequences in the inputted file
# If a sequence header has not been properly reformmated, the code could skip it--beware!

seq_dictionary = {}
number_of_sequences = len(full_seq_list)
seq_counter = 0
while seq_counter < number_of_sequences:
	seq_name_aa_list = indseq_list(full_seq_list,seq_counter)
	if seq_name_aa_list != ['null','null']:
		seq_dictionary[seq_name_aa_list[0]] = seq_name_aa_list[1]
	seq_counter = seq_counter + 1


# This code extracts only designated organisms

orgnames = seq_dictionary.keys()
print(orgnames)

subset_seq_dictionary = {}
for subset_ind in subset_list:
	for org in orgnames:
		orglist = org.split('_')
		genus_from_dic = orglist[1]
		species_from_dic = orglist[2]
		genenum_from_dic = orglist[3].rstrip('\n')
		if genenum_from_dic == subset_ind:
			subset_seq_dictionary[org]=seq_dictionary[org] 

# This code will print the alignment dictionary to a FASTA file

outfile = open('subset_fasta.fa', 'w')
for seq in subset_seq_dictionary:
	outfile.write(seq)
#	outfile.write('\n')
	for aa in seq_dictionary[seq]:
		outfile.write(aa)
	outfile.write('\n\n')


	
	
 

