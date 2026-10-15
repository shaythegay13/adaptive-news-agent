# Arc Agent Project

> Earlier note kept for the Eclipse LMOS Arc stub. Setup for the news demos is in the [README](README.md).

This project uses the Eclipse LMOS Arc framework for building AI agents.

## 🎯 Featured Demo: Adaptive News Agent

This project includes a **powerful demonstration** of an AI agent that learns and adapts over time. The agent fetches technology news and shows progressive improvement across multiple iterations.

### Quick Start the Demo

**CLI Version** (detailed output with learning progression):
```bash
./run_cli_demo.sh [iterations] [delay]
```

**Web Interface** (beautiful interactive dashboard):
```bash
./run_web_demo.sh
# Then open http://localhost:5000
```

See **[DEMO_README.md](DEMO_README.md)** for complete documentation.

## Setup

1. **Build the project**:
   ```bash
   ./gradlew build
   ```

## Running the Agent

Your `SelfUpdater.agent` is configured to summarize technology news using GPT-4o.

To run it with the arc-atlas tool:
```bash
atlas SelfUpdater.agent
```

## Dependencies

- `arc-agents:0.185.0`: Core Arc agents library
- `arc-server:0.185.0`: Arc server implementation

## Requirements

- Java 21 (required by Arc 0.185.0)
- Kotlin 2.1.21 (Arc 0.185.0 metadata is Kotlin 2.1)
