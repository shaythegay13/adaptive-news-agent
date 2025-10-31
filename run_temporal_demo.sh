#!/bin/bash
# Launch the Temporal News Agent Demo - Tracks trends over time

echo "🕐 Temporal News Agent - Pattern Learning Demo"
echo "=============================================="
echo ""

# Default values
ITERATIONS=${1:-5}
DELAY=${2:-3}

echo "Running $ITERATIONS iterations with ${DELAY}s intervals"
echo "This version tracks how topics evolve and learns patterns!"
echo ""

./venv/bin/python temporal_news_agent.py $ITERATIONS $DELAY
