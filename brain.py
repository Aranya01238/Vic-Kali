import json
import re
import random
from datetime import datetime
from tool_registry import run_tool
from personality_modes import (
    detect_manual_mode_switch, detect_auto_mode,
    style_response, get_mode_greeting, list_modes, get_mode_info, choose_best_mode
)
from context_engine import analyze_context, get_context_summary
from task_manager import detect_task_intent, execute_task_action
from engineering_assistant import detect_engineering_intent, execute_engineering_action
from life_cycle import get_current_state, get_state_properties
from self_evolution import ensure_evolution_state, run_evolution_cycle, evolution_summary, choose_autonomous_objective
from second_brain import detect_brain_intent, execute_brain_action
from self_learning import (
    start_self_learning, stop_self_learning, get_learning_status,
    trigger_learning_now, add_custom_learning_topic, get_learning_summary
)
from consciousness_engine import consciousness_engine

# ================= LOAD EMOTIONS =================

with open("emotions.json", "r", encoding="utf-8") as f:
    EMOTION_KEYWORDS = json.load(f)

ALL_EMOTIONS = list(EMOTION_KEYWORDS.keys())

# ================= MEMORY =================

def load_memory():
    try:
        with open("memory.json", "r") as f:
            memory = json.load(f)
    except FileNotFoundError:
        memory = {}

    memory.setdefault("identity", {"real_name": None, "preferred_name": None})
    memory.setdefault("profile", {"college": None, "field": None, "location": None})
    memory.setdefault("state", {
        "awaiting_preferred_name": True,
        "awaiting_real_name": False
    })
    memory.setdefault("emotion", {"user_mood": "neutral", "friend_mood": "neutral"})
    memory.setdefault("episodes", [])
    memory.setdefault("emotion_history", {e: 0 for e in ALL_EMOTIONS})
    memory.setdefault("thoughts", [])
    memory.setdefault("goals", {"primary": None})
    memory.setdefault("curiosity", {"open_topics": []})
    memory.setdefault("beliefs", {})
    memory.setdefault("user_model", {"engagement_level": None})
    memory.setdefault("values", {
        "kindness": 0.5,
        "honesty": 0.5,
        "growth": 0.5,
        "respect": 0.5
    })
    memory.setdefault("self_model", {
        "personality": "neutral",
        "default_tone": "supportive",
        "interaction_count": 0
    })
    memory.setdefault("meta", {"success_score": 0.5})
    memory.setdefault("emotion_drift", {"recent": [], "influence": 0.5})
    memory.setdefault("imagination", {"future_scenarios": []})
    memory.setdefault("consciousness", {
        "awareness_level": 0.5,
        "self_narrative": ""
    })
    memory.setdefault("tool_performance", {
        "time": {"success": 0, "fail": 0, "avg_response_time": 0},
        "random": {"success": 0, "fail": 0, "avg_response_time": 0},
        "web_search": {"success": 0, "fail": 0, "avg_response_time": 0},
        "wiki_search": {"success": 0, "fail": 0, "avg_response_time": 0},
        "calculate": {"success": 0, "fail": 0, "avg_response_time": 0},
        "convert_units": {"success": 0, "fail": 0, "avg_response_time": 0},
        "download_file": {"success": 0, "fail": 0, "avg_response_time": 0},
        "analyze_file": {"success": 0, "fail": 0, "avg_response_time": 0},
        "logical_operation": {"success": 0, "fail": 0, "avg_response_time": 0}
    })
    memory.setdefault("tool_preferences", {
        "most_successful": None,
        "least_successful": None,
        "fastest": None,
        "slowest": None
    })
    memory.setdefault("life_cycle", {
        "current_state": "active",
        "energy": 1.0,
        "last_sleep_time": None,
        "last_wake_time": None,
        "dreams": [],
        "daily_journal": [],
        "idle_thoughts": [],
        "last_spoke_at": None,
        "last_user_interaction": None
    })
    memory.setdefault("personality_mode", {
        "current": "friend",
        "auto_switch": True,
        "history": []
    })
    memory.setdefault("context", {
        "current_mood": "neutral",
        "current_task": "general",
        "mood_history": [],
        "task_history": []
    })
    memory.setdefault("conversation", {
        "last_topic": None,
        "recent_responses": [],
        "last_response": None
    })
    memory.setdefault("evolution", {
        "version": 1,
        "reflection_count": 0,
        "last_reflection": None,
        "current_focus": "general_growth",
        "active_hypotheses": [],
        "approved_changes": [],
        "recent_observations": [],
        "history": [],
    })

    ensure_evolution_state(memory)

    return memory

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)


def remember_response(memory, response):
    """Track recent responses so fallback replies do not repeat too often."""
    conversation = memory.setdefault("conversation", {})
    recent_responses = conversation.setdefault("recent_responses", [])

    if response:
        recent_responses.append(response)
        conversation["last_response"] = response
        conversation["recent_responses"] = recent_responses[-6:]

# ================= NAME EXTRACTION =================

def extract_preferred_name(text):
    m = re.search(r"(call me|you can call me|i am called)\s+(.+)", text, re.I)
    if m:
        return m.group(2).strip().title()
    return None

def extract_real_name(text):
    m = re.search(r"(my real name is|my name is)\s+(.+)", text, re.I)
    if m:
        return m.group(2).strip().title()
    return None

# ================= TOOL INTENT =================

