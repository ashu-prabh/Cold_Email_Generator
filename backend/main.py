
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import WebBaseLoader
from .chains import Chain
from .portfolio import Portfolio
from .utils import clean_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    url: str
    tone: str
    cta: str

# Initialize once
chain = Chain()
portfolio = Portfolio()

@app.post("/generate_email")
async def generate_email(request: EmailRequest):
    try:
        # Load and Clean
        loader = WebBaseLoader([request.url])
        data = clean_text(loader.load().pop().page_content)
        
        # Portfolio Load
        portfolio.load_portfolio()
        
        # Extract Jobs
        jobs = chain.extract_jobs(data)
        
        results = []
        for job in jobs:
            skills = job.get('skills', [])
            portfolio_links = portfolio.query_links(skills)
            
            # Industry specific
            industry = chain.identify_industry(job.get('description', ''))
            industry_links = portfolio.query_industry_links(industry)
            
            links = portfolio_links + industry_links
            
            # Write Email
            email = chain.write_mail(job, links, request.tone, request.cta)
            results.append(email)
            
        return {"emails": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Cold Email Generator API is running"}
