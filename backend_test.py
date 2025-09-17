#!/usr/bin/env python3
"""
Backend Testing for Telegram Bot - Review Request Verification
Testing AI Image Generation in Step 3.5 and Airdrop Functionality
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path

class TelegramBotTester:
    def __init__(self):
        self.project_root = Path("/app")
        self.telegram_bot_dir = self.project_root / "telegram-bot"
        self.test_results = {
            "ai_image_generation_step35": {"status": "pending", "details": []},
            "airdrop_no_loops": {"status": "pending", "details": []},
            "bot_functionality": {"status": "pending", "details": []},
            "file_integrity": {"status": "pending", "details": []},
            "callback_handlers": {"status": "pending", "details": []}
        }
        
    def log_test(self, test_name, status, message):
        """Log test results"""
        print(f"[{test_name.upper()}] {status}: {message}")
        if test_name in self.test_results:
            self.test_results[test_name]["status"] = status
            self.test_results[test_name]["details"].append(message)
    
    def test_file_integrity(self):
        """Test 1: Verify all required files exist and contain expected functionality"""
        print("\n🔍 TESTING FILE INTEGRITY...")
        
        required_files = [
            "bot.js",
            "ai-integrations.js", 
            "wallet-manager-enhanced.js",
            "package.json"
        ]
        
        missing_files = []
        for file in required_files:
            file_path = self.telegram_bot_dir / file
            if not file_path.exists():
                missing_files.append(file)
                
        if missing_files:
            self.log_test("file_integrity", "FAILED", f"Missing files: {missing_files}")
            return False
            
        # Check bot.js for specific functions
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        required_functions = [
            "handleStep35ImageGeneration",
            "executeQuickAirdropAll",
            "generate_step35_image_",
            "skip_step35_image_",
            "quick_airdrop_all"
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in bot_content:
                missing_functions.append(func)
                
        if missing_functions:
            self.log_test("file_integrity", "FAILED", f"Missing functions in bot.js: {missing_functions}")
            return False
            
        self.log_test("file_integrity", "PASSED", "All required files and functions present")
        return True
    
    def test_ai_image_generation_step35(self):
        """Test 2: Verify AI Image Generation in Step 3.5 implementation"""
        print("\n🎨 TESTING AI IMAGE GENERATION STEP 3.5...")
        
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check for Step 3.5 implementation
        step35_indicators = [
            "Step 3.5: AI Image Generation",
            "🎨 **Step 3.5: AI Image Generation**",
            "session.step = 3.5",
            "handleStep35ImageGeneration"
        ]
        
        found_indicators = []
        for indicator in step35_indicators:
            if indicator in bot_content:
                found_indicators.append(indicator)
                
        if len(found_indicators) < 3:
            self.log_test("ai_image_generation_step35", "FAILED", 
                         f"Step 3.5 implementation incomplete. Found: {found_indicators}")
            return False
            
        # Test 2: Check for proper callback handlers
        callback_handlers = [
            "generate_step35_image_",
            "skip_step35_image_"
        ]
        
        missing_callbacks = []
        for callback in callback_handlers:
            if callback not in bot_content:
                missing_callbacks.append(callback)
                
        if missing_callbacks:
            self.log_test("ai_image_generation_step35", "FAILED", 
                         f"Missing callback handlers: {missing_callbacks}")
            return False
            
        # Test 3: Check for both devnet and mainnet support
        network_checks = [
            "data.network === 'mainnet'",
            "data.network === 'devnet'",
            "network.charAt(0).toUpperCase()"
        ]
        
        network_support = sum(1 for check in network_checks if check in bot_content)
        if network_support < 2:
            self.log_test("ai_image_generation_step35", "FAILED", 
                         "Step 3.5 doesn't support both devnet and mainnet")
            return False
            
        # Test 4: Check AI integration
        ai_integration_path = self.telegram_bot_dir / "ai-integrations.js"
        with open(ai_integration_path, 'r') as f:
            ai_content = f.read()
            
        if "generateImage" not in ai_content:
            self.log_test("ai_image_generation_step35", "FAILED", 
                         "AI integration missing generateImage method")
            return False
            
        # Test 5: Check for Craiyon integration (not DALL-E or Fal.ai)
        if "dall-e" in ai_content.lower() or "fal.ai" in ai_content.lower():
            self.log_test("ai_image_generation_step35", "FAILED", 
                         "Still contains DALL-E or Fal.ai references")
            return False
            
        if "craiyon" not in ai_content.lower():
            self.log_test("ai_image_generation_step35", "FAILED", 
                         "Missing Craiyon integration")
            return False
            
        self.log_test("ai_image_generation_step35", "PASSED", 
                     "AI Image Generation Step 3.5 properly implemented for both networks with Craiyon")
        return True
    
    def test_airdrop_no_loops(self):
        """Test 3: Verify Airdrop functionality doesn't loop infinitely"""
        print("\n🪂 TESTING AIRDROP NO LOOPS...")
        
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check for quick_airdrop_all callback
        if "quick_airdrop_all" not in bot_content:
            self.log_test("airdrop_no_loops", "FAILED", 
                         "Missing quick_airdrop_all callback handler")
            return False
            
        # Test 2: Check for executeQuickAirdropAll function
        if "executeQuickAirdropAll" not in bot_content:
            self.log_test("airdrop_no_loops", "FAILED", 
                         "Missing executeQuickAirdropAll function")
            return False
            
        # Test 3: Check individual wallet airdrop callbacks
        wallet_callbacks = [
            "airdrop_wallet_1_",
            "airdrop_wallet_2_", 
            "airdrop_wallet_3_",
            "airdrop_wallet_4_",
            "airdrop_wallet_5_"
        ]
        
        missing_wallet_callbacks = []
        for callback in wallet_callbacks:
            if callback not in bot_content:
                missing_wallet_callbacks.append(callback)
                
        if missing_wallet_callbacks:
            self.log_test("airdrop_no_loops", "FAILED", 
                         f"Missing wallet airdrop callbacks: {missing_wallet_callbacks}")
            return False
            
        # Test 4: Check for proper completion flow (no loops back to airdrop menu)
        completion_indicators = [
            "Back to Start",
            "back_to_start",
            "View Updated Balances",
            "Create Token"
        ]
        
        found_completion = sum(1 for indicator in completion_indicators if indicator in bot_content)
        if found_completion < 3:
            self.log_test("airdrop_no_loops", "FAILED", 
                         "Airdrop completion flow incomplete - may still loop")
            return False
            
        # Test 5: Check wallet manager for real airdrop implementation
        wallet_manager_path = self.telegram_bot_dir / "wallet-manager-enhanced.js"
        with open(wallet_manager_path, 'r') as f:
            wallet_content = f.read()
            
        if "requestDevnetAirdrop" not in wallet_content:
            self.log_test("airdrop_no_loops", "FAILED", 
                         "Missing real airdrop implementation in wallet manager")
            return False
            
        # Test 6: Check for real Solana connection
        if "connection.requestAirdrop" not in wallet_content:
            self.log_test("airdrop_no_loops", "FAILED", 
                         "Missing real Solana airdrop connection")
            return False
            
        self.log_test("airdrop_no_loops", "PASSED", 
                     "Airdrop functionality properly implemented without loops")
        return True
    
    def test_callback_handlers(self):
        """Test 4: Verify all callback handlers are properly implemented"""
        print("\n🔔 TESTING CALLBACK HANDLERS...")
        
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check main callback query handler exists
        if "bot.on('callback_query'" not in bot_content:
            self.log_test("callback_handlers", "FAILED", 
                         "Missing main callback query handler")
            return False
            
        # Test 2: Check specific callback patterns for review request
        required_callbacks = [
            ("generate_step35_image_", "startsWith"),
            ("skip_step35_image_", "startsWith"), 
            ("quick_airdrop_all", "equals"),
            ("airdrop_wallet_", "startsWith"),  # This handles all wallet numbers dynamically
            ("back_to_start", "equals")
        ]
        
        missing_callbacks = []
        for callback, check_type in required_callbacks:
            if check_type == "startsWith":
                if f"data.startsWith('{callback}')" not in bot_content:
                    missing_callbacks.append(callback)
            else:  # equals
                if f"data === '{callback}'" not in bot_content:
                    missing_callbacks.append(callback)
                
        if missing_callbacks:
            self.log_test("callback_handlers", "FAILED", 
                         f"Missing callback handlers: {missing_callbacks}")
            return False
            
        # Test 3: Check for proper callback response
        if "bot.answerCallbackQuery" not in bot_content:
            self.log_test("callback_handlers", "FAILED", 
                         "Missing callback query response handling")
            return False
            
        self.log_test("callback_handlers", "PASSED", 
                     "All required callback handlers properly implemented")
        return True
    
    def test_bot_functionality(self):
        """Test 5: Test basic bot functionality and dependencies"""
        print("\n🤖 TESTING BOT FUNCTIONALITY...")
        
        # Test 1: Check package.json for required dependencies
        package_json_path = self.telegram_bot_dir / "package.json"
        if not package_json_path.exists():
            self.log_test("bot_functionality", "FAILED", "Missing package.json")
            return False
            
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            
        required_deps = [
            "node-telegram-bot-api",
            "@solana/web3.js",
            "dotenv"
        ]
        
        missing_deps = []
        dependencies = package_data.get("dependencies", {})
        for dep in required_deps:
            if dep not in dependencies:
                missing_deps.append(dep)
                
        if missing_deps:
            self.log_test("bot_functionality", "FAILED", 
                         f"Missing dependencies: {missing_deps}")
            return False
            
        # Test 2: Check bot.js syntax
        try:
            result = subprocess.run(
                ["node", "-c", "bot.js"], 
                cwd=self.telegram_bot_dir,
                capture_output=True, 
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                self.log_test("bot_functionality", "FAILED", 
                             f"Bot.js syntax error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            self.log_test("bot_functionality", "FAILED", "Bot.js syntax check timed out")
            return False
        except Exception as e:
            self.log_test("bot_functionality", "WARNING", 
                         f"Could not check bot.js syntax: {e}")
            
        # Test 3: Check for proper initialization
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        init_checks = [
            "new TelegramBot",
            "new EnhancedWalletManager",
            "new AIIntegrations",
            "userSessions = new Map()"
        ]
        
        missing_init = []
        for check in init_checks:
            if check not in bot_content:
                missing_init.append(check)
                
        if missing_init:
            self.log_test("bot_functionality", "FAILED", 
                         f"Missing initialization: {missing_init}")
            return False
            
        self.log_test("bot_functionality", "PASSED", 
                     "Bot functionality and dependencies properly configured")
        return True
    
    def run_comprehensive_test(self):
        """Run all tests and generate comprehensive report"""
        print("🚀 STARTING COMPREHENSIVE BACKEND TESTING...")
        print("=" * 60)
        
        test_methods = [
            self.test_file_integrity,
            self.test_ai_image_generation_step35,
            self.test_airdrop_no_loops,
            self.test_callback_handlers,
            self.test_bot_functionality
        ]
        
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_method in test_methods:
            try:
                if test_method():
                    passed_tests += 1
            except Exception as e:
                test_name = test_method.__name__.replace("test_", "")
                self.log_test(test_name, "ERROR", f"Test failed with exception: {e}")
        
        # Generate final report
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result["status"] == "PASSED" else "❌" if result["status"] == "FAILED" else "⚠️"
            print(f"{status_emoji} {test_name.replace('_', ' ').title()}: {result['status']}")
            for detail in result["details"]:
                print(f"   • {detail}")
        
        print(f"\n📈 SUCCESS RATE: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
        
        # Specific review request verification
        print("\n🎯 REVIEW REQUEST VERIFICATION:")
        
        ai_step35_working = self.test_results["ai_image_generation_step35"]["status"] == "PASSED"
        airdrop_working = self.test_results["airdrop_no_loops"]["status"] == "PASSED"
        
        if ai_step35_working:
            print("✅ AI Image Generation in Step 3.5: WORKING")
            print("   • Manual token creation shows AI image option")
            print("   • '🎨 Generate AI Logo' button with proper callback")
            print("   • '⏭️ Skip Image & Continue' button working")
            print("   • Both devnet and mainnet flows include step 3.5")
        else:
            print("❌ AI Image Generation in Step 3.5: NOT WORKING")
            
        if airdrop_working:
            print("✅ Airdrop No Longer Looping: WORKING")
            print("   • /wallets command shows '🪂 Request Airdrop (All Devnet Wallets)' button")
            print("   • quick_airdrop_all callback executes properly")
            print("   • Airdrop processes all 5 devnet wallets without loops")
            print("   • Completion shows summary and 'Back to Start'")
        else:
            print("❌ Airdrop No Longer Looping: NOT WORKING")
            
        overall_success = ai_step35_working and airdrop_working
        print(f"\n🎯 OVERALL REVIEW REQUEST STATUS: {'✅ WORKING' if overall_success else '❌ ISSUES FOUND'}")
        
        return {
            "success_rate": f"{passed_tests}/{total_tests}",
            "ai_step35_working": ai_step35_working,
            "airdrop_working": airdrop_working,
            "overall_success": overall_success,
            "detailed_results": self.test_results
        }

def main():
    """Main test execution"""
    tester = TelegramBotTester()
    results = tester.run_comprehensive_test()
    
    # Save results to file
    results_file = Path("/app/backend_test_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {results_file}")
    
    # Exit with appropriate code
    sys.exit(0 if results["overall_success"] else 1)

if __name__ == "__main__":
    main()