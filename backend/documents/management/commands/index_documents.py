from django.core.management.base import BaseCommand
from app import settings
from opensearchpy import OpenSearch
from documents.models import Document

class Command(BaseCommand):
    help = 'Index all documents into OpenSearch'

    def handle(self, *args, **options):
        client = OpenSearch(hosts=[settings.OPENSEARCH_HOST])
        index = settings.OPENSEARCH_INDEX

        mapping = {
            'mappings': {
                'properties': {
                    'title': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
                    'authors': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
                    'genre': {'type': 'keyword'},
                    'year': {'type': 'integer'},
                    'content': {'type': 'text'}
                }
            }
        }

        if not client.indices.exists(index=index):
            client.indices.create(index=index, body=mapping)

        for doc in Document.objects.all():
            body = {
                'title': doc.title,
                'authors': doc.authors,
                'genre': doc.genre,
                'year': doc.year,
                'content': doc.content,
            }
            client.index(index=index, id=doc.id, body=body)

        self.stdout.write(self.style.SUCCESS('Indexed documents'))
