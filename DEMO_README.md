# Adaptive News Agent Demo

> Earlier hackathon note. The [README](README.md) describes the behavior in the current code. Examples on this page, including stored confidence scores, are promotional and are not fields the program saves.

This demo showcases an AI agent that learns and adapts its summaries as it encounters more news articles over time.

## Features

- 📊 **Progressive Learning**: Watch the agent build knowledge across multiple iterations
- 🧠 **Knowledge Vector Tracking**: Monitor total articles, iterations, and topic coverage
- 📈 **Comparison View**: See how summaries evolve and improve over time
- 🎯 **Adaptive Responses**: Agent highlights what's NEW in each update
- 💾 **History Tracking**: Full learning history saved to JSON

## Installation

1. **Install dependencies**:
   ```bash
   ./venv/bin/pip install flask
   ```

2. **Set your OpenAI API key** in `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

## Running the CLI Demo

The CLI version shows progressive learning with detailed output:

```bash
python adaptive_news_agent.py [iterations] [delay]
```

**Arguments**:
- `iterations` (default: 3) - Number of learning cycles
- `delay` (default: 2) - Seconds between iterations

**Example**:
```bash
# Run 5 iterations with 3 seconds between each
python adaptive_news_agent.py 5 3
```

### CLI Output Features:
- ✅ Shows each iteration's new article count
- 📊 Displays knowledge vector after each update
- 📝 Prints AI-generated summary
- 📈 Final comparison showing all iterations side-by-side
- 💾 Saves complete history to `agent_learning_history.json`

## Running the Web Interface

The web interface provides a beautiful, interactive visualization:

```bash
python web_agent_demo.py
```

Then open: **http://localhost:5000**

### Web Interface Features:
- 🎨 Beautiful gradient UI with smooth animations
- 📊 Real-time knowledge vector display
- 🔄 Interactive "Fetch & Analyze" button
- 📚 Learning history with visual timeline
- 🏷️ Badge indicators for INITIAL vs UPDATE summaries
- 📈 Topic coverage breakdown (AI/ML, Gaming, Mobile, etc.)
- 🔄 Reset button to start fresh

## What to Watch For

### 1. **Initial Summary** (Iteration 1)
The agent analyzes its first batch of articles with no prior context.

### 2. **Updated Summaries** (Iterations 2+)
Watch how the agent:
- Identifies what's NEW compared to previous knowledge
- Refines its analysis with more data
- Groups related stories across iterations
- Adapts its tone and focus based on accumulated knowledge

### 3. **Knowledge Vector Evolution**
Track these metrics as they grow:
- **Total Articles**: Cumulative knowledge base
- **Iterations**: Learning cycles completed
- **Learning Rate**: Articles processed per iteration
- **Topic Coverage**: Distribution across tech categories

### 4. **Accuracy Improvements**
The agent's confidence and insight should improve as it sees more data:
- Better pattern recognition
- More nuanced analysis
- Stronger connections between stories
- Higher quality summaries

## Example Output

```
🔍 ITERATION 1: Initial Knowledge Acquisition
✅ Acquired 18 articles

📊 Knowledge Vector:
{
  "total_articles": 18,
  "iterations": 1,
  "summaries_count": 1,
  "learning_rate": 18.0
}

📝 Summary:
AI-Generated Technology News Summary
==================================================
Key themes emerging from today's tech news include...
[AI generates comprehensive summary]

⏳ Waiting for new news...

🔍 ITERATION 2: Knowledge Update
✅ Found 0 NEW articles (demonstrating deduplication)

📊 Updated Knowledge Vector:
{
  "total_articles": 18,
  "iterations": 2,
  "summaries_count": 2,
  "learning_rate": 9.0
}
```

## Architecture

### `AdaptiveNewsAgent` Class
- **`knowledge_base`**: List of all articles seen
- **`seen_articles`**: Set for deduplication
- **`summaries_history`**: Complete learning history
- **`iteration`**: Current cycle counter

### Key Methods
- `fetch_new_articles()`: Get news and filter for novelty
- `generate_summary()`: Create AI summary with context
- `get_knowledge_vector()`: Current knowledge state
- `_estimate_topic_coverage()`: Categorize articles by keywords

## Extending the Demo

### Add More Iterations
```python
run_adaptive_demo(iterations=10, delay=5)
```

### Custom Topic Detection
Edit `_estimate_topic_coverage()` to add your own categories:
```python
topics = {
    "Blockchain": ["blockchain", "crypto", "web3"],
    "Your Topic": ["keyword1", "keyword2"]
}
```

### Different News Sources
Modify `news_fetcher.py` to pull from other APIs or RSS feeds.

### Save Reports
The agent automatically saves JSON history to `agent_learning_history.json`.

## Tips for Best Results

1. **Use with OpenAI API**: The demo works without it, but summaries are much better with GPT-4o-mini
2. **Run Multiple Iterations**: 3-5 iterations show clear learning progression
3. **Wait Between Runs**: In production, schedule runs hourly/daily for genuinely new news
4. **Monitor Topic Coverage**: See which tech areas dominate the news cycle

## Troubleshooting

**No new articles found**: Normal if running iterations too quickly. News APIs don't update every second.

**OpenAI errors**: Check your API key in `.env` and ensure you have credits.

**Port 5000 in use**: Change the port in `web_agent_demo.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## Next Steps

- Add persistence (database instead of in-memory)
- Implement scheduled background fetching
- Add more sophisticated topic modeling
- Create accuracy scoring mechanism
- Export reports as PDF or markdown
