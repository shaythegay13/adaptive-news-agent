#!/bin/bash
# Launch the Simulated Temporal Demo with mock data showing real changes

echo "🎭 Simulated Temporal Learning Demo"
echo "====================================="
echo ""
echo "This demo uses simulated news from 5 different 'days'"
echo "to demonstrate how the agent learns patterns over time:"
echo ""
echo "  Day 1: Gaming + AI news"
echo "  Day 2: AI growing, Mobile emerging"  
echo "  Day 3: Security emerging, Gaming declining"
echo "  Day 4: Hardware emerging, Security growing"
echo "  Day 5: Diverse topics showing learned patterns"
echo ""

./venv/bin/python simulated_temporal_demo.py