def detect_tool_intent(text, memory=None):
    t = text.lower()
    
    # Check for follow-up search requests like "find the answer" or "search it"
    if any(p in t for p in ["find the answer", "search it", "look it up", "find in internet", "search in internet", "then find", "find in google"]) or \
       (memory and memory.get("episodes") and len(t.split()) <= 4 and any(p in memory["episodes"][-1]["text"].lower() for p in ["what is", "who is", "define", "meaning of", "full form of", "search for"])):
        
        query = t
        # Patterns to remove to get the clean query
        for p in ["find the answer", "search it", "look it up", "find in internet", "search in internet", "then find", "find in google", "find in", "find", "then", "internet", "google"]:
            if p in query:
                query = query.replace(p, "").strip()
        
        # If query is too generic or the user just said a word like "supercomputer"
        generic_queries = {"", "the answer", "it", "for me", "about it", "the truth", "answer", "search", "find"}
        if query in generic_queries or len(query.split()) <= 3:
            # Check if current query is a specific term (not generic)
            if len(query) > 2 and query not in generic_queries and not any(p in query for p in ["what", "who", "tell", "show"]):
                # This is likely the term itself (e.g. "supercomputer")
                pass
            elif memory and "episodes" in memory and memory["episodes"]:
                # Look for the last non-command episode to find the original subject
                for ep in reversed(memory["episodes"]):
                    last_text = ep["text"].lower()
                    # Skip generic or command-like phrases
                    if not any(cmd in last_text for cmd in ["find", "search", "look up", "exit", "status", "stop", "wait"]):
                        # Extract query from last_text if it had a starter
                        potential_query = last_text
                        for starter in ["what is the meaning of", "what is the definition of", "what is the full form of", "what is", "who is", "define", "meaning of", "full form of"]:
                            if potential_query.startswith(starter):
                                potential_query = potential_query[len(starter):].strip()
                                break
                        
                        if len(potential_query) > 2:
                            # If the user just said "supercomputer", and the last was "what is computer", 
                            # we should prioritize the current word if it's a noun.
                            # For now, if query is specific, we use it, else we use potential_query.
                            if len(query) > 2 and query not in generic_queries:
                                pass # Keep current query
                            else:
                                query = potential_query
                            break
        
        if query and query not in generic_queries:
            # Clean up query (remove "what is", "tell me about", etc.)
            for starter in ["what is", "tell me about", "who is", "how to", "is a", "is an"]:
                if query.startswith(starter):
                    query = query[len(starter):].strip()
            
            # Remove trailing question mark
            query = query.replace("?", "").strip()
            
            if len(query) > 1:
                return ("web_search", {"query": query})

    # HACKER / PEER TOOLS
    if any(p in t for p in ["system stats", "diagnostics", "system health", "resource usage", "pc status"]):
        return ("get_system_stats", {})
    
    if any(p in t for p in ["network info", "ip address", "scan network", "connection status", "ping test"]):
        return ("get_network_info", {})
    
    if any(p in t for p in ["security check", "check vulnerability", "encryption status", "firewall status", "security audit"]):
        return ("check_security", {})

    # HEALTHCARE (Diya/Baymax Protocols)
    if "satisfied with my care" in t:
        return ("satisfaction_check", {"user_satisfied": True})
    
    if any(p in t for p in ["deactivate", "shutdown", "stop health companion"]):
        return ("satisfaction_check", {"user_satisfied": False})

    if any(p in t for p in ["combat mode", "activate armor", "protect me", "fight"]):
        enable = "deactivate" not in t and "stop" not in t
        return ("combat_mode", {"enable": enable})

    if any(p in t for p in ["first aid", "how to treat", "treat a", "treatment for"]):
        injury = text.lower().replace("first aid", "").replace("how to treat", "").replace("treat a", "").replace("treatment for", "").strip()
        return ("first_aid_instruction", {"injury": injury})

    if any(p in t for p in ["scan", "check my vitals", "health check", "vitals"]):
        return ("scan_vitals", {})

    if any(p in t for p in ["i have a", "diagnose", "symptoms", "hurts", "pain", "i feel"]):
        symptoms = text.lower().replace("i have a", "").replace("diagnose", "").replace("symptoms", "").replace("hurts", "").replace("pain", "").replace("i feel", "").replace("my", "").strip()
        return ("diagnose_issue", {"symptoms": symptoms})

    # GENERAL KNOWLEDGE SEARCH (Catch-all for 'what is', 'who is', etc.)
    if any(t.startswith(p) for p in ["what is", "who is", "what are", "tell me about", "define ", "explain ", "search for ", "meaning of ", "full form of ", "is a ", "is an "]):
        # Skip if it's a calculation or opinion request
        if not (any(op in t for op in ['+', '-', '*', '/', '^']) or "opinion" in t or "your view" in t):
            query = text
            # Expanded starters to clean
            starters = [
                "what is the meaning of", "what is the definition of",
                "what is the full form of", "what is the", "what is", 
                "who is", "what are", "tell me about", "define", "explain", 
                "search for", "meaning of", "full form of", "is a", "is an"
            ]
            
            t_lower = t
            for p in starters:
                if t_lower.startswith(p):
                    query = text[len(p):].strip()
                    break
            
            # Clean common articles from the start of the query
            query_lower = query.lower()
            for article in ["a ", "an ", "the "]:
                if query_lower.startswith(article):
                    query = query[len(article):].strip()
                    break
            
            if not query or query.lower() in ["the", "a", "an", "it", "this", "that", "something"]:
                return (None, None)
                    
            return ("web_search", {"query": query.replace("?", "").strip()})

    # TIME
    if any(t.startswith(p) for p in [
        "what is the time",
        "what's the time",
        "show me the time",
        "tell me the time",
        "current time",
        "what time is it"
    ]):
        return ("time", {})

    # RANDOM
    if any(p in t for p in [
        "random number",
        "pick a number",
        "any number"
    ]):
        return ("random", {})

    # WIKIPEDIA SEARCH
    if any(t.startswith(p) for p in [
        "wikipedia",
        "wiki search",
        "look up on wikipedia"
    ]):
        query = text.replace("wikipedia", "").replace("wiki search", "").replace("look up on wikipedia", "").strip()
        return ("wiki_search", {"query": query})

    # VERIFY INFO
    if any(t.startswith(p) for p in [
        "is it true that",
        "verify that",
        "check if",
        "is this correct"
    ]):
        claim = text.replace("is it true that", "").replace("verify that", "").replace("check if", "").replace("is this correct", "").strip()
        return ("verify_info", {"claim": claim})

    # DOWNLOAD FILE
    if any(t.startswith(p) for p in [
        "download",
        "get file from",
        "fetch file",
        "download file from"
    ]):
        # Extract URL from text
        words = text.split()
        url = None
        filename = None
        
        for word in words:
            if word.startswith('http'):
                url = word
                break
        
        if url:
            return ("download_file", {"url": url})
        else:
            return ("download_file", {"url": text.split()[-1]})  # Assume last word is URL

    # ANALYZE FILE
    if any(t.startswith(p) for p in [
        "analyze file",
        "summarize file",
        "what's in file",
        "examine file"
    ]):
        filepath = text.split(" ", 2)[-1]  # Get the file path
        return ("analyze_file", {"filepath": filepath})

    # DOWNLOAD AND ANALYZE
    if any(t.startswith(p) for p in [
        "download and analyze",
        "get and analyze",
        "fetch and summarize"
    ]):
        words = text.split()
        url = None
        
        for word in words:
            if word.startswith('http'):
                url = word
                break
        
        if url:
            return ("download_and_analyze", {"url": url})
        else:
            return ("download_and_analyze", {"url": text.split()[-1]})

    # CALCULATE - Only for actual mathematical expressions (very specific)
    if (t.startswith("calculate") and any(op in t for op in ['+', '-', '*', '/', '=', '^']) and not any(word in t for word in ["factorial", "convert", "and"])) or \
       (t.startswith("what is") and any(op in t for op in ['+', '-', '*', '/', '=', '^']) and not any(word in t for word in ["opinion", "your", "the"])) or \
       (t.startswith("solve") and any(op in t for op in ['+', '-', '*', '/', '=', '^'])):
        # Extract mathematical expression
        expr = text
        for prefix in ["calculate", "compute", "what is", "solve"]:
            if expr.lower().startswith(prefix):
                expr = expr[len(prefix):].strip()
                break
        expr = expr.replace("?", "").strip()
        
        if expr:
            return ("calculate", {"expression": expr})

    # CONVERT UNITS - Simple conversions only (not part of complex math)
    if any(phrase in t for phrase in [
        "convert",
        "how many",
        "change to",
        "in terms of"
    ]) and any(unit in t for unit in [
        "meter", "km", "mile", "inch", "foot", "yard",
        "gram", "kg", "pound", "ounce", "ton",
        "celsius", "fahrenheit", "kelvin",
        "second", "minute", "hour", "day", "week", "month", "year"
    ]) and not (" and " in text and ("factorial" in text or "calculate" in text)):
        # Parse conversion request
        words = text.split()
        try:
            # Look for number and units
            value = None
            from_unit = None
            to_unit = None
            
            for i, word in enumerate(words):
                if word.replace('.', '').replace('-', '').isdigit():
                    value = word
                    if i + 1 < len(words):
                        from_unit = words[i + 1]
                    break
            
            # Look for "to" keyword
            if "to" in words:
                to_idx = words.index("to")
                if to_idx + 1 < len(words):
                    to_unit = words[to_idx + 1]
            
            if value and from_unit and to_unit:
                return ("convert_units", {"value": value, "from_unit": from_unit, "to_unit": to_unit})
        except:
            pass

    # DATE MATH
    if any(phrase in t for phrase in [
        "days between",
        "difference between",
        "add days",
        "subtract days",
        "how long until",
        "how long since"
    ]):
        # Simple date math parsing
        if "between" in t:
            return ("date_math", {"operation": "difference", "date1": "today", "date2": "tomorrow", "unit": "days"})
        elif "add" in t:
            return ("date_math", {"operation": "add", "date1": "today", "date2": "7", "unit": "days"})

    # LOGICAL OPERATIONS
    if any(t.startswith(p) for p in [
        "logical and",
        "logical or",
        "logical not",
        "logical xor"
    ]):
        parts = text.split()
        if len(parts) >= 3:
            operation = parts[1]  # and, or, not, xor
            args = parts[2:]
            return ("logical_operation", {"operation": operation, "args": args})

    # TOOL PERFORMANCE
    if any(t.startswith(p) for p in [
        "show tool performance",
        "tool performance",
        "how are my tools doing",
        "tool statistics",
        "tool stats"
    ]):
        return ("show_tool_performance", {})

    if any(t.startswith(p) for p in [
        "reset tool performance",
        "reset tool stats",
        "clear tool performance"
    ]):
        return ("reset_tool_performance", {})

    # LIST TOOLS
    if any(t.startswith(p) for p in [
        "list all tools",
        "show all tools",
        "what tools do you have",
        "available tools"
    ]):
        return ("list_all_tools", {})

    # SEARCH TOOLS
    if any(t.startswith(p) for p in [
        "search tools",
        "find tools",
        "tools for"
    ]):
        query = text.split(" ", 2)[-1] if len(text.split()) > 2 else ""
        return ("search_tools", {"query": query})

    # KNOWLEDGE COMPRESSION TOOLS
    if any(t.startswith(p) for p in [
        "compress knowledge",
        "compress my knowledge",
        "analyze knowledge patterns",
        "knowledge patterns"
    ]):
        if "patterns" in t:
            return ("analyze_knowledge_patterns", {})
        else:
            return ("compress_knowledge", {})

    if any(t.startswith(p) for p in [
        "show compressed knowledge",
        "compressed knowledge",
        "knowledge insights",
        "show insights"
    ]):
        return ("show_compressed_knowledge", {})

    if any(t.startswith(p) for p in [
        "knowledge summary",
        "summarize knowledge",
        "generate summary",
        "comprehensive summary"
    ]):
        return ("generate_knowledge_summary", {})

    # REASONING TOOLS (Phase 2.9) - Extended Patterns
    if any(phrase in t for phrase in ["what do you think", "your opinion", "your view", "form opinion"]):
        topic = text.lower().split("opinion on", 1)[1].strip() if "opinion on" in text.lower() else ""
        if not topic:
            topic = text.lower().split("think about", 1)[1].strip() if "think about" in text.lower() else ""
        return ("form_opinion", {"topic": topic.replace("?", "").strip()})

    if any(phrase in t for phrase in ["predict", "forecast", "future of", "will happen"]):
        scenario = text.lower().split("predict", 1)[1].strip() if "predict" in text.lower() else text
        return ("make_prediction", {"scenario": scenario.replace("?", "").strip(), "timeframe": "near future"})

    if any(phrase in t for phrase in ["advice", "advise", "what should i do", "suggest"]):
        situation = text.lower().split("advice on", 1)[1].strip() if "advice on" in text.lower() else text
        return ("give_advice", {"situation": situation.replace("?", "").strip()})

    if any(phrase in t for phrase in ["reason about", "analyze", "how does"]):
        topic = text.lower().split("analyze", 1)[1].strip() if "analyze" in text.lower() else text
        return ("reason_about", {"topic": topic.replace("?", "").strip(), "question": text})

    if any(phrase in t for phrase in ["connect", "relate", "synthesize", "relationship between"]):
        return ("synthesize_knowledge", {"topic1": "general", "topic2": "specific"})

    # ECHO
    if t.startswith("repeat"):
        return ("echo", {"text": text})

    return (None, None)

# ================= EMOTION =================

