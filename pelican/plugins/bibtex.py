from pelican import signals
"""
Bibtex plugin for Pelican
===========================

This plugin reads a BibTex file and creates a list of articles.

Settings:
---------

Add BIBTEX_FILE to your settings file to define the bibtex file to parse.
"""


class BibTexActivity():
    """
        A class created to parse BibTex
    """
    def __init__(self, generator):
        try:
            from pybtex.database.input import bibtex
            self.parser = bibtex.Parser()
            self.bibtex_file = generator.settings['BIBTEX_FILE']
        except ImportError:
            raise Exception("Unable to find PybTex")

    def fetch(self):
        """
            returns a list of published papers, articles, journals, etc.
        """

        data = self.parser.parse_file(self.bibtex_file)

        years = {}
        for publication in data.entries.keys():
            y = data.entries[publication].fields.get('year')
            if y not in years.keys():
                years[int(y)] = []
            else:
                years[int(y)].append(data.entries[publication])
        years_keys = years.keys()
        years_keys.sort()

        for publication in data.entries.keys():
            y = int(data.entries[publication].fields.get('year'))
            if y in years_keys:
                years[y].append(data.entries[publication])
        return years


def fetch_bibtex_activity(gen, metadata):
    """
        registered handler for the github activity plugin
        it puts in generator.context the html needed to be displayed on a
        template
    """

    if 'BIBTEX_FILE' in gen.settings.keys():
        gen.context['publications'] = gen.plugin_instance.fetch()


def bibtex_parser_initialization(generator):
    """
        Initialization of BibTex parser
    """

    generator.plugin_instance = BibTexActivity(generator)


def register():
    """
        Plugin registration
    """
    signals.article_generator_init.connect(bibtex_parser_initialization)
    signals.article_generate_context.connect(fetch_bibtex_activity)
