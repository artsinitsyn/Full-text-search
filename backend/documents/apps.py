from django.apps import AppConfig
from django.conf import settings
from opensearchpy import OpenSearch, NotFoundError

class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documents'

    def ready(self):
        client = OpenSearch(hosts=[settings.OPENSEARCH_HOST])
        index_name = settings.OPENSEARCH_INDEX

        # Проверяем наличие индекса, если нет — создаём
        try:
            if not client.indices.exists(index=index_name):
                client.indices.create(
                    index=index_name,
                    body={
                        "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 0
                        },
                        "mappings": {
                            "properties": {
                                "title":    { "type": "text" },
                                "authors":  { "type": "text" },
                                "genre":    { "type": "keyword" },
                                "year":     { "type": "integer" },
                                "content":  { "type": "text" }
                            }
                        }
                    }
                )
                print(f" Индекс '{index_name}' успешно создан.")
        except Exception as e:
            print(f" Не удалось создать индекс '{index_name}': {e}")