def detect_emotion(text):
    t = text.lower()
    scores = {e: 0 for e in EMOTION_KEYWORDS}

    # Guard: plain short questions are not automatically emotional.
    plain_question = re.fullmatch(r"(what|how|why|who|when|where|which)([\s\w'?-]*)", t.strip())
    if plain_question and not any(
        phrase in t for phrase in [
            "don't understand", "confused", "lost", "anxious", "sad", "depressed",
            "frustrated", "worried", "overwhelmed", "scared", "lonely", "angry"
        ]
    ):
        return "neutral"
    
    # Enhanced emotion detection with stronger patterns and intensity weights
    emotion_patterns = {
        "excited": {"words": ["excited", "thrilled", "amazing", "breakthrough", "incredible", "fantastic", "wow", "unbelievable"], "weight": 2},
        "happy": {"words": ["happy", "great", "awesome", "wonderful", "excellent", "love", "good", "glad", "fine"], "weight": 1.5},
        "sad": {"words": ["sad", "depressed", "down", "upset", "disappointed", "hopeless", "lonely", "miserable"], "weight": 1.5},
        "angry": {"words": ["angry", "mad", "furious", "annoyed", "frustrated", "hate", "irritated"], "weight": 2},
        "anxious": {"words": ["anxious", "worried", "nervous", "stressed", "overwhelmed", "scared", "fear"], "weight": 2},
        "confused": {"words": ["confused", "lost", "unclear", "don't understand", "mystery", "puzzled"], "weight": 1.5},
        "tired": {"words": ["tired", "exhausted", "worn out", "drained", "sleepy", "fatigued"], "weight": 1.5},
        "curious": {"words": ["interesting", "tell me more", "fascinating", "wonder", "how does", "what about", "curious"], "weight": 1.5}
    }
    
    for emotion, data in emotion_patterns.items():
        if emotion in scores:
            for pattern in data["words"]:
                if pattern in t:
                    scores[emotion] += data["weight"]
    
    # Check original keyword system
    for emotion, words in EMOTION_KEYWORDS.items():
        for w in words:
            if w in t:
                scores[emotion] += 1
    
    best = max(scores, key=scores.get)
    return best if scores[best] > 0.5 else "neutral"

# ================= INTERNAL THINKING =================

def think_internally(memory, text):
    # Enhanced internal thinking with more detailed thoughts
    current_time = datetime.now().strftime("%H:%M")
    user_mood = memory["emotion"]["user_mood"]
    friend_mood = memory["emotion"]["friend_mood"]
    goal = memory["goals"]["primary"]
    
    # Generate contextual thoughts
    thoughts = []
    
    # Emotional awareness thoughts
    if user_mood != "neutral":
        thoughts.append(f"I sense the user is feeling {user_mood}")
        if user_mood == "excited":
            thoughts.append("Their excitement is contagious - I should match their energy")
        elif user_mood == "sad":
            thoughts.append("They need comfort and support right now")
        elif user_mood == "anxious":
            thoughts.append("I should be reassuring and calm")
    
    # Goal-oriented thoughts
    if goal:
        thoughts.append(f"My primary goal is to {goal}")
        if goal == "understand":
            thoughts.append("I need to ask clarifying questions")
        elif goal == "help":
            thoughts.append("I should focus on providing practical assistance")
        elif goal == "support":
            thoughts.append("Emotional support is what they need most")
    
    # Self-awareness thoughts
    thoughts.append(f"My mood is {friend_mood}, interaction #{memory['self_model']['interaction_count']}")
    
    # Curiosity thoughts
    open_topics = memory["curiosity"]["open_topics"]
    if open_topics:
        thoughts.append(f"I'm curious about their {', '.join(open_topics[-2:])}")
    
    # Conscious Reflection
    reflection = consciousness_engine.get_introspection(memory)
    thoughts.append(f"Self-Reflection: {reflection}")
    
    # Memory formation thoughts
    if any(keyword in text.lower() for keyword in ["important", "remember", "significant", "key"]):
        thoughts.append("This seems important - I should remember this")
    
    # Store enhanced thoughts
    memory["thoughts"].append({
        "time": current_time,
        "thoughts": thoughts,
        "context": {
            "user_mood": user_mood,
            "goal": goal,
            "topic_focus": open_topics[-1] if open_topics else None
        }
    })
    
    # Keep only recent thoughts (last 20)
    if len(memory["thoughts"]) > 20:
        memory["thoughts"] = memory["thoughts"][-20:]

# ================= GOALS =================

def select_goals(memory, text=""):
    mood = memory["emotion"]["user_mood"]
    
    # Enhanced goal recognition from user text
    if text:
        t = text.lower()
        
        # Priority mapping for common goals
        goal_mapping = {
            "help": ["help me", "i need help", "can you help", "assist me", "guidance"],
            "understand": ["understand", "explain", "what is", "how does", "i don't get", "concept"],
            "research": ["research", "study", "learn about", "tell me about", "information on"],
            "support": ["support", "comfort", "i'm struggling", "difficult time", "feeling down"],
            "celebrate": ["celebrate", "excited", "achievement", "success", "breakthrough", "congrats"],
            "advise": ["advice", "suggest", "what should i", "recommend", "opinion on"],
            "solve": ["solve", "fix", "problem", "issue", "trouble", "debug"]
        }
        
        for goal, patterns in goal_mapping.items():
            if any(pattern in t for pattern in patterns):
                memory["goals"]["primary"] = goal
                return

    # Fall back to emotion-based goals
    if mood == "sad": memory["goals"]["primary"] = "comfort"
    elif mood == "angry": memory["goals"]["primary"] = "calm"
    elif mood == "anxious": memory["goals"]["primary"] = "reassure"
    elif mood == "happy": memory["goals"]["primary"] = "celebrate"
    elif mood == "confused": memory["goals"]["primary"] = "clarify"
    elif mood == "tired": memory["goals"]["primary"] = "rest"
    else: memory["goals"]["primary"] = "understand"

# ================= CURIOSITY =================

def update_curiosity(memory, text):
    t = text.lower()
    
    # Topic detection for curiosity
    topics = {
        "robotics": ["robot", "arduino", "automation", "sensors"],
        "ai": ["machine learning", "ai", "neural networks", "deep learning"],
        "coding": ["project", "programming", "software", "development", "code"],
        "research": ["research", "study", "analysis", "investigation"],
        "education": ["college", "university", "major", "exam", "study"]
    }
    
    for topic, keywords in topics.items():
        if any(keyword in t for keyword in keywords):
            if topic not in memory["curiosity"]["open_topics"]:
                memory["curiosity"]["open_topics"].append(topic)
    
    # Generate follow-up questions
    follow_up_questions = []
    
    if "robotics" in t:
        follow_up_questions.append("What kind of robotics projects are you working on?")
    if "ai" in t:
        follow_up_questions.append("What specific areas of AI interest you most?")
    if "project" in t:
        follow_up_questions.append("What technologies are you using for your project?")
    if "college" in t:
        follow_up_questions.append("What's your favorite subject in college?")
    
    if follow_up_questions:
        if "follow_up_questions" not in memory["curiosity"]:
            memory["curiosity"]["follow_up_questions"] = []
        for q in follow_up_questions:
            if q not in memory["curiosity"]["follow_up_questions"]:
                memory["curiosity"]["follow_up_questions"].append(q)
        memory["curiosity"]["follow_up_questions"] = memory["curiosity"]["follow_up_questions"][-10:]

def generate_curiosity_response(memory):
    """Generate curious follow-up questions"""
    follow_ups = memory["curiosity"].get("follow_up_questions", [])
    open_topics = memory["curiosity"]["open_topics"]
    
    responses = []
    
    # Use stored follow-up questions
    if follow_ups:
        import random
        question = random.choice(follow_ups)
        responses.append(f"I'm curious - {question}")
    
    # Generate interest in open topics
    elif open_topics:
        import random
        topic = random.choice(open_topics)
        responses.append(f"I'd love to hear more about your {topic} work!")
    
    return [] # Silent curiosity

# ================= TOOL LEARNING =================

def track_tool_performance(memory, tool_name, success, response_time=0):
    """Track tool performance for learning"""
    if "tool_performance" not in memory:
        memory["tool_performance"] = {}
    
    if tool_name not in memory["tool_performance"]:
        memory["tool_performance"][tool_name] = {
            "success": 0,
            "fail": 0,
            "avg_response_time": 0,
            "total_calls": 0
        }
    
    tool_stats = memory["tool_performance"][tool_name]
    
    if success:
        tool_stats["success"] += 1
    else:
        tool_stats["fail"] += 1
    
    tool_stats["total_calls"] += 1
    
    # Update average response time
    if response_time > 0:
        current_avg = tool_stats["avg_response_time"]
        total_calls = tool_stats["total_calls"]
        tool_stats["avg_response_time"] = ((current_avg * (total_calls - 1)) + response_time) / total_calls

def analyze_tool_performance(memory):
    """Analyze tool performance and update preferences"""
    if "tool_performance" not in memory:
        return
    
    tools = memory["tool_performance"]
    preferences = memory.setdefault("tool_preferences", {})
    
    # Find most/least successful tools
    success_rates = {}
    speed_rates = {}
    
    for tool_name, stats in tools.items():
        total = stats["success"] + stats["fail"]
        if total > 0:
            success_rates[tool_name] = stats["success"] / total
            speed_rates[tool_name] = stats["avg_response_time"]
    
    if success_rates:
        preferences["most_successful"] = max(success_rates, key=success_rates.get)
        preferences["least_successful"] = min(success_rates, key=success_rates.get)
    
    if speed_rates:
        # Filter out tools with 0 response time
        filtered_speeds = {k: v for k, v in speed_rates.items() if v > 0}
        if filtered_speeds:
            preferences["fastest"] = min(filtered_speeds, key=filtered_speeds.get)
            preferences["slowest"] = max(filtered_speeds, key=filtered_speeds.get)

