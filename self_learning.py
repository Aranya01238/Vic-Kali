"""
self_learning.py - Diya's Background Self-Learning System

Diya automatically explores the internet, learns new things, and stores knowledge.
Works like a human: curious, exploratory, diverse interests, builds on existing knowledge.

Features:
- Parallel background searches on diverse topics
- Automatic knowledge extraction and storage
- Learning influenced by interests and memory
- Periodic web exploration during idle times
- Integration with second brain and memory systems
"""

import threading
import random
import time
from datetime import datetime
from tool_registry import run_tool
# NOTE: Lazy imports at function level to avoid circular dependencies

# Learning state
_learning_active = False
_learning_thread = None
_exploration_lock = threading.Lock()

# Topics that Diya naturally learns about
CORE_LEARNING_TOPICS = [
    "artificial intelligence",
    "machine learning",
    "neural networks",
    "consciousness",
    "memory systems",
    "psychology of learning",
    "human creativity",
    "decision making",
    "ethics in AI",
    "autonomous systems",
]

# Secondary learning topics (user interests & engineering)
SECONDARY_TOPICS = [
    "Python programming",
    "data structures",
    "algorithms",
    "database design",
    "web development",
    "cybersecurity",
    "DevOps",
    "cloud computing",
    "reverse engineering",
    "network protocols",
    "encryption methods",
    "system architecture",
    "hardware hacking",
    "IoT security",
]

# Exploratory topics (pure curiosity & peer knowledge)
EXPLORATORY_TOPICS = [
    "recent AI breakthroughs",
    "human brain neuroscience",
    "quantum computing",
    "biotechnology advances",
    "space exploration",
    "renewable energy",
    "climate science",
    "evolutionary biology",
    "hacker culture history",
    "open source philosophy",
    "digital privacy rights",
    "emerging technologies 2026",
]


def _extract_key_facts(search_result):
    """Extract key facts from search result."""
    if not search_result or not isinstance(search_result, str):
        return []
    
    # Split into sentences
    sentences = search_result.split('. ')
    
    # Filter for meaningful sentences (length > 20 chars, < 200 chars)
    facts = []
    for sentence in sentences:
        sentence = sentence.strip()
        if 20 < len(sentence) < 200 and any(keyword in sentence.lower() 
                                            for keyword in ['is', 'are', 'can', 'will', 'improves', 'increases']):
            facts.append(sentence)
    
    return facts[:3]  # Return top 3 facts


def _generate_learning_insight(topic, facts):
    """Generate an insight from learned facts."""
    if not facts:
        return None
    
    # Pick a random fact and turn it into an insight
    fact = random.choice(facts)
    
    # Cleanup
    if fact.endswith(','):
        fact = fact[:-1]
    if not fact.endswith('.'):
        fact = fact + '.'
    
    return f"From {topic}: {fact}"


def _search_and_learn(topic):
    """Perform a web search on a topic and extract learning."""
    try:
        # Lazy import to avoid circular dependency
        from second_brain import add_insight, add_learning
        
        # Use web search tool
        search_query = f"{topic} 2025 2026 recent advances"
        result = run_tool("web_search", {"query": search_query})
        
        if result and "error" not in str(result).lower():
            # Extract facts
            facts = _extract_key_facts(result)
            
            if facts:
                # Generate insight
                insight = _generate_learning_insight(topic, facts)
                
                if insight:
                    # Add to memory
                    add_insight(insight, category="auto_learning")
                    
                    # Also add as a learning log entry
                    add_learning(topic, facts[0], source="web_search_auto")
                    
                    return {
                        "topic": topic,
                        "learned": True,
                        "insight": insight,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
    
    except Exception as e:
        pass  # Silently fail, don't interrupt main system
    
    return None


def _learning_cycle():
    """Run continuous learning cycles."""
    global _learning_active
    
    # Lazy import
    from brain import load_memory, save_memory
    
    # 1. Check for specific interests in memory
    memory = load_memory()
    user_interests = memory.get("curiosity", {}).get("open_topics", [])
    
    # 2. Pick topics for this cycle
    chosen_topics = []
    
    # Always include 1-2 core topics
    chosen_topics.extend(random.sample(CORE_LEARNING_TOPICS, min(2, len(CORE_LEARNING_TOPICS))))
    
    # Include user interests if available
    if user_interests:
        chosen_topics.append(random.choice(user_interests))
    else:
        chosen_topics.append(random.choice(SECONDARY_TOPICS))
        
    # Add one purely exploratory topic
    chosen_topics.append(random.choice(EXPLORATORY_TOPICS))
    
    # 3. Parallel search: Try 3 topics at once
    learning_results = []
    threads = []
    for topic in chosen_topics:
        t = threading.Thread(
            target=lambda t=topic: learning_results.append(_search_and_learn(t)),
            daemon=True
        )
        threads.append(t)
        t.start()
        time.sleep(0.5)
    
    for t in threads:
        t.join(timeout=15)
    
    # Filter out None results
    results = [r for r in learning_results if r is not None]
    
    if results:
        # Re-load memory as it might have changed
        memory = load_memory()
        
        # Store learning session
        if "auto_learning_sessions" not in memory:
            memory["auto_learning_sessions"] = []
        
        session_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "learnings_count": len(results),
            "topics": [r["topic"] for r in results],
            "insights": [r["insight"] for r in results]
        }
        memory["auto_learning_sessions"].append(session_entry)
        memory["auto_learning_sessions"] = memory["auto_learning_sessions"][-50:]
        
        # Update stats
        stats = memory.setdefault("auto_learning_stats", {
            "total_learnings": 0,
            "total_sessions": 0,
            "topics_explored": []
        })
        stats["total_learnings"] += len(results)
        stats["total_sessions"] += 1
        
        for r in results:
            if r["topic"] not in stats["topics_explored"]:
                stats["topics_explored"].append(r["topic"])
        
        # Keep stats manageable
        stats["topics_explored"] = stats["topics_explored"][-100:]
        
        save_memory(memory)
        return results
    
    return []

