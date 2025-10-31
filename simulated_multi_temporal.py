"""
Simulated Multi-Temporal Analysis with realistic historical data
Shows how the agent learns patterns across 3 time periods
"""

from multi_temporal_agent import MultiTemporalAgent
import json
from datetime import datetime

# Realistic mock data representing technology trends over time
HISTORICAL_DATA = {
    "long_term": {  # 1-3 years ago (2022-2024)
        "name": "Long-term (1-3 years ago)",
        "articles": [
            {"title": "ChatGPT Launches and Disrupts Tech Industry", "description": "OpenAI releases revolutionary chatbot", "source": "TechCrunch"},
            {"title": "Cryptocurrency Market Crashes After FTX Collapse", "description": "Bitcoin drops below $20k", "source": "Bloomberg"},
            {"title": "Twitter Acquired by Elon Musk for $44 Billion", "description": "Social media platform undergoes major changes", "source": "Reuters"},
            {"title": "Meta Invests Billions in Metaverse Development", "description": "Zuckerberg bets on VR future", "source": "The Verge"},
            {"title": "Apple Releases iPhone 14 with Satellite Features", "description": "Emergency SOS via satellite debuts", "source": "Apple Newsroom"},
            {"title": "Microsoft Activision Deal Faces Regulatory Scrutiny", "description": "$69B gaming acquisition challenged", "source": "WSJ"},
            {"title": "NFT Market Peaks Then Crashes", "description": "Digital art sales plummet 90%", "source": "CoinDesk"},
            {"title": "Tesla Cybertruck Production Delayed Again", "description": "Electric pickup faces manufacturing challenges", "source": "Automotive News"},
            {"title": "Google Launches Bard AI to Compete with ChatGPT", "description": "Search giant enters AI race", "source": "Google Blog"},
            {"title": "Web3 Gaming Promises Revolutionize Industry", "description": "Blockchain games attract investment", "source": "VentureBeat"},
            {"title": "Amazon Alexa Struggles with Profitability", "description": "Voice assistant loses billions annually", "source": "Business Insider"},
            {"title": "TikTok Faces US Ban Threats", "description": "Security concerns over Chinese ownership", "source": "CNN"},
            {"title": "Quantum Computing Makes Breakthrough", "description": "IBM achieves quantum advantage", "source": "Nature"},
            {"title": "5G Rollout Continues Worldwide", "description": "Networks expand coverage", "source": "GSMA"},
            {"title": "PlayStation VR2 Launches with Mixed Reception", "description": "Sony's VR headset gets lukewarm reviews", "source": "IGN"},
            {"title": "GitHub Copilot Raises Code Ownership Questions", "description": "AI coding assistant sparks debate", "source": "Stack Overflow"},
            {"title": "Cloud Gaming Services Struggle to Gain Traction", "description": "Stadia shuts down, others slow", "source": "Polygon"},
            {"title": "Chip Shortage Impacts Tech Production", "description": "Semiconductor crisis continues", "source": "Semiconductor Today"},
            {"title": "Layoffs Hit Major Tech Companies", "description": "Meta, Amazon, Microsoft cut thousands", "source": "CNBC"},
            {"title": "AI Art Generators Spark Copyright Debates", "description": "Stable Diffusion, Midjourney face lawsuits", "source": "Ars Technica"}
        ]
    },
    "mid_term": {  # 6 months - 1 year ago (Late 2024-Early 2025)
        "name": "Mid-term (6 months - 1 year ago)",
        "articles": [
            {"title": "GPT-4 Surpasses Human Performance on Bar Exam", "description": "AI achieves 90th percentile", "source": "OpenAI"},
            {"title": "Apple Vision Pro Launches to Strong Pre-Orders", "description": "Mixed reality headset debuts at $3,499", "source": "Apple"},
            {"title": "Google Gemini Challenges ChatGPT Dominance", "description": "Multimodal AI model shows promise", "source": "Google DeepMind"},
            {"title": "Cryptocurrency Regulations Tighten Globally", "description": "SEC cracks down on exchanges", "source": "Financial Times"},
            {"title": "AI Coding Tools Now Generate 30% of Code", "description": "GitHub reports developer productivity surge", "source": "GitHub"},
            {"title": "Quantum Computer Achieves Error Correction Milestone", "description": "Google demonstrates practical quantum computing", "source": "Science"},
            {"title": "Tesla Full Self-Driving Faces Safety Investigation", "description": "NHTSA examines crash data", "source": "Reuters"},
            {"title": "Microsoft Integrates AI Across Office Suite", "description": "Copilot becomes standard feature", "source": "Microsoft"},
            {"title": "Social Media Platforms Add AI Content Labels", "description": "New rules combat misinformation", "source": "The Guardian"},
            {"title": "Amazon Deploys Warehouse Robots at Scale", "description": "Automation reduces human workforce", "source": "WSJ"},
            {"title": "Security Breach Exposes 100M User Records", "description": "Major cloud provider hacked", "source": "Security Week"},
            {"title": "AI Chip Demand Creates Nvidia Shortage", "description": "GPU prices surge amid AI boom", "source": "Tom's Hardware"},
            {"title": "VR Gaming Market Grows 40% Year-Over-Year", "description": "Meta Quest 3 drives adoption", "source": "IDC"},
            {"title": "Open Source AI Models Challenge Proprietary Giants", "description": "Llama 3, Mistral gain traction", "source": "Hugging Face"},
            {"title": "Apple Announces Custom AI Chips", "description": "M4 processor designed for machine learning", "source": "MacRumors"},
            {"title": "Cybersecurity Spending Hits Record $300B", "description": "Ransomware attacks drive investment", "source": "Gartner"},
            {"title": "Blockchain Gaming Sees Revival", "description": "New titles avoid NFT pitfalls", "source": "GameSpot"},
            {"title": "6G Research Accelerates in Asia", "description": "China, Japan lead next-gen networks", "source": "Light Reading"},
            {"title": "AI Startups Raise $50B in Funding", "description": "Venture capital floods AI sector", "source": "CB Insights"},
            {"title": "Smartphone Sales Decline for Third Year", "description": "Market saturation impacts manufacturers", "source": "IDC"}
        ]
    },
    "recent": {  # Recent (Last 6 months)
        "name": "Recent (Last 6 months)",
        "articles": [
            {"title": "GPT-5 Rumors Suggest AGI Breakthrough", "description": "OpenAI hints at next-generation model", "source": "TechCrunch"},
            {"title": "AI Agents Automate Complex Business Tasks", "description": "New tools manage workflows autonomously", "source": "MIT Tech Review"},
            {"title": "Apple Intelligence Integrates AI Across iOS", "description": "On-device AI features debut with iPhone 16", "source": "Apple"},
            {"title": "Quantum Computing Reaches Commercial Viability", "description": "IBM offers quantum cloud services", "source": "IBM Research"},
            {"title": "AI-Generated Content Dominates Social Media", "description": "40% of posts now AI-created", "source": "Pew Research"},
            {"title": "Security AI Detects Threats Proactively", "description": "Machine learning prevents 95% of attacks", "source": "CrowdStrike"},
            {"title": "Humanoid Robots Enter Consumer Market", "description": "Tesla, Boston Dynamics ship first units", "source": "IEEE Spectrum"},
            {"title": "AI Chip Market Explodes to $100B Annually", "description": "Nvidia dominates but faces new competition", "source": "Bloomberg"},
            {"title": "Brain-Computer Interfaces Show Promise", "description": "Neuralink begins human trials", "source": "Nature Medicine"},
            {"title": "AI Regulation Bills Pass in EU and US", "description": "New laws govern AI development", "source": "Politico"},
            {"title": "Gaming Industry Adopts AI NPCs", "description": "Characters use LLMs for dynamic dialogue", "source": "GDC"},
            {"title": "Cloud Costs Skyrocket Due to AI Workloads", "description": "Companies seek optimization strategies", "source": "AWS re:Invent"},
            {"title": "Deepfake Detection AI Arms Race Intensifies", "description": "New tools combat synthetic media", "source": "WIRED"},
            {"title": "AI Discovers New Materials for Batteries", "description": "Machine learning accelerates science", "source": "Science"},
            {"title": "Autonomous Vehicles Reach Level 4 in Cities", "description": "Waymo, Cruise expand service areas", "source": "The Verge"},
            {"title": "AI-Powered Education Personalizes Learning", "description": "Adaptive systems help millions of students", "source": "EdSurge"},
            {"title": "Smartphone AI Features Drive Upgrade Cycle", "description": "Consumers embrace on-device intelligence", "source": "IDC"},
            {"title": "AI Climate Models Predict Weather Better", "description": "DeepMind outperforms traditional methods", "source": "Nature"},
            {"title": "Cybercriminals Use AI for Sophisticated Attacks", "description": "AI-generated phishing increases 300%", "source": "Mandiant"},
            {"title": "AI Ethics Debates Shape Policy Worldwide", "description": "Governments struggle with regulation", "source": "Brookings"}
        ]
    }
}