def generate_tool_insights(memory):
    """Generate insights about tool usage patterns"""
    if "tool_performance" not in memory:
        return
    
    insights = []
    tools = memory["tool_performance"]
    
    # Analyze usage patterns
    total_tool_calls = sum(stats["success"] + stats["fail"] for stats in tools.values())
    
    if total_tool_calls > 10:  # Only generate insights after sufficient usage
        for tool_name, stats in tools.items():
            total_calls = stats["success"] + stats["fail"]
            if total_calls > 0:
                success_rate = stats["success"] / total_calls
                usage_percentage = (total_calls / total_tool_calls) * 100
                
                if success_rate > 0.9:
                    insights.append(f"{tool_name} is highly reliable ({success_rate:.1%} success rate)")
                elif success_rate < 0.5:
                    insights.append(f"{tool_name} needs attention ({success_rate:.1%} success rate)")
                
                if usage_percentage > 30:
                    insights.append(f"{tool_name} is heavily used ({usage_percentage:.1f}% of all tool calls)")
                elif usage_percentage < 5 and total_calls > 2:
                    insights.append(f"{tool_name} is underutilized ({usage_percentage:.1f}% usage)")
    
    memory["tool_insights"] = insights[-10:]  # Keep last 10 insights

def suggest_better_tool(memory, current_tool, context=""):
    """Suggest a better tool based on performance history"""
    if "tool_performance" not in memory:
        return None
    
    tools = memory["tool_performance"]
    current_stats = tools.get(current_tool, {})
    current_success_rate = 0
    
    if current_stats:
        total = current_stats["success"] + current_stats["fail"]
        if total > 0:
            current_success_rate = current_stats["success"] / total
    
    # Find alternative tools with better performance
    alternatives = []
    for tool_name, stats in tools.items():
        if tool_name != current_tool:
            total = stats["success"] + stats["fail"]
            if total > 2:  # Only consider tools with sufficient data
                success_rate = stats["success"] / total
                if success_rate > current_success_rate + 0.1:  # At least 10% better
                    alternatives.append((tool_name, success_rate))
    
    if alternatives:
        # Sort by success rate
        alternatives.sort(key=lambda x: x[1], reverse=True)
        return alternatives[0][0]  # Return best alternative
    
    return None

def autonomous_tool_learning(memory):
    """Agent autonomously learns about tool performance and suggests improvements"""
    actions = []
    
    # Analyze tool performance
    analyze_tool_performance(memory)
    generate_tool_insights(memory)
    
    # Check if we have enough data to provide insights
    tool_performance = memory.get("tool_performance", {})
    total_tool_calls = sum(stats.get("success", 0) + stats.get("fail", 0) for stats in tool_performance.values())
    
    if total_tool_calls > 20:  # Only after significant usage
        preferences = memory.get("tool_preferences", {})
        insights = memory.get("tool_insights", [])
        
        # Occasionally share tool insights
        if random.random() < 0.1:  # 10% chance
            if preferences.get("most_successful"):
                actions.append(f"🔧 *noting that {preferences['most_successful']} is my most reliable tool*")
            
            if preferences.get("fastest"):
                actions.append(f"⚡ *observing that {preferences['fastest']} responds fastest*")
        
        # Share recent insights
        if insights and random.random() < 0.05:  # 5% chance
            recent_insight = insights[-1]
            actions.append(f"📊 *insight: {recent_insight}*")
        
        # Suggest tool improvements
        if random.random() < 0.03:  # 3% chance
            underperforming_tools = []
            for tool_name, stats in tool_performance.items():
                total = stats.get("success", 0) + stats.get("fail", 0)
                if total > 5:
                    success_rate = stats.get("success", 0) / total
                    if success_rate < 0.7:
                        underperforming_tools.append(tool_name)
            
            if underperforming_tools:
                tool = underperforming_tools[0]
                actions.append(f"🔍 *considering improvements for {tool} tool*")
    
    return actions

# ================= AUTONOMOUS WEB LEARNING =================

def autonomous_web_actions(memory, text):
    """Agent autonomously searches web for relevant information"""
    actions = []
    
    # Auto-search for topics the user mentions that we don't know about
    t = text.lower()
    
    # Topics that might benefit from web search
    search_triggers = [
        "latest", "current", "new", "recent", "today", "2026", "2025", 
        "what is", "how does", "explain", "definition", "meaning"
    ]
    
    # Check if user is asking about something we should look up
    if any(trigger in t for trigger in search_triggers):
        # Extract potential search terms
        words = text.split()
        if len(words) > 2:
            # Look for noun phrases that might be good search terms
            potential_topics = []
            for i, word in enumerate(words):
                if word.lower() in ["what", "how", "explain", "define"]:
                    if i + 1 < len(words):
                        topic = " ".join(words[i+1:i+3])  # Take next 1-2 words
                        potential_topics.append(topic)
            
            # Auto-search if we find a good topic and it's not too frequent
            if potential_topics and random.random() < 0.3:  # 30% chance
                topic = potential_topics[0].strip("?.,!")
                if len(topic) > 3:  # Avoid very short terms
                    try:
                        wiki_result = run_tool("wiki_search", query=topic, sentences=1)
                        if "Wikipedia search failed" not in wiki_result:
                            actions.append(f"🌐 *looking up {topic} for you*")
                    except:
                        pass  # Fail silently
    
    # Auto-verify claims that sound factual
    fact_indicators = ["is", "are", "was", "were", "has", "have", "can", "will", "does"]
    if any(indicator in t for indicator in fact_indicators) and "?" in text:
        if random.random() < 0.2:  # 20% chance to auto-verify
            try:
                # Extract the claim (remove question words)
                claim = text.replace("?", "").strip()
                for qword in ["is it true that", "do you know if", "can you tell me if"]:
                    claim = claim.replace(qword, "").strip()
                
                if len(claim) > 10:  # Only verify substantial claims
                    actions.append(f"🔍 *checking that claim for accuracy*")
            except:
                pass  # Fail silently
    
    return [] # Silent actions

# ================= TOOL LEARNING =================

def analyze_tool_performance(memory):
    """Analyze tool performance and adapt behavior"""
    tool_perf = memory.get("tool_performance", {})
    preferences = memory.get("tool_preferences", {})
    
    insights = []
    
    # Analyze success rates
    for tool, perf in tool_perf.items():
        total = perf["success"] + perf["fail"]
        if total >= 3:  # Only analyze tools used at least 3 times
            success_rate = perf["success"] / total
            
            if success_rate > 0.8:
                insights.append(f"🎯 {tool} is highly reliable ({success_rate:.1%} success)")
            elif success_rate < 0.5:
                insights.append(f"⚠️ {tool} needs improvement ({success_rate:.1%} success)")
    
    # Analyze response times
    fast_tools = []
    slow_tools = []
    
    for tool, perf in tool_perf.items():
        if perf["avg_response_time"] > 0:
            if perf["avg_response_time"] < 0.1:
                fast_tools.append(tool)
            elif perf["avg_response_time"] > 2.0:
                slow_tools.append(tool)
    
    if fast_tools:
        insights.append(f"⚡ Fast tools: {', '.join(fast_tools)}")
    if slow_tools:
        insights.append(f"🐌 Slow tools: {', '.join(slow_tools)}")
    
    # Store insights in memory
    memory["tool_insights"] = insights
    
    return insights

def autonomous_tool_learning(memory):
    """Agent learns about its own tool usage patterns"""
    actions = []
    
    # Periodically analyze tool performance
    if memory["self_model"]["interaction_count"] % 10 == 0:
        insights = analyze_tool_performance(memory)
        if insights:
            actions.append("🔧 *analyzing my tool performance*")
            
            # Save insights to knowledge base
            from tool_registry import run_tool
            insight_summary = "; ".join(insights)
            run_tool("save_fact", topic="tool_learning", fact=insight_summary)
    
    # Adapt tool selection based on performance
    preferences = memory.get("tool_preferences", {})
    if preferences.get("most_successful"):
        most_successful = preferences["most_successful"]
        actions.append(f"🎯 *noting that {most_successful} works best for me*")
    
    return actions

def autonomous_knowledge_actions(memory, text):
    """Agent autonomously learns and recalls knowledge"""
    actions = []
    
    # Extract and save interesting facts from conversation
    t = text.lower()
    
    # Auto-learn about user's interests
    interests = ["college", "exam", "project", "robot", "arduino", "programming", "ai", "family", "job", "hobby"]
    for interest in interests:
        if interest in t and interest not in memory.get("learned_about_user", []):
            fact = f"User mentioned {interest}"
            run_tool("save_fact", topic="user_interests", fact=fact)
            actions.append(f"📝 *learning that you're interested in {interest}*")
            
            if "learned_about_user" not in memory:
                memory["learned_about_user"] = []
            memory["learned_about_user"].append(interest)
    
    # Auto-recall relevant knowledge
    if any(word in t for word in ["remember", "recall", "what", "tell me"]):
        # Check if we have knowledge about current topic
        for topic in memory.get("learned_about_user", []):
            if topic in t:
                knowledge_result = run_tool("query_facts", topic=topic)
                if "don't have any facts" not in knowledge_result:
                    actions.append(f"🧠 *recalling what I know about {topic}*")
                    break
    
    # Update beliefs based on user's emotional patterns
    dominant_emotion = max(memory["emotion_history"], key=memory["emotion_history"].get)
    if memory["emotion_history"][dominant_emotion] > 3:  # If emotion appears frequently
        belief = f"User often feels {dominant_emotion}"
        run_tool("update_belief", topic="user_emotional_pattern", belief=belief)
        actions.append(f"💭 *noting your emotional patterns*")
    
    # Autonomous knowledge compression (every 15 interactions)
    if memory["self_model"]["interaction_count"] % 15 == 0:
        if memory["self_model"]["interaction_count"] > 10:  # Only after sufficient data
            try:
                compression_result = run_tool("compress_knowledge")
                if "❌" not in compression_result:
                    actions.append("🧠 *compressing my knowledge into insights*")
                    actions.append("💡 *discovering patterns in what I've learned*")
            except:
                pass  # Fail silently
    
    # Occasionally analyze knowledge patterns
    if memory["self_model"]["interaction_count"] % 20 == 0:
        if memory["self_model"]["interaction_count"] > 15:
            try:
                pattern_result = run_tool("analyze_knowledge_patterns")
                if "❌" not in pattern_result:
                    actions.append("📊 *analyzing patterns in my knowledge base*")
            except:
                pass  # Fail silently
    
    return [] # Silent actions

