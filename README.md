# XLSFORMPO

opensource tool to translate xlsform using po files instead of the column (the tool will populate the translation in the column).

# Why this tool was developped

XLSForm are great because they enable to work with bad connectivity but also enable using Calc/Exel function (search/replace, index etc.) it support multilingual but the issue with this apporach is the change management of translation is very difficult with a single xls file because:
- it is hard to know what has been changed
- the person that make the form might not know all languages required (utilistion of third party translation service)
- localisation of the form (just changing the label) will have to be redone when a new version of the form is out

# concept / getting started

the "Master" XLSform will have no language or only the reference language

the script will generate the pot files based on the Master XLSForm that will be use as a key for translation, following gettext approach (po files) the key (value în the master xlsform) will be used in case no translation is found.

one will use his prefered translation tool (e.g poeditor) or platform (Transiflex, Lokalise) to make the usable translation files (.mo)

the idea will be to have such file structure (example with fr and en support)

    myxlsform.xlsx
    locales/en/LC_MESSAGES/myxlsform.mo
    locales/fr/LC_MESSAGES/myxlsform.mo

then one will run the script that will  create an "output xlsform" with 2 set of trad in the example 'fr' & 'en'


