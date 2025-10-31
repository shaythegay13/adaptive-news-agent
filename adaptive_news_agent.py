"""
Adaptive News Agent - Demonstrates progressive learning and improvement
Shows how the agent adapts its summaries as it encounters more news.
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from news_fetcher import pull_ai_news


class AdaptiveNewsAgent:
    """Agent that learns and adapts its summaries over time."""
    
    def __init__(self):
        self.knowledge_base: List[str] = []
        self.summaries_history: List[Dict[str, Any]] = []
        self.seen_articles: set = set()
        self.iteration = 0
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if OPENAI_AVAILABLE and self.api_key else None
        
    def fetch_new_articles(self) -> tuple[List[str], List[str]]:
        """Fetch articles and identify which ones are new."""
        all_articles = pull_ai_news()
        new_articles = [a for a in all_articles if a not in self.seen_articles]
        
        # Update knowledge base
        for article in new_articles:
            self.seen_articles.add(article)
            self.knowledge_base.append(article)
        
        return new_articles, all_articles
    
    def generate_summary(self, articles: List[str], is_update: bool = False) -> Dict[str, Any]:
        """Generate a summary with context about what's new."""
        self.iteration += 1
        
        if not articles:
            return {
                "iteration": self.iteration,
                "timestamp": datetime.now().isoformat(),
                "summary": "No new articles found.",
                "new_articles_count": 0,
                "total_knowledge": len(self.knowledge_base),
                "is_update": is_update
            }
        
        # Prepare context
        context = f"This is iteration {self.iteration}. "
        if is_update:
            context += f"You have {len(articles)} NEW articles to incorporate. "
            context += f"Total articles in knowledge base: {len(self.knowledge_base)}. "
        else:
            context += "This is your initial analysis. "
        
        articles_text = "\n\n".join([f"{i+1}. {a}" for i, a in enumerate(articles[:15])])
        
        if self.client:
            try:
                # Generate summary with OpenAI
                messages = [
                    {
                        "role": "system",
                        "content": f"""You are an adaptive technology news analyst. {context}
                        
Your task:
- Provide a concise summary of the technology news
- Identify key themes and trends
- If this is an update, highlight what's NEW or CHANGED compared to previous knowledge
- Rate your confidence in the analysis (0-100%)"""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze these {len(articles)} technology news articles:\n\n{articles_text}"
                    }
                ]
                
                # Add previous summary context if available
                if self.summaries_history and is_update:
                    prev_summary = self.summaries_history[-1]["summary"]
                    messages.append({
                        "role": "assistant",
                        "content": f"Previous summary: {prev_summary[:200]}..."
                    })
                    messages.append({
                        "role": "user",
                        "content": "Now update your analysis with the new articles above. What's different or noteworthy?"
                    })
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=600,
                    temperature=0.7
                )
                
                summary_text = response.choices[0].message.content
                
            except Exception as e:
                summary_text = f"OpenAI Error: {str(e)}\n\nFallback summary of {len(articles)} articles"
        else:
            summary_text = f"No OpenAI API key. Found {len(articles)} articles (iteration {self.iteration})"
        
        result = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "summary": summary_text,
            "new_articles_count": len(articles),
            "total_knowledge": len(self.knowledge_base),
            "is_update": is_update,
            "articles": articles[:5]  # Store first 5 for reference
        }
        
        self.summaries_history.append(result)
        return result
    
    def get_knowledge_vector(self) -> Dict[str, Any]:
        """Get current state of agent's knowledge."""
        return {
            "total_articles": len(self.knowledge_base),
            "iterations": self.iteration,
            "summaries_count": len(self.summaries_history),
            "coverage_topics": self._estimate_topic_coverage(),
            "learning_rate": len(self.knowledge_base) / max(self.iteration, 1)
        }
    
    def _estimate_topic_coverage(self) -> Dict[str, int]:
        """Simple topic estimation based on keywords."""
        topics = {
            "AI/ML": 0,
            "Gaming": 0,
            "Mobile": 0,
            "Cloud": 0,
            "Hardware": 0,
            "Security": 0,
            "Software": 0
        }
        
        keywords = {
            "AI/ML": ["ai", "machine learning", "gpt", "llm", "gemini", "neural"],
            "Gaming": ["game", "gaming", "playstation", "xbox", "nintendo", "steam"],
            "Mobile": ["iphone", "android", "mobile", "smartphone", "app"],
            "Cloud": ["cloud", "aws", "azure", "google cloud"],
            "Hardware": ["chip", "processor", "cpu", "gpu", "hardware"],
            "Security": ["security", "hack", "breach", "privacy", "encryption"],
            "Software": ["software", "update", "release", "version", "patch"]
        }
        
        for article in self.knowledge_base:
            article_lower = article.lower()
            for topic, kws in keywords.items():
                if any(kw in article_lower for kw in kws):
                    topics[topic] += 1
        
        return topics
    
    def print_summary_comparison(self):
        """Print comparison of all summaries."""
        print("\n" + "="*80)
        print("📊 AGENT LEARNING PROGRESSION")
        print("="*80)
        
        for i, summary in enumerate(self.summaries_history):
            print(f"\n{'='*80}")
            print(f"📌 ITERATION {summary['iteration']} {'(UPDATE)' if summary['is_update'] else '(INITIAL)'}")
            print(f"⏰ Time: {summary['timestamp']}")
            print(f"📰 New Articles: {summary['new_articles_count']}")
            print(f"📚 Total Knowledge: {summary['total_knowledge']} articles")
            print(f"{'='*80}")
            print(summary['summary'])
            
            if i < len(self.summaries_history) - 1:
                print("\n" + "→"*40 + " LEARNING " + "→"*40)
        
        print("\n" + "="*80)
        print("✅ FINAL KNOWLEDGE STATE")
        print("="*80)
        vector = self.get_knowledge_vector()
        print(json.dumps(vector, indent=2))
        print("="*80)