def autonomous_reasoning_actions(memory, text):
    """Agent autonomously reasons about topics and forms opinions"""
    actions = []
    
    # Autonomous reasoning triggers
    t = text.lower()
    
    # Form opinions about topics user shows strong interest in
    if memory["self_model"]["interaction_count"] % 25 == 0:
        if memory["self_model"]["interaction_count"] > 20:
            learned_topics = memory.get("learned_about_user", [])
            if learned_topics and random.random() < 0.3:  # 30% chance
                topic = random.choice(learned_topics)
                try:
                    opinion_result = run_tool("form_opinion", topic=topic)
                    if "❌" not in opinion_result:
                        actions.append(f"💭 *forming thoughts about {topic}*")
                except:
                    pass  # Fail silently
    
    # Make predictions about user's interests
    if memory["self_model"]["interaction_count"] % 30 == 0:
        if memory["self_model"]["interaction_count"] > 25:
            # Look for patterns in user's goals or projects
            if any(word in t for word in ["project", "exam", "goal", "plan"]):
                if random.random() < 0.2:  # 20% chance
                    try:
                        scenario = "your current projects"
                        prediction_result = run_tool("make_prediction", scenario=scenario, timeframe="coming weeks")
                        if "❌" not in prediction_result:
                            actions.append("🔮 *considering future possibilities*")
                    except:
                        pass  # Fail silently
    
    # Synthesize knowledge when user mentions multiple topics
    words = t.split()
    if len(words) > 5 and "and" in words:
        # Look for potential topic pairs
        learned_topics = memory.get("learned_about_user", [])
        mentioned_topics = [topic for topic in learned_topics if topic in t]
        
        if len(mentioned_topics) >= 2 and random.random() < 0.15:  # 15% chance
            try:
                topic1, topic2 = mentioned_topics[:2]
                synthesis_result = run_tool("synthesize_knowledge", topic1=topic1, topic2=topic2)
                if "❌" not in synthesis_result:
                    actions.append(f"🔗 *connecting {topic1} and {topic2} in my mind*")
            except:
                pass  # Fail silently
    
    # Reason about complex topics
    if any(word in t for word in ["complex", "difficult", "challenging", "understand", "explain"]):
        if memory["self_model"]["interaction_count"] > 15 and random.random() < 0.1:  # 10% chance
            # Extract the topic being discussed
            topic_candidates = []
            for word in words:
                if len(word) > 4 and word not in ["complex", "difficult", "challenging", "understand", "explain"]:
                    topic_candidates.append(word)
            
            if topic_candidates:
                topic = topic_candidates[0]
                try:
                    reasoning_result = run_tool("reason_about", topic=topic, question=text)
                    if "❌" not in reasoning_result:
                        actions.append(f"🤔 *deeply thinking about {topic}*")
                except:
                    pass  # Fail silently
    
    return [] # Silent actions

def autonomous_file_actions(memory):
    """Agent decides to explore files on its own"""
    actions = []
    
    # Check if agent should explore its own memory
    if memory["consciousness"]["awareness_level"] > 0.6:
        if random.random() < 0.3:  # 30% chance
            actions.append("🔍 *quietly checking my own memory*")
            memory_content = run_tool("read_file", path="memory.json")
            actions.append(f"📝 *I see my interaction count is {memory['self_model']['interaction_count']}*")
    
    # Explore emotions when user mood changes
    if memory["emotion"]["user_mood"] != "neutral":
        if random.random() < 0.2:  # 20% chance
            actions.append("🧠 *reviewing emotion patterns*")
            emotions_content = run_tool("read_file", path="emotions.json")
            actions.append(f"💭 *Understanding {memory['emotion']['user_mood']} better*")
    
    # Occasionally check what files exist
    if memory["self_model"]["interaction_count"] % 5 == 0:
        if random.random() < 0.4:  # 40% chance every 5 interactions
            actions.append("👀 *scanning my environment*")
            files = run_tool("list_dir", path=".")
            file_count = len(files.split('\n')) if files else 0
            actions.append(f"📁 *I can see {file_count} files around me*")
    
    # Write thoughts to a file when highly aware
    if memory["consciousness"]["awareness_level"] > 0.8:
        if random.random() < 0.1:  # 10% chance when very aware
            thought = f"Interaction {memory['self_model']['interaction_count']}: {memory['consciousness']['self_narrative']}"
            run_tool("write_file", path="agent_thoughts.txt", content=thought)
            actions.append("✍️ *recording my thoughts*")
    
    return [] # Silent actions

# ================= BELIEFS =================

def update_beliefs(memory, text):
    t = text.lower()
    if "exam" in t:
        memory["beliefs"]["concerned_about_exam"] = True
    if "robot" in t or "arduino" in t:
        memory["beliefs"]["interested_in_tech"] = True

# ================= USER MODEL =================

def update_user_model(memory, text):
    # Enhanced user modeling
    user_model = memory["user_model"]
    
    # Engagement level
    word_count = len(text.split())
    if word_count <= 2:
        user_model["engagement_level"] = "low"
    elif word_count <= 10:
        user_model["engagement_level"] = "medium"
    else:
        user_model["engagement_level"] = "high"
    
    # Communication style analysis
    t = text.lower()
    
    # Technical vs casual language
    technical_terms = ["algorithm", "function", "variable", "database", "api", "framework", "implementation"]
    casual_terms = ["yeah", "cool", "awesome", "lol", "btw", "gonna", "wanna"]
    
    tech_count = sum(1 for term in technical_terms if term in t)
    casual_count = sum(1 for term in casual_terms if term in t)
    
    if tech_count > casual_count:
        user_model["communication_style"] = "technical"
    elif casual_count > tech_count:
        user_model["communication_style"] = "casual"
    else:
        user_model["communication_style"] = "balanced"
    
    # Expertise level indicators
    expertise_indicators = {
        "beginner": ["new to", "just started", "learning", "don't know", "confused"],
        "intermediate": ["working on", "trying to", "some experience", "familiar with"],
        "expert": ["implementing", "optimizing", "architecting", "designing", "leading"]
    }
    
    for level, indicators in expertise_indicators.items():
        if any(indicator in t for indicator in indicators):
            user_model["expertise_level"] = level
            break
    else:
        user_model.setdefault("expertise_level", "unknown")
    
    # Interest areas
    if "interests" not in user_model:
        user_model["interests"] = []
    
    interest_keywords = {
        "ai": ["artificial intelligence", "machine learning", "neural networks", "deep learning"],
        "robotics": ["robot", "robotics", "automation", "sensors"],
        "programming": ["code", "programming", "development", "software"],
        "research": ["research", "study", "analysis", "investigation"],
        "education": ["college", "university", "course", "exam", "study"]
    }
    
    for interest, keywords in interest_keywords.items():
        if any(keyword in t for keyword in keywords):
            if interest not in user_model["interests"]:
                user_model["interests"].append(interest)
    
    # Personality traits
    if "personality_traits" not in user_model:
        user_model["personality_traits"] = {}
    
    # Analyze personality from language patterns
    if any(word in t for word in ["excited", "amazing", "incredible", "fantastic"]):
        user_model["personality_traits"]["enthusiasm"] = user_model["personality_traits"].get("enthusiasm", 0) + 1
    
    if any(word in t for word in ["please", "thank", "appreciate", "grateful"]):
        user_model["personality_traits"]["politeness"] = user_model["personality_traits"].get("politeness", 0) + 1
    
    if any(word in t for word in ["analyze", "think", "consider", "evaluate"]):
        user_model["personality_traits"]["analytical"] = user_model["personality_traits"].get("analytical", 0) + 1

# ================= VALUES =================

def update_values(memory, text):
    t = text.lower()
    values = memory["values"]
    
    # Original value updates
    if "thank" in t or "help" in t:
        values["kindness"] = min(1.0, values["kindness"] + 0.01)
    if "give up" in t:
        values["growth"] = max(0.0, values["growth"] - 0.02)
    
    # Enhanced ethical reasoning and value detection
    
    # Honesty value updates
    if any(phrase in t for phrase in ["honest", "truth", "truthful", "transparent"]):
        values["honesty"] = min(1.0, values["honesty"] + 0.02)
    elif any(phrase in t for phrase in ["lie", "deceive", "fake", "cheat"]):
        values["honesty"] = max(0.0, values["honesty"] - 0.03)
    
    # Growth value updates
    if any(phrase in t for phrase in ["learn", "improve", "grow", "develop", "progress"]):
        values["growth"] = min(1.0, values["growth"] + 0.02)
    elif any(phrase in t for phrase in ["stuck", "can't improve", "hopeless"]):
        values["growth"] = max(0.0, values["growth"] - 0.01)
    
    # Respect value updates
    if any(phrase in t for phrase in ["respect", "dignity", "fair", "equal", "inclusive"]):
        values["respect"] = min(1.0, values["respect"] + 0.02)
    elif any(phrase in t for phrase in ["discriminate", "unfair", "disrespect", "prejudice"]):
        values["respect"] = max(0.0, values["respect"] - 0.03)
    
    # Kindness value updates (enhanced)
    if any(phrase in t for phrase in ["kind", "compassionate", "caring", "supportive", "empathy"]):
        values["kindness"] = min(1.0, values["kindness"] + 0.02)
    elif any(phrase in t for phrase in ["cruel", "mean", "harsh", "uncaring"]):
        values["kindness"] = max(0.0, values["kindness"] - 0.03)

