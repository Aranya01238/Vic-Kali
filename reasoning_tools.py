#!/usr/bin/env python3
"""
Knowledge Reasoning Tools (Step 2.9)
Combines memory, web knowledge, and imagination to form opinions, predictions, and advice
"""

import json
import random
from datetime import datetime
from collections import Counter
from tools import save_fact

# -------- KNOWLEDGE REASONING TOOLS (Step 2.9) --------

def form_opinion(topic, context=""):
    """Form an opinion based on knowledge, memory, and reasoning"""
    try:
        # Load knowledge bases
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
            compressed = {}
        
        # Gather relevant facts
        relevant_facts = []
        facts = knowledge.get("facts", {})
        
        # Find facts related to the topic
        topic_lower = topic.lower()
        for fact_topic, fact_list in facts.items():
            if topic_lower in fact_topic.lower() or any(word in fact_topic.lower() for word in topic_lower.split()):
                relevant_facts.extend(fact_list)
        
        # Also check compressed knowledge
        user_profile = compressed.get("user_profile", {})
        interests = user_profile.get("primary_interests", [])
        
        if not relevant_facts:
            # Try web search for more information
            try:
                from tools import web_search
                web_result = web_search(topic)
                if "❌" not in web_result:
                    relevant_facts.append(f"Web research: {web_result[:200]}...")
            except:
                pass
        
        # Form opinion based on available information
        opinion_confidence = 0.5
        opinion_text = ""
        
        if relevant_facts:
            # Analyze sentiment and patterns in facts
            positive_indicators = ['good', 'great', 'excellent', 'useful', 'helpful', 'effective', 'successful']
            negative_indicators = ['bad', 'poor', 'difficult', 'problem', 'issue', 'failed', 'unsuccessful']
            
            positive_count = sum(1 for fact in relevant_facts for indicator in positive_indicators if indicator in fact.lower())
            negative_count = sum(1 for fact in relevant_facts for indicator in negative_indicators if indicator in fact.lower())
            
            # Consider user interests
            interest_match = any(interest in topic_lower for interest in interests)
            if interest_match:
                opinion_confidence += 0.2
            
            # Form opinion
            if positive_count > negative_count:
                opinion_text = f"Based on my knowledge, I have a positive view of {topic}. "
                opinion_confidence += 0.2
            elif negative_count > positive_count:
                opinion_text = f"Based on my knowledge, I have some concerns about {topic}. "
                opinion_confidence += 0.1
            else:
                opinion_text = f"I have a balanced perspective on {topic}. "
            
            # Add reasoning
            if len(relevant_facts) > 3:
                opinion_text += f"This is based on {len(relevant_facts)} pieces of information I've gathered. "
                opinion_confidence += 0.1
            
            # Add user context
            if interest_match:
                opinion_text += f"Given your interest in {', '.join(interests)}, this seems particularly relevant to you. "
        else:
            opinion_text = f"I don't have enough information to form a strong opinion about {topic} yet. "
            opinion_confidence = 0.3
        
        # Add context if provided
        if context:
            opinion_text += f"Considering the context you provided: {context[:100]}... "
            opinion_confidence += 0.1
        
        # Cap confidence
        opinion_confidence = min(1.0, opinion_confidence)
        
        # Save opinion to knowledge base
        save_fact("opinions", f"Opinion on {topic}: {opinion_text} (confidence: {opinion_confidence:.1f})", confidence=opinion_confidence)
        
        result = f"💭 My Opinion on '{topic}':\n\n"
        result += f"{opinion_text}\n\n"
        result += f"🎯 Confidence Level: {opinion_confidence:.1%}\n"
        result += f"📊 Based on {len(relevant_facts)} relevant facts"
        
        if interest_match:
            result += f"\n🔗 This aligns with your interests in {', '.join(interests)}"
        
        return result
        
    except Exception as e:
        return f"❌ Error forming opinion: {str(e)}"

