"""
Simple web interface for the Adaptive News Agent
Shows real-time learning and adaptation
"""

from flask import Flask, render_template, jsonify, request
from adaptive_news_agent import AdaptiveNewsAgent
import json

app = Flask(__name__)
agent = AdaptiveNewsAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch', methods=['POST'])
def fetch_news():
    """Fetch new articles and generate summary."""
    new_articles, all_articles = agent.fetch_new_articles()
    
    is_update = agent.iteration > 0
    summary = agent.generate_summary(new_articles, is_update=is_update)
    
    return jsonify({
        "success": True,
        "summary": summary,
        "knowledge_vector": agent.get_knowledge_vector(),
        "history": agent.summaries_history
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current agent status."""
    return jsonify({
        "knowledge_vector": agent.get_knowledge_vector(),
        "history": agent.summaries_history
    })

@app.route('/api/reset', methods=['POST'])
def reset_agent():
    """Reset the agent."""
    global agent
    agent = AdaptiveNewsAgent()
    return jsonify({"success": True, "message": "Agent reset"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
