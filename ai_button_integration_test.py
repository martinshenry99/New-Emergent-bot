#!/usr/bin/env python3
"""
AI Button Integration & Complete Flow Testing
Testing the Telegram Bot AI token creation flow and button handlers
"""

import asyncio
import json
import subprocess
import time
import os
import sys
from pathlib import Path

class AIButtonIntegrationTester:
    def __init__(self):
        self.test_results = []
        self.telegram_bot_path = "/app/telegram-bot"
        self.bot_file = f"{self.telegram_bot_path}/bot.js"
        self.ai_integrations_file = f"{self.telegram_bot_path}/ai-integrations.js"
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    def check_file_exists(self, filepath):
        """Check if file exists"""
        return os.path.exists(filepath)
    
    def search_in_file(self, filepath, pattern):
        """Search for pattern in file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                return pattern in content
        except Exception as e:
            return False
    
    def count_occurrences(self, filepath, pattern):
        """Count occurrences of pattern in file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                return content.count(pattern)
        except Exception as e:
            return 0
    
    def test_file_structure(self):
        """Test 1: Verify file structure exists"""
        print("\n🔍 TEST 1: File Structure Verification")
        
        # Check bot.js exists
        if self.check_file_exists(self.bot_file):
            self.log_test("Bot.js file exists", "PASS", f"Found at {self.bot_file}")
        else:
            self.log_test("Bot.js file exists", "FAIL", f"Missing at {self.bot_file}")
            return
        
        # Check ai-integrations.js exists
        if self.check_file_exists(self.ai_integrations_file):
            self.log_test("AI integrations file exists", "PASS", f"Found at {self.ai_integrations_file}")
        else:
            self.log_test("AI integrations file exists", "FAIL", f"Missing at {self.ai_integrations_file}")
    
    def test_auto_brand_command(self):
        """Test 2: Verify /auto_brand command exists"""
        print("\n🤖 TEST 2: /auto_brand Command Verification")
        
        # Check for /auto_brand command handler
        if self.search_in_file(self.bot_file, "bot.onText(/\\/auto_brand/"):
            self.log_test("/auto_brand command handler", "PASS", "Command handler found in bot.js")
        else:
            self.log_test("/auto_brand command handler", "FAIL", "Command handler not found")
        
        # Check for startEnhancedAutoBrand function
        if self.search_in_file(self.bot_file, "function startEnhancedAutoBrand"):
            self.log_test("startEnhancedAutoBrand function", "PASS", "Function exists")
        else:
            self.log_test("startEnhancedAutoBrand function", "FAIL", "Function missing")
    
    def test_callback_handlers(self):
        """Test 3: Verify AI button callback handlers"""
        print("\n🔘 TEST 3: AI Button Callback Handlers")
        
        # Critical callback handlers that were supposedly added
        critical_handlers = [
            "create_ai_token_",
            "regenerate_ai_", 
            "create_trend_token_",
            "regenerate_trend_"
        ]
        
        for handler in critical_handlers:
            if self.search_in_file(self.bot_file, "} else if (data.startsWith('" + handler + "'))"):
                self.log_test(f"Callback handler: {handler}", "PASS", "Handler found in callback query")
            else:
                self.log_test(f"Callback handler: {handler}", "FAIL", "Handler missing from callback query")
    
    def test_execute_ai_token_creation(self):
        """Test 4: Verify executeAITokenCreation function"""
        print("\n⚡ TEST 4: executeAITokenCreation Function")
        
        # Check if function exists
        if self.search_in_file(self.bot_file, "async function executeAITokenCreation"):
            self.log_test("executeAITokenCreation function exists", "PASS", "Function declaration found")
            
            # Check for key functionality patterns
            if self.search_in_file(self.bot_file, "session.type = 'ai_confirmed'"):
                self.log_test("Session management in executeAITokenCreation", "PASS", "Session type setting found")
            else:
                self.log_test("Session management in executeAITokenCreation", "FAIL", "Session type setting missing")
            
            if self.search_in_file(self.bot_file, "userSessions.set(userId"):
                self.log_test("User session storage", "PASS", "Session storage found")
            else:
                self.log_test("User session storage", "FAIL", "Session storage missing")
        else:
            self.log_test("executeAITokenCreation function exists", "FAIL", "Function not found")
    
    def test_helper_functions(self):
        """Test 5: Verify helper functions"""
        print("\n🛠️ TEST 5: Helper Functions")
        
        helper_functions = [
            "startTrendAwareAI",
            "explainTrendAI", 
            "executeEnhancedAITokenCreation",
            "executeTrendAwareTokenCreation"
        ]
        
        for func in helper_functions:
            if self.search_in_file(self.bot_file, f"function {func}") or self.search_in_file(self.bot_file, f"async function {func}"):
                self.log_test(f"Helper function: {func}", "PASS", "Function found")
            else:
                self.log_test(f"Helper function: {func}", "FAIL", "Function missing")
    
    def test_ai_network_handlers(self):
        """Test 6: Verify AI network selection handlers"""
        print("\n🌐 TEST 6: AI Network Selection Handlers")
        
        # Check for network selection handlers
        network_handlers = [
            "ai_network_devnet_",
            "ai_network_mainnet_"
        ]
        
        for handler in network_handlers:
            if self.search_in_file(self.bot_file, f"} else if (data.startsWith('{handler}'))"):
                self.log_test(f"Network handler: {handler}", "PASS", "Handler found")
            else:
                self.log_test(f"Network handler: {handler}", "FAIL", "Handler missing")
    
    def test_step35_image_handlers(self):
        """Test 7: Verify Step 3.5 image generation handlers"""
        print("\n🎨 TEST 7: Step 3.5 Image Generation Handlers")
        
        # Check for step 3.5 handlers
        step35_handlers = [
            "generate_step35_image_",
            "skip_step35_image_"
        ]
        
        for handler in step35_handlers:
            if self.search_in_file(self.bot_file, f"} else if (data.startsWith('{handler}'))"):
                self.log_test(f"Step 3.5 handler: {handler}", "PASS", "Handler found")
            else:
                self.log_test(f"Step 3.5 handler: {handler}", "FAIL", "Handler missing")
        
        # Check for handleStep35ImageGeneration function
        if self.search_in_file(self.bot_file, "handleStep35ImageGeneration"):
            self.log_test("handleStep35ImageGeneration function", "PASS", "Function found")
        else:
            self.log_test("handleStep35ImageGeneration function", "FAIL", "Function missing")
    
    def test_session_management(self):
        """Test 8: Verify session management"""
        print("\n💾 TEST 8: Session Management")
        
        # Check for userSessions Map
        if self.search_in_file(self.bot_file, "const userSessions = new Map()"):
            self.log_test("userSessions Map declaration", "PASS", "Map found")
        else:
            self.log_test("userSessions Map declaration", "FAIL", "Map missing")
        
        # Check for session validation in callbacks
        session_checks = self.count_occurrences(self.bot_file, "sessionUserId === userId.toString()")
        if session_checks >= 4:  # Should have multiple session validations
            self.log_test("Session validation checks", "PASS", f"Found {session_checks} validation checks")
        else:
            self.log_test("Session validation checks", "FAIL", f"Only found {session_checks} validation checks")
    
    def test_ai_integrations(self):
        """Test 9: Verify AI integrations"""
        print("\n🧠 TEST 9: AI Integrations")
        
        # Check AIIntegrations class
        if self.search_in_file(self.ai_integrations_file, "class AIIntegrations"):
            self.log_test("AIIntegrations class", "PASS", "Class found")
        else:
            self.log_test("AIIntegrations class", "FAIL", "Class missing")
        
        # Check for Craiyon integration (no DALL-E or Fal.ai)
        if self.search_in_file(self.ai_integrations_file, "craiyon"):
            self.log_test("Craiyon integration", "PASS", "Craiyon references found")
        else:
            self.log_test("Craiyon integration", "WARN", "Craiyon references not found")
        
        # Check that DALL-E and Fal.ai are removed
        dalle_count = self.count_occurrences(self.ai_integrations_file, "dall-e") + self.count_occurrences(self.ai_integrations_file, "DALL-E")
        fal_count = self.count_occurrences(self.ai_integrations_file, "fal.ai") + self.count_occurrences(self.ai_integrations_file, "fal-ai")
        
        if dalle_count == 0:
            self.log_test("DALL-E removal", "PASS", "No DALL-E references found")
        else:
            self.log_test("DALL-E removal", "FAIL", f"Found {dalle_count} DALL-E references")
        
        if fal_count == 0:
            self.log_test("Fal.ai removal", "PASS", "No Fal.ai references found")
        else:
            self.log_test("Fal.ai removal", "FAIL", f"Found {fal_count} Fal.ai references")
    
    def test_unhandled_callback_protection(self):
        """Test 10: Verify unhandled callback protection"""
        print("\n🛡️ TEST 10: Unhandled Callback Protection")
        
        # Check for the "Button action not recognized" fix
        if self.search_in_file(self.bot_file, "Button action not recognized"):
            self.log_test("Unhandled callback message", "PASS", "Error message found")
        else:
            self.log_test("Unhandled callback message", "FAIL", "Error message missing")
        
        # Check for proper else clause in callback handler
        if self.search_in_file(self.bot_file, "} else {") and self.search_in_file(self.bot_file, "UNHANDLED CALLBACK"):
            self.log_test("Callback handler else clause", "PASS", "Proper else handling found")
        else:
            self.log_test("Callback handler else clause", "FAIL", "Proper else handling missing")
    
    def test_bot_syntax(self):
        """Test 11: Verify bot.js syntax is valid"""
        print("\n✅ TEST 11: Bot.js Syntax Validation")
        
        try:
            # Use Node.js to check syntax
            result = subprocess.run(
                ["node", "-c", self.bot_file],
                capture_output=True,
                text=True,
                cwd=self.telegram_bot_path
            )
            
            if result.returncode == 0:
                self.log_test("Bot.js syntax validation", "PASS", "No syntax errors")
            else:
                self.log_test("Bot.js syntax validation", "FAIL", f"Syntax errors: {result.stderr}")
        except Exception as e:
            self.log_test("Bot.js syntax validation", "FAIL", f"Could not validate: {str(e)}")
    
    def test_integration_completeness(self):
        """Test 12: Verify integration completeness"""
        print("\n🔗 TEST 12: Integration Completeness")
        
        # Check that all AI functions are properly integrated
        ai_functions = [
            "executeAITokenCreation",
            "executeEnhancedAITokenCreation", 
            "executeTrendAwareTokenCreation"
        ]
        
        integration_score = 0
        for func in ai_functions:
            # Check if function is called in callback handlers
            call_count = self.count_occurrences(self.bot_file, f"{func}(")
            if call_count > 0:
                self.log_test(f"{func} integration", "PASS", f"Called {call_count} times")
                integration_score += 1
            else:
                self.log_test(f"{func} integration", "FAIL", "Function not called")
        
        if integration_score == len(ai_functions):
            self.log_test("Overall AI integration", "PASS", "All AI functions integrated")
        else:
            self.log_test("Overall AI integration", "FAIL", f"Only {integration_score}/{len(ai_functions)} functions integrated")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting AI Button Integration & Complete Flow Testing")
        print("=" * 60)
        
        # Run all test methods
        test_methods = [
            self.test_file_structure,
            self.test_auto_brand_command,
            self.test_callback_handlers,
            self.test_execute_ai_token_creation,
            self.test_helper_functions,
            self.test_ai_network_handlers,
            self.test_step35_image_handlers,
            self.test_session_management,
            self.test_ai_integrations,
            self.test_unhandled_callback_protection,
            self.test_bot_syntax,
            self.test_integration_completeness
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(f"Test {test_method.__name__}", "FAIL", f"Exception: {str(e)}")
        
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warnings: {warning_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  • {result['test']}: {result['details']}")
        
        if warning_tests > 0:
            print("\n⚠️ WARNINGS:")
            for result in self.test_results:
                if result["status"] == "WARN":
                    print(f"  • {result['test']}: {result['details']}")
        
        # Critical assessment
        critical_failures = [
            "executeAITokenCreation function exists",
            "Callback handler: create_ai_token_",
            "Callback handler: regenerate_ai_",
            "/auto_brand command handler"
        ]
        
        critical_failed = [r for r in self.test_results if r["test"] in critical_failures and r["status"] == "FAIL"]
        
        if critical_failed:
            print(f"\n🚨 CRITICAL ISSUES FOUND: {len(critical_failed)} critical components failed")
            print("The AI button integration may not work properly.")
        else:
            print("\n✅ CRITICAL COMPONENTS: All critical AI button components are present")
        
        # Save results to file
        with open("/app/ai_button_integration_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "warnings": warning_tests,
                    "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
                },
                "results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: /app/ai_button_integration_test_results.json")

def main():
    """Main function"""
    tester = AIButtonIntegrationTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()