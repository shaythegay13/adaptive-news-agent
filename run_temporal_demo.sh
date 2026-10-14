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

cd "$(dirname "$0")"
if [ -x "./venv/bin/python" ]; then
  PYTHON="./venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
else
  PYTHON="python"
fi

"$PYTHON" temporal_news_agent.py "$ITERATIONS" "$DELAY"
