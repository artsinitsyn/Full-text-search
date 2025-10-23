from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from opensearchpy import OpenSearch

client = OpenSearch(hosts=[settings.OPENSEARCH_HOST])


class SearchView(APIView):
    def get(self, request):
        q = request.GET.get('q', '')
        genres = request.GET.getlist('genre')
        authors = request.GET.getlist('author')
        year_from = request.GET.get('year_from')
        year_to = request.GET.get('year_to')
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))

        must = []
        if q:
            must.append({
                'multi_match': {
                    'query': q,
                    'fields': [
                        'title^3',
                        'authors^2', 
                        'content'
                    ]
                }
            })

        filter_ = []
        if genres:
            filter_.append({'terms': {'genre.keyword': genres}})
        if authors:
            filter_.append({'terms': {'authors.keyword': authors}})
        if year_from or year_to:
            range_q = {}
            if year_from: range_q['gte'] = int(year_from)
            if year_to: range_q['lte'] = int(year_to)
            filter_.append({'range': {'year': range_q}})

        body = {
            'query': {
                'bool': {
                    'must': must if must else {'match_all': {}},
                    'filter': filter_
                }
            },
            'highlight': {
                'pre_tags': ['<mark>'],
                'post_tags': ['</mark>'],
                'fields': {
                    'content': {},
                    'title': {}
                }
            },
            'aggs': {
                'genres': {'terms': {'field': 'genre.keyword', 'size': 50}},
                'authors': {'terms': {'field': 'authors.keyword', 'size': 200}},
                'years': {'histogram': {'field': 'year', 'interval': 5}}
            },
            'from': (page - 1) * size,
            'size': size
        }

        res = client.search(index="books", body=body)

        hits = []
        for h in res['hits']['hits']:
            src = h['_source']
            src['id'] = h['_id']  # Запоминаем ID книги для /book/{id}
            src['highlight'] = h.get('highlight', {})
            hits.append(src)

        return Response({
            'hits': hits,
            'total': res['hits']['total']['value'],
            'aggs': res['aggregations']
        })

class BookDetailView(APIView):
    def get(self, request, pk):
        try:
            res = client.get(
                index="books",
                id=str(pk)
            )
            return Response(res["_source"])
        except:
            return Response({"error": "Not found"}, status=404)


