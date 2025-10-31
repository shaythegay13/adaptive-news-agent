"""
Temporal News Agent - Tracks trends and learns patterns over time
Analyzes how topics evolve and identifies significant changes
"""

import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from news_fetcher import pull_ai_news


class TemporalNewsAgent:
    """Agent that learns temporal patterns and trends in news."""
    
    def __init__(self):
        self.knowledge_base: List[Dict[str, Any]] = []  # Articles with timestamps
        self.topic_timeline: Dict[str, List[Dict]] = {}  # Topic -> timeline
        self.learned_patterns: Dict[str, Any] = {
            "trending_up": [],
            "trending_down": [],
            "emerging_topics": [],
            "persistent_themes": [],
            "volatility_scores": {}
        }
        self.summaries_history: List[Dict[str, Any]] = []
        self.seen_articles: Set[str] = set()
        self.iteration = 0
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if OPENAI_AVAILABLE and self.api_key else None
        
    def fetch_new_articles(self) -> tuple[List[str], List[str]]:
        """Fetch articles and identify which ones are new."""
        all_articles = pull_ai_news()
        new_articles = [a for a in all_articles if a not in self.seen_articles]
        
        # Update knowledge base with timestamps
        timestamp = datetime.now()
        for article in new_articles:
            self.seen_articles.add(article)
            self.knowledge_base.append({
                "content": article,
                "timestamp": timestamp.isoformat(),
                "iteration": self.iteration + 1
            })
        
        return new_articles, all_articles
    
    def analyze_temporal_patterns(self) -> Dict[str, Any]:
        """Analyze how topics are changing over time."""
        if not self.knowledge_base:
            return {}
        
        # Get topic counts per iteration
        topics_by_iteration = {}
        for article in self.knowledge_base:
            iteration = article["iteration"]
            if iteration not in topics_by_iteration:
                topics_by_iteration[iteration] = Counter()
            
            # Extract topics from article
            topics = self._extract_topics(article["content"])
            for topic in topics:
                topics_by_iteration[iteration][topic] += 1
        
        # Analyze trends
        all_topics = set()
        for counts in topics_by_iteration.values():
            all_topics.update(counts.keys())
        
        trends = {
            "trending_up": [],
            "trending_down": [],
            "stable": [],
            "emerging": [],
            "declining": []
        }
        
        iterations = sorted(topics_by_iteration.keys())
        if len(iterations) >= 2:
            prev_iter = iterations[-2]
            curr_iter = iterations[-1]
            
            prev_counts = topics_by_iteration[prev_iter]
            curr_counts = topics_by_iteration[curr_iter]
            
            for topic in all_topics:
                prev = prev_counts.get(topic, 0)
                curr = curr_counts.get(topic, 0)
                
                if prev == 0 and curr > 0:
                    trends["emerging"].append(topic)
                elif prev > 0 and curr == 0:
                    trends["declining"].append(topic)
                elif curr > prev:
                    trends["trending_up"].append(topic)
                elif curr < prev:
                    trends["trending_down"].append(topic)
                else:
                    trends["stable"].append(topic)
        
        # Update learned patterns
        self.learned_patterns.update(trends)
        
        return {
            "trends": trends,
            "topic_counts": topics_by_iteration,
            "total_unique_topics": len(all_topics),
            "iterations_analyzed": len(iterations)
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from article text using keywords."""
        topics = []
        text_lower = text.lower()
        
        topic_keywords = {
            "AI/ML": ["ai", "artificial intelligence", "machine learning", "gpt", "llm", "gemini", "neural", "chatgpt"],
            "Gaming": ["game", "gaming", "playstation", "xbox", "nintendo", "steam", "esports", "ps5"],
            "Mobile": ["iphone", "android", "mobile", "smartphone", "app", "ios"],
            "Cloud": ["cloud", "aws", "azure", "google cloud", "saas"],
            "Hardware": ["chip", "processor", "cpu", "gpu", "hardware", "chipset"],
            "Security": ["security", "hack", "breach", "privacy", "encryption", "cyber"],
            "Software": ["software", "update", "release", "version", "patch"],
            "VR/AR": ["vr", "ar", "virtual reality", "augmented reality", "metaverse"],
            "Apple": ["apple", "iphone", "ipad", "mac", "ios"],
            "Google": ["google", "android", "chrome", "pixel"],
            "Microsoft": ["microsoft", "windows", "xbox", "azure"],
            "Social Media": ["twitter", "facebook", "instagram", "tiktok", "social"],
            "Blockchain": ["blockchain", "crypto", "bitcoin", "nft", "web3"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)
        
        return topics if topics else ["Other"]
    
    def generate_temporal_summary(self, new_articles: List[str], temporal_analysis: Dict) -> Dict[str, Any]:
        """Generate a summary that highlights temporal patterns and learning."""
        self.iteration += 1
        
        if not new_articles:
            return {
                "iteration": self.iteration,
                "timestamp": datetime.now().isoformat(),
                "summary": "No new articles found.",
                "new_articles_count": 0,
                "total_knowledge": len(self.knowledge_base),
                "temporal_insights": None
            }
        
        # Prepare context with temporal awareness
        trends = temporal_analysis.get("trends", {})
        
        context = f"""You are a temporal news analyst on iteration {self.iteration}.
        
TEMPORAL CONTEXT:
- Total articles in knowledge base: {len(self.knowledge_base)}
- New articles this iteration: {len(new_articles)}
- Iterations completed: {self.iteration}

TREND ANALYSIS:
- Emerging topics: {', '.join(trends.get('emerging', [])) or 'None'}
- Declining topics: {', '.join(trends.get('declining', [])) or 'None'}  
- Trending up: {', '.join(trends.get('trending_up', [])) or 'None'}
- Trending down: {', '.join(trends.get('trending_down', [])) or 'None'}

YOUR LEARNING FOCUS:
1. Identify which stories represent actual TRENDS vs one-off events
2. Note patterns across iterations (recurring themes)
3. Highlight SIGNIFICANT changes (not just noise)
4. Build understanding of what topics matter over time"""

        articles_text = "\n\n".join([f"{i+1}. {a}" for i, a in enumerate(new_articles[:15])])
        
        if self.client:
            try:
                messages = [
                    {
                        "role": "system",
                        "content": context
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze these {len(new_articles)} NEW technology articles:

{articles_text}

Focus on:
1. What's genuinely NEW or CHANGED
2. How this fits with previous trends
3. Which stories suggest lasting trends vs temporary noise
4. What patterns you're learning to recognize

Be specific about temporal changes and your evolving understanding."""
                    }
                ]
                
                # Add previous context if available
                if self.summaries_history:
                    prev = self.summaries_history[-1]
                    messages.append({
                        "role": "assistant",
                        "content": f"Previous iteration found: {prev.get('key_insight', 'N/A')}"
                    })
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=700,
                    temperature=0.7
                )
                
                summary_text = response.choices[0].message.content
                
            except Exception as e:
                summary_text = f"OpenAI Error: {str(e)}\n\nTemporal analysis: {json.dumps(trends, indent=2)}"
        else:
            summary_text = f"No OpenAI. Trends: {json.dumps(trends, indent=2)}"
        
        # Extract a key insight for next iteration
        key_insight = self._extract_key_insight(summary_text, trends)
        
        result = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "summary": summary_text,
            "new_articles_count": len(new_articles),
            "total_knowledge": len(self.knowledge_base),
            "temporal_insights": temporal_analysis,
            "key_insight": key_insight,
            "learned_patterns": self.learned_patterns
        }
        
        self.summaries_history.append(result)
        return result
    
    def _extract_key_insight(self, summary: str, trends: Dict) -> str:
        """Extract key insight from summary for memory."""
        # Simple extraction - could be enhanced
        emerging = trends.get("emerging", [])
        if emerging:
            return f"Emerging topics: {', '.join(emerging[:3])}"
        
        trending_up = trends.get("trending_up", [])
        if trending_up:
            return f"Trending up: {', '.join(trending_up[:3])}"
        
        return "Monitoring for new patterns"
    
    def get_learning_state(self) -> Dict[str, Any]:
        """Get current learning state with temporal awareness."""
        topic_distribution = Counter()
        for article in self.knowledge_base:
            topics = self._extract_topics(article["content"])
            topic_distribution.update(topics)
        
        return {
            "total_articles": len(self.knowledge_base),
            "iterations": self.iteration,
            "summaries_count": len(self.summaries_history),
            "topic_distribution": dict(topic_distribution),
            "learned_patterns": self.learned_patterns,
            "learning_maturity": min(100, (self.iteration / 10) * 100),
            "temporal_span_hours": self._calculate_temporal_span()
        }
    
    def _calculate_temporal_span(self) -> float:
        """Calculate how much time the knowledge base spans."""
        if len(self.knowledge_base) < 2:
            return 0.0
        
        timestamps = [datetime.fromisoformat(a["timestamp"]) for a in self.knowledge_base]
        span = max(timestamps) - min(timestamps)
        return span.total_seconds() / 3600  # Convert to hours
    
    def print_temporal_analysis(self):
        """Print detailed temporal analysis."""
        print("\n" + "="*80)
        print("🕐 TEMPORAL LEARNING ANALYSIS")
        print("="*80)
        
        for i, summary in enumerate(self.summaries_history):
            print(f"\n{'='*80}")
            print(f"📌 ITERATION {summary['iteration']}")
            print(f"⏰ {summary['timestamp']}")
            print(f"📰 New: {summary['new_articles_count']} | Total: {summary['total_knowledge']}")
            print(f"{'='*80}")
            
            # Show temporal insights
            if summary.get('temporal_insights'):
                insights = summary['temporal_insights']
                trends = insights.get('trends', {})
                
                if trends.get('emerging'):
                    print(f"🆕 EMERGING: {', '.join(trends['emerging'])}")
                if trends.get('trending_up'):
                    print(f"📈 TRENDING UP: {', '.join(trends['trending_up'])}")
                if trends.get('trending_down'):
                    print(f"📉 TRENDING DOWN: {', '.join(trends['trending_down'])}")
                if trends.get('declining'):
                    print(f"⬇️  DECLINING: {', '.join(trends['declining'])}")
                
                print()
            
            print(summary['summary'])
            print(f"\n💡 Key Learning: {summary.get('key_insight', 'N/A')}")
            
            if i < len(self.summaries_history) - 1:
                print("\n" + "→"*35 + " TIME PASSES " + "→"*35)
        
        print("\n" + "="*80)
        print("🧠 FINAL LEARNING STATE")
        print("="*80)
        state = self.get_learning_state()
        print(json.dumps(state, indent=2))
        print("="*80)