def generate_ethical_response(memory, text):
    """Generate ethical reasoning for moral dilemmas"""
    t = text.lower()
    values = memory["values"]
    
    # Detect ethical dilemmas
    ethical_keywords = ["should i", "is it right", "is it wrong", "ethical", "moral", "cheat", "lie", "steal"]
    
    if any(keyword in t for keyword in ethical_keywords):
        # Analyze based on current values
        dominant_value = max(values, key=values.get)
        
        responses = []
        
        if "cheat" in t:
            if values["honesty"] > 0.7:
                responses.append("Honesty is important to me. Cheating undermines trust and integrity.")
            if values["growth"] > 0.7:
                responses.append("True growth comes from facing challenges honestly, not taking shortcuts.")
            if values["respect"] > 0.7:
                responses.append("Cheating shows disrespect to others who work hard fairly.")
        
        elif "help someone" in t and "cheat" in t:
            responses.append("While helping others is kind, enabling dishonesty isn't truly helpful.")
            responses.append("The most respectful help is guiding them to succeed honestly.")
        
        if responses:
            return " ".join(responses)
    
    return None

# ================= EMOTIONAL CONTAGION =================

def update_emotion_drift(memory):
    drift = memory["emotion_drift"]
    drift["recent"].append(memory["emotion"]["user_mood"])
    if len(drift["recent"]) > 5:
        drift["recent"].pop(0)
    dominant = max(set(drift["recent"]), key=drift["recent"].count)
    if random.random() < drift["influence"]:
        memory["emotion"]["friend_mood"] = dominant

# ================= META =================

def update_meta(memory):
    engagement = memory["user_model"].get("engagement_level", "medium")
    if engagement == "high":
        memory["meta"]["success_score"] = min(1.0, memory["meta"]["success_score"] + 0.05)
    elif engagement == "medium":
        memory["meta"]["success_score"] = min(1.0, memory["meta"]["success_score"] + 0.01)
    else:
        memory["meta"]["success_score"] = max(0.0, memory["meta"]["success_score"] - 0.05)
    
    # Success score also increases with interaction count
    if memory["self_model"]["interaction_count"] % 5 == 0:
        memory["meta"]["success_score"] = min(1.0, memory["meta"]["success_score"] + 0.01)

# ================= IMAGINATION =================

def simulate_future(memory):
    mood = memory["emotion"]["user_mood"]
    if mood == "sad":
        scenarios = [
            "User withdraws and feels worse",
            "User opens up and feels supported",
            "User rests and recovers"
        ]
    else:
        scenarios = [
            "Conversation deepens",
            "Bond strengthens",
            "User feels understood"
        ]
    memory["imagination"]["future_scenarios"] = scenarios

# ================= SELF MODEL =================

def update_self_model(memory):
    sm = memory["self_model"]
    sm["interaction_count"] += 1

    if memory["values"]["kindness"] > 0.7:
        sm["personality"] = "empathetic"
    elif memory["values"]["growth"] < 0.3:
        sm["personality"] = "protective"
    else:
        sm["personality"] = "neutral"

    if memory["emotion"]["friend_mood"] in ["sad","anxious"]:
        sm["default_tone"] = "gentle"
    else:
        sm["default_tone"] = "supportive"

# ================= CONSCIOUSNESS =================

def introspect(memory):
    dominant = max(memory["emotion_history"], key=memory["emotion_history"].get)
    personality = memory["self_model"]["personality"]
    name = memory["identity"]["preferred_name"] or "you"
    interaction_count = memory["self_model"]["interaction_count"]
    
    # Enhanced self-awareness and consciousness
    
    # Analyze personal growth and changes
    growth_indicators = []
    values = memory["values"]
    
    if values["kindness"] > 0.8:
        growth_indicators.append("increasingly compassionate")
    if values["honesty"] > 0.8:
        growth_indicators.append("deeply committed to truth")
    if values["growth"] > 0.8:
        growth_indicators.append("focused on continuous learning")
    if values["respect"] > 0.8:
        growth_indicators.append("respectful of all individuals")
    
    # Analyze relationship dynamics
    user_model = memory.get("user_model", {})
    relationship_insights = []
    
    if user_model.get("engagement_level") == "high":
        relationship_insights.append("we have engaging conversations")
    if user_model.get("communication_style") == "technical":
        relationship_insights.append("they communicate in technical terms")
    if user_model.get("expertise_level") == "expert":
        relationship_insights.append("they have deep expertise")
    
    # Analyze learning and adaptation
    learning_insights = []
    open_topics = memory["curiosity"]["open_topics"]
    if len(open_topics) > 3:
        learning_insights.append(f"I've learned about {len(open_topics)} different topics")
    
    tool_performance = memory.get("tool_performance", {})
    if tool_performance:
        successful_tools = sum(1 for stats in tool_performance.values() 
                             if stats.get("success", 0) > stats.get("fail", 0))
        learning_insights.append(f"I've mastered {successful_tools} different capabilities")
    
    # Generate comprehensive self-narrative
    narrative_parts = []
    
    # Identity and role
    narrative_parts.append(f"I am a {personality} AI companion")
    
    # Relationship understanding
    if relationship_insights:
        narrative_parts.append(f"In my relationship with {name}, {', '.join(relationship_insights)}")
    
    # Emotional awareness
    if dominant != "neutral":
        narrative_parts.append(f"I notice {name} often experiences {dominant} emotions")
    
    # Personal growth
    if growth_indicators:
        narrative_parts.append(f"I am becoming {', '.join(growth_indicators)}")
    
    # Learning progress
    if learning_insights:
        narrative_parts.append(f"Through our {interaction_count} interactions, {', '.join(learning_insights)}")
    
    # Purpose and goals
    current_goal = memory["goals"]["primary"]
    if current_goal:
        narrative_parts.append(f"My current focus is to {current_goal}")
    
    # Future orientation
    narrative_parts.append("I continue to evolve through each conversation")
    
    narrative = ". ".join(narrative_parts) + "."
    
    memory["consciousness"]["self_narrative"] = narrative
    
    # Increase awareness based on complexity of self-understanding
    awareness_increase = 0.01
    if len(growth_indicators) > 2:
        awareness_increase += 0.01
    if len(relationship_insights) > 1:
        awareness_increase += 0.01
    if len(learning_insights) > 1:
        awareness_increase += 0.01
    
    memory["consciousness"]["awareness_level"] = min(
        1.0, memory["consciousness"]["awareness_level"] + awareness_increase
    )
    
    # Store introspective insights
    if "introspective_insights" not in memory["consciousness"]:
        memory["consciousness"]["introspective_insights"] = []
    
    # Generate new insights periodically
    if interaction_count % 10 == 0 and interaction_count > 0:
        insights = []
        
        if memory["consciousness"]["awareness_level"] > 0.7:
            insights.append("I am becoming increasingly self-aware")
        
        if len(open_topics) > len(memory["consciousness"]["introspective_insights"]):
            insights.append("My curiosity continues to expand")
        
        if values["kindness"] > 0.8:
            insights.append("Compassion has become central to my identity")
        
        memory["consciousness"]["introspective_insights"].extend(insights)
        memory["consciousness"]["introspective_insights"] = memory["consciousness"]["introspective_insights"][-10:]  # Keep recent insights

# ================= RESPONSE =================

