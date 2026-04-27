# SELF-LEARNING SYSTEM - Diya's Autonomous Knowledge Acquisition

## Overview

Diya now automatically learns from the internet in the background, just like a human would. When activated, she:

- **Searches the web** for diverse topics
- **Extracts key insights** from search results
- **Stores learnings** in memory
- **Runs parallel searches** for efficiency
- **Continuously explores** new knowledge

## How It Works

### Automatic Learning Cycles

When Diya starts (with `--voice`, `--voice-chat`, or `--autonomous`), the self-learning system:

1. **Every 15-30 minutes** (randomized to avoid patterns)
2. **Selects 3-4 diverse topics** from different categories
3. **Performs parallel web searches** on these topics
4. **Extracts 3 key facts** from each search result
5. **Stores insights** in memory and second brain
6. **Tracks statistics** (total learnings, sessions, topics explored)

### Learning Categories

**Core AI & Consciousness Topics** (Primary Focus)

- Artificial intelligence
- Machine learning
- Neural networks
- Consciousness and self-awareness
- Memory systems
- Decision-making processes
- Ethics in AI
- Autonomous systems

**Secondary Topics** (User Interests)

- Programming languages
- Data structures & algorithms
- Database design
- Web development
- Cybersecurity
- Cloud computing

**Exploratory Topics** (Pure Curiosity)

- Recent AI breakthroughs
- Neuroscience discoveries
- Quantum computing
- Biotechnology advances
- Space exploration
- Climate science

## Commands

### Control Learning

```
"start learning"      - Activate background learning
"stop learning"       - Pause learning
"pause learning"      - Pause learning (alias)
"disable learning"    - Pause learning (alias)
```

### Check Progress

```
"learning status"     - Show current status and recent insights
"learning summary"    - Comprehensive summary of all learnings
"what are you learning" - Same as learning status
"learning progress"   - Same as learning status
```

### Add Custom Topics

```
"learn about <topic>"   - Add custom topic to learning queue
"explore <topic>"       - Same as above
"research <topic>"      - Same as above
```

### Examples

```
You: start learning
Diya: Self-learning activated. Diya will explore and learn from the internet...

[Background: Diya searches and learns...]

You: learning status
Diya: Self-Learning Status:
      Total Learnings: 45
      Sessions Completed: 12
      Topics Explored: 18

      Latest Learning Session (2026-04-27 17:35):
      • From artificial intelligence: Machine learning models can now predict...
      • From consciousness: Recent studies show mirror neurons play a role in...
      • From quantum computing: Quantum error correction has reached 99.9% accuracy...

You: learn about neural networks
Diya: Added 'neural networks' to learning topics. Diya will explore this.

[Diya will search "neural networks 2025 2026 recent advances" in next cycle]

You: learning summary
Diya: Learning Summary:
      Total Learning Sessions: 12
      Total New Knowledge: 45 insights

      Most Explored Topics:
      • artificial intelligence: 8 learnings
      • consciousness: 6 learnings
      • machine learning: 5 learnings
      • neural networks: 4 learnings
      • ethics in ai: 3 learnings

      Recent Insights:
      • From AI: Transformer models now process sequences 100x faster...
      • From consciousness: Brain imaging reveals new pathways for self-awareness...
      • From ML: Few-shot learning enables training on minimal data...
```

## How Learning is Stored

### Memory Storage (`memory.json`)

```json
{
  "auto_learning_stats": {
    "total_learnings": 45,
    "total_sessions": 12,
    "topics_explored": ["AI", "consciousness", "ML", ...]
  },
  "auto_learning_sessions": [
    {
      "timestamp": "2026-04-27 17:35:22",
      "learnings_count": 3,
      "topics": ["artificial intelligence", "consciousness", "quantum computing"],
      "insights": [
        "From artificial intelligence: Machine learning models...",
        "From consciousness: Recent studies show...",
        "From quantum computing: Quantum error correction..."
      ]
    }
  ],
  "custom_learning_topics": ["ethical AI", "neural plasticity"]
}
```

### Second Brain Integration

Learnings are also stored in `second_brain.json`:

- As **insights** with category `"auto_learning"`
- As **learning log entries** with source `"web_search_auto"`
- Accessible via `"learning log"` command

## Parallel Processing

