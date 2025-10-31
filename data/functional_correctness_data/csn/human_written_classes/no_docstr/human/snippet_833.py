import re
import logging

class Compare:

    def __init__(self):
        pass

    def _compare_hits(self, forward_reads, reverse_reads, file_name, slash_endings):

        def remove_endings(read_list, slash_endings):
            orfm_regex = re.compile('^(\\S+)_(\\d+)_(\\d)_(\\d+)')
            d = {}
            for read in read_list:
                orfm_match = orfm_regex.match(read)
                if orfm_match:
                    if slash_endings:
                        new_read = orfm_match.groups(0)[0][:-2]
                    else:
                        new_read = orfm_match.groups(0)[0]
                elif slash_endings:
                    new_read = read[:-2]
                else:
                    new_read = read
                d[new_read] = read
            return d
        forward_reads = remove_endings(forward_reads, slash_endings)
        reverse_reads = remove_endings(reverse_reads, slash_endings)
        crossover_hits = [x for x in forward_reads.keys() if x in reverse_reads.keys()]
        if len(crossover_hits) > 0:
            logging.info('%s reads found that crossover in %s' % (str(len(crossover_hits)), file_name))
        elif len(crossover_hits) == 0:
            logging.info('%s reads found that crossover in %s, No reads to use!' % (str(len(crossover_hits)), file_name))
        else:
            raise Exception
        return (crossover_hits, forward_reads, reverse_reads)

    def compare_placements(self, forward_gup, reverse_gup, placement_cutoff, slash_endings, base_file):
        crossover, for_dict, rev_dict = self._compare_hits(list(forward_gup.keys()), list(reverse_gup.keys()), base_file, slash_endings)
        comparison_hash = {'trusted_placements': {}}
        for read in crossover:
            f_read = for_dict[read]
            r_read = rev_dict[read]
            if forward_gup.get(f_read) is None or reverse_gup.get(r_read) is None:
                logging.info('Warning: %s was not inserted into tree' % str(f_read))
                continue
            comparison_hash[read] = {}
            comparison_hash['trusted_placements'][read] = []
            if len(forward_gup[f_read]['placement']) == len(reverse_gup[r_read]['placement']):
                comparison_hash[read]['rank_length_match'] = True
            elif len(forward_gup[f_read]['placement']) != len(reverse_gup[r_read]['placement']):
                comparison_hash[read]['rank_length_match'] = False
            else:
                raise Exception('Programming Error: Comparison of placement resolution')
            for idx, (f_rank, r_rank) in enumerate(zip(forward_gup[f_read]['placement'], reverse_gup[r_read]['placement'])):
                if f_rank == r_rank:
                    comparison_hash[read]['all_ranks_match'] = True
                    if comparison_hash[read]['rank_length_match']:
                        comparison_hash['trusted_placements'][read].append(f_rank)
                    elif not comparison_hash[read]['rank_length_match']:
                        if len(forward_gup[f_read]['placement'][idx:]) == 1:
                            comparison_hash['trusted_placements'][read] += reverse_gup[r_read]['placement'][idx:]
                        elif len(reverse_gup[r_read]['placement'][idx:]) == 1:
                            comparison_hash['trusted_placements'][read] += forward_gup[f_read]['placement'][idx:]
                        elif len(forward_gup[f_read]['placement'][idx:]) > 1 and len(reverse_gup[r_read]['placement'][idx:]) > 1:
                            comparison_hash['trusted_placements'][read].append(f_rank)
                        else:
                            raise Exception('Programming Error')
                elif f_rank != r_rank:
                    comparison_hash[read]['all_ranks_match'] = False
                    forward_confidence = forward_gup[f_read]['confidence'][idx]
                    reverse_confidence = reverse_gup[r_read]['confidence'][idx]
                    if float(forward_confidence) > float(reverse_confidence):
                        comparison_hash['trusted_placements'][read] += forward_gup[f_read]['placement'][idx:]
                        break
                    elif float(reverse_confidence) > float(forward_confidence):
                        comparison_hash['trusted_placements'][read] += reverse_gup[r_read]['placement'][idx:]
                        break
                    elif float(reverse_confidence) == float(forward_confidence):
                        break
                    else:
                        raise Exception('Programming Error: Comparing confidence values')
                else:
                    raise Exception('Programming Error: Comparison of placement resolution')
        return comparison_hash