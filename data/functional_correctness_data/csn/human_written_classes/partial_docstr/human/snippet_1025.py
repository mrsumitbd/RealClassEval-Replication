from graftm.taxonomy_cleaner import TaxonomyCleaner
import re

class Getaxnseq:

    def _taxonomy_line(self, level_index, taxon_array, taxonomic_level_names):
        if level_index == 0:
            return '%s,Root,%s,%s,%s,%s%s' % (taxon_array[level_index], taxonomic_level_names[level_index], taxon_array[level_index], 'Root', taxon_array[level_index], ''.join([','] * (len(taxonomic_level_names) - (level_index + 1))))
        else:
            return '%s,%s,%s,%s,%s,%s%s' % (taxon_array[level_index], taxon_array[level_index - 1], taxonomic_level_names[level_index], taxon_array[level_index], 'Root', ','.join(taxon_array), ''.join([','] * (len(taxonomic_level_names) - (level_index + 1))))

    def read_taxtastic_taxonomy_and_seqinfo(self, taxonomy_io, seqinfo_io):
        """Read the taxonomy and seqinfo files into a dictionary of
        sequence_name => taxonomy, where the taxonomy is an array of lineages
        given to that sequence.

        Possibly this method is unable to handle the full definition of these
        files? It doesn't return what each of the ranks are, for starters.
        Doesn't deal with duplicate taxon names either.
        """
        lineages = []
        taxon_to_lineage_index = {}
        expected_number_of_fields = None
        for line in taxonomy_io:
            splits = line.strip().split(',')
            if expected_number_of_fields is None:
                expected_number_of_fields = len(splits)
                lineages = [{}] * (expected_number_of_fields - 4)
                continue
            elif len(splits) != expected_number_of_fields:
                raise Exception('Encountered error parsing taxonomy file, expected %i fields but found %i on line: %s' % (expected_number_of_fields, len(splits), line))
            tax_id = splits[0]
            parent_id = splits[1]
            try:
                lineage_index = splits.index('') - 5
            except ValueError:
                lineage_index = len(splits) - 5
            taxon_to_lineage_index[tax_id] = lineage_index
            lineages[lineage_index][tax_id] = parent_id
        taxonomy_dictionary = {}
        for i, line in enumerate(seqinfo_io):
            if i == 0:
                continue
            splits = line.strip().split(',')
            if len(splits) != 2:
                raise Exception('Bad formatting of seqinfo file on this line: %s' % line)
            seq_name = splits[0]
            taxon = splits[1]
            lineage_index = taxon_to_lineage_index[taxon]
            if lineage_index == 0:
                taxonomy_dictionary[seq_name] = []
            else:
                full_taxonomy_rev = []
                while lineage_index > 0:
                    full_taxonomy_rev.append(taxon)
                    taxon = lineages[lineage_index][taxon]
                    lineage_index = lineage_index - 1
                taxonomy_dictionary[seq_name] = list(reversed(full_taxonomy_rev))
        return taxonomy_dictionary

    def write_taxonomy_and_seqinfo_files(self, taxonomies, output_taxonomy_file, output_seqinfo_file):
        """Write out taxonomy and seqinfo files as required by taxtastic
        from known taxonomies

        Parameters
        ----------
        taxonomies:
            hash of taxon_id to array of taxonomic information
        output_taxonomy_file:
            write taxtastic-compatible 'taxonomy' file here
        output_seqinfo_file:
            write taxtastic-compatible 'seqinfo' file here"""
        first_pass_id_and_taxonomies = []
        tc = TaxonomyCleaner()
        max_number_of_ranks = 0
        for taxon_id, tax_split in taxonomies.items():
            for idx, item in enumerate(tax_split):
                tax_split[idx] = re.sub('\\s+', '_', item.strip())
            tax_split = tc.remove_empty_ranks(tax_split)
            first_pass_id_and_taxonomies.append([taxon_id] + tax_split)
            if len(tax_split) > max_number_of_ranks:
                max_number_of_ranks = len(tax_split)
        parents = {}
        known_duplicates = set()
        for j, array in enumerate(first_pass_id_and_taxonomies):
            taxonomy = array[1:]
            for i, tax in enumerate(taxonomy):
                if i == 0:
                    continue
                ancestry = taxonomy[i - 1]
                if tax in parents:
                    if parents[tax] != ancestry:
                        dup = '%s%s' % (parents[tax], ancestry)
                        if dup not in known_duplicates:
                            print(" %s '%s' with multiple parents %s and %s" % (array[0], tax, parents[tax], ancestry))
                            known_duplicates.add(dup)
                        new_name_id = 1
                        new_name = '%s_graftm_%s' % (tax, new_name_id)
                        while new_name in parents and parents[new_name] != ancestry:
                            new_name_id += 1
                            new_name = '%s_graftm_%s' % (tax, new_name_id)
                        first_pass_id_and_taxonomies[j][i + 1] = new_name
                        taxonomy[i] = new_name
                        parents[new_name] = ancestry
                else:
                    parents[tax] = ancestry
        with open(output_seqinfo_file, 'w') as seqout:
            seqout.write('seqname,tax_id\n')
            for array in first_pass_id_and_taxonomies:
                if len(array) == 1:
                    most_specific_taxonomic_affiliation = 'Root'
                else:
                    most_specific_taxonomic_affiliation = array[-1]
                seqout.write('%s,%s\n' % (array[0], most_specific_taxonomic_affiliation))
        noted_taxonomies = set()
        taxonomic_level_names = ['rank_%i' % rank for rank in range(max_number_of_ranks)]
        with open(output_taxonomy_file, 'w') as seqout:
            seqout.write(','.join(['tax_id', 'parent_id', 'rank', 'tax_name', 'root'] + taxonomic_level_names) + '\n')
            seqout.write(','.join(['Root', 'Root', 'root', 'Root', 'Root']) + ''.join([','] * max_number_of_ranks) + '\n')
            for array in first_pass_id_and_taxonomies:
                taxons = array[1:]
                for i, tax in enumerate(taxons):
                    line = self._taxonomy_line(i, taxons[:i + 1], taxonomic_level_names)
                    if line not in noted_taxonomies:
                        seqout.write(line + '\n')
                        noted_taxonomies.add(line)