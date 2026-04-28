import random
import os
import webbrowser
import subprocess
from datetime import datetime

# -------- HACKER / PEER TOOLS --------

def get_system_stats():
    """Get basic system stats for the 'hacker' vibe."""
    try:
        import psutil
        import platform
        
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        stats = [
            f"🖥️ OS: {platform.system()} {platform.release()}",
            f"🧠 CPU Usage: {cpu_usage}%",
            f"💾 Memory: {memory.percent}% ({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)",
            f"💽 Disk: {disk.percent}% used",
            f"⏱️ Uptime: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        return "📊 System Diagnostics:\n" + "\n".join(stats)
    except Exception as e:
        return f"❌ System stats error: {e}"

def get_network_info():
    """Get network information (simulated hacker tool)."""
    try:
        import socket
        import psutil
        
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        interfaces = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    interfaces.append(f"  • {interface}: {addr.address}")
        
        net_io = psutil.net_io_counters()
        
        info = [
            f"🌐 Hostname: {hostname}",
            f"📍 Local IP: {local_ip}",
            f"🔌 Interfaces:\n" + "\n".join(interfaces[:3]),
            f"📡 Traffic: ↑{net_io.bytes_sent // (1024**2)}MB ↓{net_io.bytes_recv // (1024**2)}MB"
        ]
        return "🛡️ Network Scan Results:\n" + "\n".join(info)
    except Exception as e:
        return f"❌ Network info error: {e}"

def check_security():
    """Simulated security check for the 'hacker' vibe."""
    checks = [
        "🔍 Scanning for open ports... [80, 443, 22 detected]",
        "🔒 Checking firewall status... [Active]",
        "🛡️ Analyzing digital footprint... [Stealth mode enabled]",
        "🔑 Verifying encryption protocols... [AES-256 active]",
        "⚡ Optimizing response latency... [12ms]"
    ]
    return "🥷 Security Assessment:\n" + "\n".join(checks)

def list_processes():
    """List running processes (hacker tool)."""
    try:
        import psutil
        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            procs.append(proc.info)
        
        # Sort by PID and take top 10 for brevity
        procs = sorted(procs, key=lambda x: x['pid'])[:15]
        output = "📑 Active Processes (Top 15):\n"
        for p in procs:
            output += f"  • [{p['pid']}] {p['name']} ({p['username']})\n"
        return output
    except Exception as e:
        return f"❌ Process list error: {e}"

def search_files(filename, root_dir="."):
    """Search for files in the system (hacker tool)."""
    try:
        import os
        matches = []
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if filename.lower() in file.lower():
                    matches.append(os.path.join(root, file))
            if len(matches) > 10: break # Limit results
            
        if matches:
            return "🔍 File Search Results:\n" + "\n".join([f"  • {m}" for m in matches])
        return f"🤔 No files found matching '{filename}'."
    except Exception as e:
        return f"❌ Search error: {e}"

def get_file_metadata(path):
    """Get metadata for a specific file."""
    try:
        import os
        import time
        stats = os.stat(path)
        info = [
            f"📄 File: {os.path.basename(path)}",
            f"📍 Location: {os.path.dirname(path)}",
            f"⚖️ Size: {stats.st_size / 1024:.2f} KB",
            f"📅 Created: {time.ctime(stats.st_ctime)}",
            f"🕒 Modified: {time.ctime(stats.st_mtime)}",
            f"🔒 Permissions: {oct(stats.st_mode)[-3:]}"
        ]
        return "ℹ️ File Metadata:\n" + "\n".join(info)
    except Exception as e:
        return f"❌ Metadata error: {e}"

# -------- BASIC TOOLS --------

def echo(text):
    return f"(echo) {text}"

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def random_number(a=1, b=100):
    return f"Random number: {random.randint(a, b)}"

# -------- FILE SYSTEM TOOLS --------

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File saved at {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def list_dir(path="."):
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Error listing directory: {e}"

def open_target(target):
    """Open a local file/folder or URL using the default system handler."""
    try:
        if not target:
            return "Error: No target provided."
        if target.startswith(("http://", "https://")):
            webbrowser.open(target)
            return f"Opened URL: {target}"
        if hasattr(os, "startfile"):
            os.startfile(target)
            return f"Opened: {target}"
        webbrowser.open(target)
        return f"Opened target: {target}"
    except Exception as e:
        return f"Error opening target: {e}"

def open_folder(path):
    """Open a folder in the system file explorer."""
    return open_target(path)

def open_url(url):
    """Open a URL in the default browser."""
    return open_target(url)

def open_youtube(query=""):
    """Open YouTube, optionally with a search query."""
    base = "https://www.youtube.com"
    if query:
        from urllib.parse import quote_plus
        return open_target(f"{base}/results?search_query={quote_plus(query)}")
    return open_target(base)

def open_app(app_path_or_name):
    """Open an application by path, name, or registered shell target."""
    return open_target(app_path_or_name)

# -------- KNOWLEDGE BASE TOOLS --------

def save_fact(topic, fact, confidence=0.8):
    try:
        import json
        from rag_engine import rag_engine
        
        # Add to RAG system
        rag_engine.add_knowledge(topic, fact)
        
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        if topic not in knowledge["facts"]:
            knowledge["facts"][topic] = []
            knowledge["learned_topics"].append(topic)
        
        knowledge["facts"][topic].append(fact)
        knowledge["confidence_scores"][f"{topic}:{len(knowledge['facts'][topic])-1}"] = confidence
        knowledge["fact_sources"][f"{topic}:{len(knowledge['facts'][topic])-1}"] = "user_conversation"
        knowledge["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("knowledge.json", "w") as f:
            json.dump(knowledge, f, indent=4)
        
        return f"✅ Learned: {fact} (topic: {topic})"
    except Exception as e:
        return f"Error saving fact: {e}"

def query_facts(topic):
    try:
        import json
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        if topic in knowledge["facts"]:
            facts = knowledge["facts"][topic]
            return f"📚 What I know about {topic}:\n" + "\n".join([f"• {fact}" for fact in facts])
        else:
            return f"🤔 I don't have any facts about {topic} yet."
    except Exception as e:
        return f"Error querying facts: {e}"

def update_belief(topic, belief, confidence=0.7):
    try:
        import json
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        knowledge["beliefs"][topic] = {
            "belief": belief,
            "confidence": confidence,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        knowledge["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("knowledge.json", "w") as f:
            json.dump(knowledge, f, indent=4)
        
        return f"🧠 Updated belief about {topic}: {belief}"
    except Exception as e:
        return f"Error updating belief: {e}"

# -------- WEB & WIKIPEDIA TOOLS --------

def wiki_search(query, sentences=2):
    """
    Search Wikipedia for a query.
    """
    try:
        import requests
        
        # Clean the query
        clean_query = query.replace("wikipedia", "").replace("wiki search", "").strip()
        if not clean_query:
            return "❌ No search query provided"
            
        # Try real Wikipedia API
        url = "https://en.wikipedia.org/w/api.php"
        headers = {
            'User-Agent': 'Diya-AI-Assistant/1.0 (https://github.com/yourusername/diya; mailto:your@email.com)'
        }
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": clean_query,
            "redirects": 1,
            "exsentences": sentences
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if page_id != "-1": # Page exists
                    extract = page_info.get("extract", "")
                    if extract:
                        save_fact(f"wiki_{clean_query}", extract, confidence=0.9)
                        return extract

        # If direct page fails, try search
        search_params = {
            "action": "opensearch",
            "format": "json",
            "search": clean_query,
            "limit": 1
        }
        search_response = requests.get(url, params=search_params, headers=headers, timeout=10)
        if search_response.status_code == 200:
            search_data = search_response.json()
            if len(search_data) > 1 and search_data[1]:
                new_title = search_data[1][0]
                # Re-run with the found title
                params["titles"] = new_title
                final_response = requests.get(url, params=params, headers=headers, timeout=10)
                if final_response.status_code == 200:
                    final_data = final_response.json()
                    final_pages = final_data.get("query", {}).get("pages", {})
                    for p_id, p_info in final_pages.items():
                        if p_id != "-1":
                            final_extract = p_info.get("extract", "")
                            if final_extract:
                                save_fact(f"wiki_{new_title}", final_extract, confidence=0.9)
                                return final_extract

        return f"🤔 I couldn't find a Wikipedia article for '{clean_query}'."
            
    except Exception as e:
        return f"❌ Wikipedia error: {str(e)}"

def enhanced_wiki_mock(query, sentences=2):
    """Enhanced Wikipedia mock with comprehensive data"""
    wiki_database = {
        "python": "Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability with its notable use of significant whitespace.",
        "artificial intelligence": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.",
        "ai": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. It includes machine learning, natural language processing, computer vision, and robotics.",
        "machine learning": "Machine learning (ML) is a type of artificial intelligence (AI) that allows software applications to become more accurate at predicting outcomes without being explicitly programmed to do so. Machine learning algorithms use historical data as input to predict new output values.",
        "robotics": "Robotics is an interdisciplinary branch of computer science and engineering. Robotics involves design, construction, operation, and use of robots. The goal of robotics is to design intelligent machines that can help and assist humans in their day-to-day lives and keep everyone safe.",
        "javascript": "JavaScript, often abbreviated as JS, is a programming language that conforms to the ECMAScript specification. JavaScript is high-level, often just-in-time compiled, and multi-paradigm. It has curly-bracket syntax, dynamic typing, prototype-based object-orientation, and first-class functions.",
        "data science": "Data science is an inter-disciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from many structural and unstructured data. Data science is related to data mining, machine learning and big data.",
        "blockchain": "A blockchain, originally block chain, is a growing list of records, called blocks, that are linked and secured using cryptography. Each block contains a cryptographic hash of the previous block, a timestamp, and transaction data.",
        "cloud computing": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user. The term is generally used to describe data centers available to many users over the Internet.",
        "division by zero": "In mathematics, division by zero is division where the divisor (denominator) is zero. Such a division can be formally expressed as a/0 where a is the dividend. In ordinary arithmetic, the expression has no meaning, as there is no number which, when multiplied by 0, gives a (assuming a is not 0), and so division by zero is undefined.",
        "0/0": "The expression 0/0 is an indeterminate form in mathematics. It is undefined because any number multiplied by zero is zero, so there is no unique value that can be assigned to the result of 0/0."
    }
    
    query_lower = query.lower()
    best_match = None
    
    # Find exact matches first
    for key, value in wiki_database.items():
        if key in query_lower:
            best_match = (key, value)
            break
    
    # If no exact match, find partial matches (prefer whole word matches)
    if not best_match:
        for key, value in wiki_database.items():
            key_words = key.split()
            query_words = query_lower.split()
            # Check if any query word is exactly one of the key words
            if any(qw in key_words for qw in query_words):
                best_match = (key, value)
                break
    
    # Last resort: substring match
    if not best_match:
        for key, value in wiki_database.items():
            if query_lower in key or key in query_lower:
                best_match = (key, value)
                break
    
    if best_match:
        topic, info = best_match
        # Limit to requested sentences
        sentences_list = info.split('. ')
        limited_extract = '. '.join(sentences_list[:sentences])
        if len(sentences_list) > sentences:
            limited_extract += "..."
        
        # Auto-save to knowledge base
        save_fact(f"wikipedia_{topic}", f"{topic.title()}: {limited_extract}", confidence=0.8)
        
        return f"🌐 Wikipedia: {topic.title()}\n{limited_extract}"
    else:
        return f"🤔 No Wikipedia information found for '{query}'"

def web_search(query, max_results=3):
    """
    Search the web using Google for high-quality results.
    """
    try:
        import requests
        import re
        from html import unescape
        
        # Use a real browser User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        # Search Google
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Look for snippets in the Google results
            # Snippets are usually in spans with specific data-attr or just simple classes
            # This is a robust regex for common snippet patterns
            snippets = re.findall(r'<div class="VwiC3b.*?"><span>(.*?)</span>', response.text)
            
            if not snippets:
                # Fallback regex for different layouts
                snippets = re.findall(r'<div class="BNeawe s3v9rd AP7Wnd">(.*?)</div>', response.text)
            
            if snippets:
                results = []
                for snippet in snippets[:max_results]:
                    # Clean up HTML tags and entities
                    clean_snippet = re.sub(r'<[^>]+>', '', snippet)
                    clean_snippet = unescape(clean_snippet).strip()
                    if clean_snippet:
                        results.append(f"📝 {clean_snippet}")
                
                if results:
                    summary = "\n\n".join(results)
                    save_fact(f"web_{query}", summary, confidence=0.8)
                    return f"🌐 Google search for '{query}':\n\n{summary}"

        # If Google fails or no snippets found, try Wikipedia
        wiki_result = wiki_search(query)
        if "❌" not in wiki_result and "🤔" not in wiki_result:
            return f"🌐 Found information for '{query}':\n\n{wiki_result}"

        return f"🤔 I couldn't find a clear definition for '{query}' on the web. Maybe try a more specific search?"
            
    except Exception as e:
        return f"❌ Search error: {str(e)}"

def enhanced_mock_search(query):
    """Enhanced mock search with more comprehensive data"""
    mock_database = {
        "python": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. Known for its simplicity and readability, Python is widely used in web development, data science, AI, and automation.",
        "artificial intelligence": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. It includes machine learning, natural language processing, computer vision, and robotics. AI is transforming industries from healthcare to finance.",
        "ai": "AI, or Artificial Intelligence, is the simulation of human intelligence by machines, especially computer systems. Specific applications of AI include expert systems, natural language processing, speech recognition and machine vision.",
        "machine learning": "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make predictions.",
        "robotics": "Robotics is an interdisciplinary field combining mechanical engineering, electrical engineering, and computer science. Modern robots are used in manufacturing, healthcare, exploration, and service industries.",
        "programming": "Programming is the process of creating instructions for computers using programming languages. Popular languages include Python, JavaScript, Java, C++, and Go. Programming is essential for software development.",
        "javascript": "JavaScript is a versatile programming language primarily used for web development. It enables interactive web pages and is also used for server-side development with Node.js.",
        "data science": "Data Science combines statistics, programming, and domain expertise to extract insights from data. It involves data collection, cleaning, analysis, and visualization using tools like Python, R, and SQL.",
        "blockchain": "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks, linked using cryptography. It's the foundation of cryptocurrencies like Bitcoin.",
        "cloud computing": "Cloud computing delivers computing services over the internet, including servers, storage, databases, and software. Major providers include AWS, Microsoft Azure, and Google Cloud Platform.",
        "division by zero": "Division by zero is an operation for which there is no defined result. In most contexts, it is considered undefined because there is no number that you can multiply by 0 to get a non-zero number. When you try to divide 0 by 0, it is called an 'indeterminate form' because any number could technically work, making it impossible to choose just one.",
        "0/0": "0/0 is mathematically undefined and referred to as an indeterminate form. In simple terms, division is the inverse of multiplication. If 0/0 = x, then x * 0 = 0. Since any number times zero equals zero, x could be anything, so we say it's undefined.",
        "bhenchod": "Bhenchod is a common Hindi slang/profanity used as an expletive or insult. It literally translates to 'sister-f*cker'. While often used casually in some regions, it is generally considered offensive and inappropriate in formal or polite conversation.",
        "bin": "A bin is a container used for storing or discarding items. In common usage, it often refers to a 'trash bin' or 'recycling bin' for waste. In computing, 'bin' often refers to a directory (like /bin) that contains binary executable files, or a file format for binary data.",
        "laptop": "A laptop is a portable personal computer that combines all the components of a desktop (screen, keyboard, pointing device, and speakers) into a single, battery-powered unit. Laptops are designed for mobile use and are essential for work, education, and entertainment.",
        "computer": "A computer is an electronic device that processes data according to instructions. It can store, retrieve, and process information. Modern computers include desktops, laptops, smartphones, and tablets.",
        "internet": "The internet is a global network of interconnected computers and devices that communicate using standardized protocols (TCP/IP). It provides access to a vast array of information, services, and communication tools like the World Wide Web and email.",
        "smartphone": "A smartphone is a portable device that combines mobile telephone and computing functions into one unit. They are distinguished from feature phones by their stronger hardware capabilities and extensive mobile operating systems, which facilitate wider software, internet, and multimedia functionality.",
        "software": "Software is a collection of data or computer instructions that tell the computer how to work. This is in contrast to physical hardware, from which the system is built and actually performs the work.",
        "hardware": "Hardware refers to the physical components of a computer, such as the monitor, mouse, keyboard, computer data storage, hard disk drive (HDD), graphic cards, sound cards, memory, motherboard, and so on.",
        "google": "Google is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware.",
        "apple": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services.",
        "microsoft": "Microsoft Corporation is an American multinational technology company which produces computer software, consumer electronics, personal computers, and related services.",
        "tesla": "Tesla, Inc. is an American electric vehicle and clean energy company based in Austin, Texas. Tesla designs and manufactures electric cars, battery energy storage from home to grid-scale, solar panels and solar roof tiles, and related products and services.",
        "space-x": "Space Exploration Technologies Corp., doing business as SpaceX, is an American aerospace manufacturer and space transportation services company headquartered in Hawthorne, California. It was founded in 2002 by Elon Musk with the goal of reducing space transportation costs to enable the colonization of Mars.",
        "mars": "Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System, being larger than only Mercury. In English, Mars carries the name of the Roman god of war and is often referred to as the 'Red Planet'."
    }
    
    query_lower = query.lower()
    best_matches = []
    
    # Find exact and partial matches
    for key, value in mock_database.items():
        key_words = set(key.split())
        query_words = set(query_lower.split())
        
        # Calculate overlap
        overlap = query_words.intersection(key_words)
        
        # Exact match or significant overlap
        if key == query_lower or len(overlap) >= max(1, len(key_words) // 2):
            best_matches.append((key, value))
    
    # Also check for substring matches if nothing found yet
    if not best_matches:
        for key, value in mock_database.items():
            if query_lower in key or key in query_lower:
                best_matches.append((key, value))
    
    if best_matches:
        results = []
        for i, (topic, info) in enumerate(best_matches[:3]):
            results.append(f"📝 {info}")
            save_fact(f"web_{topic}", info, confidence=0.7)
        
        return f"🌐 Web search for '{query}':\n" + "\n\n".join(results)
    else:
        return f"🤔 No web results found for '{query}' - try a different search term"

# -------- WEB FILE DOWNLOAD & ANALYSIS TOOLS --------

def download_file(url, filename=None):
    """Download a file from the web"""
    try:
        import requests
        import os
        from urllib.parse import urlparse
        
        # Extract filename from URL if not provided
        if not filename:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = "downloaded_file.txt"
        
        # Add downloads folder
        downloads_dir = "downloads"
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        filepath = os.path.join(downloads_dir, filename)
        
        # Download the file
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Save the file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Auto-save download info to knowledge base
        save_fact("downloads", f"Downloaded {filename} from {url}", confidence=0.9)
        
        return f"📥 Downloaded: {filename}\n📁 Saved to: {filepath}\n📊 Size: {len(response.content)} bytes"
        
    except Exception as e:
        return f"❌ Download failed: {str(e)}"

def analyze_file(filepath):
    """Analyze and summarize a file's content"""
    try:
        import os
        
        if not os.path.exists(filepath):
            return f"❌ File not found: {filepath}"
        
        # Get file info
        file_size = os.path.getsize(filepath)
        file_ext = os.path.splitext(filepath)[1].lower()
        
        # Read and analyze based on file type
        if file_ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']:
            return analyze_text_file(filepath, file_ext, file_size)
        elif file_ext in ['.pdf']:
            return analyze_pdf_file(filepath, file_size)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return analyze_image_file(filepath, file_size)
        else:
            return analyze_binary_file(filepath, file_ext, file_size)
            
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"

def analyze_text_file(filepath, file_ext, file_size):
    """Analyze text-based files"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Basic analysis
        lines = content.split('\n')
        words = content.split()
        chars = len(content)
        
        # Generate summary
        summary_lines = []
        if len(lines) > 10:
            # Show first few lines and last few lines
            summary_lines = lines[:5] + ['...'] + lines[-3:]
        else:
            summary_lines = lines
        
        summary = '\n'.join(summary_lines[:20])  # Limit to 20 lines
        
        # Detect content type
        content_type = "Text file"
        if file_ext == '.py':
            content_type = "Python script"
        elif file_ext == '.js':
            content_type = "JavaScript file"
        elif file_ext == '.html':
            content_type = "HTML document"
        elif file_ext == '.json':
            content_type = "JSON data"
        elif file_ext == '.csv':
            content_type = "CSV data"
        elif file_ext == '.md':
            content_type = "Markdown document"
        
        # Auto-save analysis to knowledge base
        analysis_summary = f"{content_type}: {lines} lines, {len(words)} words"
        save_fact("file_analysis", analysis_summary, confidence=0.8)
        
        result = f"📄 File Analysis: {os.path.basename(filepath)}\n"
        result += f"📊 Type: {content_type}\n"
        result += f"📏 Size: {file_size} bytes\n"
        result += f"📝 Lines: {len(lines)}, Words: {len(words)}, Characters: {chars}\n\n"
        result += f"📖 Content Preview:\n{summary}"
        
        if len(summary) > 1000:
            result = result[:1000] + "...\n[Content truncated for display]"
        
        return result
        
    except Exception as e:
        return f"❌ Text analysis failed: {str(e)}"

def analyze_pdf_file(filepath, file_size):
    """Analyze PDF files (basic info only without external libraries)"""
    try:
        # Basic PDF analysis without external libraries
        with open(filepath, 'rb') as f:
            content = f.read(1024)  # Read first 1KB
        
        # Check if it's actually a PDF
        if not content.startswith(b'%PDF'):
            return f"❌ File doesn't appear to be a valid PDF"
        
        # Extract basic info
        content_str = content.decode('latin-1', errors='ignore')
        
        result = f"📄 File Analysis: {os.path.basename(filepath)}\n"
        result += f"📊 Type: PDF document\n"
        result += f"📏 Size: {file_size} bytes\n"
        result += f"📝 Note: PDF content analysis requires additional libraries\n"
        result += f"💡 Suggestion: Convert to text format for detailed analysis"
        
        # Auto-save analysis to knowledge base
        save_fact("file_analysis", f"PDF document: {file_size} bytes", confidence=0.7)
        
        return result
        
    except Exception as e:
        return f"❌ PDF analysis failed: {str(e)}"

def analyze_image_file(filepath, file_size):
    """Analyze image files (basic info only)"""
    try:
        result = f"📄 File Analysis: {os.path.basename(filepath)}\n"
        result += f"📊 Type: Image file\n"
        result += f"📏 Size: {file_size} bytes\n"
        result += f"🖼️ Note: Image content analysis requires computer vision libraries\n"
        result += f"💡 Suggestion: Use image description tools for detailed analysis"
        
        # Auto-save analysis to knowledge base
        save_fact("file_analysis", f"Image file: {file_size} bytes", confidence=0.7)
        
        return result
        
    except Exception as e:
        return f"❌ Image analysis failed: {str(e)}"

def analyze_binary_file(filepath, file_ext, file_size):
    """Analyze binary files (basic info only)"""
    try:
        result = f"📄 File Analysis: {os.path.basename(filepath)}\n"
        result += f"📊 Type: Binary file ({file_ext})\n"
        result += f"📏 Size: {file_size} bytes\n"
        result += f"🔧 Note: Binary file content cannot be displayed as text\n"
        result += f"💡 File extension suggests: {get_file_type_description(file_ext)}"
        
        # Auto-save analysis to knowledge base
        save_fact("file_analysis", f"Binary file {file_ext}: {file_size} bytes", confidence=0.7)
        
        return result
        
    except Exception as e:
        return f"❌ Binary analysis failed: {str(e)}"

def get_file_type_description(ext):
    """Get description of file type based on extension"""
    descriptions = {
        '.exe': 'Windows executable',
        '.zip': 'Compressed archive',
        '.rar': 'RAR archive',
        '.tar': 'TAR archive',
        '.gz': 'GZIP compressed file',
        '.mp3': 'Audio file',
        '.mp4': 'Video file',
        '.avi': 'Video file',
        '.mov': 'Video file',
        '.doc': 'Microsoft Word document',
        '.docx': 'Microsoft Word document',
        '.xls': 'Microsoft Excel spreadsheet',
        '.xlsx': 'Microsoft Excel spreadsheet',
        '.ppt': 'Microsoft PowerPoint presentation',
        '.pptx': 'Microsoft PowerPoint presentation'
    }
    return descriptions.get(ext, 'Unknown file type')

def download_and_analyze(url, filename=None):
    """Download a file and immediately analyze it"""
    try:
        # Download the file
        download_result = download_file(url, filename)
        
        if "❌" in download_result:
            return download_result
        
        # Extract filepath from download result
        lines = download_result.split('\n')
        filepath = None
        for line in lines:
            if line.startswith('📁 Saved to:'):
                filepath = line.replace('📁 Saved to:', '').strip()
                break
        
        if not filepath:
            return f"{download_result}\n❌ Could not determine file path for analysis"
        
        # Analyze the downloaded file
        analysis_result = analyze_file(filepath)
        
        return f"{download_result}\n\n{analysis_result}"
        
    except Exception as e:
        return f"❌ Download and analysis failed: {str(e)}"

def verify_info(claim):
    """Cross-reference a claim with web sources"""
    try:
        # Search for the claim
        web_result = web_search(claim, max_results=2)
        wiki_result = wiki_search(claim, sentences=1)
        
        # Auto-save verification attempt
        save_fact(f"verification_{claim.lower()[:20]}", f"Verified: {claim}", confidence=0.6)
        
        return f"🔍 Verification for: '{claim}'\n\n{web_result}\n\n{wiki_result}"
    except Exception as e:
        return f"Error verifying info: {e}"

# -------- CALCULATOR & LOGIC TOOLS --------

def calculate(expression):
    """Safely evaluate mathematical expressions"""
    try:
        import math
        import re
        
        # Clean the expression
        expr = expression.strip()
        
        # Handle factorial (simple case)
        if '!' in expr:
            expr = expr.replace('!', '')
            try:
                n = int(expr.strip())
                result = 1
                for i in range(1, n + 1):
                    result *= i
                save_fact("calculations", f"{expression} = {result}", confidence=1.0)
                return f"🧮 Calculation: {expression}\n📊 Result: {result}"
            except:
                return f"❌ Invalid factorial expression: {expression}"
        
        # Replace common math functions and constants
        expr = expr.replace('^', '**')  # Convert ^ to ** for Python
        expr = expr.replace('pi', 'math.pi')
        expr = expr.replace('sqrt(', 'math.sqrt(')
        expr = expr.replace('sin(', 'math.sin(')
        expr = expr.replace('cos(', 'math.cos(')
        expr = expr.replace('tan(', 'math.tan(')
        
        # Basic safety check - remove dangerous functions
        dangerous = ['import', 'exec', 'eval', 'open', 'file', '__']
        for danger in dangerous:
            if danger in expr.lower():
                return f"❌ Unsafe expression: {expression}"
        
        # Evaluate the expression
        result = eval(expr)
        
        # Format the result nicely
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)  # Avoid floating point precision issues
        
        # Auto-save calculation to knowledge base
        save_fact("calculations", f"{expression} = {result}", confidence=1.0)
        
        return f"🧮 Calculation: {expression}\n📊 Result: {result}"
        
    except ZeroDivisionError:
        return f"❌ Calculation error: division by zero is undefined. Try asking \"why 0/0\" for an explanation."
    except Exception as e:
        return f"❌ Calculation error: {str(e)}"

def convert_units(value, from_unit, to_unit):
    """Convert between different units"""
    try:
        # Unit conversion tables with variations
        length_units = {
            'mm': 0.001, 'millimeter': 0.001, 'millimeters': 0.001,
            'cm': 0.01, 'centimeter': 0.01, 'centimeters': 0.01,
            'm': 1, 'meter': 1, 'meters': 1, 'metre': 1, 'metres': 1,
            'km': 1000, 'kilometer': 1000, 'kilometers': 1000, 'kilometre': 1000, 'kilometres': 1000,
            'inch': 0.0254, 'inches': 0.0254, 'in': 0.0254,
            'ft': 0.3048, 'foot': 0.3048, 'feet': 0.3048,
            'yard': 0.9144, 'yards': 0.9144, 'yd': 0.9144,
            'mile': 1609.34, 'miles': 1609.34, 'mi': 1609.34
        }
        
        weight_units = {
            'mg': 0.001, 'milligram': 0.001, 'milligrams': 0.001,
            'g': 1, 'gram': 1, 'grams': 1,
            'kg': 1000, 'kilogram': 1000, 'kilograms': 1000,
            'oz': 28.3495, 'ounce': 28.3495, 'ounces': 28.3495,
            'lb': 453.592, 'pound': 453.592, 'pounds': 453.592, 'lbs': 453.592,
            'ton': 1000000, 'tons': 1000000, 'tonne': 1000000, 'tonnes': 1000000
        }
        
        temperature_units = ['celsius', 'fahrenheit', 'kelvin', 'c', 'f', 'k']
        
        time_units = {
            'second': 1, 'seconds': 1, 'sec': 1, 'secs': 1, 's': 1,
            'minute': 60, 'minutes': 60, 'min': 60, 'mins': 60,
            'hour': 3600, 'hours': 3600, 'h': 3600, 'hr': 3600, 'hrs': 3600,
            'day': 86400, 'days': 86400, 'd': 86400,
            'week': 604800, 'weeks': 604800, 'wk': 604800, 'wks': 604800,
            'month': 2629746, 'months': 2629746, 'mo': 2629746,
            'year': 31556952, 'years': 31556952, 'yr': 31556952, 'yrs': 31556952
        }
        
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Length conversions
        if from_unit in length_units and to_unit in length_units:
            meters = float(value) * length_units[from_unit]
            result = meters / length_units[to_unit]
            unit_type = "length"
        
        # Weight conversions
        elif from_unit in weight_units and to_unit in weight_units:
            grams = float(value) * weight_units[from_unit]
            result = grams / weight_units[to_unit]
            unit_type = "weight"
        
        # Time conversions
        elif from_unit in time_units and to_unit in time_units:
            seconds = float(value) * time_units[from_unit]
            result = seconds / time_units[to_unit]
            unit_type = "time"
        
        # Temperature conversions
        elif from_unit in temperature_units and to_unit in temperature_units:
            result = convert_temperature(float(value), from_unit, to_unit)
            unit_type = "temperature"
        
        else:
            return f"❌ Unsupported unit conversion: {from_unit} to {to_unit}"
        
        # Format result
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, float):
            result = round(result, 6)
        
        # Auto-save conversion to knowledge base
        save_fact("conversions", f"{value} {from_unit} = {result} {to_unit}", confidence=1.0)
        
        return f"🔄 Unit Conversion ({unit_type}):\n📏 {value} {from_unit} = {result} {to_unit}"
        
    except Exception as e:
        return f"❌ Conversion error: {str(e)}"

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Convert to Celsius first
    if from_unit in ['fahrenheit', 'f']:
        celsius = (value - 32) * 5/9
    elif from_unit in ['kelvin', 'k']:
        celsius = value - 273.15
    else:  # celsius or c
        celsius = value
    
    # Convert from Celsius to target
    if to_unit in ['fahrenheit', 'f']:
        return celsius * 9/5 + 32
    elif to_unit in ['kelvin', 'k']:
        return celsius + 273.15
    else:  # celsius or c
        return celsius

def date_math(operation, date1, date2=None, unit='days'):
    """Perform date calculations"""
    try:
        from datetime import datetime, timedelta
        import re
        
        # Parse dates
        def parse_date(date_str):
            formats = [
                '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y',
                '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Try parsing relative dates
            if date_str.lower() == 'today':
                return datetime.now()
            elif date_str.lower() == 'yesterday':
                return datetime.now() - timedelta(days=1)
            elif date_str.lower() == 'tomorrow':
                return datetime.now() + timedelta(days=1)
            
            raise ValueError(f"Could not parse date: {date_str}")
        
        dt1 = parse_date(date1)
        
        if operation == 'difference' and date2:
            dt2 = parse_date(date2)
            diff = abs((dt2 - dt1).total_seconds())
            
            if unit == 'seconds':
                result = int(diff)
            elif unit == 'minutes':
                result = int(diff / 60)
            elif unit == 'hours':
                result = int(diff / 3600)
            elif unit == 'days':
                result = int(diff / 86400)
            elif unit == 'weeks':
                result = int(diff / 604800)
            else:
                result = int(diff / 86400)  # default to days
            
            # Auto-save to knowledge base
            save_fact("date_calculations", f"Difference between {date1} and {date2}: {result} {unit}", confidence=1.0)
            
            return f"📅 Date Difference:\n⏰ {date1} to {date2}\n📊 Result: {result} {unit}"
        
        elif operation == 'add' and date2:
            # Add time to date
            amount = int(date2)
            if unit == 'days':
                new_date = dt1 + timedelta(days=amount)
            elif unit == 'weeks':
                new_date = dt1 + timedelta(weeks=amount)
            elif unit == 'months':
                # Approximate months as 30 days
                new_date = dt1 + timedelta(days=amount * 30)
            elif unit == 'years':
                # Approximate years as 365 days
                new_date = dt1 + timedelta(days=amount * 365)
            else:
                new_date = dt1 + timedelta(days=amount)
            
            result_str = new_date.strftime('%Y-%m-%d')
            
            # Auto-save to knowledge base
            save_fact("date_calculations", f"{date1} + {amount} {unit} = {result_str}", confidence=1.0)
            
            return f"📅 Date Addition:\n📆 {date1} + {amount} {unit}\n📊 Result: {result_str}"
        
        else:
            return f"❌ Unsupported date operation: {operation}"
            
    except Exception as e:
        return f"❌ Date calculation error: {str(e)}"

def logical_operation(operation, args):
    """Perform logical operations"""
    try:
        operation = operation.lower()
        
        # Convert string arguments to boolean values
        def to_bool(arg):
            if isinstance(arg, str):
                arg = arg.lower()
                if arg in ['true', '1', 'yes', 'on']:
                    return True
                elif arg in ['false', '0', 'no', 'off']:
                    return False
                else:
                    return bool(arg)
            return bool(arg)
        
        # Convert args to list if it's a string
        if isinstance(args, str):
            args = args.split()
        elif not isinstance(args, list):
            args = [args]
        
        bool_args = [to_bool(arg) for arg in args]
        
        if operation == 'and':
            result = all(bool_args)
        elif operation == 'or':
            result = any(bool_args)
        elif operation == 'not':
            if len(bool_args) != 1:
                return "❌ NOT operation requires exactly one argument"
            result = not bool_args[0]
        elif operation == 'xor':
            if len(bool_args) != 2:
                return "❌ XOR operation requires exactly two arguments"
            result = bool_args[0] != bool_args[1]
        else:
            return f"❌ Unsupported logical operation: {operation}"
        
        # Auto-save to knowledge base
        save_fact("logical_operations", f"{operation}({', '.join(map(str, args))}) = {result}", confidence=1.0)
        
        return f"🧠 Logical Operation: {operation.upper()}\n📊 Arguments: {', '.join(map(str, args))}\n✅ Result: {result}"
        
    except Exception as e:
        return f"❌ Logical operation error: {str(e)}"

# -------- TOOL LEARNING & ANALYSIS TOOLS --------

def show_tool_performance():
    """Show current tool performance statistics"""
    try:
        import json
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        tool_performance = memory.get("tool_performance", {})
        tool_preferences = memory.get("tool_preferences", {})
        tool_insights = memory.get("tool_insights", [])
        
        if not tool_performance:
            return "📊 No tool performance data available yet."
        
        result = "🔧 Tool Performance Analysis:\n\n"
        
        # Overall statistics
        total_calls = sum(stats.get("success", 0) + stats.get("fail", 0) for stats in tool_performance.values())
        total_successes = sum(stats.get("success", 0) for stats in tool_performance.values())
        
        if total_calls > 0:
            overall_success_rate = (total_successes / total_calls) * 100
            result += f"📈 Overall Success Rate: {overall_success_rate:.1f}% ({total_successes}/{total_calls} calls)\n\n"
        
        # Individual tool performance
        result += "📊 Individual Tool Performance:\n"
        for tool_name, stats in sorted(tool_performance.items()):
            success = stats.get("success", 0)
            fail = stats.get("fail", 0)
            total = success + fail
            avg_time = stats.get("avg_response_time", 0)
            
            if total > 0:
                success_rate = (success / total) * 100
                result += f"  🔧 {tool_name}: {success_rate:.1f}% success ({success}/{total}) - {avg_time:.3f}s avg\n"
        
        # Tool preferences
        if tool_preferences:
            result += f"\n🏆 Tool Preferences:\n"
            if tool_preferences.get("most_successful"):
                result += f"  ✅ Most Reliable: {tool_preferences['most_successful']}\n"
            if tool_preferences.get("fastest"):
                result += f"  ⚡ Fastest: {tool_preferences['fastest']}\n"
            if tool_preferences.get("least_successful"):
                result += f"  ⚠️ Needs Attention: {tool_preferences['least_successful']}\n"
        
        # Recent insights
        if tool_insights:
            result += f"\n💡 Recent Insights:\n"
            for insight in tool_insights[-3:]:  # Show last 3 insights
                result += f"  • {insight}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error analyzing tool performance: {str(e)}"

def reset_tool_performance():
    """Reset all tool performance statistics"""
    try:
        import json
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        # Reset tool performance data
        memory["tool_performance"] = {}
        memory["tool_preferences"] = {
            "most_successful": None,
            "least_successful": None,
            "fastest": None,
            "slowest": None
        }
        memory["tool_insights"] = []
        
        with open("memory.json", "w") as f:
            json.dump(memory, f, indent=4)
        
        return "🔄 Tool performance statistics have been reset."
        
    except Exception as e:
        return f"❌ Error resetting tool performance: {str(e)}"

def list_all_tools():
    """List all available tools by category"""
    try:
        from tool_registry import TOOLS
        
        # Categorize tools
        categories = {
            "Core Tools": ["echo", "time", "random", "read_file", "write_file", "list_dir"],
            "Knowledge Tools": ["save_fact", "query_facts", "update_belief", "wiki_search", "web_search", "verify_info"],
            "File Tools": ["download_file", "analyze_file", "download_and_analyze"],
            "Math Tools": ["calculate", "convert_units", "add", "subtract", "multiply", "divide", "power", "square_root", "factorial", "fibonacci", "prime_check"],
            "Text Tools": ["text_length", "word_count", "to_uppercase", "to_lowercase", "reverse_text", "remove_spaces", "extract_emails", "extract_urls"],
            "Data Tools": ["list_sum", "list_average", "list_median", "list_mode", "list_sort", "correlation", "linear_regression"],
            "System Tools": ["current_timestamp", "format_timestamp", "days_between", "add_days", "generate_uuid", "system_info"],
            "Encoding Tools": ["base64_encode", "base64_decode", "url_encode", "url_decode", "md5_hash", "sha256_hash"],
            "Network Tools": ["is_valid_ip", "is_valid_email", "is_valid_url", "extract_domain"],
            "Utility Tools": ["generate_password", "color_hex_to_rgb", "bmi_calculator", "loan_calculator", "tip_calculator"],
            "Logic Tools": ["logical_operation", "date_math"],
            "Performance Tools": ["show_tool_performance", "reset_tool_performance", "list_all_tools"]
        }
        
        result = f"🔧 Available Tools ({len(TOOLS)} total):\n\n"
        
        for category, tool_names in categories.items():
            available_tools = [name for name in tool_names if name in TOOLS]
            if available_tools:
                result += f"📂 {category} ({len(available_tools)} tools):\n"
                for tool in available_tools:
                    result += f"  • {tool}\n"
                result += "\n"
        
        # List any uncategorized tools
        categorized = set()
        for tools in categories.values():
            categorized.update(tools)
        
        uncategorized = [name for name in TOOLS.keys() if name not in categorized]
        if uncategorized:
            result += f"📂 Other Tools ({len(uncategorized)} tools):\n"
            for tool in sorted(uncategorized):
                result += f"  • {tool}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error listing tools: {str(e)}"

def search_tools(query):
    """Search for tools by name or functionality"""
    try:
        from tool_registry import TOOLS
        query = query.lower()
        
        matches = []
        for tool_name in TOOLS.keys():
            if query in tool_name.lower():
                matches.append(tool_name)
        
        if matches:
            result = f"🔍 Found {len(matches)} tools matching '{query}':\n"
            for tool in sorted(matches):
                result += f"  • {tool}\n"
            return result
        else:
            return f"❌ No tools found matching '{query}'"
            
    except Exception as e:
        return f"❌ Error searching tools: {str(e)}"

# -------- KNOWLEDGE COMPRESSION TOOLS --------

def compress_knowledge():
    """Compress raw facts into higher-level understanding"""
    try:
        import json
        from collections import Counter, defaultdict
        
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        facts = knowledge.get("facts", {})
        if not facts:
            return "📚 No facts to compress yet."
        
        # Initialize compressed knowledge structure
        compressed = {
            "patterns": {},
            "insights": [],
            "categories": {},
            "relationships": {},
            "user_profile": {},
            "dominant_themes": [],
            "compression_stats": {}
        }
        
        # Analyze fact patterns
        all_facts = []
        topic_word_counts = defaultdict(Counter)
        
        for topic, fact_list in facts.items():
            for fact in fact_list:
                all_facts.append(fact.lower())
                words = fact.lower().split()
                topic_word_counts[topic].update(words)
        
        # Extract dominant themes
        all_words = []
        for fact in all_facts:
            all_words.extend(fact.split())
        
        word_freq = Counter(all_words)
        # Filter out common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        meaningful_words = {word: count for word, count in word_freq.items() 
                          if word not in common_words and len(word) > 2 and count > 1}
        
        compressed["dominant_themes"] = list(dict(Counter(meaningful_words).most_common(10)).keys())
        
        # Generate user profile insights
        user_interests = []
        tech_indicators = ['python', 'programming', 'code', 'software', 'computer', 'ai', 'machine', 'learning', 'robot', 'arduino', 'tech']
        academic_indicators = ['college', 'university', 'study', 'exam', 'course', 'degree', 'research', 'academic']
        creative_indicators = ['art', 'design', 'creative', 'music', 'writing', 'draw', 'paint']
        
        for fact in all_facts:
            if any(indicator in fact for indicator in tech_indicators):
                user_interests.append("technology")
            if any(indicator in fact for indicator in academic_indicators):
                user_interests.append("academics")
            if any(indicator in fact for indicator in creative_indicators):
                user_interests.append("creative")
        
        interest_counts = Counter(user_interests)
        compressed["user_profile"] = {
            "primary_interests": list(dict(interest_counts.most_common(3)).keys()),
            "interest_strength": dict(interest_counts),
            "total_interactions": len(all_facts)
        }
        
        # Categorize knowledge
        categories = {
            "technical": [],
            "personal": [],
            "educational": [],
            "preferences": [],
            "activities": []
        }
        
        for topic, fact_list in facts.items():
            if any(word in topic.lower() for word in ['web', 'wikipedia', 'tech', 'programming', 'code']):
                categories["technical"].extend(fact_list)
            elif any(word in topic.lower() for word in ['user', 'personal', 'identity']):
                categories["personal"].extend(fact_list)
            elif any(word in topic.lower() for word in ['college', 'exam', 'study', 'learn']):
                categories["educational"].extend(fact_list)
            elif any(word in topic.lower() for word in ['like', 'prefer', 'favorite']):
                categories["preferences"].extend(fact_list)
            else:
                categories["activities"].extend(fact_list)
        
        compressed["categories"] = {k: v for k, v in categories.items() if v}
        
        # Generate insights
        insights = []
        
        if len(all_facts) > 10:
            insights.append(f"User has shared {len(all_facts)} pieces of information across {len(facts)} topics")
        
        if compressed["user_profile"]["primary_interests"]:
            primary = compressed["user_profile"]["primary_interests"][0]
            insights.append(f"User shows strong interest in {primary}")
        
        if len(compressed["dominant_themes"]) > 0:
            top_theme = compressed["dominant_themes"][0]
            insights.append(f"Most frequently mentioned topic: {top_theme}")
        
        # Analyze knowledge growth
        if "last_updated" in knowledge:
            insights.append(f"Knowledge base last updated: {knowledge['last_updated']}")
        
        compressed["insights"] = insights
        
        # Compression statistics
        original_facts = sum(len(fact_list) for fact_list in facts.values())
        compressed_insights = len(insights)
        compression_ratio = compressed_insights / original_facts if original_facts > 0 else 0
        
        compressed["compression_stats"] = {
            "original_facts": original_facts,
            "compressed_insights": compressed_insights,
            "compression_ratio": round(compression_ratio, 3),
            "topics_analyzed": len(facts),
            "themes_identified": len(compressed["dominant_themes"])
        }
        
        # Save compressed knowledge
        with open("compressed_knowledge.json", "w") as f:
            json.dump(compressed, f, indent=4)
        
        # Auto-save compression info to knowledge base
        save_fact("knowledge_compression", f"Compressed {original_facts} facts into {compressed_insights} insights", confidence=1.0)
        
        result = "🧠 Knowledge Compression Complete!\n\n"
        result += f"📊 Compression Stats:\n"
        result += f"  • Original facts: {original_facts}\n"
        result += f"  • Compressed insights: {compressed_insights}\n"
        result += f"  • Compression ratio: {compression_ratio:.1%}\n"
        result += f"  • Topics analyzed: {len(facts)}\n\n"
        
        result += f"🎯 Key Insights:\n"
        for insight in insights[:5]:  # Show top 5 insights
            result += f"  • {insight}\n"
        
        if compressed["dominant_themes"]:
            result += f"\n🔍 Dominant Themes: {', '.join(compressed['dominant_themes'][:5])}\n"
        
        if compressed["user_profile"]["primary_interests"]:
            result += f"👤 User Profile: Interested in {', '.join(compressed['user_profile']['primary_interests'])}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error compressing knowledge: {str(e)}"

def analyze_knowledge_patterns():
    """Analyze patterns in the knowledge base"""
    try:
        import json
        from collections import Counter
        
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        facts = knowledge.get("facts", {})
        if not facts:
            return "📚 No knowledge to analyze yet."
        
        patterns = {
            "topic_frequency": {},
            "fact_length_distribution": {},
            "common_words": {},
            "topic_relationships": {},
            "knowledge_growth": {}
        }
        
        # Topic frequency analysis
        patterns["topic_frequency"] = {topic: len(fact_list) for topic, fact_list in facts.items()}
        
        # Fact length analysis
        all_facts = []
        for fact_list in facts.values():
            all_facts.extend(fact_list)
        
        fact_lengths = [len(fact.split()) for fact in all_facts]
        length_dist = Counter(fact_lengths)
        patterns["fact_length_distribution"] = dict(length_dist.most_common(10))
        
        # Common words analysis
        all_words = []
        for fact in all_facts:
            all_words.extend(fact.lower().split())
        
        word_freq = Counter(all_words)
        # Filter meaningful words
        meaningful_words = {word: count for word, count in word_freq.items() 
                          if len(word) > 3 and count > 1}
        patterns["common_words"] = dict(Counter(meaningful_words).most_common(15))
        
        # Knowledge growth analysis
        total_facts = len(all_facts)
        total_topics = len(facts)
        avg_facts_per_topic = total_facts / total_topics if total_topics > 0 else 0
        
        patterns["knowledge_growth"] = {
            "total_facts": total_facts,
            "total_topics": total_topics,
            "avg_facts_per_topic": round(avg_facts_per_topic, 2),
            "most_detailed_topic": max(patterns["topic_frequency"], key=patterns["topic_frequency"].get) if patterns["topic_frequency"] else None
        }
        
        result = "📊 Knowledge Pattern Analysis:\n\n"
        
        result += f"📈 Growth Metrics:\n"
        result += f"  • Total facts: {patterns['knowledge_growth']['total_facts']}\n"
        result += f"  • Total topics: {patterns['knowledge_growth']['total_topics']}\n"
        result += f"  • Average facts per topic: {patterns['knowledge_growth']['avg_facts_per_topic']}\n"
        if patterns['knowledge_growth']['most_detailed_topic']:
            result += f"  • Most detailed topic: {patterns['knowledge_growth']['most_detailed_topic']}\n"
        
        result += f"\n🔍 Topic Distribution:\n"
        for topic, count in sorted(patterns["topic_frequency"].items(), key=lambda x: x[1], reverse=True)[:5]:
            result += f"  • {topic}: {count} facts\n"
        
        result += f"\n💭 Common Themes:\n"
        for word, count in list(patterns["common_words"].items())[:8]:
            result += f"  • {word}: {count} mentions\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error analyzing patterns: {str(e)}"

def show_compressed_knowledge():
    """Show compressed knowledge insights"""
    try:
        import json
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
            return "📚 No compressed knowledge available. Run 'compress knowledge' first."
        
        result = "🧠 Compressed Knowledge Insights:\n\n"
        
        # Show compression stats
        stats = compressed.get("compression_stats", {})
        if stats:
            result += f"📊 Compression Statistics:\n"
            result += f"  • Original facts: {stats.get('original_facts', 0)}\n"
            result += f"  • Compressed insights: {stats.get('compressed_insights', 0)}\n"
            result += f"  • Compression ratio: {stats.get('compression_ratio', 0):.1%}\n"
            result += f"  • Topics analyzed: {stats.get('topics_analyzed', 0)}\n\n"
        
        # Show key insights
        insights = compressed.get("insights", [])
        if insights:
            result += f"💡 Key Insights:\n"
            for insight in insights:
                result += f"  • {insight}\n"
            result += "\n"
        
        # Show user profile
        profile = compressed.get("user_profile", {})
        if profile.get("primary_interests"):
            result += f"👤 User Profile:\n"
            result += f"  • Primary interests: {', '.join(profile['primary_interests'])}\n"
            result += f"  • Total interactions: {profile.get('total_interactions', 0)}\n\n"
        
        # Show dominant themes
        themes = compressed.get("dominant_themes", [])
        if themes:
            result += f"🎯 Dominant Themes: {', '.join(themes[:8])}\n\n"
        
        # Show categories
        categories = compressed.get("categories", {})
        if categories:
            result += f"📂 Knowledge Categories:\n"
            for category, facts in categories.items():
                if facts:
                    result += f"  • {category.title()}: {len(facts)} items\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error showing compressed knowledge: {str(e)}"

def generate_knowledge_summary():
    """Generate a comprehensive knowledge summary"""
    try:
        import json
        
        # Load both raw and compressed knowledge
        with open("knowledge.json", "r") as f:
            raw_knowledge = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
            # Generate compression if it doesn't exist
            compress_knowledge()
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        
        result = "📋 Comprehensive Knowledge Summary:\n\n"
        
        # Overview
        facts = raw_knowledge.get("facts", {})
        total_facts = sum(len(fact_list) for fact_list in facts.values())
        
        result += f"🔍 Overview:\n"
        result += f"  • Total knowledge items: {total_facts}\n"
        result += f"  • Knowledge topics: {len(facts)}\n"
        result += f"  • Last updated: {raw_knowledge.get('last_updated', 'Unknown')}\n\n"
        
        # User insights from compression
        profile = compressed.get("user_profile", {})
        if profile:
            result += f"👤 User Intelligence Profile:\n"
            if profile.get("primary_interests"):
                result += f"  • Core interests: {', '.join(profile['primary_interests'])}\n"
            result += f"  • Engagement level: {profile.get('total_interactions', 0)} interactions\n\n"
        
        # Key insights
        insights = compressed.get("insights", [])
        if insights:
            result += f"💡 Intelligence Insights:\n"
            for insight in insights[:3]:
                result += f"  • {insight}\n"
            result += "\n"
        
        # Dominant patterns
        themes = compressed.get("dominant_themes", [])
        if themes:
            result += f"🎯 Dominant Knowledge Patterns:\n"
            result += f"  • Primary themes: {', '.join(themes[:5])}\n\n"
        
        # Knowledge distribution
        categories = compressed.get("categories", {})
        if categories:
            result += f"📊 Knowledge Distribution:\n"
            for category, items in categories.items():
                if items:
                    percentage = (len(items) / total_facts) * 100 if total_facts > 0 else 0
                    result += f"  • {category.title()}: {len(items)} items ({percentage:.1f}%)\n"
        
        # Auto-save summary
        save_fact("knowledge_summary", f"Generated comprehensive summary of {total_facts} knowledge items", confidence=1.0)
        
        return result
        
    except Exception as e:
        return f"❌ Error generating knowledge summary: {str(e)}"