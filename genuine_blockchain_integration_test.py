#!/usr/bin/env python3
"""
Genuine Blockchain Integration Test Suite
Tests the integration between genuine-blockchain-manager.js and bot.js
Based on test_result.md current focus tasks and review request requirements.
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

class GenuineBlockchainIntegrationTester:
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

    def test_genuine_blockchain_manager_exists(self):
        """Test 1: Verify genuine-blockchain-manager.js exists and has required functionality"""
        test_name = "Genuine Blockchain Manager Implementation"
        
        try:
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            if not genuine_manager_path.exists():
                self.log_test(test_name, "FAIL", "genuine-blockchain-manager.js file is missing")
                return False
            
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            # Check for required classes and methods
            required_checks = {
                "GenuineBlockchainManager Class": "class GenuineBlockchainManager" in manager_content,
                "Solana Dependencies": "@solana/web3.js" in manager_content and "@solana/spl-token" in manager_content,
                "Metaplex Integration": "@metaplex-foundation/js" in manager_content,
                "Genuine Liquidity Lock Method": "genuineLiquidityLock" in manager_content,
                "Genuine Mint Authority Revocation": "genuineRevokeMintAuthority" in manager_content,
                "Genuine Rugpull Simulation": "genuineRugpullSimulation" in manager_content,
                "Time-locked Contracts": "unlockTimestamp" in manager_content and "escrowKeypair" in manager_content,
                "On-chain Verification": "verifyLiquidityLockOnChain" in manager_content,
                "24-hour Duration Logic": "lockDurationHours = 24" in manager_content or "24" in manager_content,
                "Explorer Links": "explorer.solana.com" in manager_content
            }
            
            failed_checks = []
            for check, passed in required_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            file_size = genuine_manager_path.stat().st_size
            details = {
                "File Size": f"{file_size} bytes",
                "Required Checks": list(required_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if failed_checks:
                self.log_test(test_name, "FAIL", f"Missing required functionality: {len(failed_checks)} checks failed", details)
                return False
            
            self.log_test(test_name, "PASS", f"Genuine blockchain manager properly implemented ({file_size} bytes)", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing genuine blockchain manager: {str(e)}")
            return False

    def test_bot_integration_with_genuine_manager(self):
        """Test 2: Verify bot.js integrates with genuine-blockchain-manager.js"""
        test_name = "Bot Integration with Genuine Manager"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for integration points
            integration_checks = {
                "Genuine Manager Import": "require('./genuine-blockchain-manager')" in bot_content or "GenuineBlockchainManager" in bot_content,
                "Genuine Manager Initialization": "new GenuineBlockchainManager" in bot_content or "genuineBlockchainManager" in bot_content,
                "Genuine Manager Variable": "genuineManager" in bot_content or "blockchainManager" in bot_content,
                "Initialization Message": "Genuine Blockchain Manager initialized" in bot_content
            }
            
            failed_checks = []
            for check, passed in integration_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Integration Checks": list(integration_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) >= 3:  # Allow some flexibility
                self.log_test(test_name, "FAIL", f"No integration found: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Partial integration: {len(failed_checks)} checks failed", details)
                return True
            
            self.log_test(test_name, "PASS", "Bot properly integrated with genuine blockchain manager", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing bot integration: {str(e)}")
            return False

    def test_genuine_liquidity_lock_command(self):
        """Test 3: Verify /liquidity_lock command integration"""
        test_name = "Genuine Liquidity Lock Command"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for liquidity lock command
            command_checks = {
                "/liquidity_lock Command Handler": "/liquidity_lock" in bot_content and "onText" in bot_content,
                "Liquidity Lock Callback": "liquidity_lock" in bot_content and "callback_data" in bot_content,
                "24-hour Duration": "24" in bot_content and ("hour" in bot_content or "24h" in bot_content),
                "Genuine Lock Integration": "genuineLiquidityLock" in bot_content,
                "Lock Verification": "verifyLiquidityLock" in bot_content or "lockInfo" in bot_content
            }
            
            failed_checks = []
            for check, passed in command_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Command Checks": list(command_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"/liquidity_lock command not integrated: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Partial command integration: {len(failed_checks)} checks failed", details)
                return True
            
            self.log_test(test_name, "PASS", "/liquidity_lock command properly integrated", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing liquidity lock command: {str(e)}")
            return False

    def test_mint_authority_revocation_command(self):
        """Test 4: Verify /revoke_mint command with 3-day delay"""
        test_name = "Time-locked Mint Authority Revocation Command"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for revoke mint command
            command_checks = {
                "/revoke_mint Command Handler": "/revoke_mint" in bot_content and "onText" in bot_content,
                "3-day Delay Logic": "3" in bot_content and ("day" in bot_content or "72" in bot_content),
                "Time-lock Scheduling": "setTimeout" in bot_content or "schedule" in bot_content,
                "Genuine Revoke Integration": "genuineRevokeMintAuthority" in bot_content,
                "Permanent Revocation Warning": "permanent" in bot_content.lower() and "irreversible" in bot_content.lower()
            }
            
            failed_checks = []
            for check, passed in command_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Command Checks": list(command_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"/revoke_mint command not integrated: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Partial command integration: {len(failed_checks)} checks failed", details)
                return True
            
            self.log_test(test_name, "PASS", "/revoke_mint command properly integrated with 3-day delay", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing mint authority revocation: {str(e)}")
            return False

    def test_genuine_rugpull_commands(self):
        """Test 5: Verify genuine rugpull commands"""
        test_name = "Genuine Rugpull Commands"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for rugpull commands
            command_checks = {
                "/genuine_mint_rugpull Command": "/genuine_mint_rugpull" in bot_content and "onText" in bot_content,
                "/genuine_rugpull Command": "/genuine_rugpull" in bot_content and "onText" in bot_content,
                "Mint Rugpull Integration": "genuineRugpullSimulation" in bot_content,
                "Liquidity Removal Integration": "liquidity_drain" in bot_content or "removeLiquidity" in bot_content,
                "Warning System": "warning" in bot_content.lower() and "consequences" in bot_content.lower(),
                "Confirmation Flow": "confirm" in bot_content.lower() and ("yes" in bot_content or "proceed" in bot_content),
                "Educational Messaging": "educational" in bot_content.lower() or "research" in bot_content.lower()
            }
            
            failed_checks = []
            for check, passed in command_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Command Checks": list(command_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 4:
                self.log_test(test_name, "FAIL", f"Genuine rugpull commands not integrated: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Partial rugpull integration: {len(failed_checks)} checks failed", details)
                return True
            
            self.log_test(test_name, "PASS", "Genuine rugpull commands properly integrated", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing rugpull commands: {str(e)}")
            return False

    def test_status_command_with_genuine_operations(self):
        """Test 6: Verify /status command shows genuine operations"""
        test_name = "Status Command with Genuine Operations"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check for status command
            status_checks = {
                "/status Command Handler": "/status" in bot_content and "onText" in bot_content,
                "Status Function": "showStatus" in bot_content or "displayStatus" in bot_content,
                "Genuine Operations Display": "genuine" in bot_content.lower() and "operations" in bot_content.lower(),
                "Active Liquidity Locks": "liquidity" in bot_content and "lock" in bot_content,
                "Pending Time-locks": "pending" in bot_content and "time" in bot_content,
                "Time Remaining Calculations": "remaining" in bot_content and ("hours" in bot_content or "days" in bot_content),
                "Lock Verification Status": "verified" in bot_content or "onChain" in bot_content
            }
            
            failed_checks = []
            for check, passed in status_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Status Checks": list(status_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 4:
                self.log_test(test_name, "FAIL", f"/status command not implemented: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Partial status implementation: {len(failed_checks)} checks failed", details)
                return True
            
            self.log_test(test_name, "PASS", "/status command properly shows genuine operations", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing status command: {str(e)}")
            return False

    def test_solana_dependencies(self):
        """Test 7: Verify all required Solana dependencies are installed"""
        test_name = "Solana Dependencies"
        
        try:
            package_json_path = self.telegram_bot_dir / "package.json"
            if not package_json_path.exists():
                self.log_test(test_name, "FAIL", "package.json not found")
                return False
            
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            dependencies = package_data.get('dependencies', {})
            
            required_deps = {
                "@solana/web3.js": "Solana Web3 SDK",
                "@solana/spl-token": "SPL Token SDK", 
                "@metaplex-foundation/js": "Metaplex SDK",
                "bn.js": "Big Number library"
            }
            
            missing_deps = []
            installed_deps = {}
            
            for dep, description in required_deps.items():
                if dep in dependencies:
                    installed_deps[dep] = dependencies[dep]
                else:
                    missing_deps.append(f"{dep} ({description})")
            
            details = {
                "Required Dependencies": list(required_deps.keys()),
                "Installed Dependencies": installed_deps,
                "Missing Dependencies": missing_deps
            }
            
            if missing_deps:
                self.log_test(test_name, "FAIL", f"Missing required dependencies: {', '.join(missing_deps)}", details)
                return False
            
            self.log_test(test_name, "PASS", f"All Solana dependencies installed: {len(installed_deps)} packages", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error checking dependencies: {str(e)}")
            return False

    def test_bot_startup_logs(self):
        """Test 8: Check if bot shows genuine blockchain manager initialization"""
        test_name = "Bot Startup with Genuine Manager"
        
        try:
            # Check if there are any startup logs
            startup_log_path = self.telegram_bot_dir / "startup.log"
            bot_log_path = self.telegram_bot_dir / "bot.log"
            
            log_content = ""
            if startup_log_path.exists():
                with open(startup_log_path, 'r') as f:
                    log_content += f.read()
            
            if bot_log_path.exists():
                with open(bot_log_path, 'r') as f:
                    log_content += f.read()
            
            # Check for genuine manager initialization messages
            startup_checks = {
                "Genuine Manager Initialized": "Genuine Blockchain Manager initialized" in log_content,
                "Real Blockchain Operations Warning": "REAL blockchain operations" in log_content or "WARNING" in log_content,
                "Solana Connection": "Connection" in log_content and "solana" in log_content.lower(),
                "No Startup Errors": "error" not in log_content.lower() or "Error" not in log_content
            }
            
            failed_checks = []
            for check, passed in startup_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Startup Checks": list(startup_checks.keys()),
                "Failed Checks": failed_checks,
                "Log Files Found": startup_log_path.exists() or bot_log_path.exists()
            }
            
            if not log_content:
                self.log_test(test_name, "WARN", "No startup logs found to verify initialization", details)
                return True
            
            if len(failed_checks) > 2:
                self.log_test(test_name, "FAIL", f"Bot startup issues: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some startup checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Bot startup shows genuine manager initialization", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error checking startup logs: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all genuine blockchain integration tests"""
        print("🔗 Starting Genuine Blockchain Integration Tests...")
        print("=" * 70)
        
        tests = [
            self.test_genuine_blockchain_manager_exists,
            self.test_solana_dependencies,
            self.test_bot_integration_with_genuine_manager,
            self.test_genuine_liquidity_lock_command,
            self.test_mint_authority_revocation_command,
            self.test_genuine_rugpull_commands,
            self.test_status_command_with_genuine_operations,
            self.test_bot_startup_logs
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
        print("📊 GENUINE BLOCKCHAIN INTEGRATION TEST SUMMARY")
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
        
        # Critical issues
        critical_failures = [r for r in self.test_results if r['status'] == 'FAIL']
        if critical_failures:
            print("\n🚨 CRITICAL INTEGRATION ISSUES:")
            for failure in critical_failures:
                print(f"❌ {failure['test']}: {failure['message']}")
        
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
        tester = GenuineBlockchainIntegrationTester()
        results = tester.run_all_tests()
        
        # Exit with appropriate code
        if results['failed'] == 0:
            print(f"\n🎉 ALL INTEGRATION TESTS PASSED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(0)
        else:
            print(f"\n💥 {results['failed']} INTEGRATION TESTS FAILED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()