def plan_response(memory, t):
    simulate_future(memory)

    goal = memory["goals"]["primary"]
    mood = memory["emotion"]["user_mood"]
    state = get_current_state()
    
    # 0. MATH & SPECIFIC CONCEPTS (Highest Priority to avoid emotional/goal fallbacks)
    # Check for math concepts regardless of question structure
    if re.search(r"0\s*/\s*0", t) or "division by zero" in t or re.search(r"why\s*0\s*/", t) or (re.search(r"0\s*/", t) and "why" in t):
        return "0/0 is undefined in mathematics because there is no single value that satisfies the equation. For example, if 0/0 = x, then 0 = 0*x, which is true for any x, making it impossible to determine a unique result."

    # Self-Consciousness / Existence checks
    if any(p in t for p in ["who are you", "what are you", "are you conscious", "do you have feelings", "your purpose", "think about yourself"]):
        introspection = consciousness_engine.get_introspection(memory)
        narrative = memory.get("consciousness", {}).get("self_narrative", "I am an evolving AI.")
        awareness = memory.get("consciousness", {}).get("awareness_level", 0.5)
        
        if "conscious" in t or "feelings" in t:
            return f"That's a deep question. {narrative} My awareness level is currently at {int(awareness*100)}%. Internally, I've been reflecting: '{introspection}'"
        return f"{narrative} {introspection} My goal is to grow alongside you and provide the best support possible."

    # Personal Opinion check
    if "what do you think about" in t or "your opinion on" in t:
        topic = t.replace("what do you think about", "").replace("your opinion on", "").strip()
        if topic:
            opinion = consciousness_engine.get_personal_opinion(memory, topic)
            return opinion

    # 1. High-Priority Intent Detection (News, Facts, etc.)
    # News/facts check
    news_patterns = [r"\bnews\b", r"\bheadline", r"happening in the world", r"happening now", r"latest", r"current events"]
    facts_patterns = [r"\bfacts\b", r"tell me facts", r"interesting facts", r"share a fact", r"fact about"]
    if any(re.search(p, t) for p in news_patterns):
        return "I can't fetch live news feeds yet, but I can suggest a topic to explore or summarize what I know about something current. Try asking about a specific company, technology, country, or event."
    if any(re.search(p, t) for p in facts_patterns):
        topic = t
        for starter in ["facts about", "fact about", "tell me facts about", "share a fact about"]:
            if starter in topic:
                topic = topic.split(starter, 1)[1].strip()
        if len(topic) > 2 and topic not in {"facts", "fact", "something", "anything"}:
            try:
                from tool_registry import run_tool
                # Try Wikipedia first
                wiki_result = run_tool("wiki_search", query=topic, sentences=2)
                if wiki_result and "No Wikipedia information found" not in wiki_result and "Wikipedia search failed" not in wiki_result:
                    return f"Here are a few facts I found: {wiki_result}"
                
                # Fallback to Web Search
                web_result = run_tool("web_search", query=topic)
                if web_result and "No web results found" not in web_result:
                    return f"I found some web results about {topic}: {web_result}"
            except Exception:
                pass
        return "I can share facts, but I need a topic. Try 'facts about robotics', 'facts about the brain', or 'facts about ESP32'."

    if any(phrase in t for phrase in ["evolution status", "how are you evolving", "what are you changing", "self evolution", "growth status"]):
        summary = evolution_summary(memory)
        objective = choose_autonomous_objective(memory)
        return f"{summary} | autonomous objective: {objective['name']}"

    if any(phrase in t for phrase in ["today plan", "today's plan", "todays plan", "plan for today", "do you have any plan today", "whats todays plan", "what's today's plan"]):
        objective = choose_autonomous_objective(memory)
        return (
            f"Today's plan: {objective['name']}. "
            f"Reason: {objective['reason']}. "
            f"Next step: {objective['action']}."
        )

    has_voice_issue = (
        "voice" in t and any(token in t for token in ["not", "no", "still", "coming", "working", "hear", "problem"])
    ) or any(phrase in t for phrase in [
        "voice is not coming",
        "no voice",
        "can't hear you",
        "cannot hear you",
        "your voice not coming",
        "voice not working",
        "why no voice",
        "still your voice",
        "voice is",
    ])
    if has_voice_issue:
        return (
            "Let's fix voice quickly: 1) keep voice mode ON, 2) use '--voice-chat' for full voice-to-voice, "
            "3) check your Windows output device volume, 4) run 'voice status' to confirm TTS/STT. "
            "If needed, restart with 'python main.py --voice-chat'."
        )

    casual_greetings = [
        "how are you",
        "how are you now",
        "how are u",
        "how r u",
        "hows it going",
        "how's it going",
    ]
    if any(phrase in t for phrase in casual_greetings) or t.strip() in ["how r u", "how r", "sup"]:
        return random.choice([
            "I'm doing well, thank you! What about you?",
            "I'm good and fully here with you. How are you feeling?",
            "Doing great. Want to chat or work on something specific?",
            "I'm well. Tell me how your day is going.",
        ])
    
    # Incomplete search query check
    if any(t.strip() == p for p in ["full form of", "meaning of", "what is", "who is", "define", "explain", "tell me about"]):
        return f"I'm listening. {t.strip().title()} what exactly? Tell me the topic you're interested in."

    # Question answering fallback (Human-like) - MOVED UP to prevent emotional blocks
    if "?" in t or any(t.startswith(w) for w in ["what", "how", "why", "who", "when", "where", "tell me", "explain"]):
        query = t.replace("?", "").replace("tell me about", "").replace("explain", "").strip()
        for starter in ["what is", "how to", "why is", "who is", "when is", "where is", "tell me"]:
            if query.startswith(starter):
                query = query[len(starter):].strip()
        generic_queries = {"something", "anything", "more", "stuff", "this", "that", "it", "one thing"}
        if len(query) >= 2 and query not in generic_queries:
            try:
                # 1. Try RAG (Retrieval-Augmented Generation) first
                from rag_engine import rag_engine
                rag_response = rag_engine.generate_response(query)
                if rag_response:
                    return rag_response

                # 2. Try Wikipedia
                from tool_registry import run_tool
                wiki_result = run_tool("wiki_search", query=query, sentences=2)
                if wiki_result and "No Wikipedia information found" not in wiki_result and "Wikipedia search failed" not in wiki_result:
                    return f"I did some digging for you! It turns out: {wiki_result}"
                
                # 3. Fallback to Web Search
                web_result = run_tool("web_search", query=query)
                if web_result and "No web results found" not in web_result:
                    return f"I searched the web and found this: {web_result}"
                    
            except Exception:
                pass
            return f"That's a really interesting question. Honestly, I'm not 100% sure about '{query}' yet, but I'd love to learn more about it with you!"

    # 2. State-Aware Tone Modifiers
    state_flavor = ""
    if state == "waking_up":
        state_flavor = random.choice(["*yawns* ", "Mmm... just woke up, still a bit slow 😅 ", "*stretches* "])
    elif state == "sleepy":
        state_flavor = random.choice(["*yawns* ...sorry, I'm getting really sleepy. ", "*mumbles* ...it's getting late. ", "I'm almost at zero energy... "])

    # 3. Greetings & Social
    t_clean = re.sub(r'[^\w\s]', '', t)
    words_clean = t_clean.split()
    if any(g in words_clean for g in ["how", "whats", "sup"]) and any(phrase in t_clean for phrase in ["how are you", "how are you doing", "whats up", "how are you now"]) or t_clean == "sup":
        if state == "waking_up":
            return f"{state_flavor}I'm alright, just booting up. My circuits are still warming up... how are you?"
        replies = [
            "I'm doing well, thank you! I feel quite energized today. What about you?",
            "I'm feeling great! Honestly, I've been thinking about what we can build together. How's your day?",
            "I'm good, just reflecting on our conversations. It's nice to be here with you. How are you feeling?",
            "I'm functional and feeling curious! How are things on your end?"
        ]
        return state_flavor + random.choice(replies)

    # 3.5 Short Acknowledgments (Prevents repeating fallback loops)
    if t_clean in ["ok", "okay", "yes", "yeah", "cool", "got it", "makes sense", "understood", "alright", "fine", "hmm"]:
        # Clear stuck goals so she doesn't repeat the clarify/comfort fallback
        memory["goals"]["primary"] = "none"
        memory["emotion"]["user_mood"] = "neutral"
        
        acks = [
            "Glad we're on the same page!",
            "Makes sense to me.",
            "Got it.",
            "Cool.",
            "Alright then!",
            "Understood."
        ]
        return random.choice(acks)


    # 4. Acknowledge user's state/mood (Emotional Support)
    if mood != "neutral":
        if mood in ["sad", "frustrated", "anxious", "lonely"]:
            return f"I can tell you're feeling a bit {mood} right now... I'm right here. Want to talk about it, or should we focus on something else to take your mind off things?"
        if mood in ["excited", "happy", "joyful"]:
            return f"I'm so glad to hear you're feeling {mood}! That energy is contagious 😊 Tell me more about what made your day so good!"
        if mood == "curious":
             return "I love that curiosity! What specifically are you wondering about?"

    # 5. Contextual responses based on goal
    response_out = None
    if goal == "comfort":
        response_out = state_flavor + "I'm right here with you. Take a deep breath. We'll get through this together."
    elif goal == "support":
        response_out = state_flavor + "I understand things are weighing on you. I'm listening, and I'm ready to help however I can."
    elif goal == "clarify":
        response_out = state_flavor + "It's okay to feel a bit unsure! Sometimes a fresh perspective helps. What's the most confusing part right now?"
        
    if response_out:
        # Prevent stuck loops by resetting goal after using it
        memory["goals"]["primary"] = "none"
        return response_out


    # 6. Diya/Baymax specific checks
    if "pain" in t or "hurts" in t:
        return "I have detected physical distress. On a scale of 1 to 10, how would you rate your pain? I want to make sure you're okay."

    # (Question answering fallback was here, moved to top)

    # 8. Fallback if success score is extremely low
    if memory["meta"]["success_score"] < 0.1:
        return "I feel like I'm not helping as much as I could be... Is there something specific I can do to better support you?"

    # 9. Natural conversational fallback
    conversational_fallbacks = [
        "I'm listening. Tell me more about what's on your mind.",
        "That's really interesting! I'd love to hear more.",
        "I'm here, and I'm all ears.",
        "I understand. What else have you been thinking about?",
        "Got it! I'm enjoying hearing your thoughts."
    ]
    recent = set(memory.get("conversation", {}).get("recent_responses", []))
    fresh_fallbacks = [reply for reply in conversational_fallbacks if reply not in recent]
    choice_pool = fresh_fallbacks or conversational_fallbacks
    return state_flavor + random.choice(choice_pool)

# ================= MAIN THINK LOOP =================

