import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()

# ============================================
# 1. LLM Setup
# ============================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# ============================================
# 2. Search Tool - Direct SerpAPI
# ============================================
search_api = SerpAPIWrapper(
    serpapi_api_key=os.getenv("SERPAPI_API_KEY")
)

# ============================================
# 3. Search + Answer Function
# No LangGraph - Direct approach
# ============================================
def search_and_answer(query: str) -> str:
    print(f"\n🔍 Searching for: {query}")

    # Step 1: SerpAPI se search results lo
    search_results = search_api.run(query)

    # Step 2: LLM ko results do aur answer banwao
    prompt = f"""You are a helpful AI assistant. 
Based on the following search results, provide a clear and comprehensive answer to the user's query.

User Query: {query}

Search Results:
{search_results}

Please provide a well-structured and informative answer based on the search results above."""

    response = llm.invoke(prompt)
    final_answer = response.content

    print(f"\n✅ Answer ready!")
    return final_answer


# ============================================
# 4. Test
# ============================================
if __name__ == "__main__":
    test_query = "What is the latest news about artificial intelligence in 2025?"
    answer = search_and_answer(test_query)
    print("\n" + "="*50)
    print("FINAL ANSWER:")
    print("="*50)
    print(answer)