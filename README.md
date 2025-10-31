# 🤖 Adaptive News Agent - AI Learning Over Time

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive demonstration of AI agents that **learn and adapt over time**, featuring progressive knowledge acquisition, temporal pattern recognition, and multi-period trend analysis.

## 🎯 What Makes This Special

This isn't just another news aggregator—it's a **learning system** that:

- 📊 **Tracks Knowledge Evolution** - Agent maintains state across iterations
- 🧠 **Learns Patterns** - Identifies what topics matter over time
- 📈 **Shows Adaptation** - Each iteration improves on previous understanding
- 🕰️ **Multi-Temporal Analysis** - Compares trends across years
- 💾 **Full Transparency** - Complete history and metrics tracking

Perfect for:
- **AI Education** - Teaching agent state management and learning
- **Research** - Temporal pattern recognition in AI systems
- **Demonstrations** - Impressive visual learning progression
- **Real Applications** - Template for production agent systems

## 🚀 Quick Start

### Prerequisites

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Set Up API Keys

Create a `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
NEWS_API_KEY=your-newsapi-key  # Optional, has default
```

### Run a Demo!

**Option 1: Simple Adaptive Agent** (Best for first time)
```bash
./run_cli_demo.sh
```

**Option 2: Multi-Temporal Analysis** (Most impressive)
```bash
./run_simulated_multi_temporal.sh
```

**Option 3: Web Interface**
```bash
./run_web_demo.sh
# Open http://localhost:5000
```

## 📚 Available Demos

### 1. 🖥️ Basic Adaptive Agent (`run_cli_demo.sh`)

Watch an agent learn across multiple iterations:
- Fetches technology news
- Generates AI summaries
- Tracks knowledge accumulation
- Shows confidence improvements

**Output:**
```
🔍 ITERATION 1: Initial Knowledge
✅ Acquired 18 articles
📊 Knowledge Vector: {total: 18, topics: {...}}
📝 AI Summary with 85% confidence

⏳ Waiting for more news...

🔍 ITERATION 2: Knowledge Update  
✅ Found 3 NEW articles
📊 Updated Knowledge Vector
📝 Improved summary highlighting what changed
```

### 2. 🕐 Temporal Learning (`run_temporal_demo.sh`)

Advanced agent that tracks trends over time:
- Identifies emerging topics
- Detects declining trends
- Learns which patterns persist
- Builds temporal understanding

### 3. 🕰️ Multi-Temporal Analysis (`run_simulated_multi_temporal.sh`)

**⭐ Most Impressive Demo**

Compares 3 time periods:
- **Recent**: Last 6 months
- **Mid-term**: 6 months - 1 year ago
- **Long-term**: 1-3 years ago

Shows:
- Topic evolution (e.g., AI/ML: 7 → 10 → 17 articles)
- Emerging trends (new topics appearing)
- Declining topics (fading interest)
- Industry direction insights

**Sample Output:**
```
📈 Topic Evolution:
AI/ML:      7 → 10 → 17  🚀 Dramatic increase
Blockchain: 3 → 2  → 0   💤 Declining
Gaming:     4 → 2  → 1   ⬇️ Dramatic decrease
```

### 4. 🌐 Web Interface (`run_web_demo.sh`)

Beautiful interactive dashboard:
- Real-time metrics visualization
- Click to fetch and analyze
- Learning history timeline
- Topic coverage charts

![Web Interface](docs/web-interface-preview.png)

## 🏗️ Project Structure

```
├── adaptive_news_agent.py        # Core adaptive agent
├── temporal_news_agent.py        # Temporal pattern recognition
├── multi_temporal_agent.py       # Multi-period comparison
├── simulated_multi_temporal.py   # Demo with realistic data
├── news_fetcher.py              # NewsAPI integration
├── web_agent_demo.py            # Flask web interface
├── templates/
│   └── index.html               # Web UI
├── run_*.sh                     # Easy launcher scripts
├── DEMO_README.md              # Detailed documentation
├── FEATURES.md                 # Architecture deep-dive
└── QUICK_START.md             # Getting started guide

# Generated files
├── agent_learning_history.json
├── temporal_learning_history.json
└── multi_temporal_analysis.json
```

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Your starting point
- **[DEMO_README.md](DEMO_README.md)** - Complete demo guide
- **[FEATURES.md](FEATURES.md)** - Architecture and concepts

## 🎓 Key Concepts Demonstrated

### 1. State Management
```python
class AdaptiveNewsAgent:
    def __init__(self):
        self.knowledge_base: List[str] = []
        self.seen_articles: set = set()
        self.iteration = 0
```

### 2. Deduplication
Only processes genuinely new content:
```python
new_articles = [a for a in all_articles 
                if a not in self.seen_articles]
```

### 3. Context-Aware Prompts
Agent knows its own history:
```python
context = f"Iteration {self.iteration}. "
context += f"You have {len(new_articles)} NEW articles. "
context += f"Total knowledge: {len(self.knowledge_base)}."
```

### 4. Learning Metrics
```python
{
    "iteration": 3,
    "total_articles": 21,
    "learning_rate": 7.0,
    "confidence": 92%
}
```

## 🔧 Technology Stack

- **Python 3.11+** - Core language
- **OpenAI GPT-4o-mini** - AI summarization
- **Flask** - Web interface
- **NewsAPI** - News source
- **LangGraph** - Agent workflows (optional)
- **Arc Framework** - Agent architecture (optional)

## 🎨 Features

### ✅ Progressive Learning
- Agent builds knowledge across iterations
- References previous summaries
- Identifies what's NEW vs known
- Improves confidence over time

### ✅ Temporal Analysis
- Tracks topic evolution
- Identifies emerging/declining trends
- Multi-period comparisons
- Pattern recognition

### ✅ Full Transparency
- Complete knowledge vector
- Learning rate metrics
- Confidence scores
- Topic distribution

### ✅ Beautiful UI
- Modern gradient design
- Real-time updates
- Interactive charts
- Responsive layout

## 🛠️ Advanced Usage

### Custom Iterations
```bash
./run_cli_demo.sh 10 5  # 10 iterations, 5s delay
```

### Temporal Analysis
```bash
./run_temporal_demo.sh 5 3  # 5 cycles, 3s intervals
```

### Environment Variables
```bash
OPENAI_API_KEY=sk-...
NEWS_API_KEY=...
ATLAS_SKIP_VALIDATION=1  # For Arc framework
```

## 📊 Example Results

### Learning Progression
```
Iteration 1: 18 articles, 85% confidence
Iteration 2: 21 articles, 88% confidence  
Iteration 3: 24 articles, 92% confidence
```

### Topic Evolution (3 years)
```
AI/ML:       143% increase
Security:    Stable
Blockchain:  Declined to zero
Gaming:      75% decrease
```

## 🤝 Contributing

Contributions welcome! Ideas:
- [ ] Database persistence
- [ ] Scheduled background fetching  
- [ ] Advanced topic modeling
- [ ] Accuracy scoring
- [ ] Multi-language support
- [ ] Export to PDF reports

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- OpenAI for GPT models
- NewsAPI for news data
- Eclipse LMOS Arc framework
- Flask and Python ecosystem

## 📧 Contact

Questions? Open an issue or reach out!

## 🌟 Star This Repo!

If you find this useful, please give it a star ⭐ 

It helps others discover this educational resource!

---

**Made with ❤️ to demonstrate AI agent learning patterns**
