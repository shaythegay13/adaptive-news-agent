#!/bin/bash
# Multi-Temporal News Analysis - Compare 3 time periods

echo "🕰️  Multi-Temporal News Analysis"
echo "================================="
echo ""
echo "Analyzing technology news across 3 time periods:"
echo "  📅 Recent: Now - 6 months"
echo "  📅 Mid-term: 6 months - 1 year ago"
echo "  📅 Long-term: 1 year - 3 years ago"
echo ""
echo "This will fetch real historical data and show trend evolution!"
echo ""

./venv/bin/python multi_temporal_agent.py
