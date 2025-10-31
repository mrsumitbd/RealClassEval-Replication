
from collections import defaultdict
from Bio import Phylo


class TreeDecorator:

    def __init__(self, tree, taxonomy, seqinfo=None):
        self.tree = Phylo.read(tree, 'newick')
        self.taxonomy = self._read_taxonomy(taxonomy)
        self.seqinfo = self._read_seqinfo(seqinfo)

    def _read_taxonomy(self, taxonomy):
        tax_dict = {}
        with open(taxonomy, 'r') as f:
            for line in f:
                line = line.strip().split('\t')
                tax_dict[line[0]] = line[1].split(';')
        return tax_dict

    def _read_seqinfo(self, seqinfo):
        if seqinfo is None:
            return None
        seqinfo_dict = {}
        with open(seqinfo, 'r') as f:
            for line in f:
                line = line.strip().split('\t')
                seqinfo_dict[line[0]] = line[1:]
        return seqinfo_dict

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for tip in self.tree.get_terminals():
                name = tip.name
                if name in self.taxonomy:
                    f.write(f'{name}\t{";".join(self.taxonomy[name])}\n')

    def _rename(self, node, name):
        node.name = name

    def _get_unique_label(self, label, count_dict):
        if label not in count_dict:
            count_dict[label] = 1
            return label
        else:
            count_dict[label] += 1
            return f'{label}_{count_dict[label]}'

    def decorate(self, output_tree, output_tax, unique_names):
        count_dict = defaultdict(int)
        for node in self.tree.get_nonterminals(order='postorder'):
            children = node.clades
            tax_strings = [self.taxonomy.get(
                child.name, []) for child in children if child.is_terminal()]
            if len(tax_strings) == 0:
                continue
            consensus_tax = self._get_consensus_tax(tax_strings)
            if unique_names:
                label = self._get_unique_label(
                    ';'.join(consensus_tax), count_dict)
            else:
                label = ';'.join(consensus_tax)
            self._rename(node, label)
        Phylo.write(self.tree, output_tree, 'newick')
        self._write_consensus_strings(output_tax)

    def _get_consensus_tax(self, tax_strings):
        if len(tax_strings) == 0:
            return []
        consensus_tax = []
        for i in range(len(tax_strings[0])):
            tax_level = [tax[i] for tax in tax_strings if len(tax) > i]
            if len(set(tax_level)) == 1:
                consensus_tax.append(tax_level[0])
            else:
                break
        return consensus_tax
