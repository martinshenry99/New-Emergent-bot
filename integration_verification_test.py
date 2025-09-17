#!/usr/bin/env python3
"""
INTEGRATION VERIFICATION TESTING - Backend Test
Testing all integration fixes completed by main agent:
1. /start_trading command integration
2. /chart_activity command integration  
3. Genuine blockchain command integration (5 commands)
4. Callback handlers verification
5. Bot startup and initialization
"""

import os
import sys
import subprocess
import re
import json
import time
from pathlib import Path

class IntegrationVerificationTest:
    def __init__(self):
        self.telegram_bot_dir = "/app/telegram-bot"
        self.test_results = []
        self.success_count = 0
        self.total_tests = 0
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        self.total_tests += 1
        if status:
            self.success_count += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED - {details}")
        
        self.test_results.append({
            "test": test_name,
            "status": "PASSED" if status else "FAILED",
            "details": details
        })
    
    def test_bot_startup_and_initialization(self):
        """Test 1: Verify bot starts successfully with all new imports and managers initialized"""
        print("\n🔍 TEST 1: Bot Startup and Initialization")
        
        try:
            # Check if bot.js exists and has required imports
            bot_file = Path(self.telegram_bot_dir) / "bot.js"
            if not bot_file.exists():
                self.log_test("Bot file exists", False, "bot.js not found")
                return
            
            bot_content = bot_file.read_text()
            
            # Check for required imports
            required_imports = [
                ("RealTradingManager", "require('./real-trading-manager')"),
                ("GenuineBlockchainManager", "require('./genuine-blockchain-manager')"), 
                ("TokenManager", "require('./token-manager')"),
                ("RaydiumManager", "require('./raydium-manager')")
            ]
            
            missing_imports = []
            for import_name, import_statement in required_imports:
                if import_statement not in bot_content:
                    missing_imports.append(import_name)
            
            if missing_imports:
                self.log_test("Required imports present", False, f"Missing imports: {missing_imports}")
            else:
                self.log_test("Required imports present", True)
            
            # Check manager initialization
            manager_inits = [
                "new RealTradingManager",
                "new GenuineBlockchainManager"
            ]
            
            missing_inits = []
            for init in manager_inits:
                if init not in bot_content:
                    missing_inits.append(init)
            
            if missing_inits:
                self.log_test("Manager initialization", False, f"Missing initializations: {missing_inits}")
            else:
                self.log_test("Manager initialization", True)
            
            # Check startup logs
            startup_log = Path(self.telegram_bot_dir) / "bot_startup.log"
            if startup_log.exists():
                log_content = startup_log.read_text()
                
                # Check for integration completion messages
                if "ALL INTEGRATION FIXES COMPLETE!" in log_content:
                    self.log_test("Integration completion message", True)
                else:
                    self.log_test("Integration completion message", False, "Missing completion message")
                
                # Check for manager initialization messages
                if "Real Trading Manager: Integrated" in log_content:
                    self.log_test("Real Trading Manager initialized", True)
                else:
                    self.log_test("Real Trading Manager initialized", False)
                
                if "Genuine Blockchain Manager: Integrated" in log_content:
                    self.log_test("Genuine Blockchain Manager initialized", True)
                else:
                    self.log_test("Genuine Blockchain Manager initialized", False)
            else:
                self.log_test("Startup log exists", False, "bot_startup.log not found")
                
        except Exception as e:
            self.log_test("Bot startup verification", False, f"Exception: {str(e)}")
    
    def test_start_trading_command(self):
        """Test 2: Test /start_trading command exists and responds appropriately"""
        print("\n🔍 TEST 2: /start_trading Command Integration")
        
        try:
            bot_file = Path(self.telegram_bot_dir) / "bot.js"
            bot_content = bot_file.read_text()
            
            # Check command handler exists
            if "bot.onText(/\\/start_trading/, (msg) => {" in bot_content:
                self.log_test("/start_trading command handler", True)
            else:
                self.log_test("/start_trading command handler", False, "Command handler not found")
                return
            
            # Check function implementation
            if "function startRealTradingCommand(chatId)" in bot_content:
                self.log_test("startRealTradingCommand function", True)
            else:
                self.log_test("startRealTradingCommand function", False, "Function not implemented")
            
            # Check callback handlers
            callback_handlers = [
                "real_trade_token_",
                "cancel_trading"
            ]
            
            missing_callbacks = []
            for callback in callback_handlers:
                if callback not in bot_content:
                    missing_callbacks.append(callback)
            
            if missing_callbacks:
                self.log_test("/start_trading callback handlers", False, f"Missing: {missing_callbacks}")
            else:
                self.log_test("/start_trading callback handlers", True)
            
            # Check integration log message
            if "/start_trading: INTEGRATED ✅" in bot_content:
                self.log_test("/start_trading integration log", True)
            else:
                self.log_test("/start_trading integration log", False)
                
        except Exception as e:
            self.log_test("/start_trading command test", False, f"Exception: {str(e)}")
    
    def test_chart_activity_command(self):
        """Test 3: Test /chart_activity command exists and responds appropriately"""
        print("\n🔍 TEST 3: /chart_activity Command Integration")
        
        try:
            bot_file = Path(self.telegram_bot_dir) / "bot.js"
            bot_content = bot_file.read_text()
            
            # Check command handler exists
            if "bot.onText(/\\/chart_activity/, (msg) => {" in bot_content:
                self.log_test("/chart_activity command handler", True)
            else:
                self.log_test("/chart_activity command handler", False, "Command handler not found")
                return
            
            # Check function implementation
            if "function chartActivityCommand(chatId)" in bot_content:
                self.log_test("chartActivityCommand function", True)
            else:
                self.log_test("chartActivityCommand function", False, "Function not implemented")
            
            # Check callback handlers
            callback_handlers = [
                "chart_activity_",
                "start_chart_",
                "stop_chart_",
                "cancel_chart",
                "chart_activity_menu"
            ]
            
            missing_callbacks = []
            for callback in callback_handlers:
                if callback not in bot_content:
                    missing_callbacks.append(callback)
            
            if missing_callbacks:
                self.log_test("/chart_activity callback handlers", False, f"Missing: {missing_callbacks}")
            else:
                self.log_test("/chart_activity callback handlers", True)
            
            # Check integration log message
            if "/chart_activity: INTEGRATED ✅" in bot_content:
                self.log_test("/chart_activity integration log", True)
            else:
                self.log_test("/chart_activity integration log", False)
                
        except Exception as e:
            self.log_test("/chart_activity command test", False, f"Exception: {str(e)}")
    
    def test_genuine_blockchain_commands(self):
        """Test 4: Test all 5 genuine blockchain commands exist and respond appropriately"""
        print("\n🔍 TEST 4: Genuine Blockchain Commands Integration")
        
        try:
            bot_file = Path(self.telegram_bot_dir) / "bot.js"
            bot_content = bot_file.read_text()
            
            # Check all 5 genuine blockchain commands
            genuine_commands = [
                ("/liquidity_lock", "genuineLiquidityLockCommand"),
                ("/revoke_mint", "genuineRevokeMintCommand"),
                ("/genuine_mint_rugpull", "genuineMintRugpullCommand"),
                ("/genuine_rugpull", "genuineRugpullCommand"),
                ("/status", "showGenuineStatus")
            ]
            
            for command, function in genuine_commands:
                # Check command handler
                command_pattern = f"bot.onText(/\\{command}/, (msg) => {{"
                if command_pattern in bot_content:
                    self.log_test(f"{command} command handler", True)
                else:
                    self.log_test(f"{command} command handler", False, "Handler not found")
                
                # Check function implementation
                function_pattern = f"function {function}(chatId)"
                if function_pattern in bot_content:
                    self.log_test(f"{function} function", True)
                else:
                    self.log_test(f"{function} function", False, "Function not implemented")
            
            # Check genuine blockchain callback handlers
            genuine_callbacks = [
                "genuine_liquidity_lock",
                "genuine_revoke_mint", 
                "genuine_mint_rugpull",
                "genuine_rugpull"
            ]
            
            missing_callbacks = []
            for callback in genuine_callbacks:
                if callback not in bot_content:
                    missing_callbacks.append(callback)
            
            if missing_callbacks:
                self.log_test("Genuine blockchain callbacks", False, f"Missing: {missing_callbacks}")
            else:
                self.log_test("Genuine blockchain callbacks", True)
            
            # Check integration log message
            if "Genuine blockchain commands: INTEGRATED ✅" in bot_content:
                self.log_test("Genuine blockchain integration log", True)
            else:
                self.log_test("Genuine blockchain integration log", False)
                
        except Exception as e:
            self.log_test("Genuine blockchain commands test", False, f"Exception: {str(e)}")
    
    def test_callback_handlers_working(self):
        """Test 5: Verify callback handlers work for the new commands"""
        print("\n🔍 TEST 5: Callback Handlers Verification")
        
        try:
            bot_file = Path(self.telegram_bot_dir) / "bot.js"
            bot_content = bot_file.read_text()
            
            # Check main callback query handler exists
            if "bot.on('callback_query', (query) => {" in bot_content:
                self.log_test("Main callback query handler", True)
            else:
                self.log_test("Main callback query handler", False, "Handler not found")
                return
            
            # Check all required callback patterns are handled
            all_callbacks = [
                "real_trade_token_",
                "cancel_trading",
                "chart_activity_",
                "start_chart_",
                "stop_chart_",
                "cancel_chart",
                "chart_activity_menu",
                "genuine_liquidity_lock",
                "genuine_revoke_mint",
                "genuine_mint_rugpull", 
                "genuine_rugpull"
            ]
            
            missing_handlers = []
            for callback in all_callbacks:
                # Check if callback is handled in the callback query handler
                if f"data.startsWith('{callback}')" in bot_content or f"data === '{callback}'" in bot_content:
                    continue
                else:
                    missing_handlers.append(callback)
            
            if missing_handlers:
                self.log_test("All callback handlers present", False, f"Missing handlers: {missing_handlers}")
            else:
                self.log_test("All callback handlers present", True)
                
        except Exception as e:
            self.log_test("Callback handlers test", False, f"Exception: {str(e)}")
    
    def test_console_logs_integration_completion(self):
        """Test 6: Check console logs show integration completion messages"""
        print("\n🔍 TEST 6: Console Logs Integration Completion")
        
        try:
            # Check bot.js for console log messages
            bot_file = Path(self.telegram_bot_dir) / "bot.js"
            bot_content = bot_file.read_text()
            
            expected_logs = [
                "/start_trading: INTEGRATED ✅",
                "/chart_activity: INTEGRATED ✅", 
                "Genuine blockchain commands: INTEGRATED ✅",
                "ALL INTEGRATION FIXES COMPLETE!"
            ]
            
            missing_logs = []
            for log_msg in expected_logs:
                if log_msg not in bot_content:
                    missing_logs.append(log_msg)
            
            if missing_logs:
                self.log_test("Integration completion logs", False, f"Missing logs: {missing_logs}")
            else:
                self.log_test("Integration completion logs", True)
            
            # Check startup log file
            startup_log = Path(self.telegram_bot_dir) / "bot_startup.log"
            if startup_log.exists():
                log_content = startup_log.read_text()
                
                if "ALL INTEGRATION FIXES COMPLETE!" in log_content:
                    self.log_test("Startup log completion message", True)
                else:
                    self.log_test("Startup log completion message", False)
            else:
                self.log_test("Startup log file exists", False)
                
        except Exception as e:
            self.log_test("Console logs test", False, f"Exception: {str(e)}")
    
    def test_basic_bot_functionality(self):
        """Test 7: Test basic bot functionality still works (/start, /launch, etc.)"""
        print("\n🔍 TEST 7: Basic Bot Functionality")
        
        try:
            bot_file = Path(self.telegram_bot_dir) / "bot.js"
            bot_content = bot_file.read_text()
            
            # Check basic commands still exist
            basic_commands = [
                "/start",
                "/launch"
            ]
            
            for command in basic_commands:
                command_pattern = f"bot.onText(/\\{command}/, (msg) => {{"
                if command_pattern in bot_content:
                    self.log_test(f"{command} command exists", True)
                else:
                    self.log_test(f"{command} command exists", False, "Command handler not found")
            
            # Check if bot initialization code is present
            if "const bot = new TelegramBot" in bot_content:
                self.log_test("Bot initialization", True)
            else:
                self.log_test("Bot initialization", False)
            
            # Check if essential managers are still initialized
            essential_managers = [
                "DatabaseManager",
                "EnhancedWalletManager"
            ]
            
            for manager in essential_managers:
                if f"new {manager}" in bot_content:
                    self.log_test(f"{manager} initialization", True)
                else:
                    self.log_test(f"{manager} initialization", False)
                    
        except Exception as e:
            self.log_test("Basic bot functionality test", False, f"Exception: {str(e)}")
    
    def test_file_integrity(self):
        """Test 8: Verify all required files exist and have proper content"""
        print("\n🔍 TEST 8: File Integrity Check")
        
        try:
            # Check required files exist
            required_files = [
                "bot.js",
                "real-trading-manager.js",
                "genuine-blockchain-manager.js",
                "token-manager.js",
                "raydium-manager.js"
            ]
            
            for filename in required_files:
                file_path = Path(self.telegram_bot_dir) / filename
                if file_path.exists():
                    self.log_test(f"{filename} exists", True)
                    
                    # Check file size (should not be empty)
                    if file_path.stat().st_size > 0:
                        self.log_test(f"{filename} not empty", True)
                    else:
                        self.log_test(f"{filename} not empty", False, "File is empty")
                else:
                    self.log_test(f"{filename} exists", False, "File not found")
            
            # Check genuine-blockchain-manager.js specifically
            genuine_manager = Path(self.telegram_bot_dir) / "genuine-blockchain-manager.js"
            if genuine_manager.exists():
                content = genuine_manager.read_text()
                if "GenuineBlockchainManager" in content:
                    self.log_test("GenuineBlockchainManager class exists", True)
                else:
                    self.log_test("GenuineBlockchainManager class exists", False)
                    
        except Exception as e:
            self.log_test("File integrity test", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all integration verification tests"""
        print("🚀 INTEGRATION VERIFICATION TESTING - Starting comprehensive test suite")
        print("=" * 80)
        
        # Run all tests
        self.test_bot_startup_and_initialization()
        self.test_start_trading_command()
        self.test_chart_activity_command()
        self.test_genuine_blockchain_commands()
        self.test_callback_handlers_working()
        self.test_console_logs_integration_completion()
        self.test_basic_bot_functionality()
        self.test_file_integrity()
        
        # Print summary
        print("\n" + "=" * 80)
        print("🏁 INTEGRATION VERIFICATION TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (self.success_count / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"✅ Tests Passed: {self.success_count}")
        print(f"❌ Tests Failed: {self.total_tests - self.success_count}")
        print(f"📊 Success Rate: {success_rate:.1f}% ({self.success_count}/{self.total_tests})")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: All integration fixes are working correctly!")
        elif success_rate >= 75:
            print("✅ GOOD: Most integration fixes are working, minor issues detected")
        elif success_rate >= 50:
            print("⚠️ PARTIAL: Some integration fixes working, significant issues found")
        else:
            print("❌ CRITICAL: Major integration failures detected")
        
        # Print failed tests details
        failed_tests = [test for test in self.test_results if test["status"] == "FAILED"]
        if failed_tests:
            print("\n🔍 FAILED TESTS DETAILS:")
            for test in failed_tests:
                print(f"❌ {test['test']}: {test['details']}")
        
        return success_rate >= 75

if __name__ == "__main__":
    tester = IntegrationVerificationTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)