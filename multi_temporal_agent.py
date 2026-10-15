"""
Multi-Temporal Agent - Analyzes news across multiple time periods
Compares trends from different eras: Recent, 6mo-1yr, 1yr-3yr
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class MultiTemporalAgent:
    """Agent that analyzes and compares news across multiple time periods."""
    
    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_key) if OPENAI_AVAILABLE and self.openai_key else None
        
        self.time_periods = {
            "recent": {"name": "Recent (Now - 6 months)", "from": 0, "to": 6},
            "mid_term": {"name": "Mid-term (6 months - 1 year)", "from": 6, "to": 12},
            "long_term": {"name": "Long-term (1 year - 3 years)", "from": 12, "to": 36}
        }
        
        self.period_data = {}
        self.comparative_analysis = {}
        
    def fetch_historical_news(self, period_key: str) -> List[Dict[str, Any]]:
        """Fetch news for a specific time period."""
        period = self.time_periods[period_key]
        
        # Calculate date range
        to_date = datetime.now() - timedelta(days=period["from"] * 30)
        from_date = datetime.now() - timedelta(days=period["to"] * 30)
        
        # Format dates for API
        to_str = to_date.strftime("%Y-%m-%d")
        from_str = from_date.strftime("%Y-%m-%d")
        
        print(f"  📅 Fetching from {from_str} to {to_str}...")

        if not self.news_api_key:
            print("  NEWS_API_KEY is not set; skipping live fetch.")
            return []
        
        try:
            url = f"https://newsapi.org/v2/everything"
            params = {
                "q": "technology OR AI OR software OR hardware OR gaming",
                "from": from_str,
                "to": to_str,
                "sortBy": "popularity",
                "language": "en",
                "apiKey": self.news_api_key,
                "pageSize": 100
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                
                processed = []
                for article in articles[:50]:  # Limit to 50 per period
                    if article.get("title") and article.get("description"):
                        processed.append({
                            "title": article["title"],
                            "description": article.get("description", ""),
                            "source": article.get("source", {}).get("name", "Unknown"),
                            "published_at": article.get("publishedAt", ""),
                            "url": article.get("url", "")
                        })
                
                return processed
            else:
                print(f"  ⚠️  API returned status {response.status_code}")
                return []
                
        except (requests.RequestException, ValueError):
            print("  ❌ Error fetching news.")
            return []
    
    def analyze_period(self, period_key: str, articles: List[Dict]) -> Dict[str, Any]:
        """Analyze a single time period."""
        if not articles:
            return {
                "period": period_key,
                "article_count": 0,
                "topics": {},
                "key_themes": [],
                "summary": "No articles found for this period."
            }
        
        # Extract topics
        topics = Counter()
        sources = Counter()
        
        for article in articles:
            text = f"{article['title']} {article['description']}".lower()
            article_topics = self._extract_topics(text)
            topics.update(article_topics)
            sources[article['source']] += 1
        
        # Get top articles
        top_articles = articles[:10]
        
        return {
            "period": period_key,
            "period_name": self.time_periods[period_key]["name"],
            "article_count": len(articles),
            "topics": dict(topics),
            "top_topics": topics.most_common(5),
            "sources": dict(sources.most_common(5)),
            "sample_articles": top_articles
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text."""
        topics = []
        
        topic_keywords = {
            "AI/ML": ["ai", "artificial intelligence", "machine learning", "gpt", "llm", "neural", "chatgpt", "gemini", "claude"],
            "Gaming": ["game", "gaming", "playstation", "xbox", "nintendo", "steam", "esports"],
            "Mobile": ["iphone", "android", "mobile", "smartphone", "app", "ios"],
            "Cloud": ["cloud", "aws", "azure", "google cloud", "saas"],
            "Hardware": ["chip", "processor", "cpu", "gpu", "hardware", "semiconductor"],
            "Security": ["security", "hack", "breach", "privacy", "encryption", "cyber", "vulnerability"],
            "Software": ["software", "update", "release", "version", "app", "program"],
            "VR/AR": ["vr", "ar", "virtual reality", "augmented reality", "metaverse"],
            "Blockchain": ["blockchain", "crypto", "bitcoin", "ethereum", "nft", "web3"],
            "Social Media": ["twitter", "facebook", "instagram", "tiktok", "social media"],
            "Apple": ["apple", "iphone", "ipad", "mac", "macbook"],
            "Google": ["google", "android", "chrome", "alphabet"],
            "Microsoft": ["microsoft", "windows", "azure", "xbox"],
            "Tesla": ["tesla", "elon musk", "electric vehicle"],
            "Quantum": ["quantum computing", "quantum", "qubit"],
            "5G": ["5g", "network", "connectivity"],
            "Startup": ["startup", "funding", "venture capital", "ipo"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text for kw in keywords):
                topics.append(topic)
        
        return topics if topics else ["Other"]
    
    def compare_periods(self) -> Dict[str, Any]:
        """Compare trends across all time periods."""
        if len(self.period_data) < 2:
            return {}
        
        comparison = {
            "topic_evolution": {},
            "emerging_topics": [],
            "declining_topics": [],
            "stable_topics": [],
            "dramatic_changes": []
        }
        
        # Get topics from each period
        recent_topics = self.period_data.get("recent", {}).get("topics", {})
        mid_topics = self.period_data.get("mid_term", {}).get("topics", {})
        long_topics = self.period_data.get("long_term", {}).get("topics", {})
        
        # Analyze each topic across time
        all_topics = set(recent_topics.keys()) | set(mid_topics.keys()) | set(long_topics.keys())
        
        for topic in all_topics:
            recent_count = recent_topics.get(topic, 0)
            mid_count = mid_topics.get(topic, 0)
            long_count = long_topics.get(topic, 0)
            
            comparison["topic_evolution"][topic] = {
                "long_term": long_count,
                "mid_term": mid_count,
                "recent": recent_count,
                "trend": self._calculate_trend(long_count, mid_count, recent_count)
            }
            
            # Categorize topics
            trend = self._calculate_trend(long_count, mid_count, recent_count)
            if trend == "emerging":
                comparison["emerging_topics"].append(topic)
            elif trend == "declining":
                comparison["declining_topics"].append(topic)
            elif trend == "stable":
                comparison["stable_topics"].append(topic)
            elif trend == "dramatic_increase":
                comparison["dramatic_changes"].append(f"{topic} (↑↑)")
            elif trend == "dramatic_decrease":
                comparison["dramatic_changes"].append(f"{topic} (↓↓)")
        
        return comparison
    
    def _calculate_trend(self, long_count: int, mid_count: int, recent_count: int) -> str:
        """Calculate trend direction."""
        if long_count == 0 and recent_count > 0:
            return "emerging"
        elif long_count > 0 and recent_count == 0:
            return "declining"
        elif recent_count > long_count * 2:
            return "dramatic_increase"
        elif recent_count < long_count / 2 and long_count > 0:
            return "dramatic_decrease"
        elif recent_count > long_count:
            return "increasing"
        elif recent_count < long_count:
            return "decreasing"
        else:
            return "stable"
    
    def generate_temporal_summary(self) -> str:
        """Generate AI summary comparing all periods."""
        if not self.client:
            return self._generate_fallback_summary()
        
        try:
            # Prepare context
            context = "Multi-temporal Technology News Analysis\n\n"
            
            for period_key in ["long_term", "mid_term", "recent"]:
                data = self.period_data.get(period_key, {})
                context += f"\n{data.get('period_name', period_key)}:\n"
                context += f"- Articles: {data.get('article_count', 0)}\n"
                context += f"- Top topics: {', '.join([t[0] for t in data.get('top_topics', [])])}\n"
            
            context += f"\n\nComparative Analysis:\n"
            comp = self.comparative_analysis
            if comp.get('emerging_topics'):
                context += f"Emerging: {', '.join(comp['emerging_topics'][:5])}\n"
            if comp.get('declining_topics'):
                context += f"Declining: {', '.join(comp['declining_topics'][:5])}\n"
            if comp.get('dramatic_changes'):
                context += f"Dramatic changes: {', '.join(comp['dramatic_changes'][:5])}\n"
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a technology trend analyst examining news across 3 time periods:
                        1. Long-term: 1-3 years ago
                        2. Mid-term: 6 months-1 year ago  
                        3. Recent: Last 6 months
                        
                        Analyze how technology topics evolved, identify major shifts, and explain what these patterns reveal about the tech industry's direction."""
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze this multi-temporal data and provide insights:

{context}

Focus on:
1. What topics emerged or declined over this period
2. Major shifts in technology focus
3. Patterns that reveal industry direction
4. Predictions based on these trends"""
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating AI summary: {str(e)}\n\n{self._generate_fallback_summary()}"
    
    def _generate_fallback_summary(self) -> str:
        """Generate basic summary without AI."""
        summary = "Multi-Temporal Analysis Summary\n" + "="*50 + "\n\n"
        
        for period_key in ["long_term", "mid_term", "recent"]:
            data = self.period_data.get(period_key, {})
            summary += f"{data.get('period_name', period_key)}:\n"
            summary += f"  Articles: {data.get('article_count', 0)}\n"
            if data.get('top_topics'):
                summary += f"  Top topics: {', '.join([t[0] for t in data['top_topics']])}\n"
            summary += "\n"
        
        comp = self.comparative_analysis
        if comp:
            summary += "Trends:\n"
            if comp.get('emerging_topics'):
                summary += f"  Emerging: {', '.join(comp['emerging_topics'][:5])}\n"
            if comp.get('declining_topics'):
                summary += f"  Declining: {', '.join(comp['declining_topics'][:5])}\n"
        
        return summary
    
    def run_analysis(self):
        """Run complete multi-temporal analysis."""
        print("\n" + "🕰️"*40)
        print("MULTI-TEMPORAL NEWS ANALYSIS")
        print("Comparing 3 Time Periods: Recent vs Mid-term vs Long-term")
        print("🕰️"*40 + "\n")
        
        # Fetch and analyze each period
        for period_key in ["recent", "mid_term", "long_term"]:
            period_name = self.time_periods[period_key]["name"]
            print(f"\n{'='*80}")
            print(f"📊 Analyzing: {period_name}")
            print(f"{'='*80}")
            
            articles = self.fetch_historical_news(period_key)
            print(f"  ✅ Fetched {len(articles)} articles")
            
            analysis = self.analyze_period(period_key, articles)
            self.period_data[period_key] = analysis
            
            print(f"\n  📈 Top Topics:")
            for topic, count in analysis.get('top_topics', [])[:5]:
                print(f"    {topic}: {count} mentions")
        
        # Compare periods
        print(f"\n\n{'='*80}")
        print("🔍 COMPARATIVE ANALYSIS")
        print(f"{'='*80}\n")
        
        self.comparative_analysis = self.compare_periods()
        
        # Show comparisons
        if self.comparative_analysis:
            print("📈 Topic Evolution:")
            evolution = self.comparative_analysis.get('topic_evolution', {})
            sorted_topics = sorted(evolution.items(), 
                                 key=lambda x: x[1]['recent'], reverse=True)[:10]
            
            for topic, data in sorted_topics:
                trend = data['trend']
                emoji = {
                    "emerging": "🆕",
                    "dramatic_increase": "🚀",
                    "increasing": "📈",
                    "stable": "➡️",
                    "decreasing": "📉",
                    "dramatic_decrease": "⬇️",
                    "declining": "💤"
                }.get(trend, "❓")
                
                print(f"  {emoji} {topic}: {data['long_term']} → {data['mid_term']} → {data['recent']} ({trend})")
            
            if self.comparative_analysis.get('emerging_topics'):
                print(f"\n🆕 Emerging Topics: {', '.join(self.comparative_analysis['emerging_topics'][:8])}")
            
            if self.comparative_analysis.get('declining_topics'):
                print(f"\n💤 Declining Topics: {', '.join(self.comparative_analysis['declining_topics'][:8])}")
        
        # Generate AI summary
        print(f"\n\n{'='*80}")
        print("🤖 AI-GENERATED INSIGHTS")
        print(f"{'='*80}\n")
        
        summary = self.generate_temporal_summary()
        print(summary)
        
        # Save results
        output = {
            "periods": self.period_data,
            "comparative_analysis": self.comparative_analysis,
            "ai_summary": summary,
            "generated_at": datetime.now().isoformat()
        }
        
        output_file = "multi_temporal_analysis.json"
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"\n\n💾 Complete analysis saved to: {output_file}")
        
        print("\n" + "="*80)
        print("✅ MULTI-TEMPORAL ANALYSIS COMPLETE")
        print("="*80)


if __name__ == "__main__":
    agent = MultiTemporalAgent()
    agent.run_analysis()
