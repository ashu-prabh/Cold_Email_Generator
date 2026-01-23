from app.chains import Chain
from app.portfolio import Portfolio

def test_backend():
    print("Initializing Chain and Portfolio...")
    try:
        chain = Chain()
        portfolio = Portfolio()
        portfolio.load_portfolio()
        print("Initialization successful.")
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    job_desc = """
    We are looking for a Software Engineer to join our Retail team.
    Skills: Python, React, Cloud.
    """
    
    print("\nTesting Industry Identification...")
    try:
        industry = chain.identify_industry(job_desc)
        print(f"Identified Industry: {industry}")
    except Exception as e:
        print(f"Industry Identification failed: {e}")

    print("\nTesting Portfolio Query...")
    try:
        industry_links = portfolio.query_industry_links([industry])
        print(f"Industry Links: {industry_links}")
        
        tech_links = portfolio.query_links(["Python", "React"])
        print(f"Tech Links: {tech_links}")
        
        all_links = tech_links + industry_links
    except Exception as e:
        print(f"Portfolio Query failed: {e}")
        return

    print("\nTesting Email Generation...")
    try:
        email = chain.write_mail(job_desc, all_links, tone="Witty", call_to_action="Lets catch up")
        print("Email generated successfully!")
        print("-" * 50)
        print(email[:200] + "...")
        print("-" * 50)
    except Exception as e:
        print(f"Email Generation failed: {e}")

if __name__ == "__main__":
    test_backend()
