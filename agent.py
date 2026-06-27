import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# ============================================
# 1. LLM Setup
# ============================================
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# ============================================
# 2. Search Tool
# ============================================
search_api = SerpAPIWrapper(
    serpapi_api_key=os.getenv("SERPAPI_API_KEY")
)

@tool
def internet_search(query: str) -> str:
    """Search the internet for current information about any topic."""
    return search_api.run(query)

tools = [internet_search]

# ============================================
# 3. Agent Banana
# ============================================
agent = create_react_agent(
    model=llm,
    tools=tools,
)

# ============================================
# 4. Search Function
# ============================================
def search_and_answer(query: str) -> str:
    print(f"\n🔍 Searching for: {query}")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    final_answer = result["messages"][-1].content
    print(f"\n✅ Answer milgaya!")
    return final_answer


# ============================================
# 5. Test
# ============================================
if __name__ == "__main__":
    test_query = "What is the latest news about artificial intelligence in 2025?"
    answer = search_and_answer(test_query)
    print("\n" + "="*50)
    print("FINAL ANSWER:")
    print("="*50)
    print(answer)