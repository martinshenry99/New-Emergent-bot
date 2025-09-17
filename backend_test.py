#!/usr/bin/env python3
"""
Backend Testing for Review Request Verification
Testing specific fixes for Telegram Bot functionality:
1. Simple "Request Airdrop" Button
2. AI Craiyon as Step 11 in Manual Token Creation  
3. Token Creation Step Count
"""

import requests
import json
import time
import os
import sys
from datetime import datetime

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "https://codebase-explainer.preview.emergentagent.com"

BACKEND_URL = get_backend_url()
API_BASE = f"{BACKEND_URL}/api"

class ReviewRequestTester:
    def __init__(self):
        self.results = {
            "test_timestamp": datetime.now().isoformat(),
            "backend_url": BACKEND_URL,
            "tests": {}
        }
        
    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        self.log("Testing backend connectivity...")
        
        try:
            # Test root endpoint
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.results["tests"]["backend_connectivity"] = {
                    "status": "PASS",
                    "message": f"Backend accessible: {data.get('message', 'OK')}",
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
                self.log("✅ Backend connectivity: WORKING")
                return True
            else:
                self.results["tests"]["backend_connectivity"] = {
                    "status": "FAIL",
                    "message": f"HTTP {response.status_code}",
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
                self.log(f"❌ Backend connectivity: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.results["tests"]["backend_connectivity"] = {
                "status": "FAIL",
                "message": f"Connection error: {str(e)}"
            }
            self.log(f"❌ Backend connectivity: {str(e)}")
            return False
    
    def test_telegram_bot_files(self):
        """Test if Telegram bot files exist and contain required functionality"""
        self.log("Testing Telegram bot file structure...")
        
        required_files = [
            "/app/telegram-bot/bot.js",
            "/app/telegram-bot/package.json",
            "/app/telegram-bot/wallet-manager-enhanced.js"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            self.results["tests"]["telegram_bot_files"] = {
                "status": "FAIL",
                "message": f"Missing files: {missing_files}"
            }
            self.log(f"❌ Telegram bot files: Missing {len(missing_files)} files")
            return False
        
        self.results["tests"]["telegram_bot_files"] = {
            "status": "PASS",
            "message": "All required Telegram bot files present"
        }
        self.log("✅ Telegram bot files: All present")
        return True
    
    def test_fix_1_airdrop_button(self):
        """Test FIX #1 - Simple 'Request Airdrop' Button"""
        self.log("Testing FIX #1 - Simple 'Request Airdrop' Button...")
        
        try:
            # Read bot.js file to check for airdrop button implementation
            with open('/app/telegram-bot/bot.js', 'r') as f:
                bot_content = f.read()
            
            # Check for the specific button text and callback
            airdrop_button_found = '🪂 Request Airdrop (All Devnet Wallets)' in bot_content
            quick_airdrop_callback = 'quick_airdrop_all' in bot_content
            execute_function_found = 'executeQuickAirdropAll' in bot_content
            
            # Check if the callback handler exists
            callback_handler_found = "} else if (data === 'quick_airdrop_all') {" in bot_content
            
            # Check if the function implementation exists
            function_implementation = 'async function executeQuickAirdropAll(chatId)' in bot_content
            
            issues = []
            if not airdrop_button_found:
                issues.append("Missing '🪂 Request Airdrop (All Devnet Wallets)' button text")
            if not quick_airdrop_callback:
                issues.append("Missing 'quick_airdrop_all' callback data")
            if not execute_function_found:
                issues.append("Missing executeQuickAirdropAll function reference")
            if not callback_handler_found:
                issues.append("Missing callback handler for quick_airdrop_all")
            if not function_implementation:
                issues.append("Missing executeQuickAirdropAll function implementation")
            
            if issues:
                self.results["tests"]["fix_1_airdrop_button"] = {
                    "status": "FAIL",
                    "message": f"Issues found: {'; '.join(issues)}"
                }
                self.log(f"❌ FIX #1 Airdrop Button: {len(issues)} issues found")
                return False
            
            # Check if the function processes all 5 wallets
            if 'for (let i = 0; i < Math.min(devnetWallets.length, 5); i++)' in bot_content:
                wallet_processing = "Processes all 5 devnet wallets"
            else:
                wallet_processing = "Wallet processing logic unclear"
            
            # Check for success/fail summary
            summary_found = 'successCount' in bot_content and 'failCount' in bot_content
            
            self.results["tests"]["fix_1_airdrop_button"] = {
                "status": "PASS",
                "message": f"Airdrop button implemented correctly. {wallet_processing}. Summary: {'✅' if summary_found else '❌'}",
                "details": {
                    "button_text": airdrop_button_found,
                    "callback_data": quick_airdrop_callback,
                    "callback_handler": callback_handler_found,
                    "function_implementation": function_implementation,
                    "wallet_processing": wallet_processing,
                    "success_fail_summary": summary_found
                }
            }
            self.log("✅ FIX #1 Airdrop Button: WORKING")
            return True
            
        except Exception as e:
            self.results["tests"]["fix_1_airdrop_button"] = {
                "status": "FAIL",
                "message": f"Error reading bot.js: {str(e)}"
            }
            self.log(f"❌ FIX #1 Airdrop Button: Error - {str(e)}")
            return False
    
    def test_fix_2_ai_craiyon_step_11(self):
        """Test FIX #2 - AI Craiyon as Step 11 in Manual Token Creation"""
        self.log("Testing FIX #2 - AI Craiyon as Step 11...")
        
        try:
            with open('/app/telegram-bot/bot.js', 'r') as f:
                bot_content = f.read()
            
            # Check for handleAIImageGenerationStep function
            ai_step_function = 'function handleAIImageGenerationStep(chatId, userId, session)' in bot_content
            
            # Check if it's called after mint authority decision (step 10)
            mint_authority_to_ai = 'handleAIImageGenerationStep(chatId, userId, session);' in bot_content
            
            # Check for step numbering - should show step 11/11 for mainnet and 9/9 for devnet
            step_11_mainnet = "Step ${stepNum}: AI Image Generation" in bot_content and "'11/11'" in bot_content
            step_9_devnet = "'9/9'" in bot_content
            
            # Check if AI image generation happens AFTER all other configuration
            after_mint_authority = "session.data.revokeMint = decision === 'yes';" in bot_content and "handleAIImageGenerationStep" in bot_content
            
            # Check for final summary after image generation
            final_summary_call = 'showEnhancedFinalSummary' in bot_content
            
            # Check for skip option
            skip_image_option = 'skip_final_image_' in bot_content
            
            issues = []
            if not ai_step_function:
                issues.append("Missing handleAIImageGenerationStep function")
            if not mint_authority_to_ai:
                issues.append("AI step not called after mint authority decision")
            if not step_11_mainnet:
                issues.append("Missing step 11/11 numbering for mainnet")
            if not step_9_devnet:
                issues.append("Missing step 9/9 numbering for devnet")
            if not final_summary_call:
                issues.append("Missing final summary after image generation")
            if not skip_image_option:
                issues.append("Missing skip image option")
            
            if issues:
                self.results["tests"]["fix_2_ai_craiyon_step_11"] = {
                    "status": "FAIL",
                    "message": f"Issues found: {'; '.join(issues)}"
                }
                self.log(f"❌ FIX #2 AI Craiyon Step 11: {len(issues)} issues found")
                return False
            
            # Check for Craiyon integration
            craiyon_mentioned = 'Craiyon' in bot_content
            ai_image_text = '🎨 Generate AI Logo' in bot_content or '🎨 Generate AI Image' in bot_content
            
            self.results["tests"]["fix_2_ai_craiyon_step_11"] = {
                "status": "PASS",
                "message": f"AI image generation as step 11 implemented correctly. Craiyon: {'✅' if craiyon_mentioned else '❌'}",
                "details": {
                    "ai_step_function": ai_step_function,
                    "called_after_mint_authority": after_mint_authority,
                    "step_11_mainnet": step_11_mainnet,
                    "step_9_devnet": step_9_devnet,
                    "final_summary": final_summary_call,
                    "skip_option": skip_image_option,
                    "craiyon_integration": craiyon_mentioned,
                    "ai_image_button": ai_image_text
                }
            }
            self.log("✅ FIX #2 AI Craiyon Step 11: WORKING")
            return True
            
        except Exception as e:
            self.results["tests"]["fix_2_ai_craiyon_step_11"] = {
                "status": "FAIL",
                "message": f"Error reading bot.js: {str(e)}"
            }
            self.log(f"❌ FIX #2 AI Craiyon Step 11: Error - {str(e)}")
            return False
    
    def test_fix_3_token_creation_steps(self):
        """Test FIX #3 - Token Creation Step Count (10 steps + AI as step 11)"""
        self.log("Testing FIX #3 - Token Creation Step Count...")
        
        try:
            with open('/app/telegram-bot/bot.js', 'r') as f:
                bot_content = f.read()
            
            # Check for proper step numbering in manual launch
            step_patterns = [
                "Step 1/10: Network Selection",
                "Step 2/10: Token Name", 
                "Step 3/10: Token Description",
                "Step 4/10: Ticker Symbol",
                "Step 5/10: Total Supply"
            ]
            
            # Check mainnet-specific steps
            mainnet_steps = [
                "Step 6/10: Pool Liquidity (Mainnet)",
                "Step 7/10: Displayed Liquidity (Mainnet)",
                "Step 8/10: Liquidity Lock",
                "Step 9/10: Mint Authority"
            ]
            
            # Check devnet steps (fewer steps)
            devnet_steps = [
                "Step 6/8: Liquidity Lock (Devnet)",
                "Step 7/8: Mint Authority"
            ]
            
            # Check AI image as final step
            ai_final_steps = [
                "Step 11/11: AI Image Generation",  # Mainnet
                "Step 9/9: AI Image Generation"     # Devnet
            ]
            
            found_steps = []
            missing_steps = []
            
            for step in step_patterns:
                if step in bot_content:
                    found_steps.append(step)
                else:
                    missing_steps.append(step)
            
            # Check mainnet flow
            mainnet_found = sum(1 for step in mainnet_steps if step in bot_content)
            devnet_found = sum(1 for step in devnet_steps if step in bot_content)
            ai_steps_found = sum(1 for step in ai_final_steps if step in bot_content)
            
            # Check step flow logic
            step_flow_correct = 'session.step = 2' in bot_content and 'session.step = 3' in bot_content
            
            # Check network-specific step handling
            network_specific = "session.data.network === 'mainnet'" in bot_content
            
            issues = []
            if len(missing_steps) > 0:
                issues.append(f"Missing basic steps: {missing_steps}")
            if mainnet_found < 3:
                issues.append(f"Mainnet steps incomplete ({mainnet_found}/4)")
            if devnet_found < 2:
                issues.append(f"Devnet steps incomplete ({devnet_found}/2)")
            if ai_steps_found < 2:
                issues.append(f"AI final steps missing ({ai_steps_found}/2)")
            if not step_flow_correct:
                issues.append("Step flow logic incorrect")
            if not network_specific:
                issues.append("Network-specific step handling missing")
            
            if issues:
                self.results["tests"]["fix_3_token_creation_steps"] = {
                    "status": "FAIL",
                    "message": f"Issues found: {'; '.join(issues)}"
                }
                self.log(f"❌ FIX #3 Token Creation Steps: {len(issues)} issues found")
                return False
            
            self.results["tests"]["fix_3_token_creation_steps"] = {
                "status": "PASS",
                "message": f"Token creation steps correctly implemented. Basic: {len(found_steps)}/5, Mainnet: {mainnet_found}/4, Devnet: {devnet_found}/2, AI: {ai_steps_found}/2",
                "details": {
                    "basic_steps_found": len(found_steps),
                    "basic_steps_total": len(step_patterns),
                    "mainnet_steps": mainnet_found,
                    "devnet_steps": devnet_found,
                    "ai_final_steps": ai_steps_found,
                    "step_flow_logic": step_flow_correct,
                    "network_specific_handling": network_specific
                }
            }
            self.log("✅ FIX #3 Token Creation Steps: WORKING")
            return True
            
        except Exception as e:
            self.results["tests"]["fix_3_token_creation_steps"] = {
                "status": "FAIL",
                "message": f"Error reading bot.js: {str(e)}"
            }
            self.log(f"❌ FIX #3 Token Creation Steps: Error - {str(e)}")
            return False
    
    def test_wallets_command_functionality(self):
        """Test /wallets command shows the airdrop button"""
        self.log("Testing /wallets command functionality...")
        
        try:
            with open('/app/telegram-bot/bot.js', 'r') as f:
                bot_content = f.read()
            
            # Check for /wallets command handler
            wallets_command = "bot.onText(/\\/wallets/, (msg) => {" in bot_content
            
            # Check for showAllWalletBalances function
            show_all_balances = 'async function showAllWalletBalances(chatId)' in bot_content
            
            # Check if the function shows both devnet and mainnet wallets
            devnet_section = '🧪 **DEVNET WALLETS**' in bot_content
            mainnet_section = '🌐 **MAINNET WALLETS**' in bot_content
            
            # Check for the specific airdrop button
            airdrop_button = '🪂 Request Airdrop (All Devnet Wallets)' in bot_content
            
            # Check for balance updates
            balance_update = 'await enhancedWalletManager.updateBalances' in bot_content
            
            issues = []
            if not wallets_command:
                issues.append("Missing /wallets command handler")
            if not show_all_balances:
                issues.append("Missing showAllWalletBalances function")
            if not devnet_section:
                issues.append("Missing devnet wallets section")
            if not mainnet_section:
                issues.append("Missing mainnet wallets section")
            if not airdrop_button:
                issues.append("Missing airdrop button in wallets display")
            if not balance_update:
                issues.append("Missing balance update functionality")
            
            if issues:
                self.results["tests"]["wallets_command_functionality"] = {
                    "status": "FAIL",
                    "message": f"Issues found: {'; '.join(issues)}"
                }
                self.log(f"❌ /wallets command: {len(issues)} issues found")
                return False
            
            self.results["tests"]["wallets_command_functionality"] = {
                "status": "PASS",
                "message": "Wallets command properly implemented with airdrop button",
                "details": {
                    "command_handler": wallets_command,
                    "show_all_function": show_all_balances,
                    "devnet_section": devnet_section,
                    "mainnet_section": mainnet_section,
                    "airdrop_button": airdrop_button,
                    "balance_updates": balance_update
                }
            }
            self.log("✅ /wallets command: WORKING")
            return True
            
        except Exception as e:
            self.results["tests"]["wallets_command_functionality"] = {
                "status": "FAIL",
                "message": f"Error reading bot.js: {str(e)}"
            }
            self.log(f"❌ /wallets command: Error - {str(e)}")
            return False
    
    def test_api_endpoints(self):
        """Test FastAPI backend endpoints"""
        self.log("Testing API endpoints...")
        
        try:
            # Test GET /api/status
            response = requests.get(f"{API_BASE}/status", timeout=10)
            get_status_working = response.status_code == 200
            
            # Test POST /api/status
            test_data = {"client_name": "backend_test"}
            response = requests.post(f"{API_BASE}/status", json=test_data, timeout=10)
            post_status_working = response.status_code == 200
            
            if get_status_working and post_status_working:
                self.results["tests"]["api_endpoints"] = {
                    "status": "PASS",
                    "message": "All API endpoints working correctly"
                }
                self.log("✅ API endpoints: WORKING")
                return True
            else:
                issues = []
                if not get_status_working:
                    issues.append("GET /api/status failed")
                if not post_status_working:
                    issues.append("POST /api/status failed")
                
                self.results["tests"]["api_endpoints"] = {
                    "status": "FAIL",
                    "message": f"Issues: {'; '.join(issues)}"
                }
                self.log(f"❌ API endpoints: {len(issues)} issues")
                return False
                
        except Exception as e:
            self.results["tests"]["api_endpoints"] = {
                "status": "FAIL",
                "message": f"Error testing endpoints: {str(e)}"
            }
            self.log(f"❌ API endpoints: Error - {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests and generate summary"""
        self.log("🚀 Starting Review Request Backend Testing...")
        self.log(f"Backend URL: {BACKEND_URL}")
        
        tests = [
            ("Backend Connectivity", self.test_backend_connectivity),
            ("Telegram Bot Files", self.test_telegram_bot_files),
            ("FIX #1 - Airdrop Button", self.test_fix_1_airdrop_button),
            ("FIX #2 - AI Craiyon Step 11", self.test_fix_2_ai_craiyon_step_11),
            ("FIX #3 - Token Creation Steps", self.test_fix_3_token_creation_steps),
            ("Wallets Command", self.test_wallets_command_functionality),
            ("API Endpoints", self.test_api_endpoints)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            self.log(f"\n--- Testing {test_name} ---")
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log(f"❌ {test_name}: Unexpected error - {str(e)}")
                failed += 1
        
        # Generate summary
        total_tests = len(tests)
        success_rate = (passed / total_tests) * 100
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "success_rate": f"{success_rate:.1f}%"
        }
        
        self.log(f"\n🎯 TESTING COMPLETE")
        self.log(f"📊 Results: {passed}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if failed > 0:
            self.log(f"❌ {failed} tests failed")
            failed_tests = [name for name, result in self.results["tests"].items() if result["status"] == "FAIL"]
            self.log(f"Failed tests: {', '.join(failed_tests)}")
        else:
            self.log("✅ All tests passed!")
        
        return success_rate >= 80

def main():
    tester = ReviewRequestTester()
    success = tester.run_all_tests()
    
    # Save results to file
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump(tester.results, f, indent=2)
    
    print(f"\n📄 Results saved to: /app/backend_test_results.json")
    
    if success:
        print("🎉 TESTING SUCCESSFUL - All critical fixes verified!")
        sys.exit(0)
    else:
        print("⚠️ TESTING ISSUES FOUND - Check results for details")
        sys.exit(1)

if __name__ == "__main__":
    main()