import random
import contextlib
import pyparsing as pp

class Parser:

    def __init__(self):
        self.bnf = self.make_bnf()

    def make_bnf(self):
        invVerb = pp.one_of('INV INVENTORY I', caseless=True)
        dropVerb = pp.one_of('DROP LEAVE', caseless=True)
        takeVerb = pp.one_of('TAKE PICKUP', caseless=True) | pp.CaselessLiteral('PICK') + pp.CaselessLiteral('UP')
        moveVerb = pp.one_of('MOVE GO', caseless=True) | pp.Empty()
        useVerb = pp.one_of('USE U', caseless=True)
        openVerb = pp.one_of('OPEN O', caseless=True)
        closeVerb = pp.one_of('CLOSE CL', caseless=True)
        quitVerb = pp.one_of('QUIT Q', caseless=True)
        lookVerb = pp.one_of('LOOK L', caseless=True)
        doorsVerb = pp.CaselessLiteral('DOORS')
        helpVerb = pp.one_of('H HELP ?', caseless=True).set_name('HELP | H | ?')
        itemRef = pp.OneOrMore(pp.Word(pp.alphas)).set_parse_action(self.validate_item_name).setName('item_ref')
        nDir = pp.one_of('N NORTH', caseless=True).set_parse_action(pp.replace_with('N'))
        sDir = pp.one_of('S SOUTH', caseless=True).set_parse_action(pp.replace_with('S'))
        eDir = pp.one_of('E EAST', caseless=True).set_parse_action(pp.replace_with('E'))
        wDir = pp.one_of('W WEST', caseless=True).set_parse_action(pp.replace_with('W'))
        moveDirection = nDir | sDir | eDir | wDir
        invCommand = invVerb
        dropCommand = dropVerb + itemRef('item')
        takeCommand = takeVerb + itemRef('item')
        useCommand = useVerb + itemRef('usedObj') + pp.Opt(pp.one_of('IN ON', caseless=True)) + pp.Opt(itemRef, default=None)('targetObj')
        openCommand = openVerb + itemRef('item')
        closeCommand = closeVerb + itemRef('item')
        moveCommand = (moveVerb | '') + moveDirection('direction')
        quitCommand = quitVerb
        lookCommand = lookVerb
        examineCommand = pp.one_of('EXAMINE EX X', caseless=True) + itemRef('item')
        doorsCommand = doorsVerb.setName('DOORS')
        helpCommand = helpVerb
        invCommand.set_parse_action(InventoryCommand)
        dropCommand.set_parse_action(DropCommand)
        takeCommand.set_parse_action(TakeCommand)
        useCommand.set_parse_action(UseCommand)
        openCommand.set_parse_action(OpenCommand)
        closeCommand.set_parse_action(CloseCommand)
        moveCommand.set_parse_action(MoveCommand)
        quitCommand.set_parse_action(QuitCommand)
        lookCommand.set_parse_action(LookCommand)
        examineCommand.set_parse_action(ExamineCommand)
        doorsCommand.set_parse_action(DoorsCommand)
        helpCommand.set_parse_action(HelpCommand)
        parser = pp.ungroup(invCommand | useCommand | openCommand | closeCommand | dropCommand | takeCommand | moveCommand | lookCommand | examineCommand | doorsCommand | helpCommand | quitCommand)('command').set_name('command')
        with contextlib.suppress(Exception):
            parser.create_diagram('adventure_game_parser_diagram.html', vertical=3, show_groups=True, show_results_names=True)
        return parser

    def validate_item_name(self, s, l, t):
        iname = ' '.join(t)
        if iname not in Item.items:
            raise AppParseException(s, l, f"No such item '{iname}'.")
        return iname

    def parse_cmd(self, cmdstr):
        try:
            ret = self.bnf.parse_string(cmdstr)
            return ret
        except AppParseException as pe:
            print(pe.msg)
        except pp.ParseException as pe:
            print(random.choice(["Sorry, I don't understand that.", 'Huh?', 'Excuse me?', '???', 'What?']))