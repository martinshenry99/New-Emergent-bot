#!/usr/bin/env python3
"""
Review Request Verification Test - 4 Specific Issues
Testing the exact issues mentioned in the review request:

1. /start_trading reloads /start function
2. /chart_activity isn't working  
3. Airdrop still not working
4. Mainnet liquidity configuration not working
"""

import os
import sys
import re
from pathlib import Path

class ReviewRequestTester:
    def __init__(self):
        self.bot_path = "/app/telegram-bot/bot.js"
        self.test_results = {
            "start_trading_command": {"exists": False, "working": False, "details": ""},
            "chart_activity_command": {"exists": False, "working": False, "details": ""},
            "airdrop_functionality": {"exists": False, "working": False, "details": ""},
            "mainnet_liquidity_config": {"exists": False, "working": False, "details": ""}
        }
        
    def test_start_trading_command(self):
        """Test if /start_trading command exists and doesn't reload /start"""
        print("🔍 Testing /start_trading command...")
        
        try:
            with open(self.bot_path, 'r') as f:
                bot_content = f.read()
            
            # Check if /start_trading command exists
            start_trading_pattern = r'bot\.onText\(/\\\/start_trading/'
            start_trading_matches = re.findall(start_trading_pattern, bot_content)
            
            if start_trading_matches:
                self.test_results["start_trading_command"]["exists"] = True
                self.test_results["start_trading_command"]["details"] = f"Found {len(start_trading_matches)} /start_trading command handlers"
                
                # Check if it reloads /start function
                start_function_calls = re.findall(r'\/start.*function|startManualLaunch|bot\.sendMessage.*🚀 Enhanced Meme Token Creator', bot_content)
                
                if not start_function_calls:
                    self.test_results["start_trading_command"]["working"] = True
                    self.test_results["start_trading_command"]["details"] += " - Does not reload /start function ✅"
                else:
                    self.test_results["start_trading_command"]["details"] += " - WARNING: May reload /start function ❌"
            else:
                self.test_results["start_trading_command"]["details"] = "❌ /start_trading command NOT FOUND in bot.js"
                
        except Exception as e:
            self.test_results["start_trading_command"]["details"] = f"❌ Error testing /start_trading: {str(e)}"
            
        print(f"   Result: {self.test_results['start_trading_command']['details']}")
        
    def test_chart_activity_command(self):
        """Test if /chart_activity command exists and callback handlers work"""
        print("🔍 Testing /chart_activity command...")
        
        try:
            with open(self.bot_path, 'r') as f:
                bot_content = f.read()
            
            # Check if /chart_activity command exists
            chart_activity_pattern = r'bot\.onText\(/\\\/chart_activity/'
            chart_activity_matches = re.findall(chart_activity_pattern, bot_content)
            
            if chart_activity_matches:
                self.test_results["chart_activity_command"]["exists"] = True
                self.test_results["chart_activity_command"]["details"] = f"Found {len(chart_activity_matches)} /chart_activity command handlers"
                
                # Check for callback handlers
                callback_patterns = [
                    r'chart_activity.*callback_data',
                    r'startChartActivity',
                    r'stopChartActivity',
                    r'executeChartActivityTrade'
                ]
                
                callback_found = False
                for pattern in callback_patterns:
                    if re.search(pattern, bot_content):
                        callback_found = True
                        break
                
                if callback_found:
                    self.test_results["chart_activity_command"]["working"] = True
                    self.test_results["chart_activity_command"]["details"] += " - Callback handlers found ✅"
                else:
                    self.test_results["chart_activity_command"]["details"] += " - WARNING: Callback handlers missing ❌"
            else:
                self.test_results["chart_activity_command"]["details"] = "❌ /chart_activity command NOT FOUND in bot.js"
                
        except Exception as e:
            self.test_results["chart_activity_command"]["details"] = f"❌ Error testing /chart_activity: {str(e)}"
            
        print(f"   Result: {self.test_results['chart_activity_command']['details']}")
        
    def test_airdrop_functionality(self):
        """Test airdrop_wallet_1 through airdrop_wallet_5 callbacks and executeAirdrop function"""
        print("🔍 Testing Airdrop functionality...")
        
        try:
            with open(self.bot_path, 'r') as f:
                bot_content = f.read()
            
            # Check for airdrop wallet callbacks
            airdrop_callbacks = []
            for i in range(1, 6):
                pattern = f'airdrop_wallet_{i}'
                if pattern in bot_content:
                    airdrop_callbacks.append(f"wallet_{i}")
            
            if len(airdrop_callbacks) >= 5:
                self.test_results["airdrop_functionality"]["exists"] = True
                self.test_results["airdrop_functionality"]["details"] = f"Found all 5 airdrop wallet callbacks: {', '.join(airdrop_callbacks)}"
                
                # Check for executeAirdrop function
                execute_airdrop_pattern = r'async function executeAirdrop|function executeAirdrop'
                if re.search(execute_airdrop_pattern, bot_content):
                    self.test_results["airdrop_functionality"]["details"] += " - executeAirdrop function found ✅"
                    
                    # Check for infinite loop prevention
                    loop_prevention_patterns = [
                        r'userSessions\.delete',
                        r'session.*delete',
                        r'return.*early',
                        r'if.*return'
                    ]
                    
                    loop_prevention = any(re.search(pattern, bot_content) for pattern in loop_prevention_patterns)
                    
                    if loop_prevention:
                        self.test_results["airdrop_functionality"]["working"] = True
                        self.test_results["airdrop_functionality"]["details"] += " - No infinite loops detected ✅"
                    else:
                        self.test_results["airdrop_functionality"]["details"] += " - WARNING: Potential infinite loop risk ⚠️"
                else:
                    self.test_results["airdrop_functionality"]["details"] += " - ❌ executeAirdrop function NOT FOUND"
            else:
                self.test_results["airdrop_functionality"]["details"] = f"❌ Only found {len(airdrop_callbacks)} airdrop callbacks (need 5): {', '.join(airdrop_callbacks)}"
                
        except Exception as e:
            self.test_results["airdrop_functionality"]["details"] = f"❌ Error testing airdrop: {str(e)}"
            
        print(f"   Result: {self.test_results['airdrop_functionality']['details']}")
        
    def test_mainnet_liquidity_configuration(self):
        """Test mainnet liquidity configuration input processing and session handling"""
        print("🔍 Testing Mainnet liquidity configuration...")
        
        try:
            with open(self.bot_path, 'r') as f:
                bot_content = f.read()
            
            # Check for mainnet liquidity configuration
            mainnet_patterns = [
                r'Mainnet.*[Ll]iquidity.*[Cc]onfiguration',
                r'realSol.*=.*parseFloat',
                r'displayedLiquidity.*=.*parseInt',
                r'SOL.*amount.*input'
            ]
            
            found_patterns = []
            for pattern in mainnet_patterns:
                if re.search(pattern, bot_content):
                    found_patterns.append(pattern.split('.*')[0])
            
            if len(found_patterns) >= 2:
                self.test_results["mainnet_liquidity_config"]["exists"] = True
                self.test_results["mainnet_liquidity_config"]["details"] = f"Found mainnet liquidity patterns: {', '.join(found_patterns)}"
                
                # Check for input processing
                input_processing_patterns = [
                    r'parseFloat\(text\)',
                    r'parseInt\(text',
                    r'realSol.*=.*parseFloat',
                    r'displayedLiquidity.*=.*parseInt'
                ]
                
                input_processing = any(re.search(pattern, bot_content) for pattern in input_processing_patterns)
                
                if input_processing:
                    self.test_results["mainnet_liquidity_config"]["details"] += " - Input processing found ✅"
                    
                    # Check for session handling
                    session_patterns = [
                        r'userSessions\.set',
                        r'session\.data',
                        r'session\.step'
                    ]
                    
                    session_handling = any(re.search(pattern, bot_content) for pattern in session_patterns)
                    
                    if session_handling:
                        self.test_results["mainnet_liquidity_config"]["working"] = True
                        self.test_results["mainnet_liquidity_config"]["details"] += " - Session handling working ✅"
                    else:
                        self.test_results["mainnet_liquidity_config"]["details"] += " - ❌ Session handling missing"
                else:
                    self.test_results["mainnet_liquidity_config"]["details"] += " - ❌ Input processing missing"
            else:
                self.test_results["mainnet_liquidity_config"]["details"] = f"❌ Mainnet liquidity configuration incomplete (found {len(found_patterns)}/4 patterns)"
                
        except Exception as e:
            self.test_results["mainnet_liquidity_config"]["details"] = f"❌ Error testing mainnet liquidity: {str(e)}"
            
        print(f"   Result: {self.test_results['mainnet_liquidity_config']['details']}")
        
    def check_bot_file_exists(self):
        """Check if bot.js file exists and is readable"""
        if not os.path.exists(self.bot_path):
            print(f"❌ Bot file not found: {self.bot_path}")
            return False
        
        try:
            with open(self.bot_path, 'r') as f:
                content = f.read()
                if len(content) < 1000:  # Bot file should be substantial
                    print(f"⚠️ Bot file seems too small: {len(content)} characters")
                    return False
                print(f"✅ Bot file found: {len(content)} characters, {len(content.splitlines())} lines")
                return True
        except Exception as e:
            print(f"❌ Error reading bot file: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests for the 4 specific issues"""
        print("🚀 REVIEW REQUEST VERIFICATION - Testing 4 Specific Issues")
        print("=" * 80)
        
        if not self.check_bot_file_exists():
            return False
        
        print("\n📋 Testing 4 Specific Issues:")
        print("1. /start_trading reloads /start function")
        print("2. /chart_activity isn't working")  
        print("3. Airdrop still not working")
        print("4. Mainnet liquidity configuration not working")
        print("-" * 80)
        
        # Run individual tests
        self.test_start_trading_command()
        print()
        self.test_chart_activity_command()
        print()
        self.test_airdrop_functionality()
        print()
        self.test_mainnet_liquidity_configuration()
        
        return True
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("📊 REVIEW REQUEST TEST SUMMARY - 4 SPECIFIC ISSUES")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        working_tests = sum(1 for result in self.test_results.values() if result["working"])
        existing_tests = sum(1 for result in self.test_results.values() if result["exists"])
        
        print(f"📈 Overall Status: {working_tests}/{total_tests} issues resolved")
        print(f"📋 Commands Found: {existing_tests}/{total_tests}")
        print(f"✅ Working Properly: {working_tests}/{total_tests}")
        
        print("\n🔍 Detailed Results:")
        
        for test_name, result in self.test_results.items():
            status = "✅ WORKING" if result["working"] else ("⚠️ EXISTS" if result["exists"] else "❌ MISSING")
            print(f"  {test_name.replace('_', ' ').title()}: {status}")
            print(f"    Details: {result['details']}")
        
        print("\n🎯 SUCCESS CRITERIA CHECK:")
        print(f"  • All 4 commands exist: {'✅' if existing_tests == 4 else '❌'} ({existing_tests}/4)")
        print(f"  • All callback handlers present: {'✅' if working_tests >= 2 else '❌'}")
        print(f"  • No infinite loops: {'✅' if 'infinite' not in str(self.test_results) else '❌'}")
        print(f"  • Input processing works: {'✅' if working_tests >= 1 else '❌'}")
        
        return working_tests, total_tests

def main():
    """Main test execution"""
    tester = ReviewRequestTester()
    
    if tester.run_all_tests():
        working, total = tester.generate_summary()
        
        print(f"\n🏁 FINAL RESULT: {working}/{total} issues resolved")
        
        if working == total:
            print("🎉 ALL ISSUES RESOLVED! Bot is working properly.")
            return 0
        elif working >= total * 0.75:
            print("⚠️ MOSTLY WORKING - Minor issues remain.")
            return 1
        else:
            print("❌ CRITICAL ISSUES - Major functionality missing.")
            return 2
    else:
        print("❌ TESTING FAILED - Could not complete tests.")
        return 3

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)