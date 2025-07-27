# GreyScan Intelligence Platform

**Adaptive Web Intelligence Collection and Analysis System**

 GreyScan is a modular Python-based platform for real-time collection, analysis, and correlation of publicly available data across major web platforms. It operates without relying on APIs or authentication, and is optimized for research, intelligence, and data analysis use cases.


## System Architecture

### Core Components

The platform consists of seven specialized engines that can operate independently or in coordination:

1. **Master Orchestrator** (`greyscan_master.py`) - Coordinates multiple engines in sequential phases
2. **Discovery Engine** (`greyscan_discovery.py`) - Identifies alternative data access endpoints through failure analysis
3. **Universal Scanner** (`greyscan_universal.py`) - Multi-platform data collection with pattern learning
4. **Intelligence Platform** (`greyscan_intelligence.py`) - Entity resolution and relationship mapping
5. **Crypto Engine** (`greyscan_real_aggressive.py`) - Cryptocurrency and DeFi data collection
6. **Core Engine** (`greyscan_core.py`) - Basic adaptive collection with learning algorithms
7. **GUI Interface** (`greyscan_gui.py`) - Interactive monitoring and control interface

### Technical Approach

**Adaptive Pattern Recognition**: The system learns from successful and failed data access attempts, building a knowledge base of working patterns for each platform.

**Emergent Path Discovery**: When primary access methods fail, the discovery engine systematically tests variations to find alternative endpoints.

**Cross-Platform Entity Resolution**: The intelligence platform correlates entities across multiple platforms using name matching, aliases, and behavioral patterns.

**Multi-Phase Operation**: The master orchestrator executes collection in phases - discovery, scanning, analysis, correlation - to maximize data coverage and quality.

## Supported Platforms

The system has been tested against the following platforms with varying success rates:

- **Social Media**: Twitter, Reddit, Instagram, YouTube, Medium, Telegram
- **Development**: GitHub, GitLab
- **Financial**: CoinGecko, CoinMarketCap, DeFiLlama, Etherscan
- **Custom**: Any HTTP-accessible endpoint

## Usage

### Master Orchestrator

```python
from greyscan_master import GreyScanMaster, MasterTarget

targets = [
    MasterTarget(
        name="bitcoin",
        platforms=["coingecko", "reddit"],
        target_type="cryptocurrency",
        aliases=["btc"],
        tags=["crypto"]
    )
]

async with GreyScanMaster() as master:
    report = await master.ultimate_intelligence_operation(targets)
```

### Individual Engines

```python
# Intelligence platform with entity resolution
from greyscan_intelligence import GreyScanIntelligence, IntelligenceTarget

targets = [IntelligenceTarget("bitcoin", "coingecko", "cryptocurrency")]
async with GreyScanIntelligence() as intel:
    report = await intel.full_intelligence_scan(targets)

# Universal scanner
from greyscan_universal import GreyScanUniversal, UniversalTarget

targets = [UniversalTarget("bitcoin", "coingecko")]
async with GreyScanUniversal() as scanner:
    results = await scanner.universal_scan(targets)
```

### Command Line Interface

```bash
# Run master orchestrator
python greyscan_master.py

# Run individual engines
python greyscan_intelligence.py
python greyscan_universal.py
python greyscan_discovery.py

# Launch GUI
python greyscan_gui.py
```

## Data Storage

The system uses SQLite for persistent storage with the following schema:

- **Entities**: Unique identifiers with cross-platform aliases
- **Intelligence Data**: Raw collected data with metadata
- **Relationships**: Mapped connections between entities
- **Analysis Results**: Processed intelligence outputs

## Performance Characteristics

Based on controlled testing:

- **Discovery Engine**: Identifies alternative endpoints with ~60% success rate
- **Universal Scanner**: Achieves data collection across multiple platforms simultaneously
- **Intelligence Platform**: Performs entity resolution and relationship mapping
- **Response Times**: Varies by platform and data volume (typically 1-120 seconds per operation)

## Installation

### Requirements

```
Python 3.8+
aiohttp>=3.8.0
beautifulsoup4>=4.11.0
networkx>=2.8.0
```

### Setup

```bash
git clone https://github.com/Betti-Labs/greyscan.git
cd greyscan
pip install -r requirements.txt
```

## Configuration

The system operates with minimal configuration. Target specification includes:

- **Name**: Entity identifier
- **Platform**: Target platform(s)
- **Type**: Entity classification
- **Aliases**: Alternative identifiers
- **Priority**: Processing priority (1-10)

## Research Applications

This platform is designed for legitimate research applications including:

- **Academic Research**: Large-scale social media analysis
- **Market Research**: Public sentiment and trend analysis  
- **Security Research**: Open source intelligence gathering
- **Journalism**: Investigative research and fact verification

## Limitations

- **Rate Limiting**: Subject to platform-specific rate limits
- **Data Availability**: Limited to publicly accessible information
- **Platform Changes**: Effectiveness may vary as platforms modify their systems
- **Legal Compliance**: Users responsible for adherence to applicable laws and terms of service

## Technical Documentation

- `ENGINES_SUMMARY.md` - Detailed engine specifications
- `docs/api.md` - API documentation and examples
- `docs/best-practices.md` - Implementation guidelines
- `docs/platforms/` - Platform-specific documentation

## Contributing

This is a research project. See `CONTRIBUTING.md` for development guidelines.

## License

Proprietary software. All rights reserved.

---

**GreyScan Intelligence Platform - Modular Web Intelligence Collection System**
