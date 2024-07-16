import logging
import os
from typing import Dict, List
import openai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from qdrant_client.http.models import (
    VectorParams,
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
)
from dotenv import load_dotenv 
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "OpenAI client is not set"
logging.info("OpenAI client is set")

EMBEDDING_MODEL= os.getenv("EMBEDDING_MODEL")
assert EMBEDDING_MODEL, "Embedding model is not set"
logging.info("Embedding model is set")


QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
assert QDRANT_API_KEY, "Qdrant API key not set"

QDRANT_API_ENDPOINT=os.getenv("QDRANT_API_ENDPOINT")
assert QDRANT_API_ENDPOINT, "Qdrant api endpoint not set"

"""
Embedding service is used to create embeddings from the text using OpenAI API.
Currently we are using the open ai embeddings but any open sourced embedding models can also be used.
"""


class EmbeddingService:
    """
    Embedding service to get embeddings from the text using OpenAI API.
    """

    def __init__(self):

        self.__openai_client = openai.Client(api_key=OPENAI_API_KEY)
        self.__embedding_model = EMBEDDING_MODEL
        self.__embeddings_cache: Dict[str, List[float]] = {}

    def get_embeddings(self, text: str) -> List[float]:
        """
        Check if the embeddings are already cached.
        If already cached then we do not need to perform the embeddings again.
        We can directly reuse the data from  cache. Currently it's in-memory cache.
        """
        if text in self.__embeddings_cache:
            return self.__embeddings_cache[text]
        else:
            result = self.__openai_client.embeddings.create(
                input=[text], model=self.__embedding_model
            )
            self.__embeddings_cache[text] = result.data[0].embedding
            return self.__embeddings_cache[text]


class QdrantService:
    def __init__(self, url, api_key):
        self.__client = QdrantClient(url=url, api_key=api_key)

    def collection_exists(self, collection_name):
        try:
            response = self.__client.get_collection(collection_name)
            return response is not None
        except Exception as e:
            if "404" in str(e):
                return False
            else:
                raise e

    def create_collection(self, collection_name):

        if self.collection_exists:
            pass
        else:
            self.__client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

    def upsert_points(self, collection_name, points):
        self.__client.upsert(collection_name=collection_name, points=points)

    def search(self, query_embedding, id, limit=2):
        # filter_condition = Filter(
        #     must=[FieldCondition(key="qrId", match=MatchValue(value=id))]
        # )
        return self.__client.search(
            collection_name="sample_collection",
            query_vector=query_embedding,
            limit=limit,
            # query_filter=filter_condition,
        )


class QdrantQueryRepository:
    """
    Search repository is used to initialize the qdrant service and prepare the points.
    It also has the query_text method which is used to search the text.
    """

    def __init__(
        self, embedding_service: EmbeddingService, qdrant_service: QdrantService
    ):
        self.__embedding_service = embedding_service
        self.__qdrant_service = qdrant_service

    """
    Prepare the points from the text and metadata. Metadata includes the front end configuration 
    data for the screens.
    """

    def prepare_points(
        self, texts: List[str], metadata: List[Dict]
    ) -> List[PointStruct]:
        return [
            PointStruct(
                id=idx,
                vector=self.__embedding_service.get_embeddings(text),
                payload={"text": text, **meta},
            )
            for idx, (text, meta) in enumerate(zip(texts, metadata))
        ]

    """
    This function will be called before the start of the FastAPI application server.
    The function initializes the data points, creates the collection, and upserts the static data points.
    They will be later used as cached data for the vector search.
    """

    def initialize_qdrant(self, texts: List[str], metadata: List[Dict]):
        points = self.prepare_points(texts, metadata)
        self.__qdrant_service.create_collection("sample_collection")
        self.__qdrant_service.upsert_points("sample_collection", points)

    def query_text(self, query_text: str, qr_id: str):
        try:
            # Get the embeddings for the query text.
            query_embedding = self.__embedding_service.get_embeddings(query_text)

            # Search the text using the embeddings.
            response = self.__qdrant_service.search(query_embedding, qr_id)
            # print("########################################", response)

            logging.info(f"Query: {query_text}")
            result = []
            for data in response:
                if data.score > 0.5:
                    result.append(
                        {
                            "score": data.score,
                            "text": data.payload["text"],
                            "source": data.payload["source"],
                            "metadata": data.payload,
                        }
                    )
            return result
        except Exception as e:
            logging.error(f"Failed to search: {e}")
            return []