def run_temporal_demo(iterations: int = 5, delay: int = 3):
    """
    Run temporal learning demo with pattern recognition.
    
    Args:
        iterations: Number of learning cycles
        delay: Seconds between iterations (simulates time passing)
    """
    print("\n" + "🕐"*40)
    print("TEMPORAL NEWS AGENT - LEARNING PATTERNS OVER TIME")
    print("🕐"*40 + "\n")
    
    agent = TemporalNewsAgent()
    
    for i in range(1, iterations + 1):
        print(f"\n{'='*80}")
        print(f"🔍 ITERATION {i}: Learning Cycle")
        print(f"{'='*80}")
        
        # Fetch new articles
        new_articles, all_articles = agent.fetch_new_articles()
        
        # Analyze temporal patterns
        temporal_analysis = agent.analyze_temporal_patterns()
        
        # Generate temporal summary
        summary = agent.generate_temporal_summary(new_articles, temporal_analysis)
        
        print(f"\n✅ Processed {summary['new_articles_count']} new articles")
        print(f"📊 Learning State:")
        state = agent.get_learning_state()
        print(f"  - Total Knowledge: {state['total_articles']} articles")
        print(f"  - Maturity: {state['learning_maturity']:.1f}%")
        print(f"  - Temporal Span: {state['temporal_span_hours']:.2f} hours")
        
        # Show what the agent learned
        if temporal_analysis.get('trends'):
            trends = temporal_analysis['trends']
            print(f"\n🎯 Pattern Detection:")
            if trends.get('emerging'):
                print(f"  🆕 New: {', '.join(trends['emerging'])}")
            if trends.get('trending_up'):
                print(f"  📈 Growing: {', '.join(trends['trending_up'])}")
        
        print(f"\n📝 Analysis:\n{summary['summary'][:500]}...")
        
        if i < iterations:
            print(f"\n{'⏳'*40}")
            print(f"⏱️  Waiting {delay}s for news cycle...")
            print(f"{'⏳'*40}")
            time.sleep(delay)
    
    # Show complete temporal analysis
    agent.print_temporal_analysis()
    
    # Save
    output_file = "temporal_learning_history.json"
    with open(output_file, "w") as f:
        json.dump({
            "learning_state": agent.get_learning_state(),
            "summaries": agent.summaries_history,
            "knowledge_base": agent.knowledge_base
        }, f, indent=2)
    
    print(f"\n💾 Temporal learning history saved to: {output_file}")


if __name__ == "__main__":
    import sys
    
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    delay = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    print(f"\nRunning temporal demo: {iterations} iterations, {delay}s intervals\n")
    run_temporal_demo(iterations=iterations, delay=delay)
