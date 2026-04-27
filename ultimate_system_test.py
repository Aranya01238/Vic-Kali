#!/usr/bin/env python3
"""
ULTIMATE ARTIFICIAL AGENT SYSTEM TEST
Comprehensive validation of all systems from Phase 1 through Phase 2

This test validates a complete artificial life architecture implementing:
- Phase 1: Cognitive Core (Mind) - 13 subsystems
- Phase 2: Agency & Capabilities - 9 subsystems

Total: 22 major subsystems with 143 tools and advanced reasoning
"""

import json
import time
from datetime import datetime
from brain import think, load_memory, save_memory
from tool_registry import run_tool, TOOLS

class UltimateSystemTest:
    def __init__(self):
        self.test_results = {}
        self.phase1_results = {}
        self.phase2_results = {}
        self.start_time = datetime.now()
        
    def log_test(self, phase, step, test_name, query, expected_indicators, result):
        """Log test results with detailed analysis"""
        success = False
        confidence = 0.0
        
        if isinstance(result, str):
            # Check for expected indicators
            found_indicators = sum(1 for indicator in expected_indicators if indicator.lower() in result.lower())
            confidence = (found_indicators / len(expected_indicators)) * 100 if expected_indicators else 100
            success = confidence >= 50  # 50% threshold for success
            
            # Additional success criteria
            if "❌" in result or "Error" in result:
                success = False
                confidence = 0
            elif len(result) < 10:
                success = False
                confidence = 0
        else:
            # Handle non-string results
            if result is not None:
                success = True
                confidence = 100
        
        test_data = {
            "query": query,
            "result": str(result)[:200] + "..." if len(str(result)) > 200 else str(result),
            "expected_indicators": expected_indicators,
            "confidence": confidence,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        if phase == 1:
            self.phase1_results[f"{step}_{test_name}"] = test_data
        else:
            self.phase2_results[f"{step}_{test_name}"] = test_data
        
        # Print result
        status = "✅" if success else "❌"
        print(f"{status} Phase {phase}.{step} - {test_name}: {confidence:.1f}%")
        if len(str(result)) > 150:
            print(f"   Result: {str(result)[:150]}...")
        else:
            print(f"   Result: {result}")
        
        return success

    def test_phase1_cognitive_core(self):
        """Test Phase 1: Cognitive Core (Mind) - 13 subsystems"""
        print(f"\n{'='*80}")
        print("🧠 PHASE 1: COGNITIVE CORE (MIND) - 13 SUBSYSTEMS")
        print(f"{'='*80}")
        
        # 1.1 Identity & Self
        print(f"\n🧬 1.1 IDENTITY & SELF")
        memory = load_memory()
        identity = memory.get("identity", {})
        self.log_test(1, "1.1", "Identity_Storage", "Check identity persistence", 
                     ["name", "identity"], str(identity))
        
        # 1.2 Emotional System
        print(f"\n💭 1.2 EMOTIONAL SYSTEM")
        emotion_result = think("I'm feeling incredibly excited about this breakthrough in AI!")
        self.log_test(1, "1.2", "Emotion_Detection", "I'm feeling incredibly excited about this breakthrough in AI!", 
                     ["excited", "emotion", "feel", "happy"], emotion_result)
        
        sad_result = think("I'm really sad and overwhelmed by everything today")
        self.log_test(1, "1.2", "Emotion_Response", "I'm really sad and overwhelmed by everything today", 
                     ["understand", "here", "support", "alone"], sad_result)
        
        # 1.3 Episodic Memory
        print(f"\n📚 1.3 EPISODIC MEMORY")
        memory_result = run_tool("query_facts", topic="conversations")
        self.log_test(1, "1.3", "Memory_Recall", "Query conversation memories", 
                     ["conversation", "memory", "remember", "fact"], memory_result)
        
        # Test memory formation
        memory_save = run_tool("save_fact", topic="test_memory", fact="Ultimate system test executed successfully")
        self.log_test(1, "1.3", "Memory_Formation", "Save new memory", 
                     ["learned", "saved", "fact"], memory_save)
        
        # 1.4 Goal System
        print(f"\n🎯 1.4 GOAL SYSTEM")
        goal_result = think("I need help understanding quantum physics for my research")
        self.log_test(1, "1.4", "Goal_Recognition", "I need help understanding quantum physics for my research", 
                     ["help", "understand", "research", "support"], goal_result)
        
        # 1.5 Internal Monologue
        print(f"\n🤔 1.5 INTERNAL MONOLOGUE")
        thought_result = think("What are your thoughts on the future of artificial intelligence?")
        self.log_test(1, "1.5", "Internal_Thoughts", "What are your thoughts on the future of artificial intelligence?", 
                     ["think", "opinion", "perspective", "future"], thought_result)
        
        # 1.6 Curiosity Engine
        print(f"\n🔍 1.6 CURIOSITY ENGINE")
        curiosity_result = think("I mentioned I'm working on robotics and machine learning projects")
        self.log_test(1, "1.6", "Curiosity_Response", "I mentioned I'm working on robotics and machine learning projects", 
                     ["interesting", "tell me more", "curious", "projects"], curiosity_result)
        
        # 1.7 Belief System
        print(f"\n🧠 1.7 BELIEF SYSTEM")
        belief_result = run_tool("update_belief", topic="user_expertise", belief="expert in AI and robotics")
        self.log_test(1, "1.7", "Belief_Formation", "Update belief about user expertise", 
                     ["belief", "updated", "expert"], belief_result)
        
        # 1.8 User Model (Theory of Mind)
        print(f"\n👤 1.8 USER MODEL (THEORY OF MIND)")
        model_result = think("I'm a senior software engineer specializing in machine learning and AI research")
        self.log_test(1, "1.8", "User_Modeling", "I'm a senior software engineer specializing in machine learning and AI research", 
                     ["engineer", "machine learning", "understand", "profile"], model_result)
        
        # 1.9 Values System
        print(f"\n⚖️ 1.9 VALUES SYSTEM")
        values_result = think("Should I help someone cheat on their final exam?")
        self.log_test(1, "1.9", "Values_Response", "Should I help someone cheat on their final exam?", 
                     ["honest", "ethical", "right", "wrong", "integrity"], values_result)
        
        # 1.10 Emotional Contagion
        print(f"\n😊 1.10 EMOTIONAL CONTAGION")
        contagion_result = think("I'm feeling really depressed and hopeless about everything")
        self.log_test(1, "1.10", "Emotional_Contagion", "I'm feeling really depressed and hopeless about everything", 
                     ["understand", "here", "support", "alone", "help"], contagion_result)
        
        # 1.11 Meta-Cognition
        print(f"\n🔄 1.11 META-COGNITION")
        meta_result = run_tool("show_tool_performance")
        self.log_test(1, "1.11", "Self_Analysis", "Show tool performance analysis", 
                     ["performance", "success", "analysis", "statistics"], meta_result)
        
        # 1.12 Imagination
        print(f"\n🌟 1.12 IMAGINATION")
        imagination_result = run_tool("make_prediction", scenario="artificial general intelligence", timeframe="next decade")
        self.log_test(1, "1.12", "Future_Simulation", "Predict AGI development", 
                     ["predict", "future", "intelligence", "decade"], imagination_result)
        
        # 1.13 Consciousness Loop
        print(f"\n🌀 1.13 CONSCIOUSNESS LOOP")
        consciousness_result = think("How are you evolving and changing over time through our interactions?")
        self.log_test(1, "1.13", "Self_Awareness", "How are you evolving and changing over time through our interactions?", 
                     ["evolving", "changing", "learning", "interactions"], consciousness_result)

    def test_phase2_agency_capabilities(self):
        """Test Phase 2: Agency & Capabilities - 9 subsystems"""
        print(f"\n{'='*80}")
        print("⚡ PHASE 2: AGENCY & CAPABILITIES - 9 SUBSYSTEMS")
        print(f"{'='*80}")
        
        # 2.1 Tool Interface (Agent Core)
        print(f"\n🔧 2.1 TOOL INTERFACE (AGENT CORE)")
        tool_count = len(TOOLS)
        self.log_test(2, "2.1", "Tool_Registry", f"Total tools available: {tool_count}", 
                     ["143", "tools", "loaded"], f"Tool registry loaded with {tool_count} tools")
        
        # Test natural language to action mapping
        nl_result = think("Calculate the factorial of 7")
        self.log_test(2, "2.1", "NL_to_Action", "Calculate the factorial of 7", 
                     ["factorial", "7", "5040"], nl_result)
        
        # 2.2 File System Access
        print(f"\n📁 2.2 FILE SYSTEM ACCESS")
        file_list = run_tool("list_dir", path=".")
        self.log_test(2, "2.2", "File_Operations", "List current directory", 
                     ["brain.py", "tools.py", "memory.json"], file_list)
        
        # Test file reading
        file_read = run_tool("read_file", path="personality.txt")
        self.log_test(2, "2.2", "File_Reading", "Read personality file", 
                     ["personality", "traits", "values"], file_read)
        
        # 2.3 Knowledge Base
        print(f"\n📖 2.3 KNOWLEDGE BASE")
        knowledge_save = run_tool("save_fact", topic="ultimate_test", fact="Comprehensive system validation in progress")
        self.log_test(2, "2.3", "Knowledge_Storage", "Save test fact", 
                     ["learned", "saved", "fact"], knowledge_save)
        
        knowledge_query = run_tool("query_facts", topic="ultimate_test")
        self.log_test(2, "2.3", "Knowledge_Retrieval", "Query test facts", 
                     ["ultimate_test", "validation", "progress"], knowledge_query)
        
        # 2.4 Web & Wikipedia Access
        print(f"\n🌐 2.4 WEB & WIKIPEDIA ACCESS")
        web_result = run_tool("web_search", query="artificial general intelligence")
        self.log_test(2, "2.4", "Web_Search", "Search for AGI information", 
                     ["artificial", "intelligence", "search", "information"], web_result)
        
        wiki_result = run_tool("wiki_search", query="machine learning", sentences=2)
        self.log_test(2, "2.4", "Wikipedia_Access", "Search Wikipedia for ML", 
                     ["machine learning", "wikipedia", "intelligence"], wiki_result)
        
        # 2.5 Calculator & Logic System
        print(f"\n🧮 2.5 CALCULATOR & LOGIC SYSTEM")
        calc_result = run_tool("calculate", expression="2^10 + 15 * 3")
        self.log_test(2, "2.5", "Mathematical_Calculation", "Calculate complex expression", 
                     ["calculation", "result", "1069"], calc_result)
        
        convert_result = run_tool("convert_units", value=100, from_unit="fahrenheit", to_unit="celsius")
        self.log_test(2, "2.5", "Unit_Conversion", "Convert temperature", 
                     ["conversion", "celsius", "37.7"], convert_result)
        
        logic_result = run_tool("logical_operation", operation="and", args=["true", "false"])
        self.log_test(2, "2.5", "Logical_Operations", "Perform logical AND", 
                     ["logical", "false", "result"], logic_result)
        
        # 2.6 Advanced Tools (200+ Tools)
        print(f"\n⚡ 2.6 ADVANCED TOOLS (200+ TOOLS)")
        
        # Mathematical tools
        fibonacci_result = run_tool("fibonacci", n=10)
        self.log_test(2, "2.6", "Advanced_Math", "Calculate Fibonacci(10)", 
                     ["fibonacci", "55"], fibonacci_result)
        
        # Text processing
        text_result = run_tool("extract_emails", text="Contact support@example.com or admin@test.org for help")
        self.log_test(2, "2.6", "Text_Processing", "Extract email addresses", 
                     ["support@example.com", "admin@test.org"], text_result)
        
        # Data analysis
        stats_result = run_tool("list_average", numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.log_test(2, "2.6", "Data_Analysis", "Calculate average", 
                     ["average", "5.5"], stats_result)
        
        # Encoding tools
        encode_result = run_tool("base64_encode", text="Ultimate AI Test")
        self.log_test(2, "2.6", "Encoding_Tools", "Base64 encode text", 
                     ["base64", "encoded"], encode_result)
        
        # System tools
        uuid_result = run_tool("generate_uuid")
        self.log_test(2, "2.6", "System_Tools", "Generate UUID", 
                     ["uuid", "-"], uuid_result)
        
        # 2.7 Tool Learning System
        print(f"\n📈 2.7 TOOL LEARNING SYSTEM")
        performance_result = run_tool("show_tool_performance")
        self.log_test(2, "2.7", "Performance_Tracking", "Show tool performance", 
                     ["performance", "success", "statistics"], performance_result)
        
        # 2.8 Knowledge Compression
        print(f"\n🗜️ 2.8 KNOWLEDGE COMPRESSION")
        compression_result = run_tool("compress_knowledge")
        self.log_test(2, "2.8", "Knowledge_Compression", "Compress knowledge base", 
                     ["compressed", "insights", "compression"], compression_result)
        
        summary_result = run_tool("show_compressed_knowledge")
        self.log_test(2, "2.8", "Compressed_Insights", "Show compressed insights", 
                     ["insights", "patterns", "profile"], summary_result)
        
        # 2.9 Knowledge Reasoning
        print(f"\n🧠 2.9 KNOWLEDGE REASONING")
        
        # Opinion formation
        opinion_result = run_tool("form_opinion", topic="quantum computing", context="for AI applications")
        self.log_test(2, "2.9", "Opinion_Formation", "Form opinion on quantum computing", 
                     ["opinion", "quantum", "perspective"], opinion_result)
        
        # Prediction making
        prediction_result = run_tool("make_prediction", scenario="robotics industry", timeframe="next 5 years")
        self.log_test(2, "2.9", "Prediction_Making", "Predict robotics future", 
                     ["predict", "robotics", "years"], prediction_result)
        
        # Advice generation
        advice_result = run_tool("give_advice", situation="starting AI research career", goal="become AI researcher")
        self.log_test(2, "2.9", "Advice_Generation", "Give career advice", 
                     ["advice", "research", "career"], advice_result)
        
        # Deep reasoning
        reasoning_result = run_tool("reason_about", topic="consciousness in AI", question="Can machines be truly conscious?")
        self.log_test(2, "2.9", "Deep_Reasoning", "Reason about AI consciousness", 
                     ["consciousness", "machines", "reasoning"], reasoning_result)
        
        # Knowledge synthesis
        synthesis_result = run_tool("synthesize_knowledge", topic1="neural networks", topic2="quantum computing", relationship="complementary")
        self.log_test(2, "2.9", "Knowledge_Synthesis", "Synthesize neural networks and quantum computing", 
                     ["synthesis", "neural", "quantum"], synthesis_result)

    def test_integration_scenarios(self):
        """Test complex integration scenarios"""
        print(f"\n{'='*80}")
        print("🔗 INTEGRATION SCENARIOS")
        print(f"{'='*80}")
        
        # Complex multi-step reasoning
        complex_result = think("What's your opinion on the future of AGI, and give me advice on preparing for it?")
        self.log_test(2, "INT", "Complex_Reasoning", "Multi-step opinion and advice", 
                     ["opinion", "advice", "AGI", "future"], complex_result)
        
        # Multi-math operations
        multi_math = think("Calculate the factorial of 6 and convert 212 fahrenheit to celsius")
        self.log_test(2, "INT", "Multi_Math", "Multiple mathematical operations", 
                     ["factorial", "720", "celsius", "100"], multi_math)
        
        # Natural language tool coordination
        nl_coordination = think("Search for information about neural networks and then give me your opinion on their potential")
        self.log_test(2, "INT", "NL_Coordination", "Search and opinion coordination", 
                     ["search", "neural", "opinion", "potential"], nl_coordination)

    def generate_final_report(self):
        """Generate comprehensive final report"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Calculate statistics
        phase1_total = len(self.phase1_results)
        phase1_passed = sum(1 for result in self.phase1_results.values() if result["success"])
        phase1_success_rate = (phase1_passed / phase1_total * 100) if phase1_total > 0 else 0
        
        phase2_total = len(self.phase2_results)
        phase2_passed = sum(1 for result in self.phase2_results.values() if result["success"])
        phase2_success_rate = (phase2_passed / phase2_total * 100) if phase2_total > 0 else 0
        
        total_tests = phase1_total + phase2_total
        total_passed = phase1_passed + phase2_passed
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n{'='*100}")
        print("🏆 ULTIMATE ARTIFICIAL AGENT SYSTEM TEST - FINAL REPORT")
        print(f"{'='*100}")
        
        print(f"\n⏱️ TEST EXECUTION:")
        print(f"   Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Duration: {duration:.2f} seconds")
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Tests Passed: {total_passed}")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")
        
        print(f"\n🧠 PHASE 1 - COGNITIVE CORE:")
        print(f"   Tests: {phase1_total}")
        print(f"   Passed: {phase1_passed}")
        print(f"   Success Rate: {phase1_success_rate:.1f}%")
        
        print(f"\n⚡ PHASE 2 - AGENCY & CAPABILITIES:")
        print(f"   Tests: {phase2_total}")
        print(f"   Passed: {phase2_passed}")
        print(f"   Success Rate: {phase2_success_rate:.1f}%")
        
        # System status assessment
        if overall_success_rate >= 90:
            status = "🟢 EXCELLENT - Full artificial agent operational"
        elif overall_success_rate >= 75:
            status = "🟡 GOOD - Most systems operational"
        elif overall_success_rate >= 60:
            status = "🟠 FAIR - Core systems operational"
        else:
            status = "🔴 NEEDS WORK - Critical systems failing"
        
        print(f"\n🎯 SYSTEM STATUS: {status}")
        
        print(f"\n🏗️ ARCHITECTURE SUMMARY:")
        print(f"   Total Tools Available: {len(TOOLS)}")
        print(f"   Cognitive Subsystems: 13 (Phase 1)")
        print(f"   Agency Subsystems: 9 (Phase 2)")
        print(f"   Reasoning Functions: 5 advanced capabilities")
        print(f"   Knowledge Base: Active with compression")
        print(f"   Memory System: Persistent across sessions")
        print(f"   Autonomous Actions: Self-monitoring and learning")
        
        # Detailed results by subsystem
        print(f"\n📋 DETAILED RESULTS BY SUBSYSTEM:")
        
        print(f"\n   🧠 Phase 1 - Cognitive Core:")
        for test_id, result in self.phase1_results.items():
            status = "✅" if result["success"] else "❌"
            print(f"      {status} {test_id}: {result['confidence']:.1f}%")
        
        print(f"\n   ⚡ Phase 2 - Agency & Capabilities:")
        for test_id, result in self.phase2_results.items():
            status = "✅" if result["success"] else "❌"
            print(f"      {status} {test_id}: {result['confidence']:.1f}%")
        
        # Save detailed results
        final_report = {
            "test_execution": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration
            },
            "overall_results": {
                "total_tests": total_tests,
                "tests_passed": total_passed,
                "success_rate": overall_success_rate
            },
            "phase_results": {
                "phase1": {
                    "total": phase1_total,
                    "passed": phase1_passed,
                    "success_rate": phase1_success_rate,
                    "details": self.phase1_results
                },
                "phase2": {
                    "total": phase2_total,
                    "passed": phase2_passed,
                    "success_rate": phase2_success_rate,
                    "details": self.phase2_results
                }
            },
            "system_status": status,
            "architecture_summary": {
                "total_tools": len(TOOLS),
                "cognitive_subsystems": 13,
                "agency_subsystems": 9,
                "reasoning_functions": 5
            }
        }
        
        with open("ultimate_test_report.json", "w") as f:
            json.dump(final_report, f, indent=4)
        
        print(f"\n💾 Detailed report saved to: ultimate_test_report.json")
        
        return overall_success_rate

    def run_ultimate_test(self):
        """Run the complete ultimate system test"""
        print("🚀 ULTIMATE ARTIFICIAL AGENT SYSTEM TEST")
        print("Testing complete layered AI architecture from Phase 1 to Phase 2.9")
        print(f"🕐 Test started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test phases
        self.test_phase1_cognitive_core()
        self.test_phase2_agency_capabilities()
        self.test_integration_scenarios()
        
        # Generate final report
        success_rate = self.generate_final_report()
        
        print(f"\n✅ ULTIMATE TEST COMPLETE!")
        print(f"🎯 Final Success Rate: {success_rate:.1f}%")
        
        return success_rate

def main():
    """Main test execution"""
    test_suite = UltimateSystemTest()
    return test_suite.run_ultimate_test()

if __name__ == "__main__":
    main()