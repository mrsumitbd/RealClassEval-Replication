import re
from collections import namedtuple
from plip.basic.supplemental import read, nucleotide_linkage, sort_members_by_importance
from plip.basic import config, logger

class PDBParser:

    def __init__(self, pdbpath, as_string):
        self.as_string = as_string
        self.pdbpath = pdbpath
        self.num_fixed_lines = 0
        self.covlinkage = namedtuple('covlinkage', 'id1 chain1 pos1 conf1 id2 chain2 pos2 conf2')
        self.proteinmap, self.modres, self.covalent, self.altconformations, self.corrected_pdb = self.parse_pdb()

    def parse_pdb(self):
        """Extracts additional information from PDB files.
        I. When reading in a PDB file, OpenBabel numbers ATOMS and HETATOMS continously.
        In PDB files, TER records are also counted, leading to a different numbering system.
        This functions reads in a PDB file and provides a mapping as a dictionary.
        II. Additionally, it returns a list of modified residues.
        III. Furthermore, covalent linkages between ligands and protein residues/other ligands are identified
        IV. Alternative conformations
        """
        if self.as_string:
            fil = self.pdbpath.rstrip('\n').split('\n')
        else:
            f = read(self.pdbpath)
            fil = f.readlines()
            f.close()
        corrected_lines = []
        i, j = (0, 0)
        d = {}
        modres = set()
        covalent = []
        alt = []
        previous_ter = False
        model_dict = {0: list()}
        if not config.NOFIX:
            if not config.PLUGIN_MODE:
                lastnum = 0
                other_models = False
                current_model = 0
                for line in fil:
                    corrected_line, newnum = self.fix_pdbline(line, lastnum)
                    if corrected_line is not None:
                        if corrected_line.startswith('MODEL'):
                            lastnum = 0
                            try:
                                model_num = int(corrected_line[10:14])
                                model_dict[model_num] = list()
                                current_model = model_num
                                if model_num > 1:
                                    other_models = True
                            except ValueError:
                                logger.debug(f'ignoring invalid MODEL entry: {corrected_line}')
                        else:
                            lastnum = newnum
                        model_dict[current_model].append(corrected_line)
                try:
                    if other_models:
                        logger.info(f'selecting model {config.MODEL} for analysis')
                    corrected_pdb = ''.join(model_dict[0])
                    corrected_lines = model_dict[0]
                    if current_model > 0:
                        corrected_pdb += ''.join(model_dict[config.MODEL])
                        corrected_lines += model_dict[config.MODEL]
                except KeyError:
                    corrected_pdb = ''.join(model_dict[1])
                    corrected_lines = model_dict[1]
                    config.MODEL = 1
                    logger.warning('invalid model number specified, using first model instead')
            else:
                corrected_pdb = self.pdbpath
                corrected_lines = fil
        else:
            corrected_pdb = self.pdbpath
            corrected_lines = fil
        for line in corrected_lines:
            if line.startswith(('ATOM', 'HETATM')):
                atomid, location = (int(line[6:11]), line[16])
                location = 'A' if location == ' ' else location
                if location != 'A':
                    alt.append(atomid)
                if not previous_ter:
                    i += 1
                    j += 1
                else:
                    i += 1
                    j += 2
                d[i] = j
                previous_ter = False
            if line.startswith('TER'):
                previous_ter = True
            if line.startswith('MODRES'):
                modres.add(line[12:15].strip())
            if line.startswith('LINK'):
                covalent.append(self.get_linkage(line))
        return (d, modres, covalent, alt, corrected_pdb)

    def fix_pdbline(self, pdbline, lastnum):
        """Fix a PDB line if information is missing."""
        pdbqt_conversion = {'HD': 'H', 'HS': 'H', 'NA': 'N', 'NS': 'N', 'OA': 'O', 'OS': 'O', 'SA': 'S'}
        fixed = False
        new_num = 0
        forbidden_characters = '[^a-zA-Z0-9_]'
        pdbline = pdbline.strip('\n')
        if len(pdbline.strip()) == 0:
            self.num_fixed_lines += 1
            return (None, lastnum)
        if len(pdbline) > 100:
            self.num_fixed_lines += 1
            return (None, lastnum)
        if pdbline.startswith('TER'):
            new_num = lastnum + 1
        if pdbline.startswith('ATOM'):
            new_num = lastnum + 1
            current_num = int(pdbline[6:11])
            resnum = pdbline[22:27].strip()
            resname = pdbline[17:21].strip()
            try:
                int(resnum)
            except ValueError:
                pdbline = pdbline[:22] + '   0 ' + pdbline[27:]
                fixed = True
            if re.match(forbidden_characters, resname.strip()):
                pdbline = pdbline[:17] + 'UNK ' + pdbline[21:]
                fixed = True
            if lastnum + 1 != current_num:
                pdbline = pdbline[:6] + (5 - len(str(new_num))) * ' ' + str(new_num) + ' ' + pdbline[12:]
                fixed = True
            if pdbline[21] == ' ':
                pdbline = pdbline[:21] + 'A' + pdbline[22:]
                fixed = True
            if pdbline.endswith('H'):
                self.num_fixed_lines += 1
                return (None, lastnum)
            for pdbqttype in pdbqt_conversion:
                if pdbline.strip().endswith(pdbqttype):
                    pdbline = pdbline.strip()[:-2] + ' ' + pdbqt_conversion[pdbqttype] + '\n'
                    self.num_fixed_lines += 1
        if pdbline.startswith('HETATM'):
            new_num = lastnum + 1
            try:
                current_num = int(pdbline[6:11])
            except ValueError:
                current_num = None
                logger.debug(f'invalid HETATM entry: {pdbline}')
            if lastnum + 1 != current_num:
                pdbline = pdbline[:6] + (5 - len(str(new_num))) * ' ' + str(new_num) + ' ' + pdbline[12:]
                fixed = True
            if pdbline[21] == ' ':
                pdbline = pdbline[:21] + 'Z' + pdbline[22:]
                fixed = True
            if pdbline[23:26] == '   ':
                pdbline = pdbline[:23] + '999' + pdbline[26:]
                fixed = True
            ligname = pdbline[17:21].strip()
            if len(ligname) > 3:
                pdbline = pdbline[:17] + ligname[:3] + ' ' + pdbline[21:]
                fixed = True
            if re.match(forbidden_characters, ligname.strip()):
                pdbline = pdbline[:17] + 'LIG ' + pdbline[21:]
                fixed = True
            if len(ligname.strip()) == 0:
                pdbline = pdbline[:17] + 'LIG ' + pdbline[21:]
                fixed = True
            if pdbline.endswith('H'):
                self.num_fixed_lines += 1
                return (None, lastnum)
            for pdbqttype in pdbqt_conversion:
                if pdbline.strip().endswith(pdbqttype):
                    pdbline = pdbline.strip()[:-2] + ' ' + pdbqt_conversion[pdbqttype] + ' '
                    self.num_fixed_lines += 1
        self.num_fixed_lines += 1 if fixed else 0
        return (pdbline + '\n', max(new_num, lastnum))

    def get_linkage(self, line):
        """Get the linkage information from a LINK entry PDB line."""
        conf1, id1, chain1, pos1 = (line[16].strip(), line[17:20].strip(), line[21].strip(), int(line[22:26]))
        conf2, id2, chain2, pos2 = (line[46].strip(), line[47:50].strip(), line[51].strip(), int(line[52:56]))
        return self.covlinkage(id1=id1, chain1=chain1, pos1=pos1, conf1=conf1, id2=id2, chain2=chain2, pos2=pos2, conf2=conf2)