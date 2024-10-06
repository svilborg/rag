import loguru

loguru.logger.disable("fastembed.embedding")

from qdrant_client import QdrantClient

class Qdrant:
    def __init__(self, url="http://qdrant:6333", model="sentence-transformers/all-MiniLM-L6-v2"):
        self.client = QdrantClient(url=url)
        self.model = model

    def create(self, collection_name, documents, metadata):
        self.client.set_model(self.model)

        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=self.client.get_fastembed_vector_params(on_disk=True),
        )

        self.client.add(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata,
        )

        self.client.close()

    def query(self, collection_name, query_text, limit=2):  
        
        self.client.set_model(self.model)

        search_result = self.client.query(
            collection_name=collection_name,
            query_text=query_text,
            limit=limit
        )
        
        return search_result