def make_prediction(scenario, timeframe="near future"):
    """Make predictions based on patterns and knowledge"""
    try:
        # Load knowledge and memory
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
            compressed = {}
        
        # Analyze patterns for prediction
        scenario_lower = scenario.lower()
        relevant_patterns = []
        
        # Look for historical patterns
        facts = knowledge.get("facts", {})
        for topic, fact_list in facts.items():
            if any(word in topic.lower() for word in scenario_lower.split()):
                relevant_patterns.extend(fact_list)
        
        # Consider user behavior patterns
        user_profile = compressed.get("user_profile", {})
        dominant_themes = compressed.get("dominant_themes", [])
        
        # Analyze emotional patterns
        emotion_history = memory.get("emotion_history", {})
        dominant_emotion = max(emotion_history, key=emotion_history.get) if emotion_history else "neutral"
        
        # Generate prediction
        prediction_confidence = 0.4
        prediction_text = ""
        
        if relevant_patterns:
            # Analyze trends
            recent_patterns = relevant_patterns[-5:]  # Last 5 relevant facts
            
            # Look for growth/decline indicators
            growth_indicators = ['increase', 'grow', 'improve', 'expand', 'rise', 'more', 'better']
            decline_indicators = ['decrease', 'decline', 'reduce', 'fall', 'less', 'worse']
            
            growth_count = sum(1 for pattern in recent_patterns for indicator in growth_indicators if indicator in pattern.lower())
            decline_count = sum(1 for pattern in recent_patterns for indicator in decline_indicators if indicator in pattern.lower())
            
            if growth_count > decline_count:
                prediction_text = f"I predict {scenario} will likely show positive development in the {timeframe}. "
                prediction_confidence += 0.2
            elif decline_count > growth_count:
                prediction_text = f"I predict {scenario} may face challenges in the {timeframe}. "
                prediction_confidence += 0.1
            else:
                prediction_text = f"I predict {scenario} will remain relatively stable in the {timeframe}. "
                prediction_confidence += 0.1
            
            # Add reasoning based on patterns
            prediction_text += f"This is based on patterns I've observed in {len(relevant_patterns)} related data points. "
            
        else:
            prediction_text = f"Based on general trends, I predict {scenario} will evolve gradually in the {timeframe}. "
            prediction_confidence = 0.3
        
        # Consider user context
        interests = user_profile.get("primary_interests", [])
        if any(interest in scenario_lower for interest in interests):
            prediction_text += f"Given your interest in {', '.join(interests)}, you're likely to be actively involved in this outcome. "
            prediction_confidence += 0.1
        
        # Add emotional context
        if dominant_emotion in ["happy", "excited"]:
            prediction_text += "Your positive outlook may contribute to favorable outcomes. "
            prediction_confidence += 0.05
        elif dominant_emotion in ["worried", "anxious"]:
            prediction_text += "Being mindful of potential challenges could help you prepare better. "
            prediction_confidence += 0.05
        
        # Cap confidence
        prediction_confidence = min(0.8, prediction_confidence)  # Predictions should never be 100% confident
        
        # Save prediction
        save_fact("predictions", f"Prediction for {scenario}: {prediction_text} (confidence: {prediction_confidence:.1f})", confidence=prediction_confidence)
        
        result = f"🔮 Prediction for '{scenario}':\n\n"
        result += f"{prediction_text}\n\n"
        result += f"⏰ Timeframe: {timeframe}\n"
        result += f"🎯 Confidence Level: {prediction_confidence:.1%}\n"
        result += f"📊 Based on {len(relevant_patterns)} pattern analysis"
        
        return result
        
    except Exception as e:
        return f"❌ Error making prediction: {str(e)}"

