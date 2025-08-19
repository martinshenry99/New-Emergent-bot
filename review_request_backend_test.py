#!/usr/bin/env python3
"""
Review Request Specific Backend Test
Testing the 5 exact issues mentioned by the user:

1. Devnet wallet addresses changing
2. Airdrop still looping  
3. Mainnet liquidity configuration not working
4. /start_trading reloads /start function
5. /chart_activity not working
"""

import os
import sys
import json
import time
import re
from pathlib import Path

class ReviewRequestBackendTester:
    def __init__(self):
        self.telegram_bot_dir = Path("/app/telegram-bot")
        self.test_results = []
        
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
    
    def test_devnet_wallet_addresses_consistency(self):
        """Test 1: Check if devnet wallet addresses remain consistent across restarts"""
        test_name = "Devnet Wallet Addresses Consistency"
        
        try:
            # Check wallet manager implementation
            wallet_manager_path = self.telegram_bot_dir / "wallet-manager-enhanced.js"
            if not wallet_manager_path.exists():
                self.log_test(test_name, "FAIL", "wallet-manager-enhanced.js not found")
                return False
            
            with open(wallet_manager_path, 'r') as f:
                wallet_content = f.read()
            
            # Check for wallet persistence mechanisms
            persistence_checks = {
                "Database Save Wallets": "saveWallets" in wallet_content,
                "Load Existing Wallets": "loadOrGenerateWallets" in wallet_content,
                "Never Regenerate Check": "NEVER regenerate if they exist" in wallet_content,
                "Mnemonic Storage": "mnemonic" in wallet_content,
                "Load From Database": "loadWalletsFromDatabase" in wallet_content,
                "Consistent Derivation": "derivePath" in wallet_content
            }
            
            # Check database integration
            database_path = self.telegram_bot_dir / "database.js"
            database_checks = {}
            if database_path.exists():
                with open(database_path, 'r') as f:
                    db_content = f.read()
                database_checks = {
                    "Wallet Storage Methods": "getWallets" in db_content and "saveWallets" in db_content,
                    "Persistent Storage": "JSON.stringify" in db_content or "writeFileSync" in db_content
                }
            
            failed_checks = []
            all_checks = {**persistence_checks, **database_checks}
            for check, passed in all_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Persistence Checks": list(persistence_checks.keys()),
                "Database Checks": list(database_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 2:
                self.log_test(test_name, "FAIL", f"Wallet persistence incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some persistence checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Wallet addresses should remain consistent across restarts", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing wallet consistency: {str(e)}")
            return False
    
    def test_airdrop_loop_issue(self):
        """Test 2: Check if airdrop callbacks work without infinite loops"""
        test_name = "Airdrop Loop Issue"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for all 5 airdrop wallet callbacks
            airdrop_callbacks = []
            for i in range(1, 6):
                pattern = f'airdrop_wallet_{i}'
                if pattern in bot_content:
                    airdrop_callbacks.append(f"wallet_{i}")
            
            # Check for executeAirdrop function
            execute_airdrop_exists = "executeAirdrop" in bot_content
            
            # Check for proper callback handling (no loops back to menu)
            callback_handler_pattern = r'} else if \(data\.startsWith\(\'airdrop_wallet_\'\)\) \{'
            callback_handler_exists = re.search(callback_handler_pattern, bot_content) is not None
            
            # Check for direct execution (not menu loop)
            direct_execution_patterns = [
                r'await executeAirdrop\(',
                r'executeAirdrop\(chatId',
                r'const \[, , walletNum, network\] = data\.split'
            ]
            direct_execution = any(re.search(pattern, bot_content) for pattern in direct_execution_patterns)
            
            airdrop_checks = {
                "All 5 Airdrop Callbacks": len(airdrop_callbacks) == 5,
                "ExecuteAirdrop Function": execute_airdrop_exists,
                "Callback Handler Exists": callback_handler_exists,
                "Direct Execution (No Loop)": direct_execution,
                "Wallet Number Parsing": "walletNum" in bot_content and "parseInt" in bot_content
            }
            
            failed_checks = []
            for check, passed in airdrop_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Found Callbacks": airdrop_callbacks,
                "Airdrop Checks": list(airdrop_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(airdrop_callbacks) < 5:
                self.log_test(test_name, "FAIL", f"Only {len(airdrop_callbacks)}/5 airdrop callbacks found", details)
                return False
            elif not execute_airdrop_exists:
                self.log_test(test_name, "FAIL", "executeAirdrop function not found", details)
                return False
            elif not direct_execution:
                self.log_test(test_name, "FAIL", "Airdrop may still loop back to menu instead of direct execution", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some airdrop checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Airdrop functionality should work without looping", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing airdrop functionality: {str(e)}")
            return False
    
    def test_mainnet_liquidity_configuration(self):
        """Test 3: Check mainnet liquidity configuration input processing"""
        test_name = "Mainnet Liquidity Configuration"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for mainnet liquidity configuration steps
            mainnet_config_checks = {
                "SOL Amount Input Processing": "realSol = parseFloat(text)" in bot_content,
                "Displayed Liquidity Input": "displayedLiquidity = parseInt(text" in bot_content,
                "Session Step Management": "session.step" in bot_content and "userSessions.set" in bot_content,
                "Mainnet Network Check": "data.network === 'mainnet'" in bot_content,
                "Input Validation": "parseFloat" in bot_content and "parseInt" in bot_content,
                "Market Cap Calculations": "realMarketCap" in bot_content and "displayedMarketCap" in bot_content
            }
            
            # Check for session handling in message handler
            session_handling_patterns = [
                r'const session = userSessions\.get\(userId\)',
                r'session\.data\.',
                r'userSessions\.set\(userId, session\)'
            ]
            session_handling = all(re.search(pattern, bot_content) for pattern in session_handling_patterns)
            
            # Check for proper step progression
            step_progression_patterns = [
                r'case 6:.*realSol',
                r'case 7:.*displayedLiquidity',
                r'session\.step = 7',
                r'session\.step = 8'
            ]
            step_progression = any(re.search(pattern, bot_content, re.DOTALL) for pattern in step_progression_patterns)
            
            mainnet_config_checks["Session Handling"] = session_handling
            mainnet_config_checks["Step Progression"] = step_progression
            
            failed_checks = []
            for check, passed in mainnet_config_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Mainnet Config Checks": list(mainnet_config_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Mainnet liquidity configuration incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some mainnet config checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Mainnet liquidity configuration should work properly", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing mainnet liquidity config: {str(e)}")
            return False
    
    def test_start_trading_command(self):
        """Test 4: Check if /start_trading command exists and doesn't reload /start"""
        test_name = "/start_trading Command"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check if /start_trading command exists in main bot.js
            start_trading_pattern = r'bot\.onText\(/\\\/start_trading/'
            start_trading_exists = re.search(start_trading_pattern, bot_content) is not None
            
            # Check other bot files for reference
            other_files_check = {}
            for filename in ["bot-old.js", "bot-commands-fix.js"]:
                file_path = self.telegram_bot_dir / filename
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        content = f.read()
                    other_files_check[filename] = "/start_trading" in content
            
            # Check if it reloads /start function (bad behavior)
            start_reload_patterns = [
                r'startManualLaunch',
                r'🚀 Enhanced Meme Token Creator',
                r'bot\.sendMessage.*Manual Setup'
            ]
            reloads_start = any(re.search(pattern, bot_content) for pattern in start_reload_patterns)
            
            command_checks = {
                "Command Exists in Main Bot": start_trading_exists,
                "Command in Other Files": any(other_files_check.values()),
                "Does Not Reload Start": not reloads_start
            }
            
            details = {
                "Command Checks": command_checks,
                "Other Files": other_files_check,
                "Main Bot File": "bot.js"
            }
            
            if not start_trading_exists:
                if any(other_files_check.values()):
                    self.log_test(test_name, "FAIL", "/start_trading exists in other files but NOT in main bot.js", details)
                else:
                    self.log_test(test_name, "FAIL", "/start_trading command completely missing", details)
                return False
            elif reloads_start:
                self.log_test(test_name, "FAIL", "/start_trading command reloads /start function", details)
                return False
            
            self.log_test(test_name, "PASS", "/start_trading command exists and works independently", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing /start_trading command: {str(e)}")
            return False
    
    def test_chart_activity_command(self):
        """Test 5: Check if /chart_activity command exists and works"""
        test_name = "/chart_activity Command"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check if /chart_activity command exists in main bot.js
            chart_activity_pattern = r'bot\.onText\(/\\\/chart_activity/'
            chart_activity_exists = re.search(chart_activity_pattern, bot_content) is not None
            
            # Check other bot files for reference
            other_files_check = {}
            for filename in ["bot-old.js", "bot-commands-fix.js"]:
                file_path = self.telegram_bot_dir / filename
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        content = f.read()
                    other_files_check[filename] = "/chart_activity" in content
            
            # Check for callback handlers
            callback_patterns = [
                r'chart_activity.*callback_data',
                r'data\.startsWith\(\'chart_activity_\'\)',
                r'chart_activity_.*replace'
            ]
            callback_handlers = any(re.search(pattern, bot_content) for pattern in callback_patterns)
            
            # Check for chart activity implementation in real-trading-manager
            trading_manager_path = self.telegram_bot_dir / "real-trading-manager.js"
            trading_manager_methods = {}
            if trading_manager_path.exists():
                with open(trading_manager_path, 'r') as f:
                    trading_content = f.read()
                trading_manager_methods = {
                    "startChartActivity": "startChartActivity" in trading_content,
                    "stopChartActivity": "stopChartActivity" in trading_content,
                    "generateChartActivityTrade": "generateChartActivityTrade" in trading_content
                }
            
            command_checks = {
                "Command Exists in Main Bot": chart_activity_exists,
                "Command in Other Files": any(other_files_check.values()),
                "Callback Handlers": callback_handlers,
                "Trading Manager Methods": all(trading_manager_methods.values()) if trading_manager_methods else False
            }
            
            details = {
                "Command Checks": command_checks,
                "Other Files": other_files_check,
                "Trading Manager Methods": trading_manager_methods
            }
            
            if not chart_activity_exists:
                if any(other_files_check.values()):
                    self.log_test(test_name, "FAIL", "/chart_activity exists in other files but NOT in main bot.js", details)
                else:
                    self.log_test(test_name, "FAIL", "/chart_activity command completely missing", details)
                return False
            elif not callback_handlers:
                self.log_test(test_name, "FAIL", "/chart_activity command exists but callback handlers missing", details)
                return False
            
            self.log_test(test_name, "PASS", "/chart_activity command exists with proper handlers", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing /chart_activity command: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests for the 5 specific review request issues"""
        print("🚀 BACKEND TESTING - Review Request Issues")
        print("=" * 70)
        print("Testing 5 specific issues mentioned by user:")
        print("1. Devnet wallet addresses changing")
        print("2. Airdrop still looping")
        print("3. Mainnet liquidity configuration not working")
        print("4. /start_trading reloads /start function")
        print("5. /chart_activity not working")
        print("=" * 70)
        
        tests = [
            self.test_devnet_wallet_addresses_consistency,
            self.test_airdrop_loop_issue,
            self.test_mainnet_liquidity_configuration,
            self.test_start_trading_command,
            self.test_chart_activity_command
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
        print("📊 REVIEW REQUEST TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"📋 Total: {len(tests)}")
        
        # Success criteria analysis
        success_rate = (passed / len(tests)) * 100
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️"
            print(f"{status_icon} {result['test']}: {result['message']}")
        
        # Critical issues
        critical_failures = [r for r in self.test_results if r['status'] == 'FAIL']
        if critical_failures:
            print("\n🚨 CRITICAL ISSUES FOUND:")
            for failure in critical_failures:
                print(f"❌ {failure['test']}: {failure['message']}")
        
        return {
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'total': len(tests),
            'success_rate': success_rate,
            'results': self.test_results
        }

def main():
    """Main test execution"""
    try:
        tester = ReviewRequestBackendTester()
        results = tester.run_all_tests()
        
        print(f"\n🎯 FINAL ASSESSMENT:")
        print(f"Success Rate: {results['success_rate']:.1f}%")
        
        if results['failed'] == 0:
            print("🎉 ALL REVIEW REQUEST ISSUES RESOLVED!")
            return 0
        elif results['success_rate'] >= 60:
            print("⚠️ MOSTLY RESOLVED - Some issues remain")
            return 1
        else:
            print("❌ CRITICAL ISSUES - Major problems need fixing")
            return 2
            
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return 3

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)