def main():
    api_endpoint = QDRANT_API_ENDPOINT
    open_ai_key = OPENAI_API_KEY
    qdrant_api_key = QDRANT_API_KEY

    # Initialize services
    openai.api_key = open_ai_key
    embedding_service = EmbeddingService()
    qdrant_service = QdrantService(api_endpoint, qdrant_api_key)

    # Initialize repository
    qdrant_repository = QdrantQueryRepository(embedding_service, qdrant_service)

    # Prepare sample data with texts and metadata combined
    data = [
        {
            "text": """    User prompt: Find me events that companies in Pharmaceuticals sector are attending
               SQL query: ```sql
                SELECT e.*
                FROM events e
                INNER JOIN companies c ON e.event_url = c.event_url
                WHERE LOWER(c.company_industry) LIKE '%pharmaceutical%';```\n""",
            "source": "source1",
        },
        {
            "text": """User prompt: I need the email addresses of people working for companies that are attending finance and banking events
    SQL query:  ```sql
                SELECT first_name
                FROM people p
                INNER JOIN companies c ON p.homepage_base_url = c.homepage_base_url
                INNER JOIN events e ON c.event_url = e.event_url
                WHERE LOWER(c.company_industry) LIKE '%finance%' OR LOWER(c.company_industry) LIKE '%banking%';```\n""",
            "source": "source1",
        },
        {
            "text": """User prompt: Find first 10 entries for first name and profession of the people for companies that are attending events in Singapore over the next 12 months and who are Engineer by job title
    SQL query: ```sql
              SELECT p.first_name, p.job_title
              FROM people p
              INNER JOIN companies c ON p.homepage_base_url = c.homepage_base_url
              INNER JOIN events e ON c.event_url = e.event_url
              WHERE e.event_country = 'Singapore'
              AND (e.event_start_date >= DATE('now') AND e.event_start_date <= DATE('now', '+12 months'))
              AND LOWER(p.job_title) LIKE '%engineer%'
              LIMIT 10;```\n """,
            "source": "source1",
        },
        {
            "text": """User prompt: Find sales people for companies that are attending events in Singapore over the next 9 months.
                SQL query:  ```sql
                SELECT DISTINCT p.*
                FROM people p
                INNER JOIN companies c ON p.homepage_base_url = c.homepage_base_url
                INNER JOIN events e ON c.event_url = e.event_url
                WHERE LOWER(c.company_address) LIKE '%singapore%'
                AND (e.event_start_date >= DATE('now') AND e.event_start_date <= DATE('now', '+6 months'))
                AND LOWER(p.job_title) LIKE '%sales%';```\n""",
            "source": "source1",
        },
        {
            "text": """User prompt: Find me companies that are attending Oil & Gas related events over the next 12 months
    SQL query:  ```sql
                SELECT DISTINCT c.company_name
                FROM companies c
                INNER JOIN events e ON c.event_url = e.event_url
                WHERE LOWER(c.company_industry) LIKE '%oil%' AND LOWER(c.company_industry) LIKE '%gas%'
                AND (e.event_start_date >= DATE('now') AND e.event_start_date <= DATE('now', '+5 months'));```\n""",
            "source": "source1",
        },
    ]

    # Separate texts and metadata for initialization
    texts = [item["text"] for item in data]
    metadata = [{k: v for k, v in item.items() if k != "text"} for item in data]

    # Initialize Qdrant collection with sample data
    qdrant_repository.initialize_qdrant(texts, metadata)

    # Perform a sample search
    query_text = "I need the first name of the people who attended the events on oil"
    qr_id = "123"
    search_results = qdrant_repository.query_text(query_text, qr_id)

    # Print the search results
    for result in search_results:
        print(
            f"Score: {result['score']}, Text: {result['text']}, Source: {result['source']}"
        )


if __name__ == "__main__":
    main()