def give_advice(situation, goal=""):
    """Provide advice based on knowledge, experience, and reasoning"""
    try:
        # Load all knowledge sources
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
            compressed = {}
        
        # Analyze the situation
        situation_lower = situation.lower()
        goal_lower = goal.lower() if goal else ""
        
        # Find relevant knowledge
        relevant_advice = []
        facts = knowledge.get("facts", {})
        
        # Look for related experiences and knowledge
        advice_keywords = ['how', 'should', 'could', 'might', 'recommend', 'suggest', 'advice', 'tip', 'best']
        for topic, fact_list in facts.items():
            if any(word in situation_lower for word in topic.lower().split()) or any(keyword in topic.lower() for keyword in advice_keywords):
                relevant_advice.extend(fact_list)
        
        # Consider user profile and preferences
        user_profile = compressed.get("user_profile", {})
        interests = user_profile.get("primary_interests", [])
        
        # Analyze user's emotional state for appropriate advice tone
        emotion_history = memory.get("emotion_history", {})
        dominant_emotion = max(emotion_history, key=emotion_history.get) if emotion_history else "neutral"
        
        # Generate advice
        advice_text = ""
        advice_confidence = 0.5
        
        # Start with empathy based on emotional state
        if dominant_emotion in ["sad", "worried", "anxious"]:
            advice_text += "I understand this might be challenging for you. "
        elif dominant_emotion in ["happy", "excited"]:
            advice_text += "It's great that you're approaching this positively! "
        
        # Provide specific advice based on situation
        if "study" in situation_lower or "exam" in situation_lower or "learn" in situation_lower:
            advice_text += "For learning and studying, I'd recommend breaking things into smaller chunks, practicing regularly, and using active recall techniques. "
            advice_confidence += 0.2
        elif "project" in situation_lower or "work" in situation_lower:
            advice_text += "For project work, start by clearly defining your goals, break the work into manageable tasks, and set realistic deadlines. "
            advice_confidence += 0.2
        elif "programming" in situation_lower or "code" in situation_lower:
            advice_text += "For programming challenges, start with understanding the problem clearly, plan your approach, and don't hesitate to break complex problems into smaller functions. "
            advice_confidence += 0.2
        elif "decision" in situation_lower or "choose" in situation_lower:
            advice_text += "When making decisions, consider listing pros and cons, think about long-term consequences, and trust your instincts after careful analysis. "
            advice_confidence += 0.1
        else:
            advice_text += "Based on the situation you've described, here's what I think could help: "
        
        # Add goal-specific advice
        if goal:
            advice_text += f"Since your goal is {goal}, I'd suggest focusing on actions that directly contribute to this outcome. "
            advice_confidence += 0.1
        
        # Add personalized advice based on user interests
        if interests:
            if "technology" in interests and any(tech_word in situation_lower for tech_word in ["tech", "programming", "code", "software"]):
                advice_text += "Given your technical background, you might want to approach this systematically and consider automation opportunities. "
                advice_confidence += 0.1
            elif "creative" in interests:
                advice_text += "With your creative mindset, don't be afraid to think outside the box and explore innovative solutions. "
                advice_confidence += 0.1
        
        # Add general wisdom from knowledge base
        if relevant_advice:
            advice_text += f"Based on what I've learned from our conversations, similar situations often benefit from patience and persistence. "
            advice_confidence += 0.1
        
        # Provide actionable steps
        advice_text += "\n\nHere are some concrete steps you could consider:\n"
        advice_text += "1. Clearly define what success looks like for you\n"
        advice_text += "2. Identify the key obstacles or challenges\n"
        advice_text += "3. Break down the solution into smaller, manageable parts\n"
        advice_text += "4. Start with the easiest or most critical step\n"
        advice_text += "5. Monitor your progress and adjust as needed"
        
        # Cap confidence
        advice_confidence = min(0.9, advice_confidence)
        
        # Save advice to knowledge base
        save_fact("advice_given", f"Advice for {situation}: {advice_text[:100]}... (confidence: {advice_confidence:.1f})", confidence=advice_confidence)
        
        result = f"💡 My Advice for '{situation}':\n\n"
        result += f"{advice_text}\n\n"
        result += f"🎯 Confidence Level: {advice_confidence:.1%}\n"
        result += f"📊 Based on {len(relevant_advice)} relevant experiences"
        
        if goal:
            result += f"\n🎯 Aligned with your goal: {goal}"
        
        return result
        
    except Exception as e:
        return f"❌ Error giving advice: {str(e)}"

