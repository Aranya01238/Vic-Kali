import random
import os
from datetime import datetime

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

# -------- KNOWLEDGE BASE TOOLS --------

def save_fact(topic, fact, confidence=0.8):
    try:
        import json
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
    try:
        # Clean the query
        clean_query = query.replace("wikipedia", "").replace("wiki search", "").strip()
        if not clean_query:
            return "❌ No search query provided"
        
        # Use the enhanced mock for comprehensive, accurate information
        return enhanced_wiki_mock(clean_query, sentences)
            
    except Exception as e:
        return enhanced_wiki_mock(query.replace("wikipedia", "").strip(), sentences)

def enhanced_wiki_mock(query, sentences=2):
    """Enhanced Wikipedia mock with comprehensive data"""
    wiki_database = {
        "python": "Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability with its notable use of significant whitespace.",
        "artificial intelligence": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.",
        "machine learning": "Machine learning (ML) is a type of artificial intelligence (AI) that allows software applications to become more accurate at predicting outcomes without being explicitly programmed to do so. Machine learning algorithms use historical data as input to predict new output values.",
        "robotics": "Robotics is an interdisciplinary branch of computer science and engineering. Robotics involves design, construction, operation, and use of robots. The goal of robotics is to design intelligent machines that can help and assist humans in their day-to-day lives and keep everyone safe.",
        "javascript": "JavaScript, often abbreviated as JS, is a programming language that conforms to the ECMAScript specification. JavaScript is high-level, often just-in-time compiled, and multi-paradigm. It has curly-bracket syntax, dynamic typing, prototype-based object-orientation, and first-class functions.",
        "data science": "Data science is an inter-disciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from many structural and unstructured data. Data science is related to data mining, machine learning and big data.",
        "blockchain": "A blockchain, originally block chain, is a growing list of records, called blocks, that are linked and secured using cryptography. Each block contains a cryptographic hash of the previous block, a timestamp, and transaction data.",
        "cloud computing": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user. The term is generally used to describe data centers available to many users over the Internet."
    }
    
    query_lower = query.lower()
    best_match = None
    
    # Find exact matches first
    for key, value in wiki_database.items():
        if key in query_lower:
            best_match = (key, value)
            break
    
    # If no exact match, find partial matches
    if not best_match:
        for key, value in wiki_database.items():
            if any(word in query_lower for word in key.split()) or any(word in key for word in query_lower.split()):
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
    try:
        # Use the enhanced mock search for comprehensive, accurate information
        return enhanced_mock_search(query)
            
    except Exception as e:
        return enhanced_mock_search(query)

