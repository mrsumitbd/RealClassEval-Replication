from etk.dependencies.date_extractor_resources.constants import singleton_regex, units

class DateRegexGenerator:
    """
    get the final_regex and symbol_list for date_extractor if single regex updates
    d = DateRegexGenerator(singleton_regex, units)
    final_regex = d.final_regex
    symbol_list = d.single_list
    """

    def __init__(self, singleton_regex, units):
        self.singleton_regex = singleton_regex
        self.units = units
        temp = self.generate_all_regexes_by_singletons()
        self.final_regex = temp[0]
        self.symbol_list = temp[1]

    def generate_all_regexes_by_singletons(self):
        all = {}
        for k in self.units.keys():
            unit = self.generate_regex_for_a_unit(self.units[k])
            all[k] = unit
        s = self.singleton_regex['splitters']
        time = '(?:' + all['HOUR']['res'] + ': ?' + all['MIN']['res'] + '(?:: ?' + all['SEC']['res'] + ')?(?:' + all['MARK']['res'] + ')?(?:' + s + all['TZ']['res'] + ')?)'
        st = '(?:' + self.singleton_regex['splitters'] + '|T)?'
        time_reg = '(?:T?' + st + time + 'Z?)?'
        week_reg_post = '(?:' + s + all['W']['res'] + ')?'
        week_reg_pre = '(?:' + all['W']['res'] + s + ')?'
        day_reg_post = '(?:' + s + all['D']['res'] + ')?'
        day_reg_pre = '(?:' + all['D']['res'] + s + ')?'
        year_reg_post = '(?:' + s + all['Y']['res'] + ')?'
        year_reg_pre = '(?:' + all['Y']['res'] + s + ')?'
        pl = 'pattern_list'
        time_pattern = all['HOUR'][pl] + all['MIN'][pl] + all['SEC'][pl] + all['MARK'][pl] + all['TZ'][pl]
        return ({'MDY': '(?<=\\b)(?:(?:' + week_reg_pre + all['M']['res'] + day_reg_post + year_reg_post + week_reg_post + ')' + time_reg + ')(?=\\b)', 'DMY': '(?<=\\b)(?:(?:' + week_reg_pre + day_reg_pre + all['M']['res'] + year_reg_post + week_reg_post + ')' + time_reg + ')(?=\\b)', 'YMD': '(?<=\\b)(?:(?:' + week_reg_pre + year_reg_pre + all['M']['res'] + day_reg_post + week_reg_post + ')' + time_reg + ')(?=\\b)', 'SINGLE_YEAR': '(?<=\\b)(?:(?:' + all['SINGLE_YEAR']['res'] + ')' + time_reg + ')(?=\\b)', 'SINGLE_MONTH': '(?<=\\b)(?:(?:' + all['SINGLE_MONTH']['res'] + ')' + time_reg + ')(?=\\b)', 'SINGLE_WEEK': '(?<=\\b)(?:(?:' + all['SINGLE_WEEK']['res'] + ')' + time_reg + ')(?=\\b)'}, {'MDY': all['W'][pl] + all['M'][pl] + all['D'][pl] + all['Y'][pl] + all['W'][pl] + time_pattern, 'DMY': all['W'][pl] + all['D'][pl] + all['M'][pl] + all['Y'][pl] + all['W'][pl] + time_pattern, 'YMD': all['W'][pl] + all['Y'][pl] + all['M'][pl] + all['D'][pl] + all['W'][pl] + time_pattern, 'SINGLE_YEAR': all['SINGLE_YEAR'][pl] + time_pattern, 'SINGLE_MONTH': all['SINGLE_MONTH'][pl] + time_pattern, 'SINGLE_WEEK': all['SINGLE_WEEK'][pl] + time_pattern})

    def generate_regex_for_a_unit(self, key_list):
        if isinstance(key_list, list):
            if not key_list or len(key_list) == 0:
                return {'res': '', 'pattern_list': []}
            pattern_list = []
            regex_list = []
            for key in key_list:
                if isinstance(key, list):
                    regex = self.singleton_regex[key[0]]
                    if key[0][0] == '%':
                        pattern_list.append(key[0])
                    for sub_key in key[1:]:
                        regex = regex + self.singleton_regex[sub_key]
                        if sub_key[0] == '%':
                            pattern_list.append(sub_key)
                    regex = regex
                    regex_list.append(regex)
                else:
                    regex_list.append(self.singleton_regex[key])
                    if key[0] == '%':
                        pattern_list.append(key)
            if not regex_list or len(regex_list) == 0:
                return {'res': '', 'pattern_list': []}
            res = '(?:' + regex_list[0]
            for r in regex_list[1:]:
                res = res + '|' + r
            res = res + ')'
            return {'res': res, 'pattern_list': pattern_list}
        else:
            return {'res': '(?:' + self.singleton_regex[key_list] + ')', 'pattern_list': [key_list] if key_list[0] == '%' else []}