from typing import Dict, Optional


class Chapter:
    """изучаемый раздел знаний"""
    description: str = ''

    def __init__(self, atr_dict: dict[str, str]):
        self.description = atr_dict['description']

    def save(self, name : Optional[str] = None):
        atr_dict = dict()
        if name is not None:
            atr_dict['name'] = name
        atr_dict['description'] = self.description
        return atr_dict



chapter_dict: Dict[str, Chapter] = dict()

