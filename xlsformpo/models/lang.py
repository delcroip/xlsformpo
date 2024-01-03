from polib import POEntry, POFile
import pandas as pd
import gettext

class SingletonLangClass(object):
    languages = None
    entries = []
    po_file = None
    
    def __init__(self, base, filename, langs):
        self.po_file = POFile()
        if not langs:
            raise Exception("no translation detected")
        for lang_code in langs:
            lang =  gettext.translation(filename, f'{base}/locales' , languages=[lang_code])
            lang.install()
            self.add_lang(lang_code, lang)
       
    def __new__(self, base, filename, langs):
        if not hasattr(self, 'instance'):
            self.instance = super(SingletonLangClass, self).__new__(self)

        return self.instance
    
    def add_lang(self, code, lang):
        if self.languages is None:
            self.languages = {}
        self.languages[code] = lang
    
    def get_trads(self, message,  force_dict = False,trad=None):
        if isinstance(message, dict):
            if force_dict:
                return message
            elif trad is not None and trad in message:
                return message[trad]
            return list(message.values())[0]
        message = str(message).strip() 
        if message == '' and (self.languages is None or trad is not None):
            if force_dict:
                return {'default': ''}
            else :
                return ''
            
        if message not in self.entries:
            self.po_file.insert(0,POEntry(msgid = message))
            self.entries.append(message)
        
        if self.languages is None or len(self.languages) == 0:
            if force_dict:
                return {'default': message}
            else :
                return message
        elif trad is not None:
            return self.languages[trad].gettext(message) if len(message)>0 else ''
        else:
            trads = {}
            for code, lang in self.languages.items():
                trads[code]= lang.gettext(message) if message and pd.notna(message) else ''
            return trads

    def get_trads_map(self, col):
        if self.languages is None:
            return {col:col}
        else:
            map = {}
            for code, lang in self.languages.items():
                map[col+'::'+code] = col+'['+code+']'
            
            return map 

    def join_trads(trads_1, trads_2, separator= ' '):
        dict_3 = {**trads_1, **trads_1}
        for key, value in dict_3.items():
            if key in trads_1 and key in trads_2:
                    dict_3[key] = value + separator +  trads_1[key]
        return dict_3       
        
    def to_po_file(self, path):
        self.po_file.save(fpath = path)
        