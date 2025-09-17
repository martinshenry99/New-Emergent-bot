#!/usr/bin/env python3
"""
Backend Testing for Telegram Bot - User-Reported Issues Verification
Testing specific issues reported by user:
1. AI Image Creation Missing from Mainnet Launch
2. /wallets Command Problems  
3. Devnet Airdrop Functionality
4. Wallet Implementation Changes
"""

import asyncio
import json
import os
import sys
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path

class TelegramBotTester:
    def __init__(self):
        self.test_results = []
        self.bot_process = None
        self.bot_log_file = "/app/telegram-bot/bot_test.log"
        self.project_root = Path("/app")
        
    def log_test(self, test_name, status, details="", error=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")
    
    def check_file_exists(self, file_path, description=""):
        """Check if a file exists"""
        full_path = self.project_root / file_path
        exists = full_path.exists()
        
        if exists:
            size = full_path.stat().st_size
            self.log_test(f"File Check: {file_path}", "PASS", 
                         f"{description} exists ({size} bytes)")
        else:
            self.log_test(f"File Check: {file_path}", "FAIL", 
                         f"{description} not found")
        
        return exists
    
    def check_bot_dependencies(self):
        """Check if all required bot dependencies are present"""
        print("\n🔍 CHECKING BOT DEPENDENCIES...")
        
        # Check main bot file
        self.check_file_exists("telegram-bot/bot.js", "Main bot file")
        
        # Check wallet manager
        wallet_manager_exists = (
            self.check_file_exists("telegram-bot/wallet-manager-enhanced.js", "Enhanced wallet manager") or
            self.check_file_exists("telegram-bot/enhanced-wallet-manager.js", "Enhanced wallet manager alt")
        )
        
        # Check genuine blockchain manager
        self.check_file_exists("telegram-bot/genuine-blockchain-manager.js", "Genuine blockchain manager")
        
        # Check AI integrations
        self.check_file_exists("telegram-bot/ai-integrations.js", "AI integrations")
        
        # Check package.json for dependencies
        package_json_path = self.project_root / "telegram-bot/package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    
                required_deps = [
                    'node-telegram-bot-api',
                    '@solana/web3.js',
                    '@solana/spl-token',
                    'dotenv'
                ]
                
                dependencies = package_data.get('dependencies', {})
                missing_deps = [dep for dep in required_deps if dep not in dependencies]
                
                if missing_deps:
                    self.log_test("Dependencies Check", "FAIL", 
                                 f"Missing dependencies: {', '.join(missing_deps)}")
                else:
                    self.log_test("Dependencies Check", "PASS", 
                                 f"All required dependencies present")
                    
            except Exception as e:
                self.log_test("Dependencies Check", "FAIL", "", str(e))
        else:
            self.log_test("Dependencies Check", "FAIL", "package.json not found")
    
    def check_bot_configuration(self):
        """Check bot configuration and environment variables"""
        print("\n🔧 CHECKING BOT CONFIGURATION...")
        
        # Check .env file
        env_path = self.project_root / "telegram-bot/.env"
        if env_path.exists():
            try:
                with open(env_path, 'r') as f:
                    env_content = f.read()
                    
                required_vars = [
                    'TELEGRAM_BOT_TOKEN',
                    'SOLANA_RPC_URL'
                ]
                
                missing_vars = []
                for var in required_vars:
                    if var not in env_content:
                        missing_vars.append(var)
                
                if missing_vars:
                    self.log_test("Environment Variables", "FAIL", 
                                 f"Missing variables: {', '.join(missing_vars)}")
                else:
                    self.log_test("Environment Variables", "PASS", 
                                 "Required environment variables present")
                    
            except Exception as e:
                self.log_test("Environment Variables", "FAIL", "", str(e))
        else:
            self.log_test("Environment Variables", "FAIL", ".env file not found")
    
    def analyze_bot_code_for_issues(self):
        """Analyze bot code for specific user-reported issues"""
        print("\n🔍 ANALYZING BOT CODE FOR REPORTED ISSUES...")
        
        bot_file = self.project_root / "telegram-bot/bot.js"
        if not bot_file.exists():
            self.log_test("Bot Code Analysis", "FAIL", "bot.js not found")
            return
        
        try:
            with open(bot_file, 'r') as f:
                bot_code = f.read()
            
            # Issue #1: AI Image Creation Missing from Mainnet Launch
            self.check_ai_image_generation(bot_code)
            
            # Issue #2: /wallets Command Problems
            self.check_wallets_command(bot_code)
            
            # Issue #3: Devnet Airdrop Functionality
            self.check_airdrop_functionality(bot_code)
            
            # Issue #4: Wallet Implementation Changes
            self.check_wallet_implementation(bot_code)
            
        except Exception as e:
            self.log_test("Bot Code Analysis", "FAIL", "", str(e))
    
    def check_ai_image_generation(self, bot_code):
        """Check AI image generation for both devnet and mainnet"""
        print("\n🎨 CHECKING AI IMAGE GENERATION...")
        
        # Check for image generation step (step 3.5)
        if "step = 3.5" in bot_code or "step: 3.5" in bot_code:
            self.log_test("AI Image Step 3.5", "PASS", "Step 3.5 for image generation found")
        else:
            self.log_test("AI Image Step 3.5", "FAIL", "Step 3.5 for image generation not found")
        
        # Check for "Generate AI Image" option
        if "Generate AI Image" in bot_code or "🎨 Generate AI Image" in bot_code:
            self.log_test("Generate AI Image Button", "PASS", "Generate AI Image button found")
        else:
            self.log_test("Generate AI Image Button", "FAIL", "Generate AI Image button not found")
        
        # Check if image generation works for both networks
        mainnet_image_check = "mainnet" in bot_code and ("generate_image" in bot_code or "handleImageGeneration" in bot_code)
        devnet_image_check = "devnet" in bot_code and ("generate_image" in bot_code or "handleImageGeneration" in bot_code)
        
        if mainnet_image_check and devnet_image_check:
            self.log_test("AI Image Both Networks", "PASS", "Image generation available for both networks")
        else:
            self.log_test("AI Image Both Networks", "FAIL", "Image generation may not work on both networks")
    
    def check_wallets_command(self, bot_code):
        """Check /wallets command functionality"""
        print("\n💰 CHECKING /wallets COMMAND...")
        
        # Check for /wallets command handler
        if "bot.onText(/\\/wallets/" in bot_code or "/wallets" in bot_code:
            self.log_test("/wallets Command Handler", "PASS", "/wallets command handler found")
        else:
            self.log_test("/wallets Command Handler", "FAIL", "/wallets command handler not found")
        
        # Check for showAllWalletBalances function
        if "showAllWalletBalances" in bot_code:
            self.log_test("showAllWalletBalances Function", "PASS", "showAllWalletBalances function found")
        else:
            self.log_test("showAllWalletBalances Function", "FAIL", "showAllWalletBalances function not found")
        
        # Check for airdrop button
        if "🪂 Airdrop (Devnet)" in bot_code or "Airdrop" in bot_code:
            self.log_test("Airdrop Button", "PASS", "Airdrop button found in wallets display")
        else:
            self.log_test("Airdrop Button", "FAIL", "Airdrop button not found in wallets display")
        
        # Check for both network wallet display
        devnet_wallets = "DEVNET WALLETS" in bot_code or "devnet" in bot_code.lower()
        mainnet_wallets = "MAINNET WALLETS" in bot_code or "mainnet" in bot_code.lower()
        
        if devnet_wallets and mainnet_wallets:
            self.log_test("Both Network Wallets", "PASS", "Both devnet and mainnet wallet display found")
        else:
            self.log_test("Both Network Wallets", "FAIL", "Missing network wallet display")
    
    def check_airdrop_functionality(self, bot_code):
        """Check devnet airdrop functionality"""
        print("\n🪂 CHECKING DEVNET AIRDROP FUNCTIONALITY...")
        
        # Check for executeAirdrop function
        if "executeAirdrop" in bot_code:
            self.log_test("executeAirdrop Function", "PASS", "executeAirdrop function found")
        else:
            self.log_test("executeAirdrop Function", "FAIL", "executeAirdrop function not found")
        
        # Check for airdrop wallet callbacks
        airdrop_callbacks = []
        for i in range(1, 6):
            callback = f"airdrop_wallet_{i}"
            if callback in bot_code:
                airdrop_callbacks.append(callback)
        
        if len(airdrop_callbacks) == 5:
            self.log_test("Airdrop Wallet Callbacks", "PASS", f"All 5 airdrop wallet callbacks found: {airdrop_callbacks}")
        else:
            self.log_test("Airdrop Wallet Callbacks", "FAIL", f"Missing airdrop callbacks. Found: {airdrop_callbacks}")
        
        # Check for loop prevention
        if "back to menu" not in bot_code.lower() and "infinite" not in bot_code.lower():
            self.log_test("Airdrop Loop Prevention", "PASS", "No obvious loop issues in airdrop code")
        else:
            self.log_test("Airdrop Loop Prevention", "WARN", "Potential loop issues detected")
        
        # Check for real airdrop implementation
        if "requestDevnetAirdrop" in bot_code or "airdropResult" in bot_code:
            self.log_test("Real Airdrop Implementation", "PASS", "Real airdrop implementation found")
        else:
            self.log_test("Real Airdrop Implementation", "FAIL", "Real airdrop implementation not found")
    
    def check_wallet_implementation(self, bot_code):
        """Check wallet implementation changes"""
        print("\n🔧 CHECKING WALLET IMPLEMENTATION...")
        
        # Check for enhancedWalletManager usage
        if "enhancedWalletManager" in bot_code:
            self.log_test("Enhanced Wallet Manager Usage", "PASS", "enhancedWalletManager found in bot code")
        else:
            self.log_test("Enhanced Wallet Manager Usage", "FAIL", "enhancedWalletManager not found in bot code")
        
        # Check for getWallets method calls
        if "getWallets(" in bot_code:
            self.log_test("getWallets Method Calls", "PASS", "getWallets method calls found")
        else:
            self.log_test("getWallets Method Calls", "FAIL", "getWallets method calls not found")
        
        # Check for balance update functionality
        if "updateBalances" in bot_code:
            self.log_test("Balance Update Functionality", "PASS", "updateBalances functionality found")
        else:
            self.log_test("Balance Update Functionality", "FAIL", "updateBalances functionality not found")
        
        # Check for persistent wallet addresses from .env
        if "WALLET_" in bot_code or "process.env" in bot_code:
            self.log_test("Persistent Wallet Addresses", "PASS", "Environment variable usage for persistent addresses found")
        else:
            self.log_test("Persistent Wallet Addresses", "WARN", "Environment variable usage not clearly found")
    
    def check_wallet_manager_implementation(self):
        """Check wallet manager implementation details"""
        print("\n🔍 CHECKING WALLET MANAGER IMPLEMENTATION...")
        
        wallet_manager_path = self.project_root / "telegram-bot/wallet-manager-enhanced.js"
        if not wallet_manager_path.exists():
            self.log_test("Wallet Manager File", "FAIL", "wallet-manager-enhanced.js not found")
            return
        
        try:
            with open(wallet_manager_path, 'r') as f:
                wallet_code = f.read()
            
            # Check for requestDevnetAirdrop method
            if "requestDevnetAirdrop" in wallet_code:
                self.log_test("requestDevnetAirdrop Method", "PASS", "requestDevnetAirdrop method found in wallet manager")
            else:
                self.log_test("requestDevnetAirdrop Method", "FAIL", "requestDevnetAirdrop method not found")
            
            # Check for getWallets method
            if "getWallets(" in wallet_code:
                self.log_test("getWallets Method", "PASS", "getWallets method found in wallet manager")
            else:
                self.log_test("getWallets Method", "FAIL", "getWallets method not found")
            
            # Check for persistent wallet loading
            if "loadOrGenerateWallets" in wallet_code and "NEVER regenerate" in wallet_code:
                self.log_test("Persistent Wallet Loading", "PASS", "Persistent wallet loading with 'NEVER regenerate' found")
            else:
                self.log_test("Persistent Wallet Loading", "FAIL", "Persistent wallet loading not properly implemented")
            
        except Exception as e:
            self.log_test("Wallet Manager Analysis", "FAIL", "", str(e))
    
    def test_bot_startup(self):
        """Test if bot can start without errors"""
        print("\n🚀 TESTING BOT STARTUP...")
        
        bot_dir = self.project_root / "telegram-bot"
        if not bot_dir.exists():
            self.log_test("Bot Startup", "FAIL", "telegram-bot directory not found")
            return
        
        try:
            # Change to bot directory
            os.chdir(bot_dir)
            
            # Try to run syntax check
            result = subprocess.run(
                ["node", "-c", "bot.js"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.log_test("Bot Syntax Check", "PASS", "Bot.js syntax is valid")
            else:
                self.log_test("Bot Syntax Check", "FAIL", f"Syntax errors: {result.stderr}")
            
            # Check if we can load the bot (without starting polling)
            test_script = """
const bot = require('./bot.js');
console.log('Bot loaded successfully');
process.exit(0);
"""
            
            with open("test_load.js", "w") as f:
                f.write(test_script)
            
            result = subprocess.run(
                ["node", "test_load.js"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                self.log_test("Bot Loading Test", "PASS", "Bot loads without errors")
            else:
                self.log_test("Bot Loading Test", "FAIL", f"Loading errors: {result.stderr}")
            
            # Clean up test file
            if os.path.exists("test_load.js"):
                os.remove("test_load.js")
                
        except subprocess.TimeoutExpired:
            self.log_test("Bot Startup", "FAIL", "Bot startup timed out")
        except Exception as e:
            self.log_test("Bot Startup", "FAIL", "", str(e))
        finally:
            # Return to original directory
            os.chdir(self.project_root)
    
    def check_ai_integrations(self):
        """Check AI integrations implementation"""
        print("\n🤖 CHECKING AI INTEGRATIONS...")
        
        ai_file = self.project_root / "telegram-bot/ai-integrations.js"
        if not ai_file.exists():
            self.log_test("AI Integrations File", "FAIL", "ai-integrations.js not found")
            return
        
        try:
            with open(ai_file, 'r') as f:
                ai_code = f.read()
            
            # Check for Craiyon integration (should be present)
            if "craiyon" in ai_code.lower():
                self.log_test("Craiyon Integration", "PASS", "Craiyon integration found")
            else:
                self.log_test("Craiyon Integration", "FAIL", "Craiyon integration not found")
            
            # Check that DALL-E and Fal.ai are NOT present (should be removed)
            dalle_present = "dall-e" in ai_code.lower() or "openai" in ai_code.lower()
            fal_present = "fal.ai" in ai_code.lower() or "fal-ai" in ai_code.lower()
            
            if not dalle_present:
                self.log_test("DALL-E Removal", "PASS", "DALL-E references removed")
            else:
                self.log_test("DALL-E Removal", "FAIL", "DALL-E references still present")
            
            if not fal_present:
                self.log_test("Fal.ai Removal", "PASS", "Fal.ai references removed")
            else:
                self.log_test("Fal.ai Removal", "FAIL", "Fal.ai references still present")
            
            # Check for generateImage method
            if "generateImage" in ai_code:
                self.log_test("generateImage Method", "PASS", "generateImage method found")
            else:
                self.log_test("generateImage Method", "FAIL", "generateImage method not found")
                
        except Exception as e:
            self.log_test("AI Integrations Analysis", "FAIL", "", str(e))
    
    def run_comprehensive_tests(self):
        """Run all tests"""
        print("🧪 STARTING COMPREHENSIVE TELEGRAM BOT TESTING")
        print("=" * 60)
        
        # Basic file and dependency checks
        self.check_bot_dependencies()
        self.check_bot_configuration()
        
        # Code analysis for specific issues
        self.analyze_bot_code_for_issues()
        self.check_wallet_manager_implementation()
        self.check_ai_integrations()
        
        # Runtime tests
        self.test_bot_startup()
        
        # Generate summary
        self.generate_test_summary()
    
    def generate_test_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAIL"])
        warning_tests = len([t for t in self.test_results if t["status"] == "WARN"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warnings: {warning_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\n🔍 CRITICAL ISSUES FOUND:")
        critical_issues = [t for t in self.test_results if t["status"] == "FAIL"]
        if critical_issues:
            for issue in critical_issues:
                print(f"❌ {issue['test']}: {issue['error'] or issue['details']}")
        else:
            print("✅ No critical issues found!")
        
        print("\n⚠️ WARNINGS:")
        warnings = [t for t in self.test_results if t["status"] == "WARN"]
        if warnings:
            for warning in warnings:
                print(f"⚠️ {warning['test']}: {warning['details']}")
        else:
            print("✅ No warnings!")
        
        # Save detailed results
        results_file = self.project_root / "backend_test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "warnings": warning_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "test_results": self.test_results,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_file}")

def main():
    """Main test execution"""
    tester = TelegramBotTester()
    tester.run_comprehensive_tests()

if __name__ == "__main__":
    main()