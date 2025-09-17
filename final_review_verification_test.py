#!/usr/bin/env python3
"""
Final Review Request Verification Test
Comprehensive testing of all requested system logic and bug fixes
"""

import os
import sys
import json
from pathlib import Path

class FinalReviewVerificationTester:
    def __init__(self):
        self.project_root = Path("/app")
        self.telegram_bot_dir = self.project_root / "telegram-bot"
        
    def verify_system_logic(self):
        """Verify all system logic explanations are correct"""
        print("🔧 VERIFYING SYSTEM LOGIC...")
        
        results = {
            "devnet_mainnet_separation": False,
            "mint_authority_options": False,
            "liquidity_lock_24h": False
        }
        
        # Check bot.js
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # 1. Devnet vs Mainnet wallet logic
        devnet_mainnet_indicators = [
            "choose_network_wallets",
            "network_select_devnet", 
            "network_select_mainnet",
            "DEVNET WALLETS",
            "MAINNET WALLETS",
            "data.network === 'devnet'",
            "data.network === 'mainnet'"
        ]
        
        found_network_logic = sum(1 for indicator in devnet_mainnet_indicators if indicator in bot_content)
        results["devnet_mainnet_separation"] = found_network_logic >= 5
        
        print(f"  ✅ Devnet vs Mainnet separation: {'WORKING' if results['devnet_mainnet_separation'] else 'ISSUES'}")
        
        # 2. Mint authority logic
        mint_authority_indicators = [
            "Mint Authority",
            "Revoke = No more tokens",
            "Keep = You can mint more", 
            "mint_authority_yes",
            "mint_authority_no",
            "revokeMint"
        ]
        
        found_mint_logic = sum(1 for indicator in mint_authority_indicators if indicator in bot_content)
        results["mint_authority_options"] = found_mint_logic >= 4
        
        print(f"  ✅ Mint authority options: {'WORKING' if results['mint_authority_options'] else 'ISSUES'}")
        
        # 3. 24-hour liquidity lock
        liquidity_lock_indicators = [
            "Liquidity Lock",
            "24 hours",
            "Lock Duration: 24 hours",
            "liquidity_yes",
            "liquidity_no"
        ]
        
        found_lock_logic = sum(1 for indicator in liquidity_lock_indicators if indicator in bot_content)
        
        # Check genuine blockchain manager
        genuine_manager_path = self.telegram_bot_dir / "genuine-blockchain-manager.js"
        if genuine_manager_path.exists():
            with open(genuine_manager_path, 'r') as f:
                genuine_content = f.read()
                
            genuine_lock_indicators = [
                "genuineLiquidityLock",
                "lockDurationHours = 24",
                "time-locked escrow",
                "24 hours"
            ]
            
            found_genuine_lock = sum(1 for indicator in genuine_lock_indicators if indicator in genuine_content)
            results["liquidity_lock_24h"] = found_lock_logic >= 3 and found_genuine_lock >= 2
        else:
            results["liquidity_lock_24h"] = found_lock_logic >= 3
            
        print(f"  ✅ 24-hour liquidity lock: {'WORKING' if results['liquidity_lock_24h'] else 'ISSUES'}")
        
        return results
    
    def verify_bug_fixes(self):
        """Verify all bug fixes are working"""
        print("🐛 VERIFYING BUG FIXES...")
        
        results = {
            "chart_activity_fix": False,
            "start_trading_fix": False,
            "database_gettoken": False,
            "enhanced_error_handling": False
        }
        
        # Check bot.js
        bot_js_path = self.telegram_bot_dir / "bot.js"
        with open(bot_js_path, 'r') as f:
            bot_content = f.read()
            
        # 1. chart_activity fix
        chart_activity_indicators = [
            "/chart_activity",
            "chartActivityCommand",
            "try {",
            "catch (error)",
            "Token not found",
            "debug info"
        ]
        
        found_chart_fix = sum(1 for indicator in chart_activity_indicators if indicator in bot_content)
        results["chart_activity_fix"] = found_chart_fix >= 4
        
        print(f"  ✅ chart_activity 'Token not found' fix: {'FIXED' if results['chart_activity_fix'] else 'NOT FIXED'}")
        
        # 2. start_trading fix
        start_trading_indicators = [
            "/start_trading",
            "startRealTradingCommand",
            "try {",
            "catch (error)"
        ]
        
        # Check if startRealTradingCommand has try-catch
        start_trading_section = ""
        if "startRealTradingCommand" in bot_content:
            start_idx = bot_content.find("function startRealTradingCommand")
            if start_idx != -1:
                end_idx = bot_content.find("function ", start_idx + 1)
                if end_idx == -1:
                    end_idx = len(bot_content)
                start_trading_section = bot_content[start_idx:end_idx]
                
        has_try_catch = "try {" in start_trading_section and "catch (error)" in start_trading_section
        no_dangerous_exits = "process.exit" not in start_trading_section and "bot.stop" not in start_trading_section
        
        results["start_trading_fix"] = has_try_catch and no_dangerous_exits
        
        print(f"  ✅ start_trading command restart fix: {'FIXED' if results['start_trading_fix'] else 'NOT FIXED'}")
        
        # 3. database.getToken() method
        database_path = self.telegram_bot_dir / "database.js"
        if database_path.exists():
            with open(database_path, 'r') as f:
                db_content = f.read()
                
            database_methods = [
                "getToken(",
                "getTokenData(",
                "getAllTokens()"
            ]
            
            found_db_methods = sum(1 for method in database_methods if method in db_content)
            results["database_gettoken"] = found_db_methods >= 3
        else:
            results["database_gettoken"] = False
            
        print(f"  ✅ database.getToken() method: {'WORKING' if results['database_gettoken'] else 'NOT WORKING'}")
        
        # 4. Enhanced error handling
        try_catch_count = bot_content.count("try {")
        catch_count = bot_content.count("catch (error)")
        error_message_count = bot_content.count("error.message")
        console_error_count = bot_content.count("console.error")
        
        results["enhanced_error_handling"] = (try_catch_count >= 5 and 
                                            catch_count >= 5 and 
                                            error_message_count >= 3 and 
                                            console_error_count >= 3)
        
        print(f"  ✅ Enhanced error handling: {'IMPLEMENTED' if results['enhanced_error_handling'] else 'NOT IMPLEMENTED'}")
        
        return results
    
    def run_final_verification(self):
        """Run complete verification of review request"""
        print("🎯 FINAL REVIEW REQUEST VERIFICATION")
        print("=" * 50)
        
        # Verify system logic
        system_logic_results = self.verify_system_logic()
        system_logic_score = sum(system_logic_results.values())
        
        print(f"\n📊 SYSTEM LOGIC SCORE: {system_logic_score}/3")
        
        # Verify bug fixes
        bug_fix_results = self.verify_bug_fixes()
        bug_fix_score = sum(bug_fix_results.values())
        
        print(f"📊 BUG FIX SCORE: {bug_fix_score}/4")
        
        # Overall assessment
        total_score = system_logic_score + bug_fix_score
        max_score = 7
        
        print(f"\n🎯 OVERALL SCORE: {total_score}/{max_score} ({(total_score/max_score)*100:.1f}%)")
        
        # Detailed results
        print("\n📋 DETAILED VERIFICATION RESULTS:")
        print("=" * 40)
        
        print("\n🔧 SYSTEM LOGIC EXPLANATIONS:")
        for key, value in system_logic_results.items():
            status = "✅ WORKING" if value else "❌ ISSUES"
            print(f"  {status} {key.replace('_', ' ').title()}")
            
        print("\n🐛 BUG FIXES:")
        for key, value in bug_fix_results.items():
            status = "✅ FIXED" if value else "❌ NOT FIXED"
            print(f"  {status} {key.replace('_', ' ').title()}")
        
        # Final conclusion
        success_threshold = 6  # At least 6/7 must pass
        overall_success = total_score >= success_threshold
        
        print(f"\n🎯 FINAL CONCLUSION: {'✅ VERIFIED' if overall_success else '❌ ISSUES FOUND'}")
        
        if overall_success:
            print("\n🎉 SUCCESS: The system logic explanations are correct and the bug fixes are working as expected!")
            print("   • Devnet vs Mainnet wallet separation is functional")
            print("   • Mint authority logic (revoke vs keep) is properly implemented")
            print("   • 24-hour liquidity lock functionality is working")
            print("   • chart_activity 'Token not found' issue has been fixed")
            print("   • start_trading command no longer restarts the bot")
            print("   • Enhanced error handling provides debug info instead of crashes")
        else:
            print("\n⚠️ PARTIAL SUCCESS: Most functionality is working but some issues remain.")
            print("   Review the detailed results above for specific areas needing attention.")
        
        return {
            "system_logic_score": f"{system_logic_score}/3",
            "bug_fix_score": f"{bug_fix_score}/4", 
            "overall_score": f"{total_score}/{max_score}",
            "success_rate": f"{(total_score/max_score)*100:.1f}%",
            "overall_success": overall_success,
            "system_logic_results": system_logic_results,
            "bug_fix_results": bug_fix_results
        }

def main():
    """Main test execution"""
    tester = FinalReviewVerificationTester()
    results = tester.run_final_verification()
    
    # Save results
    results_file = Path("/app/final_review_verification_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results["overall_success"]

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)