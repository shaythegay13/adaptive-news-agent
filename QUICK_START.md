# Quick Start Guide

## ✅ You're All Set! Here's What You Can Do:

### 1. 🖥️ Run the CLI Demo (Recommended First)

The CLI version provides detailed output showing the agent's learning process:

```bash
./run_cli_demo.sh 3 2
```

**What you'll see:**
- 🔍 Iteration-by-iteration breakdown
- 📊 Knowledge vector updates after each cycle
- 📝 AI-generated summaries with confidence scores
- 📈 Side-by-side comparison of all iterations
- 💾 Complete history saved to `agent_learning_history.json`

**Arguments:**
- First number: iterations (default: 3)
- Second number: delay between iterations in seconds (default: 2)

**Examples:**
```bash
./run_cli_demo.sh              # 3 iterations, 2s delay
./run_cli_demo.sh 5 3          # 5 iterations, 3s delay
./run_cli_demo.sh 10 1         # 10 iterations, 1s delay (fast demo)
```

---

### 2. 🌐 Run the Web Interface

Beautiful, interactive dashboard for visual exploration:

```bash
./run_web_demo.sh
```

Then open: **http://localhost:5000**

**Features:**
- 🎨 Modern gradient UI with smooth animations
- 📊 Real-time knowledge metrics
- 🔄 Click "Fetch & Analyze News" to add iterations
- 📚 Full learning history timeline
- 🏷️ Visual badges for INITIAL vs UPDATE summaries
- 📈 Topic coverage breakdown
- 🔄 Reset button to start over

---

### 3. 🔍 Check the Learning History

After running the CLI demo, inspect the saved history:

```bash
cat agent_learning_history.json
```

You'll see:
- Complete knowledge vector state
- All summaries with timestamps
- Article counts per iteration
- Learning progression data

---

### 4. 🎓 Learn More

**Detailed Documentation:**
- **[DEMO_README.md](DEMO_README.md)** - Complete demo documentation
- **[FEATURES.md](FEATURES.md)** - Feature deep-dive and architecture
- **[README.md](README.md)** - Project overview

---

## 🎯 What to Observe

### First Iteration
Watch how the agent:
- Acquires its initial knowledge (18 articles)
- Generates a baseline summary
- Categorizes by topic (Gaming, AI, Mobile, etc.)
- Reports 85%+ confidence

### Subsequent Iterations
Notice how the agent:
- Identifies NEW articles (deduplication working)
- References previous knowledge ("Building on...")
- Highlights what CHANGED
- Improves confidence scores
- Adapts its analysis style

### Knowledge Vector Evolution
Track these metrics growing:
```
Iteration 1: 18 articles, learning_rate: 18.0
Iteration 2: 18 articles, learning_rate: 9.0  (no new)
Iteration 3: 21 articles, learning_rate: 7.0  (3 new)
```

---

## ⚙️ Configuration

### Set Your OpenAI API Key

The demo uses OpenAI for intelligent summarization. Edit `.env`:

```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

**Without API key:** Demo still works but uses simple fallback summaries.

**With API key:** Get sophisticated AI-generated analysis with:
- Theme identification
- Trend analysis
- Confidence scoring
- Context-aware updates

---

## 🎮 Try These Demo Scenarios

### Scenario 1: Quick Demo (2 minutes)
```bash
./run_cli_demo.sh 2 1
```
Shows basic learning in 2 iterations with 1s delay.

### Scenario 2: Full Demonstration (5 minutes)
```bash
./run_cli_demo.sh 5 2
```
Comprehensive view with 5 learning cycles.

### Scenario 3: Web Experience
```bash
./run_web_demo.sh
```
Click "Fetch & Analyze" 3-5 times, watching the UI update.

### Scenario 4: Long-Running Monitor
```bash
./run_cli_demo.sh 10 5
```
Simulates periodic monitoring with 10 iterations.

---

## 🐛 Troubleshooting

### "No new articles found"
**Normal!** The NewsAPI doesn't update every second. 
- Try waiting longer between iterations
- Or run the demo less frequently

### OpenAI Errors
Check:
- ✅ API key is set in `.env`
- ✅ You have OpenAI credits
- ✅ Key starts with `sk-`

### Port 5000 Already in Use
Edit `web_agent_demo.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 📊 Expected Results

### CLI Output Pattern:
```
🤖 ADAPTIVE NEWS AGENT
🔍 ITERATION 1: Initial Knowledge Acquisition
✅ Acquired 18 articles
📊 Knowledge Vector: {total_articles: 18, ...}
📝 Summary: [Detailed AI analysis]

⏳ Waiting for new news...

🔍 ITERATION 2: Knowledge Update
ℹ️ No new articles (or ✅ Found X new articles)
📊 Updated Knowledge Vector: {...}
📝 Updated Summary: [Incorporating new info]

📊 AGENT LEARNING PROGRESSION
[Complete comparison of all iterations]

💾 Learning history saved to: agent_learning_history.json
```

### Web Interface Pattern:
1. **Knowledge Vector Panel**: Shows metrics
2. **Current Summary Panel**: Latest analysis
3. **Learning History Panel**: Timeline of all iterations

---

## 🚀 Next Steps

1. **Run the demo** with your OpenAI key
2. **Try both CLI and Web** versions
3. **Read the output** carefully to understand learning
4. **Check** `agent_learning_history.json` for full data
5. **Explore** the code to see how it works
6. **Customize** for your own use cases!

---

## 💡 Tips for Best Results

✅ **Use OpenAI API** - Much better summaries than fallback  
✅ **Run 3-5 iterations** - Shows clear progression  
✅ **Try the web interface** - Great for presentations  
✅ **Save the JSON output** - Analyze learning patterns  
✅ **Read FEATURES.md** - Understand the architecture  

---

## 🎉 You're Ready!

Start with:
```bash
./run_cli_demo.sh
```

Or jump straight to the web interface:
```bash
./run_web_demo.sh
```

**Enjoy exploring progressive AI learning!** 🤖✨
