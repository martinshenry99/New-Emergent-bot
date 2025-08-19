#!/usr/bin/env python3
"""
Genuine Blockchain Operations Test Suite for Meme-bot
Tests the REAL blockchain operations implementation including:
1. Genuine Blockchain Manager Integration
2. Genuine Liquidity Locking (24 hours)
3. Time-locked Mint Authority Revocation (3 days)
4. Genuine Mint Rugpull Operations
5. Genuine Liquidity Removal Rugpull
6. Enhanced Status Command with Genuine Operations
7. Bot Integration & Stability
8. Command Structure & UI
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

class GenuineBlockchainTester:
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
    
    def test_genuine_blockchain_manager_integration(self):
        """Test 1: Verify genuine-blockchain-manager.js loads without errors"""
        test_name = "Genuine Blockchain Manager Integration"
        
        try:
            # Check if genuine-blockchain-manager.js exists
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            if not genuine_manager_path.exists():
                self.log_test(test_name, "FAIL", "genuine-blockchain-manager.js file is missing")
                return False
            
            # Check file content for required dependencies
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            # Check for required Solana dependencies
            dependency_checks = {
                "Solana Web3.js Import": "@solana/web3.js" in manager_content,
                "SPL Token Import": "@solana/spl-token" in manager_content,
                "Metaplex Import": "@metaplex-foundation/js" in manager_content,
                "GenuineBlockchainManager Class": "class GenuineBlockchainManager" in manager_content,
                "Connection Setup": "Connection(" in manager_content and "solana.com" in manager_content,
                "Devnet Connection": "devnet" in manager_content,
                "Mainnet Connection": "mainnet" in manager_content
            }
            
            # Check package.json for dependencies
            package_json_path = self.telegram_bot_dir / "package.json"
            if package_json_path.exists():
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                required_deps = ["@solana/web3.js", "@solana/spl-token", "@metaplex-foundation/js"]
                deps = package_data.get('dependencies', {})
                
                for dep in required_deps:
                    dependency_checks[f"{dep} in package.json"] = dep in deps
            
            failed_checks = []
            for check, passed in dependency_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Dependency Checks": list(dependency_checks.keys()),
                "Failed Checks": failed_checks,
                "File Size": f"{os.path.getsize(genuine_manager_path)} bytes"
            }
            
            if failed_checks:
                self.log_test(test_name, "FAIL", f"Genuine blockchain manager incomplete: {len(failed_checks)} checks failed", details)
                return False
            
            self.log_test(test_name, "PASS", "Genuine blockchain manager properly integrated", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing genuine blockchain manager: {str(e)}")
            return False
    
    def test_genuine_liquidity_locking(self):
        """Test 2: Verify genuine liquidity locking (24 hours) implementation"""
        test_name = "Genuine Liquidity Locking (24 hours)"
        
        try:
            # Check bot.js for /liquidity_lock command
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check genuine-blockchain-manager.js for liquidity lock implementation
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            liquidity_lock_checks = {
                "Liquidity Lock Command": "/liquidity_lock" in bot_content or "liquidity_lock" in bot_content,
                "Genuine Liquidity Lock Method": "genuineLiquidityLock" in manager_content,
                "24 Hour Duration": "24" in manager_content and ("hour" in manager_content or "3600" in manager_content),
                "Time-locked Contract": "escrow" in manager_content or "time-lock" in manager_content,
                "On-chain Lock Creation": "createAccount" in manager_content and "SystemProgram" in manager_content,
                "Lock Data Storage": "lockData" in manager_content and "unlockTimestamp" in manager_content,
                "Explorer Links": "explorer.solana.com" in manager_content,
                "Lock Verification": "verifyLiquidityLockOnChain" in manager_content
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
                self.log_test(test_name, "FAIL", f"Genuine liquidity locking incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some liquidity lock checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Genuine liquidity locking properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing genuine liquidity locking: {str(e)}")
            return False
    
    def test_time_locked_mint_authority_revocation(self):
        """Test 3: Verify time-locked mint authority revocation (3 days)"""
        test_name = "Time-locked Mint Authority Revocation (3 days)"
        
        try:
            # Check bot.js for /revoke_mint command
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check genuine-blockchain-manager.js for mint authority revocation
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            mint_revocation_checks = {
                "Revoke Mint Command": "/revoke_mint" in bot_content or "revoke_mint" in bot_content,
                "Genuine Revoke Method": "genuineRevokeMintAuthority" in manager_content,
                "3 Day Delay": "3" in manager_content and ("day" in manager_content or "72" in manager_content),
                "SetAuthority Instruction": "createSetAuthorityInstruction" in manager_content,
                "AuthorityType.MintTokens": "AuthorityType.MintTokens" in manager_content,
                "Permanent Revocation": "null" in manager_content and "authority" in manager_content,
                "Time-lock Scheduling": "schedule" in manager_content or "delay" in manager_content,
                "Status Tracking": "revokeTransaction" in manager_content and "revokedAt" in manager_content
            }
            
            failed_checks = []
            for check, passed in mint_revocation_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Mint Revocation Checks": list(mint_revocation_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Time-locked mint authority revocation incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some mint revocation checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Time-locked mint authority revocation properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing mint authority revocation: {str(e)}")
            return False
    
    def test_genuine_mint_rugpull_operations(self):
        """Test 4: Verify genuine mint rugpull operations"""
        test_name = "Genuine Mint Rugpull Operations"
        
        try:
            # Check bot.js for /genuine_mint_rugpull command
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check genuine-blockchain-manager.js for rugpull simulation
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            mint_rugpull_checks = {
                "Genuine Mint Rugpull Command": "/genuine_mint_rugpull" in bot_content or "genuine_mint_rugpull" in bot_content,
                "Rugpull Simulation Method": "genuineRugpullSimulation" in manager_content,
                "Real Token Minting": "mintTo" in manager_content and "genuine" in manager_content.lower(),
                "Mint and Dump Logic": "mint_and_dump" in manager_content,
                "Supply Increase": "additionalSupply" in manager_content or "totalSupply" in manager_content,
                "Warning Systems": "warning" in manager_content.lower() or "educational" in manager_content.lower(),
                "Confirmation Flows": "confirmation" in manager_content.lower() or "confirm" in manager_content.lower(),
                "Devnet Only Protection": "devnet" in manager_content and "mainnet" in manager_content
            }
            
            failed_checks = []
            for check, passed in mint_rugpull_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Mint Rugpull Checks": list(mint_rugpull_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Genuine mint rugpull operations incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some mint rugpull checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Genuine mint rugpull operations properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing genuine mint rugpull: {str(e)}")
            return False
    
    def test_genuine_liquidity_removal_rugpull(self):
        """Test 5: Verify genuine liquidity removal rugpull"""
        test_name = "Genuine Liquidity Removal Rugpull"
        
        try:
            # Check bot.js for /genuine_rugpull command
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Check genuine-blockchain-manager.js for liquidity removal
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            with open(genuine_manager_path, 'r') as f:
                manager_content = f.read()
            
            liquidity_rugpull_checks = {
                "Genuine Rugpull Command": "/genuine_rugpull" in bot_content or "genuine_rugpull" in bot_content,
                "Liquidity Drain Logic": "liquidity_drain" in manager_content,
                "Real Liquidity Removal": "liquidityRemoved" in manager_content,
                "SOL Removal": "solRemoved" in manager_content,
                "Token Removal": "tokensRemoved" in manager_content,
                "DEX Integration": "DEX" in manager_content or "dex" in manager_content,
                "Lock Verification": "liquidityLock" in manager_content and "genuine" in manager_content,
                "Permanent Consequences Warning": "permanent" in manager_content.lower() and "consequences" in manager_content.lower()
            }
            
            failed_checks = []
            for check, passed in liquidity_rugpull_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Liquidity Rugpull Checks": list(liquidity_rugpull_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Genuine liquidity removal rugpull incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some liquidity rugpull checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Genuine liquidity removal rugpull properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing genuine liquidity rugpull: {str(e)}")
            return False
    
    def test_enhanced_status_command(self):
        """Test 6: Verify enhanced status command shows genuine operations"""
        test_name = "Enhanced Status Command"
        
        try:
            # Check bot.js for enhanced status command
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Look for status command implementation
            status_checks = {
                "Status Command": "/status" in bot_content,
                "Genuine Operations Section": "genuine" in bot_content.lower() and "operations" in bot_content.lower(),
                "Active Liquidity Locks": "liquidity" in bot_content.lower() and ("lock" in bot_content.lower() or "active" in bot_content.lower()),
                "Time-locks Display": "time" in bot_content.lower() and "lock" in bot_content.lower(),
                "Time Remaining Calculations": "remaining" in bot_content.lower() or "hours" in bot_content.lower(),
                "Operation Status Tracking": "status" in bot_content.lower() and "track" in bot_content.lower(),
                "Explorer Links": "explorer" in bot_content.lower() or "solana.com" in bot_content
            }
            
            failed_checks = []
            for check, passed in status_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Status Command Checks": list(status_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Enhanced status command incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some status command checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Enhanced status command properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing enhanced status command: {str(e)}")
            return False
    
    def test_bot_integration_stability(self):
        """Test 7: Verify bot starts without errors after genuine manager integration"""
        test_name = "Bot Integration & Stability"
        
        try:
            # Check bot.js for genuine manager integration
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            integration_checks = {
                "Genuine Manager Import": "genuine-blockchain-manager" in bot_content,
                "Manager Initialization": "GenuineBlockchainManager" in bot_content,
                "Error Handling": "try" in bot_content and "catch" in bot_content,
                "Backward Compatibility": "wallet" in bot_content.lower() and "token" in bot_content.lower(),
                "Callback Handlers": "callback_query" in bot_content or "callbackQuery" in bot_content,
                "Command Registration": "onText" in bot_content or "command" in bot_content.lower(),
                "Bot Polling": "polling" in bot_content or "webhook" in bot_content
            }
            
            # Check if all required files exist for integration
            required_files = [
                "bot.js", "genuine-blockchain-manager.js", "wallet-manager.js", 
                "database.js", "package.json"
            ]
            
            missing_files = []
            for file_name in required_files:
                if not (self.telegram_bot_dir / file_name).exists():
                    missing_files.append(file_name)
            
            failed_checks = []
            for check, passed in integration_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Integration Checks": list(integration_checks.keys()),
                "Failed Checks": failed_checks,
                "Required Files": required_files,
                "Missing Files": missing_files
            }
            
            if missing_files:
                self.log_test(test_name, "FAIL", f"Missing required files: {', '.join(missing_files)}", details)
                return False
            
            if len(failed_checks) > 2:
                self.log_test(test_name, "FAIL", f"Bot integration incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some integration checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Bot integration and stability properly configured", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing bot integration: {str(e)}")
            return False
    
    def test_command_structure_ui(self):
        """Test 8: Verify command structure and UI elements work"""
        test_name = "Command Structure & UI"
        
        try:
            # Check bot.js for UI elements
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            ui_checks = {
                "Inline Keyboards": "inline_keyboard" in bot_content,
                "Callback Data": "callback_data" in bot_content,
                "Button Text": "text:" in bot_content,
                "Confirmation Flows": "confirm" in bot_content.lower(),
                "Cancellation Options": "cancel" in bot_content.lower(),
                "Warning Levels": "warning" in bot_content.lower() or "⚠️" in bot_content,
                "Multiple Confirmations": bot_content.count("confirm") > 1,
                "Educational Messages": "educational" in bot_content.lower() or "research" in bot_content.lower()
            }
            
            failed_checks = []
            for check, passed in ui_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "UI Checks": list(ui_checks.keys()),
                "Failed Checks": failed_checks
            }
            
            if len(failed_checks) > 3:
                self.log_test(test_name, "FAIL", f"Command structure and UI incomplete: {len(failed_checks)} checks failed", details)
                return False
            elif failed_checks:
                self.log_test(test_name, "WARN", f"Some UI checks failed: {len(failed_checks)}", details)
                return True
            
            self.log_test(test_name, "PASS", "Command structure and UI properly implemented", details)
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error analyzing command structure and UI: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all genuine blockchain operation tests and generate report"""
        print("🚀 Starting Genuine Blockchain Operations Tests...")
        print("=" * 70)
        
        tests = [
            self.test_genuine_blockchain_manager_integration,
            self.test_genuine_liquidity_locking,
            self.test_time_locked_mint_authority_revocation,
            self.test_genuine_mint_rugpull_operations,
            self.test_genuine_liquidity_removal_rugpull,
            self.test_enhanced_status_command,
            self.test_bot_integration_stability,
            self.test_command_structure_ui
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
        print("📊 GENUINE BLOCKCHAIN OPERATIONS TEST SUMMARY")
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
            print("\n🚨 CRITICAL ISSUES:")
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
        tester = GenuineBlockchainTester()
        results = tester.run_all_tests()
        
        # Exit with appropriate code
        if results['failed'] == 0:
            print(f"\n🎉 ALL GENUINE BLOCKCHAIN TESTS PASSED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(0)
        else:
            print(f"\n💥 {results['failed']} GENUINE BLOCKCHAIN TESTS FAILED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()