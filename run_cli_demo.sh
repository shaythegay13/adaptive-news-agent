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

cd "$(dirname "$0")"
if [ -x "./venv/bin/python" ]; then
  PYTHON="./venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
else
  PYTHON="python"
fi

"$PYTHON" adaptive_news_agent.py "$ITERATIONS" "$DELAY"
