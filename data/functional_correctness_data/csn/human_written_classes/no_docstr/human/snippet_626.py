import datetime
from pathlib import Path
import polib
import xml.etree.ElementTree as ET

class Resx2Po:

    def __init__(self, en_resx: Path, translation_resx: Path, code: str, output_po: Path) -> None:
        if not en_resx.is_file():
            msg = f'EN Resx {en_resx.absolute()} not found'
            raise FileNotFoundError(msg)
        if not translation_resx.is_file():
            msg = f'Translation {code} {translation_resx.absolute()} Resx bound not found'
            raise FileNotFoundError(msg)
        self.en_resx = self.resx2dict(en_resx)
        self.translation_resx = self.resx2dict(translation_resx)
        self.code = code
        self.output_po = output_po
        self.generate()

    def resx2dict(self, resx: Path) -> dict[str, str]:
        tree = ET.parse(resx)
        root = tree.getroot()
        translation_table = {}
        for first in root.findall('./data'):
            found_value = first.find('./value')
            if found_value is not None and found_value.text:
                translation_table[first.attrib['name']] = found_value.text
        return translation_table

    def generate(self) -> None:
        po = polib.POFile()
        now = datetime.datetime.now(datetime.timezone.utc)
        po.metadata = {'Project-Id-Version': '1.0', 'Report-Msgid-Bugs-To': 'adam.schubert@sg1-game.net', 'POT-Creation-Date': now.strftime('%Y-%m-%d %H:%M%z'), 'PO-Revision-Date': now.strftime('%Y-%m-%d %H:%M%z'), 'Last-Translator': 'Adam Schubert <adam.schubert@sg1-game.net>', 'Language-Team': '', 'MIME-Version': '1.0', 'Content-Type': 'text/plain; charset=utf-8', 'Content-Transfer-Encoding': '8bit', 'Language': self.code}
        for message_en_id, message_en in self.en_resx.items():
            if message_en_id in self.translation_resx:
                entry = polib.POEntry(msgid=message_en, msgstr=self.translation_resx[message_en_id], comment=message_en_id)
                po.append(entry)
            else:
                log.warning('%s not found in %s resx', message_en_id, self.code)
        po.save(str(self.output_po.absolute()))