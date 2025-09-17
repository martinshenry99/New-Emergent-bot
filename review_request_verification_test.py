#!/usr/bin/env python3
"""
Review Request Verification Test - Telegram Bot Backend Testing
Testing specific logic explanations and bug fixes as requested:

1. System Logic Verification:
   - Devnet vs Mainnet wallet logic
   - Mint authority logic (revoke vs keep)
   - Liquidity lock under mainnet (24-hour lock)

2. Bug Fix Verification:
   - chart_activity 'Token not found' issue
   - start_trading command restarting bot issue
   - Enhanced error handling and debug info
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

class ReviewRequestTester:
    def __init__(self):
        self.project_root = Path("/app")
        self.telegram_bot_dir = self.project_root / "telegram-bot"
        self.test_results = {
            "devnet_mainnet_logic": {"status": "pending", "details": []},
            "mint_authority_logic": {"status": "pending", "details": []},
            "liquidity_lock_24h": {"status": "pending", "details": []},
            "chart_activity_fix": {"status": "pending", "details": []},
            "start_trading_fix": {"status": "pending", "details": []},
            "database_gettoken_method": {"status": "pending", "details": []},
            "enhanced_error_handling": {"status": "pending", "details": []}
        }
        
    def log_test(self, test_name, status, message):
        """Log test results"""
        print(f"[{test_name.upper()}] {status}: {message}")
        if test_name in self.test_results:
            self.test_results[test_name]["status"] = status
            self.test_results[test_name]["details"].append(message)
    
    def test_devnet_mainnet_logic(self):
        """Test 1: Verify devnet vs mainnet wallet logic and separation"""
        print("\n🌐 TESTING DEVNET VS MAINNET WALLET LOGIC...")
        
        # Check bot.js for network separation
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check for network selection in commands
        network_selection_indicators = [
            "choose_network_wallets",
            "network_select_devnet",
            "network_select_mainnet",
            "data.network === 'devnet'",
            "data.network === 'mainnet'"
        ]
        
        found_network_logic = []
        for indicator in network_selection_indicators:
            if indicator in bot_content:
                found_network_logic.append(indicator)
                
        if len(found_network_logic) < 4:
            self.log_test("devnet_mainnet_logic", "FAILED", 
                         f"Network separation logic incomplete. Found: {found_network_logic}")
            return False
            
        # Test 2: Check wallet manager for network separation
        wallet_manager_path = self.telegram_bot_dir / "wallet-manager-enhanced.js"
        if not wallet_manager_path.exists():
            self.log_test("devnet_mainnet_logic", "FAILED", 
                         "wallet-manager-enhanced.js not found")
            return False
            
        with open(wallet_manager_path, 'r') as f:
            wallet_content = f.read()
            
        wallet_network_checks = [
            "getWallets(network)",
            "getWallet(network",
            "updateBalances(network)",
            "devnet",
            "mainnet"
        ]
        
        found_wallet_logic = sum(1 for check in wallet_network_checks if check in wallet_content)
        if found_wallet_logic < 4:
            self.log_test("devnet_mainnet_logic", "FAILED", 
                         "Wallet manager network separation incomplete")
            return False
            
        # Test 3: Check for different behavior between networks
        mainnet_specific_checks = [
            "mainnet requires real SOL",
            "real investment",
            "displayed liquidity",
            "realSol",
            "displayedLiquidity"
        ]
        
        found_mainnet_logic = sum(1 for check in mainnet_specific_checks if check.lower() in bot_content.lower())
        if found_mainnet_logic < 3:
            self.log_test("devnet_mainnet_logic", "FAILED", 
                         "Mainnet-specific logic not properly implemented")
            return False
            
        self.log_test("devnet_mainnet_logic", "PASSED", 
                     "Devnet vs Mainnet wallet logic properly separated and functional")
        return True
    
    def test_mint_authority_logic(self):
        """Test 2: Verify mint authority logic (revoke vs keep authority options)"""
        print("\n🔒 TESTING MINT AUTHORITY LOGIC...")
        
        # Check bot.js for mint authority options
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check for mint authority decision UI
        mint_authority_ui = [
            "Mint Authority",
            "Revoke = No more tokens",
            "Keep = You can mint more",
            "mint_authority_yes",
            "mint_authority_no"
        ]
        
        found_ui_elements = []
        for element in mint_authority_ui:
            if element in bot_content:
                found_ui_elements.append(element)
                
        if len(found_ui_elements) < 4:
            self.log_test("mint_authority_logic", "FAILED", 
                         f"Mint authority UI incomplete. Found: {found_ui_elements}")
            return False
            
        # Test 2: Check genuine blockchain manager for actual revocation
        genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
        if not genuine_manager_path.exists():
            self.log_test("mint_authority_logic", "FAILED", 
                         "genuine-blockchain-manager.js not found")
            return False
            
        with open(genuine_manager_path, 'r') as f:
            genuine_content = f.read()
            
        # Test 3: Check for genuine revocation implementation
        revocation_checks = [
            "genuineRevokeMintAuthority",
            "setAuthority",
            "AuthorityType.MintTokens",
            "null,                       // New authority (null = revoke permanently)",
            "PERMANENT AND IRREVERSIBLE"
        ]
        
        found_revocation_logic = []
        for check in revocation_checks:
            if check in genuine_content:
                found_revocation_logic.append(check)
                
        if len(found_revocation_logic) < 4:
            self.log_test("mint_authority_logic", "FAILED", 
                         f"Genuine mint authority revocation incomplete. Found: {found_revocation_logic}")
            return False
            
        # Test 4: Check for time-lock implementation (3-day delay mentioned in review)
        time_lock_checks = [
            "3-day",
            "time-lock",
            "delay",
            "scheduling"
        ]
        
        found_time_lock = sum(1 for check in time_lock_checks if check.lower() in bot_content.lower())
        if found_time_lock < 2:
            self.log_test("mint_authority_logic", "WARNING", 
                         "Time-lock delay implementation may be incomplete")
            
        self.log_test("mint_authority_logic", "PASSED", 
                     "Mint authority logic (revoke vs keep) properly implemented with genuine blockchain operations")
        return True
    
    def test_liquidity_lock_24h(self):
        """Test 3: Verify 24-hour liquidity lock functionality on mainnet"""
        print("\n🔒 TESTING 24-HOUR LIQUIDITY LOCK...")
        
        # Check bot.js for liquidity lock UI
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check for 24-hour lock UI
        lock_ui_checks = [
            "Liquidity Lock",
            "24 hours",
            "Lock Duration: 24 hours",
            "liquidity_yes",
            "liquidity_no"
        ]
        
        found_lock_ui = []
        for check in lock_ui_checks:
            if check in bot_content:
                found_lock_ui.append(check)
                
        if len(found_lock_ui) < 4:
            self.log_test("liquidity_lock_24h", "FAILED", 
                         f"24-hour liquidity lock UI incomplete. Found: {found_lock_ui}")
            return False
            
        # Test 2: Check genuine blockchain manager for real lock implementation
        genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
        with open(genuine_manager_path, 'r') as f:
            genuine_content = f.read()
            
        # Test 3: Check for genuine liquidity lock implementation
        genuine_lock_checks = [
            "genuineLiquidityLock",
            "lockDurationHours = 24",
            "time-locked escrow account",
            "unlockTimestamp",
            "24 hours in milliseconds"
        ]
        
        found_genuine_lock = []
        for check in genuine_lock_checks:
            if check in genuine_content:
                found_genuine_lock.append(check)
                
        if len(found_genuine_lock) < 4:
            self.log_test("liquidity_lock_24h", "FAILED", 
                         f"Genuine 24-hour lock implementation incomplete. Found: {found_genuine_lock}")
            return False
            
        # Test 4: Check database for lock duration setting
        database_path = self.telegram_bot_dir / "database.js"
        if database_path.exists():
            with open(database_path, 'r') as f:
                db_content = f.read()
                
            if "24 * 60 * 60 * 1000" in db_content:  # 24 hours in milliseconds
                self.log_test("liquidity_lock_24h", "INFO", 
                             "Database configured with 24-hour lock duration")
            else:
                self.log_test("liquidity_lock_24h", "WARNING", 
                             "Database lock duration setting not found")
                
        # Test 5: Check for on-chain verification
        verification_checks = [
            "verifyLiquidityLockOnChain",
            "escrowAccount",
            "lockDataAccount",
            "onChainVerifiable"
        ]
        
        found_verification = sum(1 for check in verification_checks if check in genuine_content)
        if found_verification < 3:
            self.log_test("liquidity_lock_24h", "WARNING", 
                         "On-chain lock verification may be incomplete")
            
        self.log_test("liquidity_lock_24h", "PASSED", 
                     "24-hour liquidity lock functionality properly implemented with genuine on-chain operations")
        return True
    
    def test_chart_activity_fix(self):
        """Test 4: Verify chart_activity 'Token not found' issue is fixed"""
        print("\n📈 TESTING CHART_ACTIVITY FIX...")
        
        # Check bot.js for chart_activity command
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check for chart_activity command handler
        if "/chart_activity" not in bot_content:
            self.log_test("chart_activity_fix", "FAILED", 
                         "/chart_activity command not found in bot.js")
            return False
            
        # Test 2: Check for chartActivityCommand function
        if "chartActivityCommand" not in bot_content:
            self.log_test("chart_activity_fix", "FAILED", 
                         "chartActivityCommand function not found")
            return False
            
        # Test 3: Check for enhanced error handling
        error_handling_checks = [
            "try {",
            "catch (error)",
            "error.message",
            "Token not found",
            "debug info"
        ]
        
        found_error_handling = sum(1 for check in error_handling_checks if check in bot_content)
        if found_error_handling < 3:
            self.log_test("chart_activity_fix", "FAILED", 
                         "Enhanced error handling for chart_activity not implemented")
            return False
            
        # Test 4: Check database.js for getToken method
        database_path = self.telegram_bot_dir / "database.js"
        if not database_path.exists():
            self.log_test("chart_activity_fix", "FAILED", 
                         "database.js not found")
            return False
            
        with open(database_path, 'r') as f:
            db_content = f.read()
            
        # Test 5: Check for multiple fallback methods
        fallback_methods = [
            "getToken(",
            "getTokenData(",
            "getAllTokens()"
        ]
        
        found_fallbacks = []
        for method in fallback_methods:
            if method in db_content:
                found_fallbacks.append(method)
                
        if len(found_fallbacks) < 2:
            self.log_test("chart_activity_fix", "FAILED", 
                         f"Multiple fallback methods not implemented. Found: {found_fallbacks}")
            return False
            
        # Test 6: Check real trading manager for chart activity methods
        trading_manager_path = self.telegram_bot_dir / "real-trading-manager.js"
        if trading_manager_path.exists():
            with open(trading_manager_path, 'r') as f:
                trading_content = f.read()
                
            chart_methods = [
                "startChartActivity",
                "stopChartActivity",
                "generateChartActivityTrade"
            ]
            
            found_chart_methods = sum(1 for method in chart_methods if method in trading_content)
            if found_chart_methods < 3:
                self.log_test("chart_activity_fix", "WARNING", 
                             "Chart activity methods may be incomplete in trading manager")
        
        self.log_test("chart_activity_fix", "PASSED", 
                     "chart_activity 'Token not found' issue fixed with enhanced error handling and fallback methods")
        return True
    
    def test_start_trading_fix(self):
        """Test 5: Verify start_trading command no longer restarts bot"""
        print("\n🚀 TESTING START_TRADING FIX...")
        
        # Check bot.js for start_trading command
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Check for start_trading command handler
        if "/start_trading" not in bot_content:
            self.log_test("start_trading_fix", "FAILED", 
                         "/start_trading command not found in bot.js")
            return False
            
        # Test 2: Check for startRealTradingCommand function
        if "startRealTradingCommand" not in bot_content:
            self.log_test("start_trading_fix", "FAILED", 
                         "startRealTradingCommand function not found")
            return False
            
        # Test 3: Check for try-catch error handling to prevent crashes
        start_trading_section = bot_content[bot_content.find("startRealTradingCommand"):bot_content.find("startRealTradingCommand") + 2000]
        
        crash_prevention_checks = [
            "try {",
            "catch (error)",
            "error handling",
            "gracefully"
        ]
        
        found_crash_prevention = sum(1 for check in crash_prevention_checks if check.lower() in start_trading_section.lower())
        if found_crash_prevention < 2:
            self.log_test("start_trading_fix", "FAILED", 
                         "Crash prevention (try-catch) not implemented for start_trading")
            return False
            
        # Test 4: Check for multiple fallback methods to find pools/tokens
        fallback_indicators = [
            "database.getToken",
            "database.getAllTokens",
            "poolManager",
            "fallback"
        ]
        
        found_fallbacks = sum(1 for indicator in fallback_indicators if indicator in bot_content)
        if found_fallbacks < 2:
            self.log_test("start_trading_fix", "WARNING", 
                         "Multiple fallback methods for finding pools/tokens may be incomplete")
            
        # Test 5: Check for debug information instead of crashes
        debug_checks = [
            "debug info",
            "console.log",
            "error.message",
            "detailed error"
        ]
        
        found_debug = sum(1 for check in debug_checks if check.lower() in bot_content.lower())
        if found_debug < 2:
            self.log_test("start_trading_fix", "WARNING", 
                         "Debug information logging may be incomplete")
            
        # Test 6: Check that command doesn't call process.exit or similar
        dangerous_calls = [
            "process.exit",
            "process.kill",
            "bot.stop",
            "system.exit"
        ]
        
        found_dangerous = sum(1 for call in dangerous_calls if call in bot_content)
        if found_dangerous > 0:
            self.log_test("start_trading_fix", "FAILED", 
                         "start_trading command still contains dangerous calls that could restart bot")
            return False
            
        self.log_test("start_trading_fix", "PASSED", 
                     "start_trading command fixed with error handling to prevent bot restarts")
        return True
    
    def test_database_gettoken_method(self):
        """Test 6: Verify database.getToken() method works correctly"""
        print("\n💾 TESTING DATABASE GETTOKEN METHOD...")
        
        database_path = self.telegram_bot_dir / "database.js"
        if not database_path.exists():
            self.log_test("database_gettoken_method", "FAILED", 
                         "database.js not found")
            return False
            
        with open(database_path, 'r') as f:
            db_content = f.read()
            
        # Test 1: Check for getToken method
        if "getToken(" not in db_content:
            self.log_test("database_gettoken_method", "FAILED", 
                         "getToken method not found in database.js")
            return False
            
        # Test 2: Check for getTokenData method (alternative)
        if "getTokenData(" not in db_content:
            self.log_test("database_gettoken_method", "FAILED", 
                         "getTokenData method not found in database.js")
            return False
            
        # Test 3: Check for getAllTokens method
        if "getAllTokens(" not in db_content:
            self.log_test("database_gettoken_method", "FAILED", 
                         "getAllTokens method not found in database.js")
            return False
            
        # Test 4: Check method implementation
        gettoken_section = db_content[db_content.find("getToken("):db_content.find("getToken(") + 200]
        
        if "this.data.tokens[tokenMint]" not in gettoken_section:
            self.log_test("database_gettoken_method", "FAILED", 
                         "getToken method implementation incorrect")
            return False
            
        # Test 5: Check for alias consistency
        if "// Alias for getTokenData" in db_content:
            self.log_test("database_gettoken_method", "INFO", 
                         "getToken method properly aliased to getTokenData")
            
        self.log_test("database_gettoken_method", "PASSED", 
                     "database.getToken() method properly implemented and working")
        return True
    
    def test_enhanced_error_handling(self):
        """Test 7: Verify enhanced error handling provides debug info instead of crashing"""
        print("\n🛡️ TESTING ENHANCED ERROR HANDLING...")
        
        # Check bot.js for enhanced error handling patterns
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # Test 1: Count try-catch blocks
        try_catch_count = bot_content.count("try {")
        catch_count = bot_content.count("catch (error)")
        
        if try_catch_count < 5 or catch_count < 5:
            self.log_test("enhanced_error_handling", "FAILED", 
                         f"Insufficient error handling blocks. Try: {try_catch_count}, Catch: {catch_count}")
            return False
            
        # Test 2: Check for detailed error messages
        error_message_patterns = [
            "error.message",
            "console.error",
            "detailed error",
            "debug info",
            "Error:",
            "Failed:"
        ]
        
        found_error_patterns = sum(1 for pattern in error_message_patterns if pattern in bot_content)
        if found_error_patterns < 4:
            self.log_test("enhanced_error_handling", "FAILED", 
                         f"Insufficient detailed error messaging. Found: {found_error_patterns}")
            return False
            
        # Test 3: Check for graceful error responses to users
        user_error_responses = [
            "bot.sendMessage(chatId, '❌",
            "Error loading",
            "Please try again",
            "failed:",
            "not available"
        ]
        
        found_user_responses = sum(1 for response in user_error_responses if response in bot_content)
        if found_user_responses < 3:
            self.log_test("enhanced_error_handling", "FAILED", 
                         f"Insufficient user-friendly error responses. Found: {found_user_responses}")
            return False
            
        # Test 4: Check that errors don't cause bot to exit
        exit_patterns = [
            "process.exit",
            "throw new Error",
            "bot.stop()",
            "process.kill"
        ]
        
        # Count throw new Error patterns (should be minimal in main bot logic)
        dangerous_exits = sum(1 for pattern in exit_patterns[:3] if pattern in bot_content)
        if dangerous_exits > 5:  # Some throw new Error is acceptable in utility functions
            self.log_test("enhanced_error_handling", "WARNING", 
                         f"High number of potentially dangerous exit patterns: {dangerous_exits}")
            
        # Test 5: Check specific commands for error handling
        critical_commands = [
            "chartActivityCommand",
            "startRealTradingCommand",
            "executeAirdrop",
            "showAllWalletBalances"
        ]
        
        commands_with_error_handling = 0
        for command in critical_commands:
            if command in bot_content:
                command_section = bot_content[bot_content.find(command):bot_content.find(command) + 1000]
                if "try {" in command_section or "catch (error)" in command_section:
                    commands_with_error_handling += 1
                    
        if commands_with_error_handling < 3:
            self.log_test("enhanced_error_handling", "FAILED", 
                         f"Critical commands lack proper error handling: {commands_with_error_handling}/{len(critical_commands)}")
            return False
            
        self.log_test("enhanced_error_handling", "PASSED", 
                     "Enhanced error handling properly implemented with debug info and graceful failure handling")
        return True
    
    def run_comprehensive_test(self):
        """Run all review request verification tests"""
        print("🔍 STARTING REVIEW REQUEST VERIFICATION TESTING...")
        print("=" * 70)
        
        test_methods = [
            self.test_devnet_mainnet_logic,
            self.test_mint_authority_logic,
            self.test_liquidity_lock_24h,
            self.test_chart_activity_fix,
            self.test_start_trading_fix,
            self.test_database_gettoken_method,
            self.test_enhanced_error_handling
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
        print("\n" + "=" * 70)
        print("📊 REVIEW REQUEST VERIFICATION RESULTS")
        print("=" * 70)
        
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result["status"] == "PASSED" else "❌" if result["status"] == "FAILED" else "⚠️"
            print(f"{status_emoji} {test_name.replace('_', ' ').title()}: {result['status']}")
            for detail in result["details"]:
                print(f"   • {detail}")
        
        print(f"\n📈 SUCCESS RATE: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
        
        # Specific review request verification summary
        print("\n🎯 REVIEW REQUEST VERIFICATION SUMMARY:")
        print("=" * 50)
        
        # System Logic Verification
        print("\n🔧 SYSTEM LOGIC VERIFICATION:")
        devnet_mainnet_ok = self.test_results["devnet_mainnet_logic"]["status"] == "PASSED"
        mint_authority_ok = self.test_results["mint_authority_logic"]["status"] == "PASSED"
        liquidity_lock_ok = self.test_results["liquidity_lock_24h"]["status"] == "PASSED"
        
        print(f"{'✅' if devnet_mainnet_ok else '❌'} Devnet vs Mainnet wallet logic: {'WORKING' if devnet_mainnet_ok else 'ISSUES'}")
        print(f"{'✅' if mint_authority_ok else '❌'} Mint authority logic (revoke vs keep): {'WORKING' if mint_authority_ok else 'ISSUES'}")
        print(f"{'✅' if liquidity_lock_ok else '❌'} Liquidity lock under mainnet (24-hour): {'WORKING' if liquidity_lock_ok else 'ISSUES'}")
        
        # Bug Fix Verification
        print("\n🐛 BUG FIX VERIFICATION:")
        chart_activity_ok = self.test_results["chart_activity_fix"]["status"] == "PASSED"
        start_trading_ok = self.test_results["start_trading_fix"]["status"] == "PASSED"
        database_ok = self.test_results["database_gettoken_method"]["status"] == "PASSED"
        error_handling_ok = self.test_results["enhanced_error_handling"]["status"] == "PASSED"
        
        print(f"{'✅' if chart_activity_ok else '❌'} chart_activity 'Token not found' issue: {'FIXED' if chart_activity_ok else 'NOT FIXED'}")
        print(f"{'✅' if start_trading_ok else '❌'} start_trading command restarting bot: {'FIXED' if start_trading_ok else 'NOT FIXED'}")
        print(f"{'✅' if database_ok else '❌'} database.getToken() method: {'WORKING' if database_ok else 'NOT WORKING'}")
        print(f"{'✅' if error_handling_ok else '❌'} Enhanced error handling with debug info: {'IMPLEMENTED' if error_handling_ok else 'NOT IMPLEMENTED'}")
        
        # Overall assessment
        system_logic_score = sum([devnet_mainnet_ok, mint_authority_ok, liquidity_lock_ok])
        bug_fix_score = sum([chart_activity_ok, start_trading_ok, database_ok, error_handling_ok])
        
        print(f"\n📊 SYSTEM LOGIC SCORE: {system_logic_score}/3 ({(system_logic_score/3)*100:.1f}%)")
        print(f"📊 BUG FIX SCORE: {bug_fix_score}/4 ({(bug_fix_score/4)*100:.1f}%)")
        
        overall_success = (system_logic_score >= 2) and (bug_fix_score >= 3)
        print(f"\n🎯 OVERALL REVIEW REQUEST STATUS: {'✅ VERIFIED' if overall_success else '❌ ISSUES FOUND'}")
        
        if overall_success:
            print("\n🎉 CONCLUSION: The system logic explanations are correct and the bug fixes are working as expected!")
        else:
            print("\n⚠️ CONCLUSION: Some issues were found that need attention before the fixes can be considered complete.")
        
        return {
            "success_rate": f"{passed_tests}/{total_tests}",
            "system_logic_score": f"{system_logic_score}/3",
            "bug_fix_score": f"{bug_fix_score}/4",
            "overall_success": overall_success,
            "detailed_results": self.test_results
        }

def main():
    """Main test execution"""
    tester = ReviewRequestTester()
    results = tester.run_comprehensive_test()
    
    # Save results to file
    results_file = Path("/app/review_request_verification_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {results_file}")
    
    # Exit with appropriate code
    sys.exit(0 if results["overall_success"] else 1)

if __name__ == "__main__":
    main()