#!/bin/bash
# Launch the CLI Adaptive News Agent Demo

echo "🤖 Adaptive News Agent - CLI Demo"
echo "=================================="
echo ""

# Default values
ITERATIONS=${1:-3}
DELAY=${2:-2}

echo "Running $ITERATIONS iterations with ${DELAY}s delay between each"
echo ""

./venv/bin/python adaptive_news_agent.py $ITERATIONS $DELAY
