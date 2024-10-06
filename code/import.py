from bs4 import BeautifulSoup
import pandas as pd
from qdrant import Qdrant
import warnings

warnings.filterwarnings('ignore') 


def build_collection():
    """
    Read data from a CSV file, clean HTML, create metadata and document
    """
    df = pd.read_csv("/data/data.csv")

    df['Description'] = df['Description'].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

    metadata = [
        
        {
            "id": row["ID"],
            "title": row["Title"],
            "description": row["Description"],
            "price": row["Price"]
        } for _, row in df.iterrows()
        
    ]

    documents = (
        df['Title'] + ' \n ' + 
        df['Description'] + '\n' + 
        'Price: ' + df['Price'].astype(str)
        ).tolist()
    
    return documents, metadata


if __name__ == "__main__":
 
    documents, metadata = build_collection()

    Qdrant().create(
        collection_name="products",
        documents=documents,
        metadata=metadata
    )