def reason_about(topic, question=""):
    """Deep reasoning combining multiple knowledge sources"""
    try:
        # Load all knowledge sources
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
            compressed = {}
        
        # Gather information from multiple sources
        topic_lower = topic.lower()
        
        # 1. Direct knowledge
        direct_facts = []
        facts = knowledge.get("facts", {})
        for fact_topic, fact_list in facts.items():
            if topic_lower in fact_topic.lower() or any(word in fact_topic.lower() for word in topic_lower.split()):
                direct_facts.extend(fact_list)
        
        # 2. Compressed insights
        insights = compressed.get("insights", [])
        themes = compressed.get("dominant_themes", [])
        user_profile = compressed.get("user_profile", {})
        
        # 3. Memory patterns
        beliefs = knowledge.get("beliefs", {})
        
        # 4. Web knowledge (if needed)
        web_info = []
        if len(direct_facts) < 3:
            try:
                from tools import web_search
                web_result = web_search(topic)
                if "❌" not in web_result:
                    web_info.append(web_result)
            except:
                pass
        
        # Begin reasoning process
        reasoning_text = f"🤔 Let me think about {topic}...\n\n"
        
        # Analyze what we know
        if direct_facts:
            reasoning_text += f"📚 From my knowledge base, I have {len(direct_facts)} relevant facts:\n"
            # Show most relevant facts
            for fact in direct_facts[:3]:
                reasoning_text += f"  • {fact[:100]}...\n"
            reasoning_text += "\n"
        
        # Consider patterns and themes
        if any(theme in topic_lower for theme in themes):
            matching_themes = [theme for theme in themes if theme in topic_lower]
            reasoning_text += f"🎯 This connects to dominant themes in our conversations: {', '.join(matching_themes)}\n\n"
        
        # User context
        interests = user_profile.get("primary_interests", [])
        if any(interest in topic_lower for interest in interests):
            reasoning_text += f"👤 This aligns with your interests in {', '.join(interests)}, which suggests it's particularly relevant to you.\n\n"
        
        # Logical reasoning
        reasoning_text += "🧠 My reasoning process:\n"
        
        if question:
            reasoning_text += f"Considering your question: '{question}'\n"
        
        # Synthesize information
        if direct_facts and web_info:
            reasoning_text += "Combining my stored knowledge with current information, "
        elif direct_facts:
            reasoning_text += "Based on my accumulated knowledge, "
        elif web_info:
            reasoning_text += "From available information, "
        else:
            reasoning_text += "While I have limited specific information, "
        
        # Draw connections
        reasoning_text += f"I can see several important aspects of {topic}:\n\n"
        
        # Analyze different dimensions
        if "technology" in interests and any(tech_word in topic_lower for tech_word in ["tech", "ai", "programming", "software"]):
            reasoning_text += "🔧 Technical perspective: This involves understanding systems, processes, and optimization.\n"
        
        if "creative" in interests:
            reasoning_text += "🎨 Creative perspective: There are opportunities for innovation and unique approaches.\n"
        
        if "academics" in interests:
            reasoning_text += "📖 Academic perspective: This can be approached through systematic study and research.\n"
        
        # Consider implications
        reasoning_text += f"\n💭 Implications and considerations:\n"
        reasoning_text += f"• This topic intersects with {len(direct_facts)} areas of knowledge I have\n"
        
        if beliefs:
            reasoning_text += f"• It relates to beliefs I've formed about patterns in our conversations\n"
        
        reasoning_text += f"• The complexity suggests multiple valid approaches exist\n"
        
        # Conclusion
        reasoning_text += f"\n🎯 Conclusion:\n"
        reasoning_text += f"{topic.title()} appears to be a multifaceted subject that benefits from combining "
        
        if direct_facts:
            reasoning_text += "established knowledge, "
        if web_info:
            reasoning_text += "current information, "
        if interests:
            reasoning_text += f"your {', '.join(interests)} background, "
        
        reasoning_text += "and careful analysis of the specific context."
        
        # Save reasoning to knowledge base
        save_fact("reasoning", f"Reasoned about {topic}: Multi-source analysis completed", confidence=0.8)
        
        return reasoning_text
        
    except Exception as e:
        return f"❌ Error in reasoning process: {str(e)}"