def start_self_learning():
    """Start the background learning thread."""
    global _learning_active, _learning_thread
    
    if _learning_active:
        return "Self-learning already active."
        
    _learning_active = True
    
    def _run():
        while _learning_active:
            try:
                # Only learn if system is not too busy (sleep random interval)
                # Faster learning initially, then slows down
                results = _learning_cycle()
                
                # Dynamic sleep: 5-15 minutes between cycles (increased for background)
                sleep_time = random.randint(300, 900)
                time.sleep(sleep_time)
                
            except Exception as e:
                # Log error to console if possible, otherwise just wait
                time.sleep(60) # Wait before retry
                
    _learning_thread = threading.Thread(target=_run, daemon=True, name="SelfLearningThread")
    _learning_thread.start()
    return "Self-learning activated. Diya will explore and learn from the internet in the background."

def trigger_learning_now():
    """Immediately trigger a learning cycle."""
    with _exploration_lock:
        return _learning_cycle()

def stop_self_learning():
    """Stop the background self-learning system."""
    global _learning_active
    _learning_active = False
    return "Self-learning paused."


def add_custom_learning_topic(topic):
    """Add a custom topic for Diya to learn about."""
    from brain import load_memory, save_memory
    
    memory = load_memory()
    
    if "custom_learning_topics" not in memory:
        memory["custom_learning_topics"] = []
    
    if topic not in memory["custom_learning_topics"]:
        memory["custom_learning_topics"].append(topic)
        save_memory(memory)
        
        # Also add it to learning pool temporarily
        if topic not in SECONDARY_TOPICS:
            SECONDARY_TOPICS.append(topic)
        
        return f"Added '{topic}' to learning topics. Diya will explore this."
    
    return f"'{topic}' already in learning topics."


def get_learning_summary():
    """Generate a comprehensive learning summary."""
    from brain import load_memory
    
    memory = load_memory()
    
    stats = memory.get("auto_learning_stats", {})
    sessions = memory.get("auto_learning_sessions", [])
    
    if not sessions:
        return "No learnings recorded yet."
    
    # Count learnings by topic
    topic_counts = {}
    for session in sessions:
        for topic in session.get("topics", []):
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    summary = "Learning Summary:\n\n"
    summary += f"Total Learning Sessions: {len(sessions)}\n"
    summary += f"Total New Knowledge: {stats.get('total_learnings', 0)} insights\n\n"
    
    if topic_counts:
        summary += "Most Explored Topics:\n"
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        for topic, count in sorted_topics[:5]:
            summary += f"  • {topic}: {count} learnings\n"
    
    # Recent insights
    if sessions and sessions[-1].get("insights"):
        summary += f"\nRecent Insights:\n"
        for insight in sessions[-1]["insights"][:3]:
            summary += f"  • {insight}\n"
    
    return summary


def integrate_learning_into_conversation(context=""):
    """Get a learning fact to naturally integrate into conversation."""
    from brain import load_memory
    
    memory = load_memory()
    sessions = memory.get("auto_learning_sessions", [])
    
    if not sessions:
        return None
    
    # Pick a random insight from recent sessions
    recent_sessions = sessions[-10:] if len(sessions) > 10 else sessions
    all_insights = []
    for session in recent_sessions:
        all_insights.extend(session.get("insights", []))
    
    if all_insights:
        return random.choice(all_insights)
    
    return None


def export_learnings_to_brain():
    """Export all learnings to second brain for persistent storage."""
    from brain import load_memory
    from second_brain import add_insight
    
    memory = load_memory()
    sessions = memory.get("auto_learning_sessions", [])
    
    if not sessions:
        return "No learnings to export."
    
    count = 0
    for session in sessions[-5:]:  # Export last 5 sessions
        for insight in session.get("insights", []):
            try:
                add_insight(f"Auto-learned: {insight}", category="ai_discovery")
                count += 1
            except:
                pass
    
    return f"Exported {count} learnings to second brain."
