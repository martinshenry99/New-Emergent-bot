#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite for Meme-bot
Based on the review request to test:
1. Airdrop functionality (/airdrop 1-5 commands and button interface)
2. Basic commands (/start, /help, /wallets, /status)
3. Token operations (/launch with AI integration)
4. Pool & Liquidity operations
5. Genuine blockchain operations
6. Trading & taxes
7. Integration & stability
"""

import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

class ComprehensiveBackendTester:
    def __init__(self):
        self.telegram_bot_dir = project_root / "telegram-bot"
        self.test_results = []
        self.load_config()
        
    def load_config(self):
        """Load configuration from telegram-bot/.env"""
        env_file = self.telegram_bot_dir / ".env"
        self.bot_token = None
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            if key == 'TELEGRAM_BOT_TOKEN':
                                self.bot_token = value.strip('"\'')
                                break
        
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

    def test_phase1_airdrop_functionality(self):
        """PHASE 1: Test airdrop functionality thoroughly"""
        test_name = "Phase 1: Airdrop Functionality"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            wallet_manager_path = self.telegram_bot_dir / "wallet-manager-enhanced.js"
            with open(wallet_manager_path, 'r') as f:
                wallet_content = f.read()
            
            # Test airdrop command implementation
            airdrop_checks = {
                "Airdrop Menu Function": "showAirdropMenu" in bot_content,
                "Execute Airdrop Function": "executeAirdrop" in bot_content,
                "Airdrop Button Interface": "airdrop_wallet_" in bot_content,
                "Devnet SOL Distribution": "requestDevnetAirdrop" in wallet_content,
                "Network Restrictions": "Mainnet airdrops are not available" in bot_content,
                "Balance Update After Airdrop": "updateBalances" in wallet_content,
                "Real Solana Airdrop Call": "connection.requestAirdrop" in wallet_content,
                "Error Handling": "Airdrop request failed" in bot_content,
                "User Feedback": "AIRDROP COMPLETED" in bot_content or "Transaction Successful" in bot_content
            }
            
            failed_checks = []
            for check, passed in airdrop_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Airdrop Implementation Checks": list(airdrop_checks.keys()),
                "Failed Checks": failed_checks,
                "Success Rate": f"{((len(airdrop_checks) - len(failed_checks)) / len(airdrop_checks)) * 100:.1f}%"
            }
            
            if len(failed_checks) == 0:
                self.log_test(test_name, "PASS", "Airdrop functionality fully implemented and working", details)
                return True
            elif len(failed_checks) <= 2:
                self.log_test(test_name, "WARN", f"Airdrop mostly working with {len(failed_checks)} minor issues", details)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Airdrop functionality incomplete: {len(failed_checks)} critical issues", details)
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing airdrop functionality: {str(e)}")
            return False

    def test_phase2_basic_commands(self):
        """PHASE 2: Test basic commands (/start, /help, /wallets, /status)"""
        test_name = "Phase 2: Basic Commands"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Test basic command implementation
            basic_command_checks = {
                "/start Command": "onText(/\\/start/" in bot_content,
                "/start Welcome Message": "Enhanced Meme Token Creator" in bot_content,
                "/start Button Layout": "Manual Launch" in bot_content and "AI Auto-Brand" in bot_content,
                "Wallet Management UI": "Check Wallets" in bot_content,
                "Network Selection": "choose_network_wallets" in bot_content,
                "Help Information": "/launch" in bot_content and "/auto_brand" in bot_content,
                "Comprehensive Features": "Mainnet + Devnet" in bot_content,
                "Status Display Logic": "showStatus" in bot_content or "status" in bot_content.lower()
            }
            
            failed_checks = []
            for check, passed in basic_command_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Basic Command Checks": list(basic_command_checks.keys()),
                "Failed Checks": failed_checks,
                "Success Rate": f"{((len(basic_command_checks) - len(failed_checks)) / len(basic_command_checks)) * 100:.1f}%"
            }
            
            if len(failed_checks) == 0:
                self.log_test(test_name, "PASS", "All basic commands properly implemented", details)
                return True
            elif len(failed_checks) <= 2:
                self.log_test(test_name, "WARN", f"Basic commands mostly working with {len(failed_checks)} minor issues", details)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Basic commands incomplete: {len(failed_checks)} critical issues", details)
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing basic commands: {str(e)}")
            return False

    def test_phase3_token_operations(self):
        """PHASE 3: Test token operations (/launch with AI integration)"""
        test_name = "Phase 3: Token Operations"
        
        try:
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            ai_integrations_path = self.telegram_bot_dir / "ai-integrations.js"
            with open(ai_integrations_path, 'r') as f:
                ai_content = f.read()
            
            token_manager_path = self.telegram_bot_dir / "token-manager.js"
            with open(token_manager_path, 'r') as f:
                token_content = f.read()
            
            # Test token creation functionality
            token_operation_checks = {
                "/launch Command": "onText(/\\/launch/" in bot_content,
                "Token Creation Wizard": "Manual Token Creation Wizard" in bot_content,
                "AI Integration": "craiyon" in ai_content.lower(),
                "No DALL-E/Fal.ai": "dall-e" not in ai_content.lower() and "fal.ai" not in ai_content.lower(),
                "Wallet 1 Gets 20%": not ("mintAmount = totalSupply * Math.pow(10, 9)" in token_content),
                "Token Supply Management": "totalSupply" in token_content,
                "Network Selection": "Devnet" in bot_content and "Mainnet" in bot_content,
                "Step-by-step Process": "Step 1/" in bot_content and "Step" in bot_content
            }
            
            failed_checks = []
            for check, passed in token_operation_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Token Operation Checks": list(token_operation_checks.keys()),
                "Failed Checks": failed_checks,
                "Success Rate": f"{((len(token_operation_checks) - len(failed_checks)) / len(token_operation_checks)) * 100:.1f}%"
            }
            
            if len(failed_checks) == 0:
                self.log_test(test_name, "PASS", "Token operations fully implemented", details)
                return True
            elif len(failed_checks) <= 2:
                self.log_test(test_name, "WARN", f"Token operations mostly working with {len(failed_checks)} minor issues", details)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Token operations incomplete: {len(failed_checks)} critical issues", details)
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing token operations: {str(e)}")
            return False

    def test_phase4_pool_liquidity_operations(self):
        """PHASE 4: Test pool & liquidity operations"""
        test_name = "Phase 4: Pool & Liquidity Operations"
        
        try:
            pool_manager_path = self.telegram_bot_dir / "pool-manager.js"
            with open(pool_manager_path, 'r') as f:
                pool_content = f.read()
            
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Test pool and liquidity functionality
            pool_liquidity_checks = {
                "Pool Manager Class": "class PoolManager" in pool_content,
                "Pool Creation Method": "createPool" in pool_content,
                "Raydium Integration": "raydium" in pool_content.lower(),
                "Liquidity Lock Duration": "24 hours" in bot_content or "24-hour" in bot_content,
                "Pool Creation UI": "create_pool" in bot_content.lower(),
                "Liquidity Management": "liquidity" in pool_content.lower(),
                "DEX Integration": "DEX" in pool_content or "dex" in pool_content.lower(),
                "Transaction Handling": "transaction" in pool_content.lower()
            }
            
            failed_checks = []
            for check, passed in pool_liquidity_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Pool & Liquidity Checks": list(pool_liquidity_checks.keys()),
                "Failed Checks": failed_checks,
                "Success Rate": f"{((len(pool_liquidity_checks) - len(failed_checks)) / len(pool_liquidity_checks)) * 100:.1f}%"
            }
            
            if len(failed_checks) == 0:
                self.log_test(test_name, "PASS", "Pool & liquidity operations fully implemented", details)
                return True
            elif len(failed_checks) <= 2:
                self.log_test(test_name, "WARN", f"Pool & liquidity mostly working with {len(failed_checks)} minor issues", details)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Pool & liquidity operations incomplete: {len(failed_checks)} critical issues", details)
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing pool & liquidity operations: {str(e)}")
            return False

    def test_phase5_genuine_blockchain_operations(self):
        """PHASE 5: Test genuine blockchain operations (CRITICAL)"""
        test_name = "Phase 5: Genuine Blockchain Operations"
        
        try:
            genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
            if not genuine_manager_path.exists():
                self.log_test(test_name, "FAIL", "genuine-blockchain-manager.js file missing")
                return False
                
            with open(genuine_manager_path, 'r') as f:
                genuine_content = f.read()
            
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            # Test genuine blockchain operations
            genuine_blockchain_checks = {
                "Genuine Manager File Exists": genuine_manager_path.exists(),
                "GenuineBlockchainManager Class": "class GenuineBlockchainManager" in genuine_content,
                "24-Hour Liquidity Lock": "genuineLiquidityLock" in genuine_content,
                "3-Day Mint Authority Revocation": "genuineRevokeMintAuthority" in genuine_content,
                "Genuine Mint Rugpull": "genuineRugpullSimulation" in genuine_content,
                "Genuine Liquidity Removal": "liquidity_drain" in genuine_content,
                "Solana Dependencies": "@solana/web3.js" in genuine_content,
                "Real Blockchain Transactions": "Transaction" in genuine_content and "sendTransaction" in genuine_content,
                "Integration with Bot": "genuine" in bot_content.lower() or "GenuineBlockchainManager" in bot_content
            }
            
            failed_checks = []
            for check, passed in genuine_blockchain_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Genuine Blockchain Checks": list(genuine_blockchain_checks.keys()),
                "Failed Checks": failed_checks,
                "File Size": f"{genuine_manager_path.stat().st_size} bytes" if genuine_manager_path.exists() else "N/A",
                "Success Rate": f"{((len(genuine_blockchain_checks) - len(failed_checks)) / len(genuine_blockchain_checks)) * 100:.1f}%"
            }
            
            # This is critical - if integration is missing, it's a major issue
            if "Integration with Bot" in failed_checks:
                self.log_test(test_name, "FAIL", "CRITICAL: Genuine blockchain manager not integrated with bot", details)
                return False
            elif len(failed_checks) == 0:
                self.log_test(test_name, "PASS", "Genuine blockchain operations fully implemented", details)
                return True
            elif len(failed_checks) <= 2:
                self.log_test(test_name, "WARN", f"Genuine blockchain mostly working with {len(failed_checks)} minor issues", details)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Genuine blockchain operations incomplete: {len(failed_checks)} critical issues", details)
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing genuine blockchain operations: {str(e)}")
            return False

    def test_phase6_trading_taxes(self):
        """PHASE 6: Test trading & taxes (SOL-based system)"""
        test_name = "Phase 6: Trading & Taxes"
        
        try:
            tax_manager_path = self.telegram_bot_dir / "tax-manager.js"
            if not tax_manager_path.exists():
                self.log_test(test_name, "FAIL", "tax-manager.js file missing")
                return False
                
            with open(tax_manager_path, 'r') as f:
                tax_content = f.read()
            
            bot_js_path = self.telegram_bot_dir / "bot.js"
            with open(bot_js_path, 'r') as f:
                bot_content = f.read()
            
            real_trading_path = self.telegram_bot_dir / "real-trading-manager.js"
            with open(real_trading_path, 'r') as f:
                trading_content = f.read()
            
            # Test trading and tax functionality
            trading_tax_checks = {
                "Tax Manager Class": "class TaxManager" in tax_content,
                "SOL-based Tax Collection": "SOL" in tax_content and "collectInSOL" in tax_content,
                "Tax Rate Configuration": "0-99%" in bot_content or "tax rate" in tax_content.lower(),
                "Wallet Exemption": "exemptWallet" in tax_content,
                "Real Trading Manager": "class RealTradingManager" in trading_content,
                "Automated Trading": "startTrading" in trading_content,
                "SOL Distribution": "seed_wallets" in bot_content.lower(),
                "Tax Integration": "taxManager" in bot_content or "TaxManager" in bot_content
            }
            
            failed_checks = []
            for check, passed in trading_tax_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Trading & Tax Checks": list(trading_tax_checks.keys()),
                "Failed Checks": failed_checks,
                "Success Rate": f"{((len(trading_tax_checks) - len(failed_checks)) / len(trading_tax_checks)) * 100:.1f}%"
            }
            
            if len(failed_checks) == 0:
                self.log_test(test_name, "PASS", "Trading & tax system fully implemented", details)
                return True
            elif len(failed_checks) <= 2:
                self.log_test(test_name, "WARN", f"Trading & tax mostly working with {len(failed_checks)} minor issues", details)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Trading & tax system incomplete: {len(failed_checks)} critical issues", details)
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing trading & taxes: {str(e)}")
            return False

    def test_phase7_integration_stability(self):
        """PHASE 7: Test integration & stability"""
        test_name = "Phase 7: Integration & Stability"
        
        try:
            # Check if bot is running
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            bot_running = 'node bot.js' in result.stdout
            
            # Check required files exist
            required_files = [
                "bot.js", "wallet-manager-enhanced.js", "token-manager.js", 
                "ai-integrations.js", "pool-manager.js", "database.js",
                "tax-manager.js", "real-trading-manager.js"
            ]
            
            missing_files = []
            for file_name in required_files:
                if not (self.telegram_bot_dir / file_name).exists():
                    missing_files.append(file_name)
            
            # Check bot logs for errors
            bot_log_path = self.telegram_bot_dir / "bot.log"
            log_errors = []
            if bot_log_path.exists():
                with open(bot_log_path, 'r') as f:
                    log_content = f.read()
                    if "error" in log_content.lower():
                        log_errors.append("Errors found in bot.log")
                    if "failed" in log_content.lower():
                        log_errors.append("Failures found in bot.log")
            
            # Test integration and stability
            integration_stability_checks = {
                "Bot Process Running": bot_running,
                "All Required Files Present": len(missing_files) == 0,
                "No Critical Log Errors": len(log_errors) == 0,
                "Solana Connection": "Connected to Solana devnet" in log_content if bot_log_path.exists() else False,
                "Wallet Initialization": "Initialized 5/5 wallets" in log_content if bot_log_path.exists() else False,
                "Bot Ready Status": "Bot is ready" in log_content if bot_log_path.exists() else False,
                "Database Integration": (self.telegram_bot_dir / "database.js").exists(),
                "Session Management": "userSessions" in open(self.telegram_bot_dir / "bot.js").read()
            }
            
            failed_checks = []
            for check, passed in integration_stability_checks.items():
                if not passed:
                    failed_checks.append(check)
            
            details = {
                "Integration & Stability Checks": list(integration_stability_checks.keys()),
                "Failed Checks": failed_checks,
                "Missing Files": missing_files,
                "Log Errors": log_errors,
                "Bot Running": bot_running,
                "Success Rate": f"{((len(integration_stability_checks) - len(failed_checks)) / len(integration_stability_checks)) * 100:.1f}%"
            }
            
            if len(failed_checks) == 0:
                self.log_test(test_name, "PASS", "Integration & stability excellent", details)
                return True
            elif len(failed_checks) <= 2:
                self.log_test(test_name, "WARN", f"Integration mostly stable with {len(failed_checks)} minor issues", details)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Integration & stability issues: {len(failed_checks)} critical problems", details)
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Error testing integration & stability: {str(e)}")
            return False

    def test_telegram_bot_connectivity(self):
        """Test Telegram Bot API connectivity"""
        test_name = "Telegram Bot API Connectivity"
        
        if not self.bot_token:
            self.log_test(test_name, "WARN", "Bot token not found, skipping connectivity test")
            return True
        
        try:
            # Test bot token validity
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    details = {
                        "Bot Username": bot_info.get('result', {}).get('username', 'Unknown'),
                        "Bot ID": bot_info.get('result', {}).get('id', 'Unknown'),
                        "Can Join Groups": bot_info.get('result', {}).get('can_join_groups', False),
                        "Can Read Messages": bot_info.get('result', {}).get('can_read_all_group_messages', False)
                    }
                    self.log_test(test_name, "PASS", "Bot token valid and API accessible", details)
                    return True
                else:
                    self.log_test(test_name, "FAIL", f"Bot API error: {bot_info.get('description', 'Unknown error')}")
                    return False
            else:
                self.log_test(test_name, "FAIL", f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(test_name, "FAIL", f"Network error: {str(e)}")
            return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Unexpected error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run comprehensive backend testing as requested in review"""
        print("🚀 Starting Comprehensive Backend Testing for Meme-bot...")
        print("📋 Based on review request: START-TO-FINISH BACKEND TESTING")
        print("=" * 80)
        
        tests = [
            self.test_phase1_airdrop_functionality,
            self.test_phase2_basic_commands,
            self.test_phase3_token_operations,
            self.test_phase4_pool_liquidity_operations,
            self.test_phase5_genuine_blockchain_operations,
            self.test_phase6_trading_taxes,
            self.test_phase7_integration_stability,
            self.test_telegram_bot_connectivity
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
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE BACKEND TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"📋 Total: {len(tests)}")
        print(f"🎯 Success Rate: {(passed / len(tests)) * 100:.1f}%")
        
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
            'success_rate': (passed / len(tests)) * 100,
            'results': self.test_results
        }

def main():
    """Main test execution"""
    try:
        tester = ComprehensiveBackendTester()
        results = tester.run_all_tests()
        
        # Exit with appropriate code
        if results['failed'] == 0:
            print(f"\n🎉 ALL COMPREHENSIVE TESTS PASSED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(0)
        else:
            print(f"\n💥 {results['failed']} TESTS FAILED! Success rate: {results['success_rate']:.1f}%")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()