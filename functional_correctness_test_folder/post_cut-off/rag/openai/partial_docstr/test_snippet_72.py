import tokenize as module_0
import snippet_72 as module_1

def test_case_0():
    var_0 = module_0.maybe()
    assert var_0 == '()?'
    assert module_0.BOM_UTF8 == b'\xef\xbb\xbf'
    assert module_0.tok_name == {0: 'ENDMARKER', 1: 'NAME', 2: 'NUMBER', 3: 'STRING', 4: 'NEWLINE', 5: 'INDENT', 6: 'DEDENT', 7: 'LPAR', 8: 'RPAR', 9: 'LSQB', 10: 'RSQB', 11: 'COLON', 12: 'COMMA', 13: 'SEMI', 14: 'PLUS', 15: 'MINUS', 16: 'STAR', 17: 'SLASH', 18: 'VBAR', 19: 'AMPER', 20: 'LESS', 21: 'GREATER', 22: 'EQUAL', 23: 'DOT', 24: 'PERCENT', 25: 'LBRACE', 26: 'RBRACE', 27: 'EQEQUAL', 28: 'NOTEQUAL', 29: 'LESSEQUAL', 30: 'GREATEREQUAL', 31: 'TILDE', 32: 'CIRCUMFLEX', 33: 'LEFTSHIFT', 34: 'RIGHTSHIFT', 35: 'DOUBLESTAR', 36: 'PLUSEQUAL', 37: 'MINEQUAL', 38: 'STAREQUAL', 39: 'SLASHEQUAL', 40: 'PERCENTEQUAL', 41: 'AMPEREQUAL', 42: 'VBAREQUAL', 43: 'CIRCUMFLEXEQUAL', 44: 'LEFTSHIFTEQUAL', 45: 'RIGHTSHIFTEQUAL', 46: 'DOUBLESTAREQUAL', 47: 'DOUBLESLASH', 48: 'DOUBLESLASHEQUAL', 49: 'AT', 50: 'ATEQUAL', 51: 'RARROW', 52: 'ELLIPSIS', 53: 'COLONEQUAL', 54: 'OP', 55: 'AWAIT', 56: 'ASYNC', 57: 'TYPE_IGNORE', 58: 'TYPE_COMMENT', 59: 'SOFT_KEYWORD', 60: 'ERRORTOKEN', 61: 'COMMENT', 62: 'NL', 63: 'ENCODING', 64: 'N_TOKENS', 256: 'NT_OFFSET'}
    assert module_0.ENDMARKER == 0
    assert module_0.NAME == 1
    assert module_0.NUMBER == 2
    assert module_0.STRING == 3
    assert module_0.NEWLINE == 4
    assert module_0.INDENT == 5
    assert module_0.DEDENT == 6
    assert module_0.LPAR == 7
    assert module_0.RPAR == 8
    assert module_0.LSQB == 9
    assert module_0.RSQB == 10
    assert module_0.COLON == 11
    assert module_0.COMMA == 12
    assert module_0.SEMI == 13
    assert module_0.PLUS == 14
    assert module_0.MINUS == 15
    assert module_0.STAR == 16
    assert module_0.SLASH == 17
    assert module_0.VBAR == 18
    assert module_0.AMPER == 19
    assert module_0.LESS == 20
    assert module_0.GREATER == 21
    assert module_0.EQUAL == 22
    assert module_0.DOT == 23
    assert module_0.PERCENT == 24
    assert module_0.LBRACE == 25
    assert module_0.RBRACE == 26
    assert module_0.EQEQUAL == 27
    assert module_0.NOTEQUAL == 28
    assert module_0.LESSEQUAL == 29
    assert module_0.GREATEREQUAL == 30
    assert module_0.TILDE == 31
    assert module_0.CIRCUMFLEX == 32
    assert module_0.LEFTSHIFT == 33
    assert module_0.RIGHTSHIFT == 34
    assert module_0.DOUBLESTAR == 35
    assert module_0.PLUSEQUAL == 36
    assert module_0.MINEQUAL == 37
    assert module_0.STAREQUAL == 38
    assert module_0.SLASHEQUAL == 39
    assert module_0.PERCENTEQUAL == 40
    assert module_0.AMPEREQUAL == 41
    assert module_0.VBAREQUAL == 42
    assert module_0.CIRCUMFLEXEQUAL == 43
    assert module_0.LEFTSHIFTEQUAL == 44
    assert module_0.RIGHTSHIFTEQUAL == 45
    assert module_0.DOUBLESTAREQUAL == 46
    assert module_0.DOUBLESLASH == 47
    assert module_0.DOUBLESLASHEQUAL == 48
    assert module_0.AT == 49
    assert module_0.ATEQUAL == 50
    assert module_0.RARROW == 51
    assert module_0.ELLIPSIS == 52
    assert module_0.COLONEQUAL == 53
    assert module_0.OP == 54
    assert module_0.AWAIT == 55
    assert module_0.ASYNC == 56
    assert module_0.TYPE_IGNORE == 57
    assert module_0.TYPE_COMMENT == 58
    assert module_0.SOFT_KEYWORD == 59
    assert module_0.ERRORTOKEN == 60
    assert module_0.COMMENT == 61
    assert module_0.NL == 62
    assert module_0.ENCODING == 63
    assert module_0.N_TOKENS == 64
    assert module_0.NT_OFFSET == 256
    assert module_0.EXACT_TOKEN_TYPES == {'!=': 28, '%': 24, '%=': 40, '&': 19, '&=': 41, '(': 7, ')': 8, '*': 16, '**': 35, '**=': 46, '*=': 38, '+': 14, '+=': 36, ',': 12, '-': 15, '-=': 37, '->': 51, '.': 23, '...': 52, '/': 17, '//': 47, '//=': 48, '/=': 39, ':': 11, ':=': 53, ';': 13, '<': 20, '<<': 33, '<<=': 44, '<=': 29, '=': 22, '==': 27, '>': 21, '>=': 30, '>>': 34, '>>=': 45, '@': 49, '@=': 50, '[': 9, ']': 10, '^': 32, '^=': 43, '{': 25, '|': 18, '|=': 42, '}': 26, '~': 31}
    assert f'{type(module_0.cookie_re).__module__}.{type(module_0.cookie_re).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.blank_re).__module__}.{type(module_0.blank_re).__qualname__}' == 're.Pattern'
    assert module_0.Whitespace == '[ \\f\\t]*'
    assert module_0.Comment == '#[^\\r\\n]*'
    assert module_0.Ignore == '[ \\f\\t]*(\\\\\\r?\\n[ \\f\\t]*)*(#[^\\r\\n]*)?'
    assert module_0.Name == '\\w+'
    assert module_0.Hexnumber == '0[xX](?:_?[0-9a-fA-F])+'
    assert module_0.Binnumber == '0[bB](?:_?[01])+'
    assert module_0.Octnumber == '0[oO](?:_?[0-7])+'
    assert module_0.Decnumber == '(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
    assert module_0.Intnumber == '(0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?[0-9])*))'
    assert module_0.Exponent == '[eE][-+]?[0-9](?:_?[0-9])*'
    assert module_0.Pointfloat == '([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?'
    assert module_0.Expfloat == '[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*'
    assert module_0.Floatnumber == '(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)'
    assert module_0.Imagnumber == '([0-9](?:_?[0-9])*[jJ]|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)[jJ])'
    assert module_0.Number == '(([0-9](?:_?[0-9])*[jJ]|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)[jJ])|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)|(0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?[0-9])*)))'
    assert module_0.StringPrefix == '(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)'
    assert module_0.Single == "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
    assert module_0.Double == '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
    assert module_0.Single3 == "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
    assert module_0.Double3 == '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
    assert module_0.Triple == '((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'\'\'|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)""")'
    assert module_0.String == '((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'[^\\n\'\\\\]*(?:\\\\.[^\\n\'\\\\]*)*\'|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*")'
    assert module_0.Special == '(\\~|\\}|\\|=|\\||\\{|\\^=|\\^|\\]|\\[|@=|@|>>=|>>|>=|>|==|=|<=|<<=|<<|<|;|:=|:|/=|//=|//|/|\\.\\.\\.|\\.|\\->|\\-=|\\-|,|\\+=|\\+|\\*=|\\*\\*=|\\*\\*|\\*|\\)|\\(|\\&=|\\&|%=|%|!=)'
    assert module_0.Funny == '(\\r?\\n|(\\~|\\}|\\|=|\\||\\{|\\^=|\\^|\\]|\\[|@=|@|>>=|>>|>=|>|==|=|<=|<<=|<<|<|;|:=|:|/=|//=|//|/|\\.\\.\\.|\\.|\\->|\\-=|\\-|,|\\+=|\\+|\\*=|\\*\\*=|\\*\\*|\\*|\\)|\\(|\\&=|\\&|%=|%|!=))'
    assert module_0.PlainToken == '((([0-9](?:_?[0-9])*[jJ]|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)[jJ])|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)|(0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?[0-9])*)))|(\\r?\\n|(\\~|\\}|\\|=|\\||\\{|\\^=|\\^|\\]|\\[|@=|@|>>=|>>|>=|>|==|=|<=|<<=|<<|<|;|:=|:|/=|//=|//|/|\\.\\.\\.|\\.|\\->|\\-=|\\-|,|\\+=|\\+|\\*=|\\*\\*=|\\*\\*|\\*|\\)|\\(|\\&=|\\&|%=|%|!=))|((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'[^\\n\'\\\\]*(?:\\\\.[^\\n\'\\\\]*)*\'|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*")|\\w+)'
    assert module_0.Token == '[ \\f\\t]*(\\\\\\r?\\n[ \\f\\t]*)*(#[^\\r\\n]*)?((([0-9](?:_?[0-9])*[jJ]|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)[jJ])|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)|(0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?[0-9])*)))|(\\r?\\n|(\\~|\\}|\\|=|\\||\\{|\\^=|\\^|\\]|\\[|@=|@|>>=|>>|>=|>|==|=|<=|<<=|<<|<|;|:=|:|/=|//=|//|/|\\.\\.\\.|\\.|\\->|\\-=|\\-|,|\\+=|\\+|\\*=|\\*\\*=|\\*\\*|\\*|\\)|\\(|\\&=|\\&|%=|%|!=))|((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'[^\\n\'\\\\]*(?:\\\\.[^\\n\'\\\\]*)*\'|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*")|\\w+)'
    assert module_0.ContStr == '((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'[^\\n\'\\\\]*(?:\\\\.[^\\n\'\\\\]*)*(\'|\\\\\\r?\\n)|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*("|\\\\\\r?\\n))'
    assert module_0.PseudoExtras == '(\\\\\\r?\\n|\\Z|#[^\\r\\n]*|((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'\'\'|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)"""))'
    assert module_0.PseudoToken == '[ \\f\\t]*((\\\\\\r?\\n|\\Z|#[^\\r\\n]*|((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'\'\'|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)"""))|(([0-9](?:_?[0-9])*[jJ]|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)[jJ])|(([0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?|\\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)|(0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?[0-9])*)))|(\\r?\\n|(\\~|\\}|\\|=|\\||\\{|\\^=|\\^|\\]|\\[|@=|@|>>=|>>|>=|>|==|=|<=|<<=|<<|<|;|:=|:|/=|//=|//|/|\\.\\.\\.|\\.|\\->|\\-=|\\-|,|\\+=|\\+|\\*=|\\*\\*=|\\*\\*|\\*|\\)|\\(|\\&=|\\&|%=|%|!=))|((|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)\'[^\\n\'\\\\]*(?:\\\\.[^\\n\'\\\\]*)*(\'|\\\\\\r?\\n)|(|rf|rb|B|f|R|Br|BR|fR|rF|Rb|rB|r|F|u|RB|Fr|bR|RF|Rf|fr|U|br|b|FR)"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*("|\\\\\\r?\\n))|\\w+)'
    assert module_0.endpats == {"'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", '"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", '"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "rf'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'rf"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "rf'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'rf"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "rb'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'rb"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "rb'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'rb"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "B'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'B"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "B'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'B"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "f'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'f"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "f'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'f"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "R'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'R"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "R'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'R"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "Br'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'Br"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "Br'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'Br"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "BR'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'BR"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "BR'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'BR"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "fR'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'fR"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "fR'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'fR"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "rF'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'rF"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "rF'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'rF"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "Rb'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'Rb"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "Rb'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'Rb"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "rB'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'rB"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "rB'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'rB"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "r'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'r"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "r'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'r"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "F'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'F"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "F'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'F"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "u'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'u"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "u'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'u"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "RB'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'RB"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "RB'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'RB"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "Fr'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'Fr"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "Fr'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'Fr"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "bR'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'bR"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "bR'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'bR"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "RF'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'RF"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "RF'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'RF"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "Rf'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'Rf"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "Rf'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'Rf"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "fr'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'fr"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "fr'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'fr"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "U'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'U"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "U'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'U"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "br'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'br"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "br'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'br"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "b'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'b"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "b'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'b"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""', "FR'": "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", 'FR"': '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', "FR'''": "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''", 'FR"""': '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'}
    assert module_0.single_quoted == {"r'", "br'", "rb'", 'rb"', "Br'", "fR'", 'F"', "RB'", 'rf"', "U'", 'BR"', 'fr"', 'Fr"', "fr'", "rf'", 'U"', 'br"', 'B"', 'Br"', "rB'", "BR'", "F'", "'", 'bR"', "bR'", "u'", "f'", "Rf'", 'Rf"', 'rB"', "R'", 'R"', '"', "B'", 'RB"', "RF'", 'fR"', 'f"', "Rb'", 'FR"', 'Rb"', "b'", "rF'", "Fr'", 'r"', 'u"', 'b"', 'rF"', 'RF"', "FR'"}
    assert module_0.triple_quoted == {"rB'''", 'F"""', "U'''", "BR'''", 'U"""', "Br'''", 'bR"""', 'rB"""', "Rb'''", "R'''", "RF'''", '"""', 'u"""', 'RB"""', 'BR"""', 'B"""', "B'''", "f'''", "rf'''", "FR'''", "r'''", 'RF"""', "Rf'''", "fR'''", "u'''", "rF'''", 'R"""', "rb'''", 'rF"""', 'fR"""', 'br"""', 'b"""', 'rf"""', "b'''", "bR'''", "RB'''", "fr'''", "br'''", 'rb"""', 'FR"""', 'Fr"""', 'Rb"""', 'Br"""', 'r"""', 'f"""', "F'''", 'Rf"""', "Fr'''", 'fr"""', "'''"}
    assert module_0.t == 'FR'
    assert module_0.u == "FR'''"
    assert module_0.tabsize == 8
    session_agent_0 = module_1.SessionAgent(var_0, var_0, var_0)
    assert f'{type(session_agent_0).__module__}.{type(session_agent_0).__qualname__}' == 'snippet_72.SessionAgent'
    assert session_agent_0.agent_id == '()?'
    assert session_agent_0.state == '()?'
    assert session_agent_0.conversation_manager_state == '()?'
    assert module_1.TYPE_CHECKING is False
    assert f'{type(module_1.SessionAgent.from_agent).__module__}.{type(module_1.SessionAgent.from_agent).__qualname__}' == 'builtins.method'
    assert f'{type(module_1.SessionAgent.from_dict).__module__}.{type(module_1.SessionAgent.from_dict).__qualname__}' == 'builtins.method'

def test_case_1():
    str_0 = "7wA'gWMX]i7OJ'39\n2VF"
    dict_0 = {}
    session_agent_0 = module_1.SessionAgent(str_0, str_0, dict_0, str_0)
    assert f'{type(session_agent_0).__module__}.{type(session_agent_0).__qualname__}' == 'snippet_72.SessionAgent'
    assert session_agent_0.agent_id == "7wA'gWMX]i7OJ'39\n2VF"
    assert session_agent_0.state == "7wA'gWMX]i7OJ'39\n2VF"
    assert session_agent_0.conversation_manager_state == {}
    assert session_agent_0.created_at == "7wA'gWMX]i7OJ'39\n2VF"
    assert module_1.TYPE_CHECKING is False
    assert f'{type(module_1.SessionAgent.from_agent).__module__}.{type(module_1.SessionAgent.from_agent).__qualname__}' == 'builtins.method'
    assert f'{type(module_1.SessionAgent.from_dict).__module__}.{type(module_1.SessionAgent.from_dict).__qualname__}' == 'builtins.method'
    session_agent_0.to_dict()
    session_agent_1 = module_1.SessionAgent(str_0, dict_0, dict_0)
    assert f'{type(session_agent_1).__module__}.{type(session_agent_1).__qualname__}' == 'snippet_72.SessionAgent'
    assert session_agent_1.agent_id == "7wA'gWMX]i7OJ'39\n2VF"
    assert session_agent_1.state == {}
    assert session_agent_1.conversation_manager_state == {}