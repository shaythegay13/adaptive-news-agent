"""Simple news summarization agent using LangGraph."""

from typing import TypedDict
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


# Define a simple stub when dependencies are missing
class SimpleGraph:
    """Simple stub graph when LangGraph is not available."""
    def invoke(self, state):
        return {"summary": "Dependencies not available", "submit": True}


def pull_ai_news():
    """Import news fetcher at runtime."""
    try:
        from news_fetcher import pull_ai_news as fetch
        return fetch()
    except Exception as e:
        return [f"Error fetching news: {str(e)}"]


class AgentState(TypedDict):
    """State for the news agent."""
    task: str
    observation: dict
    news_articles: list
    summary: str
    action: dict
    submit: bool


def fetch_news_node(state: AgentState) -> AgentState:
    """Fetch latest AI news."""
    try:
        articles = pull_ai_news()
        state["news_articles"] = articles
        state["action"] = {"type": "fetch", "articles_count": len(articles)}
        return state
    except Exception as e:
        state["news_articles"] = []
        state["action"] = {"type": "error", "message": str(e)}
        return state


def summarize_news_node(state: AgentState) -> AgentState:
    """Summarize the news articles using OpenAI."""
    articles = state.get("news_articles", [])
    
    if not articles:
        state["summary"] = "No news articles found."
        state["submit"] = True
        state["action"] = {"type": "summarize", "summary": state["summary"]}
        return state
    
    # Combine articles (limit to top 15 for API limits)
    news_text = "\n\n".join([f"{i+1}. {article}" for i, article in enumerate(articles[:15])])
    
    # Try to use OpenAI for intelligent summarization
    api_key = os.getenv("OPENAI_API_KEY")
    
    if OPENAI_AVAILABLE and api_key:
        try:
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using the more affordable mini model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that creates concise, engaging summaries of technology news. Identify key themes and highlight the most important stories."
                    },
                    {
                        "role": "user",
                        "content": f"Please summarize these {len(articles)} technology news articles. Group similar topics together and highlight the most significant developments:\n\n{news_text}"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content
            state["summary"] = f"AI-Generated Technology News Summary\n{'='*50}\n\n{summary}\n\n---\nSummarized {len(articles)} articles"
            
        except Exception as e:
            # Fallback if OpenAI fails
            state["summary"] = f"OpenAI Error: {str(e)}\n\nFallback - Raw Articles:\n{news_text}"
    else:
        # Fallback without OpenAI
        reason = "OpenAI not available" if not OPENAI_AVAILABLE else "API key not set"
        state["summary"] = f"Technology News ({reason})\n{'='*50}\n\nFound {len(articles)} articles:\n\n{news_text}"
    
    state["submit"] = True
    state["action"] = {"type": "summarize", "summary": state["summary"]}
    return state


def create_news_graph():
    """Create the LangGraph workflow."""
    if not LANGGRAPH_AVAILABLE:
        return SimpleGraph()
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("fetch_news", fetch_news_node)
    workflow.add_node("summarize", summarize_news_node)
    
    # Define edges
    workflow.set_entry_point("fetch_news")
    workflow.add_edge("fetch_news", "summarize")
    workflow.add_edge("summarize", END)
    
    return workflow.compile()


# Create the graph instance for Atlas to use
news_graph = create_news_graph()