def run_simulated_multi_temporal():
    """Run multi-temporal analysis with simulated data."""
    print("\n" + "🎭"*40)
    print("SIMULATED MULTI-TEMPORAL ANALYSIS")
    print("Realistic data showing 3-year technology evolution")
    print("🎭"*40 + "\n")
    
    agent = MultiTemporalAgent()
    
    # Load simulated data
    for period_key in ["recent", "mid_term", "long_term"]:
        period_data = HISTORICAL_DATA[period_key]
        
        print(f"\n{'='*80}")
        print(f"📊 Analyzing: {period_data['name']}")
        print(f"{'='*80}")
        print(f"  ✅ Loaded {len(period_data['articles'])} historical articles")
        
        # Analyze the period
        analysis = agent.analyze_period(period_key, period_data['articles'])
        agent.period_data[period_key] = analysis
        
        print(f"\n  📈 Top Topics:")
        for topic, count in analysis.get('top_topics', [])[:7]:
            print(f"    {topic}: {count} mentions")
    
    # Compare periods
    print(f"\n\n{'='*80}")
    print("🔍 COMPARATIVE TREND ANALYSIS")
    print(f"{'='*80}\n")
    
    agent.comparative_analysis = agent.compare_periods()
    
    # Show evolution
    if agent.comparative_analysis:
        print("📈 Topic Evolution Over 3 Years:")
        print(f"{'='*80}")
        evolution = agent.comparative_analysis.get('topic_evolution', {})
        sorted_topics = sorted(evolution.items(), 
                             key=lambda x: x[1]['recent'], reverse=True)[:15]
        
        print(f"\n{'Topic':<20} {'1-3yr ago':<12} {'6mo-1yr ago':<12} {'Recent':<12} {'Trend'}")
        print("-"*80)
        
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
            
            print(f"{topic:<20} {data['long_term']:<12} {data['mid_term']:<12} {data['recent']:<12} {emoji} {trend}")
        
        print(f"\n{'='*80}")
        print("🎯 KEY INSIGHTS")
        print(f"{'='*80}\n")
        
        if agent.comparative_analysis.get('emerging_topics'):
            emerging = agent.comparative_analysis['emerging_topics'][:6]
            print(f"🆕 EMERGING (New in recent period):")
            print(f"   {', '.join(emerging)}")
        
        if agent.comparative_analysis.get('dramatic_changes'):
            dramatic = agent.comparative_analysis['dramatic_changes'][:6]
            print(f"\n🚀 DRAMATIC CHANGES:")
            print(f"   {', '.join(dramatic)}")
        
        if agent.comparative_analysis.get('declining_topics'):
            declining = agent.comparative_analysis['declining_topics'][:6]
            print(f"\n💤 DECLINING (Was popular, now fading):")
            print(f"   {', '.join(declining)}")
    
    # Generate AI insights
    print(f"\n\n{'='*80}")
    print("🤖 AI-GENERATED MULTI-TEMPORAL INSIGHTS")
    print(f"{'='*80}\n")
    
    summary = agent.generate_temporal_summary()
    print(summary)
    
    # Save results
    output = {
        "periods": agent.period_data,
        "comparative_analysis": agent.comparative_analysis,
        "ai_insights": summary,
        "generated_at": datetime.now().isoformat()
    }
    
    output_file = "simulated_multi_temporal_results.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n\n💾 Complete analysis saved to: {output_file}")
    
    print("\n" + "="*80)
    print("✅ MULTI-TEMPORAL ANALYSIS COMPLETE")
    print("="*80)
    print("\nKey Learnings:")
    print("  ✓ Tracked topic evolution across 3 years")
    print("  ✓ Identified emerging and declining trends")
    print("  ✓ Showed how AI/ML dramatically increased")
    print("  ✓ Revealed industry shift from hype to practical AI")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_simulated_multi_temporal()
