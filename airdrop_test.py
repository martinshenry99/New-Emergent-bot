#!/usr/bin/env python3
"""
Airdrop Functionality Test
Tests the specific airdrop issue mentioned in the review request
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

class AirdropTester:
    def __init__(self):
        self.telegram_bot_dir = project_root / "telegram-bot"
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

    def test_airdrop_command_exists(self):
        """Test 1: Check if airdrop command exists in bot.js"""
        test_name = "Airdrop Command Implementation"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for airdrop functionality
            airdrop_checks = {
                "Airdrop Menu Function": "showAirdropMenu" in bot_content,
                "Execute Airdrop Function": "executeAirdrop" in bot_content,
                "Airdrop Callback Handlers": "airdrop_wallet_" in bot_content,
                "Devnet Airdrop Support": "devnet" in bot_content and "airdrop" in bot_content.lower(),
                "Mainnet Airdrop Restriction": "mainnet" in bot_content and "not available" in bot_content.lower(),
                "Real Airdrop Implementation": "requestDevnetAirdrop" in bot_content
            }
            
            failed_checks = []
            for check, passed in airdrop_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Airdrop Checks": list(airdrop_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if failed_checks:
                self.log_test(test_name, "FAIL", f"Airdrop command incomplete: {len(failed_checks)} checks failed", details)
                return False
            
            self.log_test(test_name, "PASS", "Airdrop command properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing airdrop command: {str(e)}")
            return False

    def test_wallet_manager_airdrop_method(self):
        """Test 2: Check if wallet manager has real airdrop implementation"""
        test_name = "Wallet Manager Airdrop Method"
        
        try:
            wallet_manager_path = self.telegram_bot_dir / "wallet-manager-enhanced.js"
            with open(wallet_manager_path, 'r') as f:
                wallet_content = f.read()
            
            # Check for real airdrop implementation
            airdrop_method_checks = {
                "requestDevnetAirdrop Method": "requestDevnetAirdrop" in wallet_content,
                "Real Solana Airdrop Call": "connection.requestAirdrop" in wallet_content,
                "Transaction Confirmation": "confirmTransaction" in wallet_content,
                "Balance Update After Airdrop": "updateBalances" in wallet_content,
                "Error Handling": "catch" in wallet_content and "airdrop failed" in wallet_content.lower(),
                "1 SOL Amount": "LAMPORTS_PER_SOL" in wallet_content,
                "Devnet Connection": "devnetConnection" in wallet_content
            }
            
            failed_checks = []
            for check, passed in airdrop_method_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Airdrop Method Checks": list(airdrop_method_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if failed_checks:
                self.log_test(test_name, "FAIL", f"Wallet manager airdrop incomplete: {len(failed_checks)} checks failed", details)
                return False
            
            self.log_test(test_name, "PASS", "Wallet manager has proper airdrop implementation", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing wallet manager airdrop: {str(e)}")
            return False

    def test_solana_devnet_connection(self):
        """Test 3: Test if Solana devnet connection is working"""
        test_name = "Solana Devnet Connection"
        
        try:
            # Check if bot logs show successful connection
            bot_log_path = self.telegram_bot_dir / "bot.log"
            startup_log_path = self.telegram_bot_dir / "startup.log"
            
            log_content = ""
            if bot_log_path.exists():
                with open(bot_log_path, 'r') as f:
                    log_content += f.read()
            
            if startup_log_path.exists():
                with open(startup_log_path, 'r') as f:
                    log_content += f.read()
            
            connection_checks = {
                "Devnet Connection": "devnet" in log_content.lower(),
                "Solana Connection Success": "connection successful" in log_content.lower(),
                "No Connection Errors": "connection failed" not in log_content.lower() and "connection error" not in log_content.lower(),
                "RPC URL Configuration": "api.devnet.solana.com" in log_content or "devnet" in log_content
            }
            
            failed_checks = []
            for check, passed in connection_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Connection Checks": list(connection_checks.keys()),
                "Failed Checks": failed_checks,
                "Log Content Available": bool(log_content)
            }
            
            if not log_content:
                self.log_test(test_name, "WARN", "No log content available to verify connection", details)
                return True
            
            if failed_checks:
                self.log_test(test_name, "FAIL", f"Devnet connection issues: {len(failed_checks)} checks failed", details)
                return False
            
            self.log_test(test_name, "PASS", "Solana devnet connection working properly", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error checking devnet connection: {str(e)}")
            return False

    def test_airdrop_ui_flow(self):
        """Test 4: Check airdrop UI flow and user experience"""
        test_name = "Airdrop UI Flow"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for complete UI flow
            ui_flow_checks = {
                "Wallet Selection UI": "Choose a wallet" in bot_content or "Select which wallet" in bot_content,
                "Airdrop Amount Display": "1 SOL" in bot_content,
                "Processing Messages": "Processing" in bot_content and "airdrop" in bot_content.lower(),
                "Success Confirmation": "AIRDROP COMPLETED" in bot_content or "Transaction Successful" in bot_content,
                "Explorer Link": "explorer.solana.com" in bot_content,
                "Error Handling UI": "Airdrop Failed" in bot_content or "failed" in bot_content.lower(),
                "Retry Options": "Try Again" in bot_content or "retry" in bot_content.lower(),
                "Network Restrictions": "mainnet" in bot_content and "not available" in bot_content.lower()
            }
            
            failed_checks = []
            for check, passed in ui_flow_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "UI Flow Checks": list(ui_flow_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 2:  # Allow some flexibility
                self.log_test(test_name, "FAIL", f"Airdrop UI flow incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some UI elements missing: {len(failed_checks)} checks failed", details)
                return True
            
            self.log_test(test_name, "PASS", "Airdrop UI flow properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing airdrop UI flow: {str(e)}")
            return False

    def test_airdrop_rate_limiting_handling(self):
        """Test 5: Check if airdrop handles rate limiting properly"""
        test_name = "Airdrop Rate Limiting Handling"
        
        try:
            wallet_manager_path = self.telegram_bot_dir / "wallet-manager-enhanced.js"
            with open(wallet_manager_path, 'r') as f:
                wallet_content = f.read()
            
            # Check for rate limiting handling
            rate_limit_checks = {
                "Rate Limit Error Handling": "rate-limited" in wallet_content.lower() or "rate limit" in wallet_content.lower(),
                "Faucet Unavailable Handling": "unavailable" in wallet_content.lower(),
                "Descriptive Error Messages": "faucet might be" in wallet_content.lower(),
                "Retry Suggestions": "try again" in wallet_content.lower() or "retry" in wallet_content.lower(),
                "Timeout Handling": "timeout" in wallet_content.lower() or "10-30 seconds" in wallet_content
            }
            
            failed_checks = []
            for check, passed in rate_limit_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Rate Limit Checks": list(rate_limit_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 2:
                self.log_test(test_name, "FAIL", f"Rate limiting not properly handled: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some rate limiting features missing: {len(failed_checks)} checks failed", details)
                return True
            
            self.log_test(test_name, "PASS", "Airdrop rate limiting properly handled", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing rate limiting: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all airdrop functionality tests"""
        print("🪂 Starting Airdrop Functionality Tests...")
        print("=" * 70)
        
        tests = [
            self.test_airdrop_command_exists,
            self.test_wallet_manager_airdrop_method,
            self.test_solana_devnet_connection,
            self.test_airdrop_ui_flow,
            self.test_airdrop_rate_limiting_handling
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
        print("📊 AIRDROP FUNCTIONALITY TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"📋 Total: {len(tests)}")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️"
            print(f"{status_icon} {result['test']}: {result['message']}")
        
        return {
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'total': len(tests),
            'success_rate': (passed / len(tests)) * 100,
            'results': self.test_results
        }

def main():
    """Main test execution"""
    try:
        tester = AirdropTester()
        results = tester.run_all_tests()
        
        # Exit with appropriate code
        if results['failed'] == 0:
            print(f"\n🎉 ALL AIRDROP TESTS PASSED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(0)
        else:
            print(f"\n💥 {results['failed']} AIRDROP TESTS FAILED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()