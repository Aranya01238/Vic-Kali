import json
import re
import os
from datetime import datetime

class RAGEngine:
    def __init__(self, knowledge_file="knowledge.json"):
        self.knowledge_file = knowledge_file
        self.knowledge_base = self._load_knowledge()
        self.stop_words = {"what", "is", "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "about", "why", "how"}

    def _load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {"facts": {}}
        return {"facts": {}}

    def _get_keywords(self, text):
        # Extract meaningful keywords for matching
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if w not in self.stop_words and len(w) > 2]

    def add_knowledge(self, category, content):
        if "facts" not in self.knowledge_base:
            self.knowledge_base["facts"] = {}
        
        if category not in self.knowledge_base["facts"]:
            self.knowledge_base["facts"][category] = []
        
        # Avoid duplicate exact content
        if content not in self.knowledge_base["facts"][category]:
            self.knowledge_base["facts"][category].append(content)
            self._save_knowledge()
            return True
        return False

    def _save_knowledge(self):
        with open(self.knowledge_file, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f, indent=4)

    def retrieve(self, query, limit=3):
        query_keywords = self._get_keywords(query)
        if not query_keywords:
            return []

        results = []
        facts = self.knowledge_base.get("facts", {})

        for category, entries in facts.items():
            cat_keywords = self._get_keywords(category.replace("_", " "))
            
            # Calculate category relevance
            cat_score = sum(2 for kw in query_keywords if kw in cat_keywords)
            
            for entry in entries:
                if not isinstance(entry, str):
                    continue
                    
                entry_keywords = self._get_keywords(entry)
                # Calculate entry relevance
                entry_score = sum(1 for kw in query_keywords if kw in entry_keywords)
                
                total_score = cat_score + entry_score
                
                # Require a minimum score to prevent totally irrelevant matches
                # If query has multiple keywords, require at least some significant match
                threshold = 1
                if len(query_keywords) > 2:
                    threshold = 2

                if total_score >= threshold:
                    results.append({
                        "content": entry,
                        "score": total_score,
                        "category": category
                    })

        # Sort by score descending and return top results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def generate_response(self, query):
        retrieved = self.retrieve(query)
        if not retrieved:
            return None

        # Format the retrieved information into a cohesive response
        # In a real RAG, this would be passed to an LLM, but here we synthesize it
        best_results = []
        seen_content = set()
        
        for res in retrieved:
            content = res["content"]
            # Basic cleaning
            if content.startswith("Verified: "):
                content = content.replace("Verified: ", "")
            
            if content not in seen_content:
                best_results.append(content)
                seen_content.add(content)

        if not best_results:
            return None

        # Construct a response from the best matches
        header = "Based on what I know: "
        body = " ".join(best_results[:2])
        return f"{header}{body}"

# Global instance
rag_engine = RAGEngine()
