import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv", industry_file_path="app/resource/industry_portfolio.csv"):
        self.file_path = file_path
        self.industry_file_path = industry_file_path
        self.data = pd.read_csv(file_path)
        self.industry_data = pd.read_csv(industry_file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
        self.industry_collection = self.chroma_client.get_or_create_collection(name="industry_portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

        if not self.industry_collection.count():
            for _, row in self.industry_data.iterrows():
                self.industry_collection.add(documents=row["Industry"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

    def query_industry_links(self, industry):
        return self.industry_collection.query(query_texts=industry, n_results=1).get('metadatas', [])