def run_adaptive_demo(iterations: int = 3, delay: int = 2):
    """
    Run a demo showing the agent adapting over multiple iterations.
    
    Args:
        iterations: Number of times to fetch and analyze news
        delay: Seconds to wait between iterations (simulates time passing)
    """
    print("\n" + "🤖"*40)
    print("ADAPTIVE NEWS AGENT - PROGRESSIVE LEARNING DEMO")
    print("🤖"*40 + "\n")
    
    agent = AdaptiveNewsAgent()
    
    # Initial fetch and summary
    print("🔍 ITERATION 1: Initial Knowledge Acquisition")
    print("-"*80)
    new_articles, all_articles = agent.fetch_new_articles()
    summary = agent.generate_summary(new_articles, is_update=False)
    
    print(f"\n✅ Acquired {summary['new_articles_count']} articles")
    print(f"\n📊 Knowledge Vector:")
    print(json.dumps(agent.get_knowledge_vector(), indent=2))
    print(f"\n📝 Summary:\n{summary['summary']}")
    
    # Simulate updates
    for i in range(2, iterations + 1):
        print(f"\n\n{'⏳'*40}")
        print(f"Waiting {delay} seconds for new news...")
        print('⏳'*40)
        time.sleep(delay)
        
        print(f"\n🔍 ITERATION {i}: Knowledge Update")
        print("-"*80)
        
        # In a real scenario, this would fetch actually new articles
        # For demo, we'll re-fetch and show what's "new" to the agent
        new_articles, all_articles = agent.fetch_new_articles()
        
        if new_articles:
            summary = agent.generate_summary(new_articles, is_update=True)
            print(f"\n✅ Found {summary['new_articles_count']} NEW articles")
            print(f"\n📊 Updated Knowledge Vector:")
            print(json.dumps(agent.get_knowledge_vector(), indent=2))
            print(f"\n📝 Updated Summary:\n{summary['summary']}")
        else:
            print("ℹ️  No new articles found in this iteration")
    
    # Show complete learning progression
    agent.print_summary_comparison()
    
    # Save history to file
    output_file = "agent_learning_history.json"
    with open(output_file, "w") as f:
        json.dump({
            "knowledge_vector": agent.get_knowledge_vector(),
            "summaries": agent.summaries_history,
            "total_articles": len(agent.knowledge_base)
        }, f, indent=2)
    
    print(f"\n💾 Learning history saved to: {output_file}")


if __name__ == "__main__":
    import sys
    
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    delay = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    print(f"\nRunning adaptive demo with {iterations} iterations, {delay}s delay between iterations\n")
    run_adaptive_demo(iterations=iterations, delay=delay)