def synthesize_knowledge(topic1, topic2, relationship=""):
    """Synthesize knowledge by finding connections between topics"""
    try:
        # Load knowledge
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
            compressed = {}
        
        # Find facts related to both topics
        topic1_lower = topic1.lower()
        topic2_lower = topic2.lower()
        
        facts = knowledge.get("facts", {})
        topic1_facts = []
        topic2_facts = []
        shared_facts = []
        
        for fact_topic, fact_list in facts.items():
            topic_words = fact_topic.lower().split()
            
            # Check for topic1
            if topic1_lower in fact_topic.lower() or any(word in topic1_lower for word in topic_words):
                topic1_facts.extend(fact_list)
            
            # Check for topic2
            if topic2_lower in fact_topic.lower() or any(word in topic2_lower for word in topic_words):
                topic2_facts.extend(fact_list)
            
            # Check for facts mentioning both topics
            if (topic1_lower in fact_topic.lower() or any(word in topic1_lower for word in topic_words)) and \
               (topic2_lower in fact_topic.lower() or any(word in topic2_lower for word in topic_words)):
                shared_facts.extend(fact_list)
        
        # Analyze word overlap
        topic1_words = set()
        for fact in topic1_facts:
            topic1_words.update(fact.lower().split())
        
        topic2_words = set()
        for fact in topic2_facts:
            topic2_words.update(fact.lower().split())
        
        common_words = topic1_words.intersection(topic2_words)
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        meaningful_common = common_words - stop_words
        
        # Generate synthesis
        synthesis_text = f"🔗 Knowledge Synthesis: {topic1} ↔ {topic2}\n\n"
        
        if shared_facts:
            synthesis_text += f"📊 Direct Connections Found:\n"
            synthesis_text += f"I found {len(shared_facts)} facts that mention both topics:\n"
            for fact in shared_facts[:3]:
                synthesis_text += f"  • {fact[:100]}...\n"
            synthesis_text += "\n"
        
        if meaningful_common:
            synthesis_text += f"🎯 Common Themes:\n"
            synthesis_text += f"Both topics share these concepts: {', '.join(list(meaningful_common)[:8])}\n\n"
        
        # Analyze relationship
        if relationship:
            synthesis_text += f"🔍 Analyzing relationship: '{relationship}'\n"
        
        # Look for patterns
        synthesis_text += f"📈 Pattern Analysis:\n"
        synthesis_text += f"• {topic1}: {len(topic1_facts)} related facts\n"
        synthesis_text += f"• {topic2}: {len(topic2_facts)} related facts\n"
        synthesis_text += f"• Overlap: {len(shared_facts)} shared facts\n"
        synthesis_text += f"• Common concepts: {len(meaningful_common)} themes\n\n"
        
        # Generate insights
        synthesis_text += f"💡 Synthesis Insights:\n"
        
        if len(shared_facts) > 0:
            synthesis_text += f"• Strong connection exists between {topic1} and {topic2}\n"
        elif len(meaningful_common) > 3:
            synthesis_text += f"• Moderate thematic overlap suggests related domains\n"
        else:
            synthesis_text += f"• Limited direct connection, but may share underlying principles\n"
        
        # Consider user context
        user_profile = compressed.get("user_profile", {})
        interests = user_profile.get("primary_interests", [])
        
        if any(interest in topic1_lower or interest in topic2_lower for interest in interests):
            synthesis_text += f"• Both topics align with your interests in {', '.join(interests)}\n"
        
        # Suggest applications
        synthesis_text += f"\n🚀 Potential Applications:\n"
        if "technology" in interests:
            synthesis_text += f"• Technical integration opportunities between {topic1} and {topic2}\n"
        if "creative" in interests:
            synthesis_text += f"• Creative fusion possibilities combining both domains\n"
        if "academics" in interests:
            synthesis_text += f"• Research opportunities exploring the intersection\n"
        
        synthesis_text += f"• Cross-pollination of ideas and methods\n"
        synthesis_text += f"• Potential for innovative solutions using both approaches\n"
        
        # Save synthesis
        save_fact("knowledge_synthesis", f"Synthesized {topic1} and {topic2}: {len(shared_facts)} connections found", confidence=0.7)
        
        return synthesis_text
        
    except Exception as e:
        return f"❌ Error in knowledge synthesis: {str(e)}"