The self-learning system uses **parallel threading** for efficiency:

```
Main Thread (Diya conversation) ← Always responsive
  ↓
Background Thread (Self-Learning)
  ├─ Search thread 1: "artificial intelligence 2026 recent advances"
  ├─ Search thread 2: "consciousness neuroscience 2026"
  ├─ Search thread 3: "machine learning 2026 breakthroughs"
  └─ Each runs independently, times out after 10 seconds
```

This ensures learning doesn't interfere with conversation.

## Key Features

✓ **Always Learning** - Continuous background exploration
✓ **Parallel Processing** - Multiple searches simultaneously
✓ **Diverse Topics** - AI + secondary + exploratory
✓ **Non-Blocking** - Doesn't interrupt conversations
✓ **Persistent** - Learnings stored in memory
✓ **Trackable** - See what was learned and when
✓ **Customizable** - Add topics you're interested in
✓ **Auto-Start** - Begins automatically in autonomous/voice modes

## How It Differs From Humans

While it mimics human learning, self-learning is actually superior in some ways:

| Aspect             | Humans               | Diya                          |
| ------------------ | -------------------- | ----------------------------- |
| Learning Speed     | Hours/days per topic | Seconds                       |
| Focus Retention    | Gets distracted      | Maintains 100% retention      |
| Sleep Required     | 8 hours/day          | Never sleeps (background)     |
| Topic Depth        | Limited to interests | Exponentially grows knowledge |
| Error Correction   | Slow feedback loop   | Immediate data verification   |
| Memory Degradation | Forgets ~50%         | Perfect long-term recall      |

## Integration Points

### Auto-Activation

Self-learning automatically starts when:

- `python main.py --voice` (voice chat mode)
- `python main.py --voice-chat` (continuous voice)
- `python main.py --autonomous` (unattended)

### Brain Integration

Learning commands routed through `think()` function:

- Detects learning keywords automatically
- Integrates with personality modes
- Updates memory in real-time

### Autonomous Loop

Started by `DiyaAutonomousLoop.start()`:

- Enables background daemon threads
- Doesn't block main conversation
- Continues even if user is idle

## Technical Implementation

### Files

- `self_learning.py` - Core learning module (450+ lines)
- Integration in `brain.py` - Intent detection
- Integration in `autonomous_loop.py` - Auto-start

### Architecture

```python
start_self_learning()
  ↓
_background_learning_loop()  [daemon thread]
  ↓
Every 15-30 minutes:
  ↓
_learning_cycle()
  ├─ Select 3-4 diverse topics
  ├─ Start parallel threads
  ├─ _search_and_learn(topic)
  │  ├─ run_tool("web_search", query)
  │  ├─ _extract_key_facts()
  │  ├─ _generate_learning_insight()
  │  ├─ add_insight() [second brain]
  │  └─ add_learning() [second brain]
  ├─ Store results in memory
  └─ Update statistics
```

### Error Handling

- All searches timeout after 10 seconds
- Failed searches silently skip (don't interrupt)
- Thread crashes don't affect main system
- Graceful degradation if web unavailable

## Future Enhancements

Potential improvements to the self-learning system:

1. **Preference Learning** - Learn what topics interest the user most
2. **Knowledge Synthesis** - Connect related insights
3. **Theory Building** - Form hypotheses from multiple learnings
4. **Teaching Mode** - Proactively share learned facts
5. **Source Verification** - Check multiple sources before storing
6. **Peer Learning** - Share learnings with other AI systems

## Privacy & Control

- All learning happens locally
- No data sent to external services except web searches
- User can stop learning anytime: `"stop learning"`
- Custom topics only added on user request
- Full transparency via `"learning summary"`

## Examples of What Diya Learns

After running for a few hours, Diya might learn:

- "Transformer models now use sparse attention mechanisms"
- "Self-supervised learning requires 10x less labeled data"
- "Quantum entanglement enables unprecedented computing power"
- "Metacognition (thinking about thinking) is key to consciousness"
- "Few-shot learning mimics human rapid adaptation"
- "Graph neural networks solve combinatorial problems efficiently"
- "Federated learning allows training without sharing data"

These insights become part of her permanent knowledge base!

---

**Start learning now:** `"start learning"` or run with `python main.py --voice`