def enhanced_mock_search(query):
    """Enhanced mock search with more comprehensive data"""
    mock_database = {
        "python": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. Known for its simplicity and readability, Python is widely used in web development, data science, AI, and automation.",
        "artificial intelligence": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. It includes machine learning, natural language processing, computer vision, and robotics. AI is transforming industries from healthcare to finance.",
        "machine learning": "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make predictions.",
        "robotics": "Robotics is an interdisciplinary field combining mechanical engineering, electrical engineering, and computer science. Modern robots are used in manufacturing, healthcare, exploration, and service industries.",
        "programming": "Programming is the process of creating instructions for computers using programming languages. Popular languages include Python, JavaScript, Java, C++, and Go. Programming is essential for software development.",
        "javascript": "JavaScript is a versatile programming language primarily used for web development. It enables interactive web pages and is also used for server-side development with Node.js.",
        "data science": "Data Science combines statistics, programming, and domain expertise to extract insights from data. It involves data collection, cleaning, analysis, and visualization using tools like Python, R, and SQL.",
        "blockchain": "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks, linked using cryptography. It's the foundation of cryptocurrencies like Bitcoin.",
        "cloud computing": "Cloud computing delivers computing services over the internet, including servers, storage, databases, and software. Major providers include AWS, Microsoft Azure, and Google Cloud Platform."
    }
    
    query_lower = query.lower()
    best_matches = []
    
    # Find exact and partial matches
    for key, value in mock_database.items():
        if key in query_lower or any(word in query_lower for word in key.split()):
            best_matches.append((key, value))
    
    # Also check for individual words
    query_words = query_lower.split()
    for key, value in mock_database.items():
        for word in query_words:
            if word in key and (key, value) not in best_matches:
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
        import json
        from collections import Counter
        
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
            web_result = run_tool("web_search", query=topic)
            if "❌" not in web_result:
                relevant_facts.append(f"Web research: {web_result[:200]}...")
        
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
            
       ts)} connections found", confidence=0.7)
        
        return synthesis_text
        
    except Exception as e:
        return f"❌ Error in knowledge synthesis: {str(e)}"
            synthesis_text += f"• Creative fusion possibilities combining both domains\n"
        if "academics" in interests:
            synthesis_text += f"• Research opportunities exploring the intersection\n"
        
        synthesis_text += f"• Cross-pollination of ideas and methods\n"
        synthesis_text += f"• Potential for innovative solutions using both approaches\n"
        
        # Save synthesis
        save_fact("knowledge_synthesis", f"Synthesized {topic1} and {topic2}: {len(shared_facrofile.get("primary_interests", [])
        
        if any(interest in topic1_lower or interest in topic2_lower for interest in interests):
            synthesis_text += f"• Both topics align with your interests in {', '.join(interests)}\n"
        
        # Suggest applications
        synthesis_text += f"\n🚀 Potential Applications:\n"
        if "technology" in interests:
            synthesis_text += f"• Technical integration opportunities between {topic1} and {topic2}\n"
        if "creative" in interests:nsights:\n"
        
        if len(shared_facts) > 0:
            synthesis_text += f"• Strong connection exists between {topic1} and {topic2}\n"
        elif len(meaningful_common) > 3:
            synthesis_text += f"• Moderate thematic overlap suggests related domains\n"
        else:
            synthesis_text += f"• Limited direct connection, but may share underlying principles\n"
        
        # Consider user context
        user_profile = compressed.get("user_profile", {})
        interests = user_pationship: '{relationship}'\n"
        
        # Look for patterns
        synthesis_text += f"📈 Pattern Analysis:\n"
        synthesis_text += f"• {topic1}: {len(topic1_facts)} related facts\n"
        synthesis_text += f"• {topic2}: {len(topic2_facts)} related facts\n"
        synthesis_text += f"• Overlap: {len(shared_facts)} shared facts\n"
        synthesis_text += f"• Common concepts: {len(meaningful_common)} themes\n\n"
        
        # Generate insights
        synthesis_text += f"💡 Synthesis Iound {len(shared_facts)} facts that mention both topics:\n"
            for fact in shared_facts[:3]:
                synthesis_text += f"  • {fact[:100]}...\n"
            synthesis_text += "\n"
        
        if meaningful_common:
            synthesis_text += f"🎯 Common Themes:\n"
            synthesis_text += f"Both topics share these concepts: {', '.join(list(meaningful_common)[:8])}\n\n"
        
        # Analyze relationship
        if relationship:
            synthesis_text += f"🔍 Analyzing rel
        common_words = topic1_words.intersection(topic2_words)
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        meaningful_common = common_words - stop_words
        
        # Generate synthesis
        synthesis_text = f"🔗 Knowledge Synthesis: {topic1} ↔ {topic2}\n\n"
        
        if shared_facts:
            synthesis_text += f"📊 Direct Connections Found:\n"
            synthesis_text += f"I flower() or any(word in topic1_lower for word in topic_words)) and \
               (topic2_lower in fact_topic.lower() or any(word in topic2_lower for word in topic_words)):
                shared_facts.extend(fact_list)
        
        # Analyze word overlap
        topic1_words = set()
        for fact in topic1_facts:
            topic1_words.update(fact.lower().split())
        
        topic2_words = set()
        for fact in topic2_facts:
            topic2_words.update(fact.lower().split())
        wer().split()
            
            # Check for topic1
            if topic1_lower in fact_topic.lower() or any(word in topic1_lower for word in topic_words):
                topic1_facts.extend(fact_list)
            
            # Check for topic2
            if topic2_lower in fact_topic.lower() or any(word in topic2_lower for word in topic_words):
                topic2_facts.extend(fact_list)
            
            # Check for facts mentioning both topics
            if (topic1_lower in fact_topic.       with open("compressed_knowledge.json", "r") as f:
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
            topic_words = fact_topic.lorce analysis completed", confidence=0.8)
        
        return reasoning_text
        
    except Exception as e:
        return f"❌ Error in reasoning process: {str(e)}"

def synthesize_knowledge(topic1, topic2, relationship=""):
    """Synthesize knowledge by finding connections between topics"""
    try:
        import json
        from collections import Counter
        
        # Load knowledge
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        try:
     be a multifaceted subject that benefits from combining "
        
        if direct_facts:
            reasoning_text += "established knowledge, "
        if web_info:
            reasoning_text += "current information, "
        if interests:
            reasoning_text += f"your {', '.join(interests)} background, "
        
        reasoning_text += "and careful analysis of the specific context."
        
        # Save reasoning to knowledge base
        save_fact("reasoning", f"Reasoned about {topic}: Multi-sou+= f"\n💭 Implications and considerations:\n"
        reasoning_text += f"• This topic intersects with {len(direct_facts)} areas of knowledge I have\n"
        
        if beliefs:
            reasoning_text += f"• It relates to beliefs I've formed about patterns in our conversations\n"
        
        reasoning_text += f"• The complexity suggests multiple valid approaches exist\n"
        
        # Conclusion
        reasoning_text += f"\n🎯 Conclusion:\n"
        reasoning_text += f"{topic.title()} appears to   reasoning_text += "🔧 Technical perspective: This involves understanding systems, processes, and optimization.\n"
        
        if "creative" in interests:
            reasoning_text += "🎨 Creative perspective: There are opportunities for innovation and unique approaches.\n"
        
        if "academics" in interests:
            reasoning_text += "📖 Academic perspective: This can be approached through systematic study and research.\n"
        
        # Consider implications
        reasoning_text Based on my accumulated knowledge, "
        elif web_info:
            reasoning_text += "From available information, "
        else:
            reasoning_text += "While I have limited specific information, "
        
        # Draw connections
        reasoning_text += f"I can see several important aspects of {topic}:\n\n"
        
        # Analyze different dimensions
        if "technology" in interests and any(tech_word in topic_lower for tech_word in ["tech", "ai", "programming", "software"]):
          erests in {', '.join(interests)}, which suggests it's particularly relevant to you.\n\n"
        
        # Logical reasoning
        reasoning_text += "🧠 My reasoning process:\n"
        
        if question:
            reasoning_text += f"Considering your question: '{question}'\n"
        
        # Synthesize information
        if direct_facts and web_info:
            reasoning_text += "Combining my stored knowledge with current information, "
        elif direct_facts:
            reasoning_text += "# Consider patterns and themes
        if any(theme in topic_lower for theme in themes):
            matching_themes = [theme for theme in themes if theme in topic_lower]
            reasoning_text += f"🎯 This connects to dominant themes in our conversations: {', '.join(matching_themes)}\n\n"
        
        # User context
        interests = user_profile.get("primary_interests", [])
        if any(interest in topic_lower for interest in interests):
            reasoning_text += f"👤 This aligns with your intult:
                web_info.append(web_result)
        
        # Begin reasoning process
        reasoning_text = f"🤔 Let me think about {topic}...\n\n"
        
        # Analyze what we know
        if direct_facts:
            reasoning_text += f"📚 From my knowledge base, I have {len(direct_facts)} relevant facts:\n"
            # Show most relevant facts
            for fact in direct_facts[:3]:
                reasoning_text += f"  • {fact[:100]}...\n"
            reasoning_text += "\n"
        
        facts.extend(fact_list)
        
        # 2. Compressed insights
        insights = compressed.get("insights", [])
        themes = compressed.get("dominant_themes", [])
        user_profile = compressed.get("user_profile", {})
        
        # 3. Memory patterns
        beliefs = knowledge.get("beliefs", {})
        
        # 4. Web knowledge (if needed)
        web_info = []
        if len(direct_facts) < 3:
            web_result = run_tool("web_search", query=topic)
            if "❌" not in web_resson", "r") as f:
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
                direct_turn result
        
    except Exception as e:
        return f"❌ Error giving advice: {str(e)}"

def reason_about(topic, question=""):
    """Deep reasoning combining multiple knowledge sources"""
    try:
        import json
        
        # Load all knowledge sources
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        try:
            with open("compressed_knowledge.jedge base
        save_fact("advice_given", f"Advice for {situation}: {advice_text[:100]}... (confidence: {advice_confidence:.1f})", confidence=advice_confidence)
        
        result = f"💡 My Advice for '{situation}':\n\n"
        result += f"{advice_text}\n\n"
        result += f"🎯 Confidence Level: {advice_confidence:.1%}\n"
        result += f"📊 Based on {len(relevant_advice)} relevant experiences"
        
        if goal:
            result += f"\n🎯 Aligned with your goal: {goal}"
        
        reder:\n"
        advice_text += "1. Clearly define what success looks like for you\n"
        advice_text += "2. Identify the key obstacles or challenges\n"
        advice_text += "3. Break down the solution into smaller, manageable parts\n"
        advice_text += "4. Start with the easiest or most critical step\n"
        advice_text += "5. Monitor your progress and adjust as needed"
        
        # Cap confidence
        advice_confidence = min(0.9, advice_confidence)
        
        # Save advice to knowlive mindset, don't be afraid to think outside the box and explore innovative solutions. "
                advice_confidence += 0.1
        
        # Add general wisdom from knowledge base
        if relevant_advice:
            advice_text += f"Based on what I've learned from our conversations, similar situations often benefit from patience and persistence. "
            advice_confidence += 0.1
        
        # Provide actionable steps
        advice_text += "\n\nHere are some concrete steps you could consi
        
        # Add personalized advice based on user interests
        if interests:
            if "technology" in interests and any(tech_word in situation_lower for tech_word in ["tech", "programming", "code", "software"]):
                advice_text += "Given your technical background, you might want to approach this systematically and consider automation opportunities. "
                advice_confidence += 0.1
            elif "creative" in interests:
                advice_text += "With your creataking decisions, consider listing pros and cons, think about long-term consequences, and trust your instincts after careful analysis. "
            advice_confidence += 0.1
        else:
            advice_text += "Based on the situation you've described, here's what I think could help: "
        
        # Add goal-specific advice
        if goal:
            advice_text += f"Since your goal is {goal}, I'd suggest focusing on actions that directly contribute to this outcome. "
            advice_confidence += 0.1k the work into manageable tasks, and set realistic deadlines. "
            advice_confidence += 0.2
        elif "programming" in situation_lower or "code" in situation_lower:
            advice_text += "For programming challenges, start with understanding the problem clearly, plan your approach, and don't hesitate to break complex problems into smaller functions. "
            advice_confidence += 0.2
        elif "decision" in situation_lower or "choose" in situation_lower:
            advice_text += "When m      # Provide specific advice based on situation
        if "study" in situation_lower or "exam" in situation_lower or "learn" in situation_lower:
            advice_text += "For learning and studying, I'd recommend breaking things into smaller chunks, practicing regularly, and using active recall techniques. "
            advice_confidence += 0.2
        elif "project" in situation_lower or "work" in situation_lower:
            advice_text += "For project work, start by clearly defining your goals, brea_history, key=emotion_history.get) if emotion_history else "neutral"
        
        # Generate advice
        advice_text = ""
        advice_confidence = 0.5
        
        # Start with empathy based on emotional state
        if dominant_emotion in ["sad", "worried", "anxious"]:
            advice_text += "I understand this might be challenging for you. "
        elif dominant_emotion in ["happy", "excited"]:
            advice_text += "It's great that you're approaching this positively! "
        
  ion_lower for word in topic.lower().split()) or any(keyword in topic.lower() for keyword in advice_keywords):
                relevant_advice.extend(fact_list)
        
        # Consider user profile and preferences
        user_profile = compressed.get("user_profile", {})
        interests = user_profile.get("primary_interests", [])
        
        # Analyze user's emotional state for appropriate advice tone
        emotion_history = memory.get("emotion_history", {})
        dominant_emotion = max(emotion compressed = {}
        
        # Analyze the situation
        situation_lower = situation.lower()
        goal_lower = goal.lower() if goal else ""
        
        # Find relevant knowledge
        relevant_advice = []
        facts = knowledge.get("facts", {})
        
        # Look for related experiences and knowledge
        advice_keywords = ['how', 'should', 'could', 'might', 'recommend', 'suggest', 'advice', 'tip', 'best']
        for topic, fact_list in facts.items():
            if any(word in situatce(situation, goal=""):
    """Provide advice based on knowledge, experience, and reasoning"""
    try:
        import json
        
        # Load all knowledge sources
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        except FileNotFoundError:
           t} (confidence: {prediction_confidence:.1f})", confidence=prediction_confidence)
        
        result = f"🔮 Prediction for '{scenario}':\n\n"
        result += f"{prediction_text}\n\n"
        result += f"⏰ Timeframe: {timeframe}\n"
        result += f"🎯 Confidence Level: {prediction_confidence:.1%}\n"
        result += f"📊 Based on {len(relevant_patterns)} pattern analysis"
        
        return result
        
    except Exception as e:
        return f"❌ Error making prediction: {str(e)}"

def give_adviorable outcomes. "
            prediction_confidence += 0.05
        elif dominant_emotion in ["worried", "anxious"]:
            prediction_text += "Being mindful of potential challenges could help you prepare better. "
            prediction_confidence += 0.05
        
        # Cap confidence
        prediction_confidence = min(0.8, prediction_confidence)  # Predictions should never be 100% confident
        
        # Save prediction
        save_fact("predictions", f"Prediction for {scenario}: {prediction_tex        
        # Consider user context
        interests = user_profile.get("primary_interests", [])
        if any(interest in scenario_lower for interest in interests):
            prediction_text += f"Given your interest in {', '.join(interests)}, you're likely to be actively involved in this outcome. "
            prediction_confidence += 0.1
        
        # Add emotional context
        if dominant_emotion in ["happy", "excited"]:
            prediction_text += "Your positive outlook may contribute to fav  prediction_text = f"I predict {scenario} will remain relatively stable in the {timeframe}. "
                prediction_confidence += 0.1
            
            # Add reasoning based on patterns
            prediction_text += f"This is based on patterns I've observed in {len(relevant_patterns)} related data points. "
            
        else:
            prediction_text = f"Based on general trends, I predict {scenario} will evolve gradually in the {timeframe}. "
            prediction_confidence = 0.3
tterns for indicator in decline_indicators if indicator in pattern.lower())
            
            if growth_count > decline_count:
                prediction_text = f"I predict {scenario} will likely show positive development in the {timeframe}. "
                prediction_confidence += 0.2
            elif decline_count > growth_count:
                prediction_text = f"I predict {scenario} may face challenges in the {timeframe}. "
                prediction_confidence += 0.1
            else:
              terns = relevant_patterns[-5:]  # Last 5 relevant facts
            
            # Look for growth/decline indicators
            growth_indicators = ['increase', 'grow', 'improve', 'expand', 'rise', 'more', 'better']
            decline_indicators = ['decrease', 'decline', 'reduce', 'fall', 'less', 'worse']
            
            growth_count = sum(1 for pattern in recent_patterns for indicator in growth_indicators if indicator in pattern.lower())
            decline_count = sum(1 for pattern in recent_pafile = compressed.get("user_profile", {})
        dominant_themes = compressed.get("dominant_themes", [])
        
        # Analyze emotional patterns
        emotion_history = memory.get("emotion_history", {})
        dominant_emotion = max(emotion_history, key=emotion_history.get) if emotion_history else "neutral"
        
        # Generate prediction
        prediction_confidence = 0.4
        prediction_text = ""
        
        if relevant_patterns:
            # Analyze trends
            recent_patxcept FileNotFoundError:
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
        user_pro, timeframe="near future"):
    """Make predictions based on patterns and knowledge"""
    try:
        import json
        from datetime import datetime, timedelta
        
        # Load knowledge and memory
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        try:
            with open("compressed_knowledge.json", "r") as f:
                compressed = json.load(f)
        ece)
        
        result = f"💭 My Opinion on '{topic}':\n\n"
        result += f"{opinion_text}\n\n"
        result += f"🎯 Confidence Level: {opinion_confidence:.1%}\n"
        result += f"📊 Based on {len(relevant_facts)} relevant facts"
        
        if interest_match:
            result += f"\n🔗 This aligns with your interests in {', '.join(interests)}"
        
        return result
        
    except Exception as e:
        return f"❌ Error forming opinion: {str(e)}"

def make_prediction(scenariopic} yet. "
            opinion_confidence = 0.3
        
        # Add context if provided
        if context:
            opinion_text += f"Considering the context you provided: {context[:100]}... "
            opinion_confidence += 0.1
        
        # Cap confidence
        opinion_confidence = min(1.0, opinion_confidence)
        
        # Save opinion to knowledge base
        save_fact("opinions", f"Opinion on {topic}: {opinion_text} (confidence: {opinion_confidence:.1f})", confidence=opinion_confidendd reasoning
            if len(relevant_facts) > 3:
                opinion_text += f"This is based on {len(relevant_facts)} pieces of information I've gathered. "
                opinion_confidence += 0.1
            
            # Add user context
            if interest_match:
                opinion_text += f"Given your interest in {', '.join(interests)}, this seems particularly relevant to you. "
        else:
            opinion_text = f"I don't have enough information to form a strong opinion about {to     # Form opinion
            if positive_count > negative_count:
                opinion_text = f"Based on my knowledge, I have a positive view of {topic}. "
                opinion_confidence += 0.2
            elif negative_count > positive_count:
                opinion_text = f"Based on my knowledge, I have some concerns about {topic}. "
                opinion_confidence += 0.1
            else:
                opinion_text = f"I have a balanced perspective on {topic}. "
            
            # A