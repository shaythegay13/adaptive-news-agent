"""
Simulated Temporal Demo - Uses mock news batches to demonstrate learning
This shows the agent adapting to ACTUAL changes over time
"""

import json
import time
from datetime import datetime
from temporal_news_agent import TemporalNewsAgent
import os

# Mock news batches simulating different time periods
MOCK_NEWS_BATCHES = [
    # Day 1: Gaming and AI news
    [
        "Nintendo announces Switch 2 with improved graphics and battery life",
        "PlayStation 6 rumored for 2026 release with VR integration",
        "OpenAI releases GPT-5 with improved reasoning capabilities",
        "Google's Gemini surpasses ChatGPT in coding tasks",
        "Meta unveils new VR headset with eye tracking",
        "Xbox Game Pass reaches 50 million subscribers",
        "AI agents show promise in customer service applications",
        "New study reveals AI still struggles with creative writing"
    ],
    # Day 2: AI growing, gaming stable, mobile news emerging
    [
        "Google's Gemini Pro now available for enterprise customers",
        "AI coding assistants reduce development time by 40% study shows",
        "OpenAI announces new safety protocols for AI deployment",
        "PlayStation announces 10 new exclusive titles for 2025",
        "Apple rumored to launch foldable iPhone in September",
        "Samsung Galaxy S25 features revolutionary camera AI",
        "Microsoft integrates AI into Windows 12",
        "iPhone 16 pre-orders break previous records"
    ],
    # Day 3: Security emerging, AI continues, gaming declining
    [
        "Major security breach affects 50 million cloud accounts",
        "New ransomware targets healthcare institutions",
        "AI models found vulnerable to prompt injection attacks",
        "Microsoft announces enhanced security features for Azure",
        "Google DeepMind creates AI that detects security threats",
        "Apple introduces end-to-end encryption for iCloud",
        "Anthropic releases Claude 3 with improved safety",
        "Samsung patches critical vulnerability in Galaxy devices"
    ],
    # Day 4: Security growing, hardware emerging, AI stabilizing
    [
        "Intel announces breakthrough in quantum computing chips",
        "AMD's new Ryzen processors promise 60% performance gain",
        "Zero-day exploit discovered in popular VPN software",
        "Cybersecurity spending to reach $300 billion in 2025",
        "NVIDIA releases AI chip specifically for edge computing",
        "Apple Silicon M4 chip leaked specifications show major upgrade",
        "Security researchers warn of AI-powered phishing attacks",
        "MediaTek's new chip promises fanless laptop designs"
    ],
    # Day 5: Diverse topics, showing learned patterns
    [
        "Quantum computing breakthrough enables room-temperature qubits",
        "AI-generated code now accounts for 30% of GitHub commits",
        "Major tech companies form alliance for AI safety standards",
        "New hardware vulnerability affects billions of devices",
        "Cloud gaming subscriptions surpass traditional game sales",
        "Blockchain technology adopted by major banks for settlements",
        "VR market expected to triple by 2027",
        "Open source AI models challenge proprietary alternatives"
    ]
]


def run_simulated_demo():
    """Run demo with simulated news batches to show real temporal changes."""
    print("\n" + "🎭"*40)
    print("SIMULATED TEMPORAL DEMO - Watch the Agent Learn!")
    print("🎭"*40 + "\n")
    print("This demo uses simulated news from 5 different 'days'")
    print("to show how the agent identifies trends over time.\n")
    
    # Create a modified agent that uses our mock data
    agent = TemporalNewsAgent()
    
    for day_num, news_batch in enumerate(MOCK_NEWS_BATCHES, 1):
        print(f"\n{'='*80}")
        print(f"📅 DAY {day_num}: Simulating news cycle")
        print(f"{'='*80}")
        
        # Manually add articles to agent (simulating fresh news)
        new_articles = []
        for article in news_batch:
            if article not in agent.seen_articles:
                new_articles.append(article)
                agent.seen_articles.add(article)
                agent.knowledge_base.append({
                    "content": article,
                    "timestamp": datetime.now().isoformat(),
                    "iteration": day_num
                })
        
        print(f"\n✅ Received {len(new_articles)} new articles on Day {day_num}")
        
        # Analyze patterns
        temporal_analysis = agent.analyze_temporal_patterns()
        
        # Generate summary
        summary = agent.generate_temporal_summary(new_articles, temporal_analysis)
        
        # Show what the agent is learning
        state = agent.get_learning_state()
        print(f"\n📊 Learning Progress:")
        print(f"  - Total Articles: {state['total_articles']}")
        print(f"  - Learning Maturity: {state['learning_maturity']:.1f}%")
        print(f"  - Topics Tracked: {len(state['topic_distribution'])}")
        
        if temporal_analysis.get('trends'):
            trends = temporal_analysis['trends']
            print(f"\n🎯 What the Agent Learned:")
            
            if trends.get('emerging'):
                print(f"  🆕 NEW TOPICS EMERGING: {', '.join(trends['emerging'])}")
            if trends.get('trending_up'):
                print(f"  📈 GROWING INTEREST: {', '.join(trends['trending_up'])}")
            if trends.get('trending_down'):
                print(f"  📉 DECLINING INTEREST: {', '.join(trends['trending_down'])}")
            if trends.get('declining'):
                print(f"  ⬇️  TOPICS FADING: {', '.join(trends['declining'])}")
            if trends.get('stable'):
                print(f"  ⚖️  STABLE TOPICS: {', '.join(trends['stable'][:3])}")
        
        print(f"\n📝 AI Analysis:")
        print(summary['summary'])
        
        print(f"\n💡 Agent's Key Learning: {summary.get('key_insight', 'Building understanding...')}")
        
        if day_num < len(MOCK_NEWS_BATCHES):
            print(f"\n{'⏳'*40}")
            print(f"⏱️  Simulating passage of time to next day...")
            print(f"{'⏳'*40}")
            time.sleep(2)
    
    # Final analysis
    print("\n" + "="*80)
    print("🎓 WHAT THE AGENT LEARNED OVER TIME")
    print("="*80 + "\n")
    
    state = agent.get_learning_state()
    patterns = state['learned_patterns']
    
    print("📊 Topic Evolution:")
    topic_dist = state['topic_distribution']
    sorted_topics = sorted(topic_dist.items(), key=lambda x: x[1], reverse=True)
    for topic, count in sorted_topics:
        print(f"  {topic}: {count} articles")
    
    print(f"\n🔍 Patterns Identified:")
    if patterns.get('trending_up'):
        print(f"  📈 Growing: {', '.join(patterns['trending_up'][:5])}")
    if patterns.get('emerging_topics'):
        print(f"  🆕 Emerged: {', '.join(patterns['emerging_topics'][:5])}")
    
    print(f"\n🧠 Learning Maturity: {state['learning_maturity']:.1f}%")
    print(f"📚 Knowledge Base: {state['total_articles']} articles across {state['iterations']} iterations")
    
    # Show detailed progression
    agent.print_temporal_analysis()
    
    # Save results
    output_file = "simulated_temporal_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "learning_state": state,
            "summaries": agent.summaries_history,
            "patterns": patterns
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE")
    print("="*80)
    print("\nKey Takeaways:")
    print("  ✓ Agent tracked topic evolution across 5 'days'")
    print("  ✓ Identified emerging and declining trends")
    print("  ✓ Learned which topics matter over time")
    print("  ✓ Built temporal understanding of news patterns")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_simulated_demo()