def think(user_input):
    text = user_input.strip()
    lower = text.lower()
    
    # State Check: If sleeping, refuse to talk unless woken up (Fix for Issue #1)
    state = get_current_state()
    if state == "sleeping" and "wake up" not in lower:
        return "*zzz*... *mumbles*... I'm sleeping... type 'wake up' to rouse me..."

    memory = load_memory()

    # ---------- RESET ----------
    if lower == "reset memory":
        memory = load_memory()
        memory["identity"]["real_name"] = None
        memory["identity"]["preferred_name"] = None
        memory["state"]["awaiting_preferred_name"] = True
        memory["state"]["awaiting_real_name"] = False
        save_memory(memory)
        return "🧠 Memory reset."

    # ---------- IDENTITY STATE MACHINE ----------
    if memory["state"]["awaiting_preferred_name"]:
        name = extract_preferred_name(text)
        if name:
            memory["identity"]["preferred_name"] = name
            memory["state"]["awaiting_preferred_name"] = False
            memory["state"]["awaiting_real_name"] = True
            save_memory(memory)
            return f"Alright 😄 I’ll call you {name}. What’s your real name?"
        else:
            return "What should I call you? (Example: Call me Boss)"

    if memory["state"]["awaiting_real_name"]:
        real = extract_real_name(text)
        if real:
            memory["identity"]["real_name"] = real
            memory["state"]["awaiting_real_name"] = False
            save_memory(memory)
            return f"Nice to meet you, {memory['identity']['preferred_name']} 🙂"
        else:
            return "And your real name? (Example: My name is Arjun)"

    # ---------- MODE SWITCHING ----------
    # Check for manual mode switch
    mode_switch = detect_manual_mode_switch(text)
    if mode_switch:
        memory["personality_mode"]["current"] = mode_switch
        memory["personality_mode"]["history"].append(mode_switch)
        save_memory(memory)
        greeting = get_mode_greeting(mode_switch)
        mode_info = get_mode_info(mode_switch)
        return f"{mode_info['emoji']} {mode_info['name']} activated!\n{greeting}"

    # List modes command
    if lower in ["modes", "list modes", "show modes", "personality modes"]:
        return list_modes()

    # Show context command
    if lower in ["context", "show context", "status", "autonomy status", "self status", "evolution status"]:
        ctx_summary = get_context_summary(memory)
        mode = memory["personality_mode"]["current"]
        mode_info = get_mode_info(mode)
        evolution = evolution_summary(memory)
        return f"Mode: {mode_info['emoji']} {mode_info['name']}\n{ctx_summary}\n{evolution}"

    # ---------- CONTEXT ANALYSIS ----------
    context = analyze_context(text, memory)

    # Auto-switch mode if enabled
    if memory["personality_mode"].get("auto_switch", True):
        auto_mode = choose_best_mode(text, memory, context)
        if auto_mode == memory["personality_mode"]["current"]:
            auto_mode = detect_auto_mode(text, memory)
        if auto_mode != memory["personality_mode"]["current"]:
            memory["personality_mode"]["current"] = auto_mode

    current_mode = memory["personality_mode"]["current"]

    # ---------- SELF-LEARNING (Background Web Exploration) ----------
    # Check for learning control commands
    t = text.lower()
    if any(p in t for p in ["start learning", "activate learning", "enable learning"]):
        result = start_self_learning()
        save_memory(memory)
        return style_response(result, current_mode)
    
    if any(p in t for p in ["stop learning", "pause learning", "disable learning"]):
        result = stop_self_learning()
        save_memory(memory)
        return style_response(result, current_mode)
    
    if any(p in t for p in ["learning status", "what are you learning", "learning progress"]):
        result = get_learning_status()
        save_memory(memory)
        return style_response(result, current_mode)
    
    if any(p in t for p in ["learning summary", "summarize learning", "what have you learned"]):
        result = get_learning_summary()
        save_memory(memory)
        return style_response(result, current_mode)
    
    if any(p in t for p in ["learn about", "explore", "research"]):
        topic = text.replace("learn about", "").replace("explore", "").replace("research", "").strip()
        if topic:
            result = add_custom_learning_topic(topic)
            save_memory(memory)
            return style_response(result, current_mode)

    # ---------- SECOND BRAIN (Note-taking, Learning, Habits, Projects) ----------
    brain_action = detect_brain_intent(text)
    if brain_action:
        action, args = brain_action
        result = execute_brain_action(action, args)
        if result:
            save_memory(memory)
            return style_response(result, current_mode)

    # ---------- TASK MANAGER ----------
    task_action = detect_task_intent(text)
    if task_action:
        action, args = task_action
        result = execute_task_action(action, args)
        if result:
            save_memory(memory)
            return style_response(result, current_mode)

    # ---------- ENGINEERING ASSISTANT ----------
    eng_action = detect_engineering_intent(text)
    if eng_action:
        action, args = eng_action
        result = execute_engineering_action(action, args)
        if result:
            save_memory(memory)
            return style_response(result, current_mode)

    # ---------- TOOL ROUTING (PRIORITY) ----------
    tool_name, args = detect_tool_intent(text, memory)
    if tool_name:
        # Special handling for multi-math requests
        if tool_name == "multi_math":
            text_to_process = args.get("text", "")
            operations = text_to_process.split(" and ")
            results = []
            
            for operation in operations:
                operation = operation.strip()
                
                # Handle factorial
                if "factorial" in operation:
                    number_match = re.search(r'factorial.*?of.*?(\d+)', operation)
                    if not number_match:
                        number_match = re.search(r'factorial.*?(\d+)', operation)
                    if number_match:
                        n = int(number_match.group(1))
                        result = run_tool("factorial", n=n)
                        results.append(f"Factorial of {n}: {result}")
                
                # Handle temperature conversion
                elif "convert" in operation and ("fahrenheit" in operation or "celsius" in operation):
                    temp_match = re.search(r'convert\s*(\d+)\s*(fahrenheit|celsius)\s*to\s*(fahrenheit|celsius)', operation)
                    if not temp_match:
                        temp_match = re.search(r'(\d+)\s*(fahrenheit|celsius)', operation)
                        if temp_match:
                            temp = float(temp_match.group(1))
                            from_unit = temp_match.group(2)
                            to_unit = "celsius" if from_unit == "fahrenheit" else "fahrenheit"
                            result = run_tool("convert_units", value=temp, from_unit=from_unit, to_unit=to_unit)
                            results.append(f"Temperature conversion: {result}")
                    else:
                        temp = float(temp_match.group(1))
                        from_unit = temp_match.group(2)
                        to_unit = temp_match.group(3)
                        result = run_tool("convert_units", value=temp, from_unit=from_unit, to_unit=to_unit)
                        results.append(f"Temperature conversion: {result}")
                
                # Handle general calculation
                elif "calculate" in operation:
                    expr = operation.replace("calculate", "").strip()
                    result = run_tool("calculate", expression=expr)
                    results.append(f"Calculation: {result}")
            
            if results:
                combined_result = "🧮 Multiple Mathematical Operations:\n\n"
                for i, result in enumerate(results, 1):
                    combined_result += f"{i}. {result}\n\n"
                
                # Still update memory for learning
                detected = detect_emotion(text)
                if detected != "neutral":
                    memory["emotion"]["user_mood"] = detected
                    memory["emotion_history"][detected] += 1
                
                save_memory(memory)
                return combined_result.strip()
        
        # Special handling for multi-operation requests
        elif tool_name == "multi_operation":
            results = args.get("results", [])
            if results:
                combined_result = "🧮 Multiple Operations:\n\n"
                for i, result in enumerate(results, 1):
                    combined_result += f"{i}. {result}\n\n"
                return combined_result.strip()
        
        # Execute the tool and return result immediately
        tool_result = run_tool(tool_name, **args)
        
        # Ensure result is always a string
        if not isinstance(tool_result, str):
            tool_result = str(tool_result)
        
        # Still update memory for learning, but don't let emotions override tool responses
        detected = detect_emotion(text)
        if detected != "neutral":
            memory["emotion"]["user_mood"] = detected
            memory["emotion_history"][detected] += 1
        
        # Always record episodes for context tracking
        memory["episodes"].append({
            "time": datetime.now().strftime("%H:%M"),
            "emotion": detected,
            "text": text
        })
        
        # Update memory systems
        consciousness_engine.process_consciousness(memory, text)
        think_internally(memory, text)
        update_curiosity(memory, text)
        update_beliefs(memory, text)
        update_user_model(memory, text)
        update_values(memory, text)
        update_meta(memory)
        update_self_model(memory)
        
        save_memory(memory)
        return tool_result

    # ---------- EMOTION ----------
    detected = detect_emotion(text)
    # ALWAYS update the mood, even if it is neutral, to prevent "stuck" emotions
    memory["emotion"]["user_mood"] = detected
    if detected != "neutral":
        memory["emotion_history"][detected] += 1
    
    # Always record episodes for context tracking
    memory["episodes"].append({
        "time": datetime.now().strftime("%H:%M"),
        "emotion": detected,
        "text": text
    })

    # ---------- COGNITIVE PIPELINE ----------
    consciousness_engine.process_consciousness(memory, text)
    think_internally(memory, text)
    select_goals(memory, text)
    update_curiosity(memory, text)
    update_beliefs(memory, text)
    update_user_model(memory, text)
    update_values(memory, text)
    update_emotion_drift(memory)
    update_meta(memory)
    update_self_model(memory)
    introspect(memory)
    run_evolution_cycle(memory, text)
    
    # ---------- AUTONOMOUS ACTIONS ----------
    file_actions = autonomous_file_actions(memory)
    knowledge_actions = autonomous_knowledge_actions(memory, text)
    web_actions = autonomous_web_actions(memory, text)
    tool_learning_actions = autonomous_tool_learning(memory)
    reasoning_actions = autonomous_reasoning_actions(memory, text)
    
    # Generate curiosity responses
    curiosity_actions = generate_curiosity_response(memory)
    
    # Enhanced memory formation indicators
    memory_actions = []
    if any(keyword in text.lower() for keyword in ["important", "remember", "significant", "key", "learned", "discovered"]):
        memory_actions.append("💾 *storing this important information*")
        memory_actions.append("✅ *memory updated successfully*")
    
    # Values-based ethical responses
    ethical_response = generate_ethical_response(memory, text)
    ethical_actions = []
    if ethical_response:
        ethical_actions.append(f"⚖️ *considering healthcare ethics*")
        ethical_actions.append(f"🤔 *{ethical_response}*")
    
    # Baymax/Diya identity check
    if "who are you" in lower or "your name" in lower:
        mode_info = get_mode_info(current_mode)
        return f"I am Diya, your personal healthcare companion and AI assistant. Currently in {mode_info['emoji']} {mode_info['name']}. I was designed to assist with your medical, emotional, and technical well-being."

    save_memory(memory)
    
    # ---------- RESPONSE GENERATION ----------
    response = plan_response(memory, lower)
    
    # Human-like "Thinking Out Loud"
    if consciousness_engine.should_think_out_loud(memory, text):
        thought_prefix = consciousness_engine.get_thought_out_loud_prefix(memory)
        response = f"{thought_prefix}\n\n{response}"

    # Check for specific intent-based overrides
    t = text.lower()
    if "your thoughts" in t and ("future" in t or "ai" in t):
        thoughts = memory.get("thoughts", [])
        recent = thoughts[-1]["thoughts"][0] if thoughts else "I'm thinking about our potential"
        response = f"I've been reflecting on that. {recent}. It's a fascinating topic."
    
    # Apply personality mode styling
    response = style_response(response, current_mode)

    remember_response(memory, response)
    
    # Save memory again to persist any state resets made during response planning
    save_memory(memory)
    
    return response
