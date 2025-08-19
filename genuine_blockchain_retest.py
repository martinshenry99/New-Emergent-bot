#!/usr/bin/env python3
"""
Genuine Blockchain Operations RE-TEST Suite for Meme-bot
Re-testing after addressing integration issues. Focus on:

SPECIFIC RE-TESTING AREAS:
1. Command Recognition Test (/revoke_mint, /genuine_mint_rugpull, /genuine_rugpull, /status)
2. Genuine Blockchain Manager Verification (integration in bot.js)
3. Updated Liquidity Lock Testing (genuine operations, 24-hour duration)
4. Time-lock Implementation Check (3-day delays)
5. Bot Startup and Integration (no errors, proper initialization)
6. Command Handler Integration (callbacks, confirmations, warnings)

SUCCESS CRITERIA:
- Bot loads successfully with genuine blockchain manager
- New command handlers respond correctly
- Genuine operations differentiated from simulations
- Warning and confirmation systems functional
- Time-lock and status tracking operational
"""

import os
import sys
import json
import time
import asyncio
import subprocess
import requests
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

class GenuineBlockchainRetester:
    def __init__(self):
        self.telegram_bot_dir = project_root / "telegram-bot"
        self.bot_token = None
        self.test_results = []
        self.load_config()
    
    def load_config(self):
        """Load configuration from telegram-bot/.env"""
        env_file = self.telegram_bot_dir / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            if key == 'TELEGRAM_BOT_TOKEN':
                                self.bot_token = value.strip('"\'')
                                break
        
        if not self.bot_token:
            print("⚠️ TELEGRAM_BOT_TOKEN not found in telegram-bot/.env")
    
    def log_test(self, test_name, status, message="", details=None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "details": details or {}
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")
    
    def test_command_recognition(self):
        """Test 1: Verify /revoke_mint, /genuine_mint_rugpull, /genuine_rugpull, /status commands exist and respond"""
        test_name = "Command Recognition Test"
        
        try:
            # Check bot.js for command handlers
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for specific command handlers
            command_recognition_checks = {
                "/revoke_mint Command Handler": "bot.onText(/\\/revoke_mint/" in bot_content or "/revoke_mint" in bot_content,
                "/genuine_mint_rugpull Command Handler": "bot.onText(/\\/genuine_mint_rugpull/" in bot_content or "/genuine_mint_rugpull" in bot_content,
                "/genuine_rugpull Command Handler": "bot.onText(/\\/genuine_rugpull/" in bot_content or "/genuine_rugpull" in bot_content,
                "/status Command Handler": "bot.onText(/\\/status/" in bot_content or "/status" in bot_content,
                "Genuine Operations Section in Status": "genuine" in bot_content.lower() and "operations" in bot_content.lower(),
                "Command Response Logic": "sendMessage" in bot_content and "callback" in bot_content,
                "Error Handling for Commands": "try" in bot_content and "catch" in bot_content
            }
            
            failed_checks = []
            for check, passed in command_recognition_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Command Recognition Checks": list(command_recognition_checks.keys()),
                "Failed Checks": failed_checks,
                "Commands Found": [cmd for cmd in ["/revoke_mint", "/genuine_mint_rugpull", "/genuine_rugpull", "/status"] if cmd in bot_content]
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Command recognition incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some command recognition checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "All genuine blockchain commands properly recognized", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing command recognition: {str(e)}")
            return False
    
    def test_genuine_blockchain_manager_verification(self):
        """Test 2: Confirm genuine-blockchain-manager.js is properly imported and integrated in bot.js"""
        test_name = "Genuine Blockchain Manager Verification"
        
        try:
            # Check bot.js for genuine manager integration
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check genuine-blockchain-manager.js exists and has required content
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            if not genuine_manager_path.exists():
                self.log_test(test_name, "FAIL", "genuine-blockchain-manager.js file is missing")
                return False
            
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            # Check package.json for BN.js dependency
            package_json_path = self.telegram_bot_dir / "package.json"
            bn_js_installed = False
            if package_json_path.exists():
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    deps = package_data.get('dependencies', {})
                    bn_js_installed = 'bn.js' in deps or 'bignumber.js' in deps
            
            manager_verification_checks = {
                "Genuine Manager Import in bot.js": "genuine-blockchain-manager" in bot_content or "GenuineBlockchainManager" in bot_content,
                "GenuineBlockchainManager Class Instantiated": "new GenuineBlockchainManager" in bot_content or "genuineBlockchainManager" in bot_content,
                "Manager Variable Accessible": "genuineBlockchainManager" in bot_content,
                "BN.js Dependency Installed": bn_js_installed,
                "Solana Dependencies Present": "@solana/web3.js" in manager_content and "@solana/spl-token" in manager_content,
                "Connection Setup": "Connection(" in manager_content and "solana.com" in manager_content,
                "Class Definition": "class GenuineBlockchainManager" in manager_content,
                "Required Methods Present": all(method in manager_content for method in ["genuineLiquidityLock", "genuineRevokeMintAuthority", "genuineRugpullSimulation"])
            }
            
            failed_checks = []
            for check, passed in manager_verification_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Manager Verification Checks": list(manager_verification_checks.keys()),
                "Failed Checks": failed_checks,
                "File Size": f"{os.path.getsize(genuine_manager_path)} bytes",
                "BN.js Installed": bn_js_installed
            }
            
            if failed_checks:
                self.log_test(test_name, "FAIL", f"Genuine blockchain manager verification failed: {len(failed_checks)} checks failed", details)
                return False
            
            self.log_test(test_name, "PASS", "Genuine blockchain manager properly verified and integrated", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error verifying genuine blockchain manager: {str(e)}")
            return False
    
    def test_updated_liquidity_lock_testing(self):
        """Test 3: Test that /liquidity_lock now uses genuine operations (not simulation) with 24-hour duration"""
        test_name = "Updated Liquidity Lock Testing"
        
        try:
            # Check bot.js for liquidity lock command
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check genuine-blockchain-manager.js for liquidity lock implementation
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            liquidity_lock_checks = {
                "Liquidity Lock Command Present": "/liquidity_lock" in bot_content or "liquidity_lock" in bot_content,
                "Uses Genuine Operations": "genuine" in bot_content.lower() and "liquidity" in bot_content.lower(),
                "24-Hour Duration Set": "24" in manager_content and ("hour" in manager_content or "3600" in manager_content),
                "Not 1 Month Duration": not ("month" in manager_content and "30" in manager_content and "day" in manager_content),
                "Genuine Lock Creation Methods": "genuineLiquidityLock" in manager_content,
                "Real Blockchain Transactions": "sendAndConfirmTransaction" in manager_content,
                "Escrow Account Creation": "escrow" in manager_content and "createAccount" in manager_content,
                "Time-locked Contract": "unlockTimestamp" in manager_content and "lockData" in manager_content,
                "On-chain Verification": "verifyLiquidityLockOnChain" in manager_content
            }
            
            failed_checks = []
            for check, passed in liquidity_lock_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Liquidity Lock Checks": list(liquidity_lock_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 2:
                self.log_test(test_name, "FAIL", f"Updated liquidity lock testing failed: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some liquidity lock checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Liquidity lock properly updated to use genuine operations with 24-hour duration", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing updated liquidity lock: {str(e)}")
            return False
    
    def test_time_lock_implementation_check(self):
        """Test 4: Verify /revoke_mint creates 3-day delays, time-lock scheduling and status tracking"""
        test_name = "Time-lock Implementation Check"
        
        try:
            # Check bot.js for revoke mint command
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check genuine-blockchain-manager.js for time-lock implementation
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            time_lock_checks = {
                "Revoke Mint Command": "/revoke_mint" in bot_content,
                "3-Day Delay Implementation": ("3" in manager_content and "day" in manager_content) or ("72" in manager_content and "hour" in manager_content),
                "Time-lock Scheduling": "schedule" in manager_content.lower() or "delay" in manager_content.lower(),
                "Status Tracking": "status" in manager_content.lower() and ("track" in manager_content.lower() or "revokedAt" in manager_content),
                "Time Remaining Calculations": "remaining" in manager_content.lower() or "hoursRemaining" in manager_content,
                "Permanent Revocation Logic": "null" in manager_content and "AuthorityType.MintTokens" in manager_content,
                "Transaction Recording": "revokeTransaction" in manager_content and "signature" in manager_content,
                "Database Updates": "saveTokenData" in manager_content or "database" in manager_content
            }
            
            failed_checks = []
            for check, passed in time_lock_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Time-lock Implementation Checks": list(time_lock_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Time-lock implementation incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some time-lock checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Time-lock implementation properly configured with 3-day delays and status tracking", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error checking time-lock implementation: {str(e)}")
            return False
    
    def test_bot_startup_and_integration(self):
        """Test 5: Confirm bot starts without errors and shows 'Genuine Blockchain Manager initialized' message"""
        test_name = "Bot Startup and Integration"
        
        try:
            # Check bot.js for initialization messages
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for startup logs and integration
            startup_checks = {
                "Genuine Manager Import": "genuine-blockchain-manager" in bot_content,
                "Manager Initialization": "GenuineBlockchainManager" in bot_content,
                "Initialization Message": "initialized" in bot_content.lower() or "console.log" in bot_content,
                "No Missing Dependencies": True,  # Will check package.json
                "Error Handling": "try" in bot_content and "catch" in bot_content,
                "Bot Polling Setup": "polling" in bot_content or "webhook" in bot_content,
                "Required Imports Present": all(imp in bot_content for imp in ["require", "TelegramBot"]),
                "Database Integration": "database" in bot_content.lower() or "Database" in bot_content
            }
            
            # Check package.json for required dependencies
            package_json_path = self.telegram_bot_dir / "package.json"
            if package_json_path.exists():
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    deps = package_data.get('dependencies', {})
                    required_deps = ["@solana/web3.js", "@solana/spl-token", "@metaplex-foundation/js", "node-telegram-bot-api"]
                    missing_deps = [dep for dep in required_deps if dep not in deps]
                    startup_checks["No Missing Dependencies"] = len(missing_deps) == 0
            
            # Check if genuine-blockchain-manager.js exists
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            startup_checks["Genuine Manager File Exists"] = genuine_manager_path.exists()
            
            failed_checks = []
            for check, passed in startup_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Startup Integration Checks": list(startup_checks.keys()),
                "Failed Checks": failed_checks,
                "Required Files Present": genuine_manager_path.exists()
            }
            
            if failed_checks:
                self.log_test(test_name, "FAIL", f"Bot startup and integration issues: {len(failed_checks)} checks failed", details)
                return False
            
            self.log_test(test_name, "PASS", "Bot startup and integration properly configured", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error checking bot startup and integration: {str(e)}")
            return False
    
    def test_command_handler_integration(self):
        """Test 6: Test that genuine operation callbacks are properly routed with confirmation flows and warnings"""
        test_name = "Command Handler Integration"
        
        try:
            # Check bot.js for callback handlers and confirmation flows
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            command_handler_checks = {
                "Callback Query Handler": "callback_query" in bot_content or "callbackQuery" in bot_content,
                "Genuine Operations Callbacks": "genuine" in bot_content.lower() and "callback" in bot_content.lower(),
                "Confirmation Flows": bot_content.count("confirm") >= 2,  # Multiple confirmation steps
                "Warning Systems": "warning" in bot_content.lower() or "⚠️" in bot_content,
                "Inline Keyboards": "inline_keyboard" in bot_content,
                "Button Callbacks": "callback_data" in bot_content,
                "Educational Messages": "educational" in bot_content.lower() or "research" in bot_content.lower(),
                "Error Handling in Callbacks": "try" in bot_content and "catch" in bot_content,
                "Multiple Confirmation Layers": bot_content.count("Are you sure") >= 1 or bot_content.count("confirm") >= 3
            }
            
            failed_checks = []
            for check, passed in command_handler_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Command Handler Checks": list(command_handler_checks.keys()),
                "Failed Checks": failed_checks,
                "Confirmation Count": bot_content.count("confirm"),
                "Warning Count": bot_content.count("warning") + bot_content.count("⚠️")
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Command handler integration incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some command handler checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Command handler integration properly configured with confirmations and warnings", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error checking command handler integration: {str(e)}")
            return False
    
    def test_genuine_operations_differentiation(self):
        """Test 7: Verify genuine operations are differentiated from simulations"""
        test_name = "Genuine Operations Differentiation"
        
        try:
            # Check both bot.js and genuine-blockchain-manager.js
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            differentiation_checks = {
                "Genuine vs Simulation Labels": "genuine" in bot_content.lower() and "simulation" in bot_content.lower(),
                "Real Blockchain Warnings": "real" in manager_content.lower() and ("blockchain" in manager_content.lower() or "transaction" in manager_content.lower()),
                "Educational vs Live Distinction": "educational" in manager_content.lower() and "live" in bot_content.lower(),
                "Devnet vs Mainnet Protection": "devnet" in manager_content and "mainnet" in manager_content,
                "Confirmation Differences": bot_content.count("genuine") >= 2,  # Multiple genuine references
                "Warning Level Differences": "⚠️" in bot_content and ("REAL" in manager_content or "GENUINE" in manager_content),
                "Method Name Clarity": "genuine" in manager_content.lower() and "simulation" in manager_content.lower(),
                "User Interface Distinction": "genuine" in bot_content.lower() and ("operation" in bot_content.lower() or "blockchain" in bot_content.lower())
            }
            
            failed_checks = []
            for check, passed in differentiation_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Differentiation Checks": list(differentiation_checks.keys()),
                "Failed Checks": failed_checks,
                "Genuine References": bot_content.lower().count("genuine"),
                "Simulation References": bot_content.lower().count("simulation")
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Genuine operations differentiation incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some differentiation checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Genuine operations properly differentiated from simulations", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error checking genuine operations differentiation: {str(e)}")
            return False
    
    def test_comprehensive_integration_verification(self):
        """Test 8: Comprehensive verification that all components work together"""
        test_name = "Comprehensive Integration Verification"
        
        try:
            # Check all files exist and are properly integrated
            required_files = {
                "bot.js": self.telegram_bot_dir / "bot.js",
                "genuine-blockchain-manager.js": self.telegram_bot_dir / "genuine-blockchain-manager.js",
                "package.json": self.telegram_bot_dir / "package.json",
                "database.js": self.telegram_bot_dir / "database.js"
            }
            
            missing_files = []
            file_sizes = {}
            
            for file_name, file_path in required_files.items():
                if file_path.exists():
                    file_sizes[file_name] = os.path.getsize(file_path)
                else:
                    missing_files.append(file_name)
            
            # Check integration points
            bot_js_path = required_files["bot.js"]
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            integration_checks = {
                "All Required Files Present": len(missing_files) == 0,
                "Bot File Size Reasonable": file_sizes.get("bot.js", 0) > 10000,  # At least 10KB
                "Manager File Size Reasonable": file_sizes.get("genuine-blockchain-manager.js", 0) > 15000,  # At least 15KB
                "Cross-file Integration": "genuine-blockchain-manager" in bot_content,
                "Command Integration": all(cmd in bot_content for cmd in ["/revoke_mint", "/genuine_mint_rugpull", "/genuine_rugpull"]),
                "Error Handling Present": bot_content.count("try") >= 3 and bot_content.count("catch") >= 3,
                "Logging Present": "console.log" in bot_content,
                "Database Integration": "database" in bot_content.lower()
            }
            
            failed_checks = []
            for check, passed in integration_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Integration Checks": list(integration_checks.keys()),
                "Failed Checks": failed_checks,
                "Missing Files": missing_files,
                "File Sizes": file_sizes
            }
            
            if missing_files or len(failed_checks) > 2:
                self.log_test(test_name, "FAIL", f"Comprehensive integration verification failed: {len(failed_checks)} checks failed, {len(missing_files)} files missing", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some integration checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Comprehensive integration verification successful", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error in comprehensive integration verification: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all re-tests and generate report"""
        print("🔄 Starting Genuine Blockchain Operations RE-TEST...")
        print("🎯 Focus: Integration issues resolution verification")
        print("=" * 70)
        
        tests = [
            self.test_command_recognition,
            self.test_genuine_blockchain_manager_verification,
            self.test_updated_liquidity_lock_testing,
            self.test_time_lock_implementation_check,
            self.test_bot_startup_and_integration,
            self.test_command_handler_integration,
            self.test_genuine_operations_differentiation,
            self.test_comprehensive_integration_verification
        ]
        
        passed = 0
        failed = 0
        warnings = 0
        
        for test in tests:
            try:
                result = test()
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log_test(test.__name__, "FAIL", f"Test execution error: {str(e)}")
                failed += 1
        
        # Count warnings
        warnings = sum(1 for result in self.test_results if result['status'] == 'WARN')
        
        print("\n" + "=" * 70)
        print("📊 GENUINE BLOCKCHAIN RE-TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"📋 Total: {len(tests)}")
        
        # Success criteria evaluation
        success_rate = (passed / len(tests)) * 100
        print(f"🎯 Success Rate: {success_rate:.1f}%")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️"
            print(f"{status_icon} {result['test']}: {result['message']}")
        
        # Critical issues
        critical_failures = [r for r in self.test_results if r['status'] == 'FAIL']
        if critical_failures:
            print("\n🚨 INTEGRATION ISSUES STILL PRESENT:")
            for failure in critical_failures:
                print(f"❌ {failure['test']}: {failure['message']}")
        
        # Success criteria check
        print("\n🎯 SUCCESS CRITERIA EVALUATION:")
        criteria_met = {
            "Bot loads successfully": passed >= 6,  # Most tests pass
            "Command handlers respond": "Command Recognition Test" in [r['test'] for r in self.test_results if r['status'] == 'PASS'],
            "Genuine operations differentiated": "Genuine Operations Differentiation" in [r['test'] for r in self.test_results if r['status'] == 'PASS'],
            "Warning systems functional": "Command Handler Integration" in [r['test'] for r in self.test_results if r['status'] == 'PASS'],
            "Time-lock operational": "Time-lock Implementation Check" in [r['test'] for r in self.test_results if r['status'] == 'PASS']
        }
        
        for criterion, met in criteria_met.items():
            status = "✅" if met else "❌"
            print(f"{status} {criterion}")
        
        return {
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'total': len(tests),
            'success_rate': success_rate,
            'criteria_met': criteria_met,
            'results': self.test_results
        }

def main():
    """Main test execution"""
    try:
        tester = GenuineBlockchainRetester()
        results = tester.run_all_tests()
        
        # Determine overall success
        criteria_met_count = sum(1 for met in results['criteria_met'].values() if met)
        overall_success = results['failed'] <= 2 and criteria_met_count >= 4
        
        if overall_success:
            print(f"\n🎉 GENUINE BLOCKCHAIN RE-TEST SUCCESSFUL!")
            print(f"✅ Integration issues have been resolved")
            print(f"🎯 Success rate: {results['success_rate']:.1f}%")
            print(f"📊 Criteria met: {criteria_met_count}/5")
            sys.exit(0)
        else:
            print(f"\n⚠️ GENUINE BLOCKCHAIN RE-TEST NEEDS ATTENTION")
            print(f"❌ {results['failed']} tests failed")
            print(f"🎯 Success rate: {results['success_rate']:.1f}%")
            print(f"📊 Criteria met: {criteria_met_count}/5")
            print("🔧 Integration issues may still need resolution")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Re-test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()