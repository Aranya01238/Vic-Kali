from tools import (
    echo,
    get_time,
    random_number,
    read_file,
    write_file,
    list_dir,
    open_target,
    open_folder,
    open_url,
    open_youtube,
    open_app,
    save_fact,
    query_facts,
    update_belief,
    wiki_search,
    web_search,
    get_system_stats,
    get_network_info,
    check_security,
    list_processes,
    search_files,
    get_file_metadata,
    verify_info,
    download_file,
    analyze_file,
    download_and_analyze,
    calculate,
    convert_units,
    date_math,
    logical_operation,
    show_tool_performance,
    reset_tool_performance,
    list_all_tools,
    search_tools,
    compress_knowledge,
    analyze_knowledge_patterns,
    show_compressed_knowledge,
    generate_knowledge_summary
)

# Import knowledge reasoning tools
from reasoning_tools import (
    form_opinion,
    make_prediction,
    give_advice,
    reason_about,
    synthesize_knowledge
)

# Import healthcare tools (Diya/Baymax features)
from healthcare_tools import (
    scan_vitals,
    diagnose_issue,
    first_aid_instruction,
    emotional_support_protocol,
    combat_mode,
    satisfaction_check
)

# Vision tools are imported lazily to avoid heavy dependencies like OpenCV
def _lazy_import_vision():
    import importlib
    return importlib.import_module('vision_tools')

def analyze_image(*args, **kwargs):
    return _lazy_import_vision().analyze_image(*args, **kwargs)

def detect_faces(*args, **kwargs):
    return _lazy_import_vision().detect_faces(*args, **kwargs)

def take_snapshot(*args, **kwargs):
    return _lazy_import_vision().take_snapshot(*args, **kwargs)

def get_edge_detection(*args, **kwargs):
    return _lazy_import_vision().get_edge_detection(*args, **kwargs)

# Import all advanced tools
from advanced_tools import ADVANCED_TOOLS

import time
import json

TOOLS = {
    "echo": echo,
    "time": get_time,
    "random": random_number,
    "read_file": read_file,
    "write_file": write_file,
    "list_dir": list_dir,
    "open_target": open_target,
    "open_folder": open_folder,
    "open_url": open_url,
    "open_youtube": open_youtube,
    "open_app": open_app,
    "save_fact": save_fact,
    "query_facts": query_facts,
    "update_belief": update_belief,
    "wiki_search": wiki_search,
    "web_search": web_search,
    "get_system_stats": get_system_stats,
    "get_network_info": get_network_info,
    "check_security": check_security,
    "list_processes": list_processes,
    "search_files": search_files,
    "get_file_metadata": get_file_metadata,
    "verify_info": verify_info,
    "download_file": download_file,
    "analyze_file": analyze_file,
    "download_and_analyze": download_and_analyze,
    "calculate": calculate,
    "convert_units": convert_units,
    "date_math": date_math,
    "logical_operation": logical_operation,
    "show_tool_performance": show_tool_performance,
    "reset_tool_performance": reset_tool_performance,
    "list_all_tools": list_all_tools,
    "search_tools": search_tools,
    "compress_knowledge": compress_knowledge,
    "analyze_knowledge_patterns": analyze_knowledge_patterns,
    "show_compressed_knowledge": show_compressed_knowledge,
    "generate_knowledge_summary": generate_knowledge_summary,
    "form_opinion": form_opinion,
    "make_prediction": make_prediction,
    "give_advice": give_advice,
    "reason_about": reason_about,
    "synthesize_knowledge": synthesize_knowledge,
    "scan_vitals": scan_vitals,
    "diagnose_issue": diagnose_issue,
    "first_aid_instruction": first_aid_instruction,
    "emotional_support_protocol": emotional_support_protocol,
    "combat_mode": combat_mode,
    "satisfaction_check": satisfaction_check,
    "analyze_image": analyze_image,
    "detect_faces": detect_faces,
    "take_snapshot": take_snapshot,
    "get_edge_detection": get_edge_detection
}

# Add all advanced tools
TOOLS.update(ADVANCED_TOOLS)

print(f"Total tools loaded: {len(TOOLS)}")

def update_tool_performance(tool_name, success, response_time):
    """Update tool performance metrics in memory"""
    try:
        with open("memory.json", "r") as f:
            memory = json.load(f)
        
        if "tool_performance" not in memory:
            memory["tool_performance"] = {}
        
        if tool_name not in memory["tool_performance"]:
            memory["tool_performance"][tool_name] = {
                "success": 0, "fail": 0, "avg_response_time": 0, "total_calls": 0
            }
        
        perf = memory["tool_performance"][tool_name]
        
        # Ensure all fields exist
        if "total_calls" not in perf:
            perf["total_calls"] = 0
        if "avg_response_time" not in perf:
            perf["avg_response_time"] = 0
        
        # Update success/fail counts
        if success:
            perf["success"] += 1
        else:
            perf["fail"] += 1
        
        # Update average response time
        perf["total_calls"] += 1
        perf["avg_response_time"] = (
            (perf["avg_response_time"] * (perf["total_calls"] - 1) + response_time) 
            / perf["total_calls"]
        )
        
        # Update tool preferences
        update_tool_preferences(memory)
        
        with open("memory.json", "w") as f:
            json.dump(memory, f, indent=4)
            
    except Exception as e:
        print(f"Error updating tool performance: {e}")

def update_tool_preferences(memory):
    """Update tool preferences based on performance"""
    tool_perf = memory.get("tool_performance", {})
    
    if not tool_perf:
        return
    
    # Initialize tool_preferences if not exists
    if "tool_preferences" not in memory:
        memory["tool_preferences"] = {
            "most_successful": None,
            "least_successful": None,
            "fastest": None,
            "slowest": None
        }
    
    # Calculate success rates
    success_rates = {}
    response_times = {}
    
    for tool, perf in tool_perf.items():
        total = perf["success"] + perf["fail"]
        if total > 0:
            success_rates[tool] = perf["success"] / total
            response_times[tool] = perf["avg_response_time"]
    
    if success_rates:
        # Most and least successful tools
        memory["tool_preferences"]["most_successful"] = max(success_rates, key=success_rates.get)
        memory["tool_preferences"]["least_successful"] = min(success_rates, key=success_rates.get)
    
    if response_times:
        # Fastest and slowest tools
        memory["tool_preferences"]["fastest"] = min(response_times, key=response_times.get)
        memory["tool_preferences"]["slowest"] = max(response_times, key=response_times.get)

def run_tool(name, **kwargs):
    if name not in TOOLS:
        return f"Tool '{name}' not found."
    
    start_time = time.time()
    success = True
    
    try:
        result = TOOLS[name](**kwargs)
        
        # Check if result indicates failure
        if isinstance(result, str) and ("❌" in result or "Error" in result):
            success = False
            
        return result
        
    except Exception as e:
        success = False
        return f"Tool error: {str(e)}"
        
    finally:
        # Always update performance metrics
        response_time = time.time() - start_time
        update_tool_performance(name, success, response_time)
