#!/bin/bash
# Launch the Web Adaptive News Agent Demo

echo "🌐 Adaptive News Agent - Web Interface"
echo "======================================"
echo ""
echo "Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
if [ -x "./venv/bin/python" ]; then
  PYTHON="./venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
else
  PYTHON="python"
fi

"$PYTHON" web_agent_demo.py
