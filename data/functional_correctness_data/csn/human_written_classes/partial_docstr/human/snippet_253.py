import pandas as pd
from typing import List, Tuple, Iterable

class _PlayerSearchClient:

    def __init__(self) -> None:
        self.table = get_lookup_table()

    def search(self, last: str, first: str=None, fuzzy: bool=False, ignore_accents: bool=False) -> pd.DataFrame:
        """Lookup playerIDs (MLB AM, bbref, retrosheet, FG) for a given player

        Args:
            last (str, required): Player's last name.
            first (str, optional): Player's first name. Defaults to None.
            fuzzy (bool, optional): In case of typos, returns players with names close to input. Defaults to False.
            ignore_accents (bool, optional): Normalizes accented letters. Defaults to False

        Returns:
            pd.DataFrame: DataFrame of playerIDs, name, years played
        """
        last = last.lower()
        first = first.lower() if first else None
        if ignore_accents:
            last = normalize_accents(last)
            first = normalize_accents(first) if first else None
            self.table['name_last'] = self.table['name_last'].apply(normalize_accents)
            self.table['name_first'] = self.table['name_first'].apply(normalize_accents)
        if first is None:
            results = self.table.loc[self.table['name_last'] == last]
        else:
            results = self.table.loc[(self.table['name_last'] == last) & (self.table['name_first'] == first)]
        results = results.reset_index(drop=True)
        if len(results) == 0 and fuzzy:
            print('No identically matched names found! Returning the 5 most similar names.')
            results = get_closest_names(last=last, first=first, player_table=self.table)
        return results

    def search_list(self, player_list: List[Tuple[str, str]]) -> pd.DataFrame:
        """
        Lookup playerIDs (MLB AM, bbref, retrosheet, FG) for a list of players.

        Args:
            player_list: List of (last, first) tupels.

        Returns:
            pd.DataFrame: DataFrame of playerIDs, name, years played
        """
        results = pd.DataFrame()
        for last, first in player_list:
            results = results.append(self.search(last, first), ignore_index=True)
        return results

    def reverse_lookup(self, player_ids: List[str], key_type: str='mlbam') -> pd.DataFrame:
        """Retrieve a table of player information given a list of player ids

        :param player_ids: list of player ids
        :type player_ids: list
        :param key_type: name of the key type being looked up (one of "mlbam", "retro", "bbref", or "fangraphs")
        :type key_type: str

        :rtype: :class:`pandas.core.frame.DataFrame`
        """
        key_types = ('mlbam', 'retro', 'bbref', 'fangraphs')
        if key_type not in key_types:
            raise ValueError(f'[Key Type: {key_type}] Invalid; Key Type must be one of {key_types}')
        key = f'key_{key_type}'
        results = self.table[self.table[key].isin(player_ids)]
        results = results.reset_index(drop=True)
        return results