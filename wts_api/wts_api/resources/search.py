"""
SW tutorial
~~~~~~~~~~~

Search API
"""
from flask_restful import abort, fields, marshal, Resource

import elasticsearch_dsl

from wts_api.settings import Settings


def abort_on_invalid_terms(terms):
    """Abort if search string is empty"""
    if terms is None:
        abort(400, message="No search terms provided")


def build_search_terms(terms):
    """Build a search string from the GET parameters"""
    return terms.replace('+', ' ')


class Search(Resource):
    """Send search request to Elasticsearch and send the result
    """
    video_fields = {'file': fields.String,
                    'title': fields.String, }

    def get(self, terms=None):
        """
        Return a list of videos matching the supplied terms.

        :arg terms: Search terms
        """
        abort_on_invalid_terms(terms)
        sch = elasticsearch_dsl.Search(index=Settings.get('SEARCH_INDEX'),
                                       doc_type=Settings.get('SEARCH_DOC'))\
                               .query('query_string',
                                      default_field='title',
                                      query=build_search_terms(terms))
        res = sch.execute()
        hits = [{'file': hit.file, 'title': hit.title} for hit in res]

        return marshal(hits, self.video_fields, envelope='search_results')
