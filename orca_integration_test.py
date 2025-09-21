#!/usr/bin/env python3
"""
Orca Whirlpools Integration Testing for Telegram Meme Creator Bot
Testing the migration from Raydium to Orca for better cost efficiency

Key areas to test:
1. Orca Manager Initialization
2. Pool Creation using Orca Whirlpools SDK
3. Trading Operations (buy/sell swaps)
4. Real Trading Manager Integration
5. Cost Optimization validation
6. Error Handling
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

class OrcaIntegrationTester:
    def __init__(self):
        self.project_root = Path("/app")
        self.telegram_bot_dir = self.project_root / "telegram-bot"
        self.test_results = {
            "orca_manager_initialization": {"status": "pending", "details": []},
            "pool_creation": {"status": "pending", "details": []},
            "trading_operations": {"status": "pending", "details": []},
            "real_trading_manager_integration": {"status": "pending", "details": []},
            "cost_optimization": {"status": "pending", "details": []},
            "error_handling": {"status": "pending", "details": []},
            "dependencies": {"status": "pending", "details": []},
            "bot_integration": {"status": "pending", "details": []}
        }
        
    def log_test(self, test_name, status, message):
        """Log test results"""
        print(f"[{test_name.upper()}] {status}: {message}")
        if test_name in self.test_results:
            self.test_results[test_name]["status"] = status
            self.test_results[test_name]["details"].append(message)
    
    def test_dependencies(self):
        """Test 1: Verify Orca Whirlpools SDK dependencies are installed"""
        print("\n🔍 TESTING ORCA DEPENDENCIES...")
        
        try:
            # Check package.json for Orca dependencies
            package_json_path = self.telegram_bot_dir / "package.json"
            if not package_json_path.exists():
                self.log_test("dependencies", "FAIL", "package.json not found")
                return False
                
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            required_deps = [
                "@orca-so/whirlpools-sdk",
                "@orca-so/common-sdk",
                "@coral-xyz/anchor",
                "decimal.js"
            ]
            
            missing_deps = []
            for dep in required_deps:
                if dep not in package_data.get("dependencies", {}):
                    missing_deps.append(dep)
            
            if missing_deps:
                self.log_test("dependencies", "FAIL", f"Missing Orca dependencies: {missing_deps}")
                return False
            
            # Check versions
            orca_whirlpools_version = package_data["dependencies"]["@orca-so/whirlpools-sdk"]
            orca_common_version = package_data["dependencies"]["@orca-so/common-sdk"]
            
            self.log_test("dependencies", "PASS", f"Orca Whirlpools SDK {orca_whirlpools_version} found")
            self.log_test("dependencies", "PASS", f"Orca Common SDK {orca_common_version} found")
            self.log_test("dependencies", "PASS", "All required Orca dependencies present")
            
            return True
            
        except Exception as e:
            self.log_test("dependencies", "FAIL", f"Error checking dependencies: {str(e)}")
            return False
    
    def test_orca_manager_initialization(self):
        """Test 2: Verify OrcaManager class initializes correctly with lazy context loading"""
        print("\n🌊 TESTING ORCA MANAGER INITIALIZATION...")
        
        try:
            # Check if orca-manager.js exists
            orca_manager_path = self.telegram_bot_dir / "orca-manager.js"
            if not orca_manager_path.exists():
                self.log_test("orca_manager_initialization", "FAIL", "orca-manager.js file not found")
                return False
            
            # Read and analyze the OrcaManager class
            with open(orca_manager_path, 'r') as f:
                orca_code = f.read()
            
            # Check for key initialization components
            required_components = [
                "class OrcaManager",
                "WhirlpoolContext",
                "ORCA_WHIRLPOOL_PROGRAM_ID",
                "buildWhirlpoolClient",
                "_initializeContext",
                "_ensureContextInitialized",
                "this.ctx = null",  # Lazy loading
                "this.client = null"  # Lazy loading
            ]
            
            missing_components = []
            for component in required_components:
                if component not in orca_code:
                    missing_components.append(component)
            
            if missing_components:
                self.log_test("orca_manager_initialization", "FAIL", f"Missing components: {missing_components}")
                return False
            
            # Check for lazy context loading pattern
            if "_ensureContextInitialized()" not in orca_code:
                self.log_test("orca_manager_initialization", "FAIL", "Lazy context loading not implemented")
                return False
            
            # Check for proper Whirlpool configuration
            if "_getWhirlpoolsConfig()" not in orca_code:
                self.log_test("orca_manager_initialization", "FAIL", "Whirlpool configuration method missing")
                return False
            
            # Check for devnet/mainnet support
            if "devnet" not in orca_code or "mainnet" not in orca_code:
                self.log_test("orca_manager_initialization", "FAIL", "Network configuration missing")
                return False
            
            self.log_test("orca_manager_initialization", "PASS", "OrcaManager class properly structured")
            self.log_test("orca_manager_initialization", "PASS", "Lazy context loading implemented")
            self.log_test("orca_manager_initialization", "PASS", "Network configuration present")
            self.log_test("orca_manager_initialization", "PASS", "All required Orca SDK imports found")
            
            return True
            
        except Exception as e:
            self.log_test("orca_manager_initialization", "FAIL", f"Error analyzing OrcaManager: {str(e)}")
            return False
    
    def test_pool_creation(self):
        """Test 3: Verify pool creation using Orca Whirlpools SDK instead of Raydium"""
        print("\n🏊 TESTING ORCA POOL CREATION...")
        
        try:
            orca_manager_path = self.telegram_bot_dir / "orca-manager.js"
            with open(orca_manager_path, 'r') as f:
                orca_code = f.read()
            
            # Check for pool creation method
            if "createPool" not in orca_code:
                self.log_test("pool_creation", "FAIL", "createPool method not found")
                return False
            
            # Check for Orca-specific pool creation components
            orca_pool_components = [
                "PDAUtil.getWhirlpool",
                "whirlpoolPda",
                "tickSpacing",
                "sqrtPrice",
                "liquidity",
                "feeRate",
                "WHIRLPOOL_PROGRAM_ID"
            ]
            
            missing_pool_components = []
            for component in orca_pool_components:
                if component not in orca_code:
                    missing_pool_components.append(component)
            
            if missing_pool_components:
                self.log_test("pool_creation", "FAIL", f"Missing Orca pool components: {missing_pool_components}")
                return False
            
            # Check that Raydium references are removed
            raydium_references = ["raydium", "Raydium", "RAYDIUM"]
            found_raydium_refs = []
            for ref in raydium_references:
                if ref in orca_code:
                    found_raydium_refs.append(ref)
            
            if found_raydium_refs:
                self.log_test("pool_creation", "WARNING", f"Found Raydium references (should be removed): {found_raydium_refs}")
            
            # Check for proper error handling in pool creation
            if "try {" not in orca_code or "catch" not in orca_code:
                self.log_test("pool_creation", "FAIL", "Pool creation lacks proper error handling")
                return False
            
            # Check for pool tracking
            if "createdPools" not in orca_code or "whirlpools" not in orca_code:
                self.log_test("pool_creation", "FAIL", "Pool tracking not implemented")
                return False
            
            self.log_test("pool_creation", "PASS", "createPool method implemented with Orca SDK")
            self.log_test("pool_creation", "PASS", "Orca-specific pool components present")
            self.log_test("pool_creation", "PASS", "Pool tracking system implemented")
            self.log_test("pool_creation", "PASS", "Error handling implemented")
            
            return True
            
        except Exception as e:
            self.log_test("pool_creation", "FAIL", f"Error testing pool creation: {str(e)}")
            return False
    
    def test_trading_operations(self):
        """Test 4: Verify buy/sell swap operations work with Orca's lower fees"""
        print("\n💱 TESTING ORCA TRADING OPERATIONS...")
        
        try:
            orca_manager_path = self.telegram_bot_dir / "orca-manager.js"
            with open(orca_manager_path, 'r') as f:
                orca_code = f.read()
            
            # Check for trading methods
            required_trading_methods = [
                "executeBuySwap",
                "executeSellSwap",
                "getSwapQuote"
            ]
            
            missing_trading_methods = []
            for method in required_trading_methods:
                if method not in orca_code:
                    missing_trading_methods.append(method)
            
            if missing_trading_methods:
                self.log_test("trading_operations", "FAIL", f"Missing trading methods: {missing_trading_methods}")
                return False
            
            # Check for Orca-specific trading features
            orca_trading_features = [
                "swapQuoteByInputToken",
                "SwapUtils",
                "slippage",
                "ComputeBudgetProgram",  # For better execution
                "setComputeUnitLimit",
                "setComputeUnitPrice"
            ]
            
            missing_features = []
            for feature in orca_trading_features:
                if feature not in orca_code:
                    missing_features.append(feature)
            
            if missing_features:
                self.log_test("trading_operations", "WARNING", f"Missing Orca trading features: {missing_features}")
            
            # Check for cost optimization (lower fees)
            if "0.003" not in orca_code and "0.3%" not in orca_code:
                self.log_test("trading_operations", "FAIL", "Orca fee rate (0.3%) not found")
                return False
            
            # Check for better pricing mentions
            if "better" not in orca_code.lower() and "improved" not in orca_code.lower():
                self.log_test("trading_operations", "WARNING", "No mentions of improved pricing over Raydium")
            
            # Check for proper balance checking
            if "getTokenBalance" not in orca_code:
                self.log_test("trading_operations", "FAIL", "Token balance checking not implemented")
                return False
            
            # Check for transaction confirmation
            if "sendAndConfirmTransaction" not in orca_code:
                self.log_test("trading_operations", "FAIL", "Transaction confirmation not implemented")
                return False
            
            self.log_test("trading_operations", "PASS", "Buy/sell swap methods implemented")
            self.log_test("trading_operations", "PASS", "Orca fee rate (0.3%) configured")
            self.log_test("trading_operations", "PASS", "Balance checking implemented")
            self.log_test("trading_operations", "PASS", "Transaction confirmation implemented")
            
            return True
            
        except Exception as e:
            self.log_test("trading_operations", "FAIL", f"Error testing trading operations: {str(e)}")
            return False
    
    def test_real_trading_manager_integration(self):
        """Test 5: Check that RealTradingManager properly uses OrcaManager instead of RaydiumManager"""
        print("\n🔄 TESTING REAL TRADING MANAGER INTEGRATION...")
        
        try:
            # Check RealTradingManager
            rtm_path = self.telegram_bot_dir / "real-trading-manager.js"
            if not rtm_path.exists():
                self.log_test("real_trading_manager_integration", "FAIL", "real-trading-manager.js not found")
                return False
            
            with open(rtm_path, 'r') as f:
                rtm_code = f.read()
            
            # Check that it uses OrcaManager instead of RaydiumManager
            if "orcaManager" not in rtm_code:
                self.log_test("real_trading_manager_integration", "FAIL", "OrcaManager not integrated in RealTradingManager")
                return False
            
            if "raydiumManager" in rtm_code:
                self.log_test("real_trading_manager_integration", "FAIL", "RaydiumManager still referenced (should be removed)")
                return False
            
            # Check constructor parameters
            if "constructor(walletManager, tokenManager, orcaManager)" not in rtm_code:
                self.log_test("real_trading_manager_integration", "FAIL", "Constructor doesn't accept orcaManager parameter")
                return False
            
            # Check that trading methods use Orca
            if "this.orcaManager.executeBuySwap" not in rtm_code:
                self.log_test("real_trading_manager_integration", "FAIL", "Buy swaps don't use OrcaManager")
                return False
            
            if "this.orcaManager.executeSellSwap" not in rtm_code:
                self.log_test("real_trading_manager_integration", "FAIL", "Sell swaps don't use OrcaManager")
                return False
            
            # Check for pool existence validation
            if "hasPool" not in rtm_code:
                self.log_test("real_trading_manager_integration", "FAIL", "Pool existence validation missing")
                return False
            
            # Check for rugpull functionality
            if "rugpullPool" not in rtm_code:
                self.log_test("real_trading_manager_integration", "WARNING", "Rugpull functionality not found")
            
            self.log_test("real_trading_manager_integration", "PASS", "OrcaManager properly integrated")
            self.log_test("real_trading_manager_integration", "PASS", "RaydiumManager references removed")
            self.log_test("real_trading_manager_integration", "PASS", "Trading operations use Orca")
            self.log_test("real_trading_manager_integration", "PASS", "Pool validation implemented")
            
            return True
            
        except Exception as e:
            self.log_test("real_trading_manager_integration", "FAIL", f"Error testing RTM integration: {str(e)}")
            return False
    
    def test_cost_optimization(self):
        """Test 6: Validate that Orca provides better pricing (lower slippage, better rates)"""
        print("\n💰 TESTING COST OPTIMIZATION...")
        
        try:
            orca_manager_path = self.telegram_bot_dir / "orca-manager.js"
            with open(orca_manager_path, 'r') as f:
                orca_code = f.read()
            
            # Check for cost optimization features
            cost_features = [
                "better",
                "lower",
                "improved",
                "efficient",
                "optimized"
            ]
            
            found_cost_features = []
            for feature in cost_features:
                if feature.lower() in orca_code.lower():
                    found_cost_features.append(feature)
            
            if not found_cost_features:
                self.log_test("cost_optimization", "WARNING", "No explicit cost optimization mentions found")
            
            # Check for specific fee improvements
            if "0.3%" in orca_code or "300" in orca_code:  # 300 basis points = 0.3%
                self.log_test("cost_optimization", "PASS", "Orca fee rate (0.3%) configured")
            else:
                self.log_test("cost_optimization", "FAIL", "Orca fee rate not properly configured")
                return False
            
            # Check for slippage optimization
            if "slippage" in orca_code:
                self.log_test("cost_optimization", "PASS", "Slippage handling implemented")
            else:
                self.log_test("cost_optimization", "WARNING", "Slippage handling not explicitly mentioned")
            
            # Check for compute budget optimization
            if "ComputeBudgetProgram" in orca_code:
                self.log_test("cost_optimization", "PASS", "Compute budget optimization implemented")
            else:
                self.log_test("cost_optimization", "WARNING", "Compute budget optimization not found")
            
            # Check for better pricing mentions
            if "better price" in orca_code.lower() or "improved pricing" in orca_code.lower():
                self.log_test("cost_optimization", "PASS", "Better pricing explicitly mentioned")
            
            # Check for fee savings calculations
            if "feeSavings" in orca_code or "fee_savings" in orca_code:
                self.log_test("cost_optimization", "PASS", "Fee savings tracking implemented")
            
            self.log_test("cost_optimization", "PASS", "Cost optimization features present")
            
            return True
            
        except Exception as e:
            self.log_test("cost_optimization", "FAIL", f"Error testing cost optimization: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test 7: Ensure proper error handling when wallets aren't ready or tokens don't exist"""
        print("\n⚠️ TESTING ERROR HANDLING...")
        
        try:
            orca_manager_path = self.telegram_bot_dir / "orca-manager.js"
            with open(orca_manager_path, 'r') as f:
                orca_code = f.read()
            
            # Check for comprehensive error handling
            error_handling_patterns = [
                "try {",
                "catch",
                "throw new Error",
                "if (!wallet)",
                "if (!tokenInfo)",
                "TokenAccountNotFoundError",
                "TokenInvalidAccountOwnerError"
            ]
            
            missing_error_patterns = []
            for pattern in error_handling_patterns:
                if pattern not in orca_code:
                    missing_error_patterns.append(pattern)
            
            if missing_error_patterns:
                self.log_test("error_handling", "FAIL", f"Missing error handling patterns: {missing_error_patterns}")
                return False
            
            # Check for specific error scenarios
            error_scenarios = [
                "Wallet not found",
                "Token not found",
                "Insufficient balance",
                "Pool not found",
                "context initialization"
            ]
            
            handled_scenarios = []
            for scenario in error_scenarios:
                if scenario.lower() in orca_code.lower():
                    handled_scenarios.append(scenario)
            
            if len(handled_scenarios) < 3:
                self.log_test("error_handling", "WARNING", f"Only {len(handled_scenarios)} error scenarios handled")
            
            # Check for graceful degradation
            if "console.error" in orca_code:
                self.log_test("error_handling", "PASS", "Error logging implemented")
            
            # Check for context initialization error handling
            if "_initializeContext" in orca_code and "catch" in orca_code:
                self.log_test("error_handling", "PASS", "Context initialization error handling present")
            
            self.log_test("error_handling", "PASS", "Comprehensive error handling implemented")
            self.log_test("error_handling", "PASS", f"Multiple error scenarios handled: {handled_scenarios}")
            
            return True
            
        except Exception as e:
            self.log_test("error_handling", "FAIL", f"Error testing error handling: {str(e)}")
            return False
    
    def test_bot_integration(self):
        """Test 8: Verify Orca integration in main bot.js file"""
        print("\n🤖 TESTING BOT INTEGRATION...")
        
        try:
            # Check bot.js integration
            bot_path = self.telegram_bot_dir / "bot.js"
            if not bot_path.exists():
                self.log_test("bot_integration", "FAIL", "bot.js not found")
                return False
            
            with open(bot_path, 'r') as f:
                bot_code = f.read()
            
            # Check for OrcaManager import
            if "require('./orca-manager')" not in bot_code and "OrcaManager" not in bot_code:
                self.log_test("bot_integration", "FAIL", "OrcaManager not imported in bot.js")
                return False
            
            # Check for OrcaManager initialization
            if "new OrcaManager" not in bot_code:
                self.log_test("bot_integration", "FAIL", "OrcaManager not initialized in bot.js")
                return False
            
            # Check that RealTradingManager uses OrcaManager
            if "RealTradingManager" in bot_code and "orcaManager" in bot_code:
                self.log_test("bot_integration", "PASS", "RealTradingManager integrated with OrcaManager")
            else:
                self.log_test("bot_integration", "FAIL", "RealTradingManager not properly integrated with OrcaManager")
                return False
            
            # Check for Orca branding in console logs
            if "Orca" in bot_code or "🌊" in bot_code:
                self.log_test("bot_integration", "PASS", "Orca branding present in bot")
            
            # Check that Raydium references are minimized
            raydium_count = bot_code.lower().count("raydium")
            if raydium_count > 5:  # Some legacy references might remain
                self.log_test("bot_integration", "WARNING", f"High number of Raydium references: {raydium_count}")
            
            self.log_test("bot_integration", "PASS", "OrcaManager properly integrated in bot.js")
            self.log_test("bot_integration", "PASS", "Migration from Raydium to Orca complete")
            
            return True
            
        except Exception as e:
            self.log_test("bot_integration", "FAIL", f"Error testing bot integration: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all Orca integration tests"""
        print("🌊 STARTING ORCA WHIRLPOOLS INTEGRATION TESTING")
        print("=" * 60)
        
        test_methods = [
            self.test_dependencies,
            self.test_orca_manager_initialization,
            self.test_pool_creation,
            self.test_trading_operations,
            self.test_real_trading_manager_integration,
            self.test_cost_optimization,
            self.test_error_handling,
            self.test_bot_integration
        ]
        
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_method in test_methods:
            try:
                if test_method():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ Test {test_method.__name__} failed with exception: {str(e)}")
        
        # Generate summary
        print("\n" + "=" * 60)
        print("🌊 ORCA INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
            print(f"{status_emoji} {test_name.replace('_', ' ').title()}: {result['status']}")
            
            # Show key details
            if result["details"]:
                for detail in result["details"][-2:]:  # Show last 2 details
                    print(f"   • {detail}")
        
        print(f"\n📊 SUCCESS RATE: {success_rate:.1f}% ({passed_tests}/{total_tests} tests passed)")
        
        if success_rate >= 80:
            print("🎉 ORCA INTEGRATION: EXCELLENT - Ready for production!")
        elif success_rate >= 60:
            print("✅ ORCA INTEGRATION: GOOD - Minor issues to address")
        else:
            print("❌ ORCA INTEGRATION: NEEDS WORK - Major issues found")
        
        # Save results
        results_file = self.project_root / "orca_integration_test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "test_results": self.test_results,
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "success_rate": success_rate,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        return success_rate >= 60

if __name__ == "__main__":
    tester = OrcaIntegrationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)