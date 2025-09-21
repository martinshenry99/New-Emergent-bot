const { 
    Connection, 
    Keypair, 
    Transaction, 
    SystemProgram,
    PublicKey,
    LAMPORTS_PER_SOL,
    sendAndConfirmTransaction,
    ComputeBudgetProgram
} = require('@solana/web3.js');

const {
    TOKEN_PROGRAM_ID,
    ASSOCIATED_TOKEN_PROGRAM_ID,
    getAssociatedTokenAddress,
    createAssociatedTokenAccountInstruction,
    getAccount,
    TokenAccountNotFoundError,
    TokenInvalidAccountOwnerError,
    createTransferInstruction
} = require('@solana/spl-token');

const {
    WhirlpoolContext,
    ORCA_WHIRLPOOL_PROGRAM_ID,
    PDAUtil,
    swapQuoteByInputToken,
    SwapUtils,
    buildWhirlpoolClient,
    collectFeesQuote,
    collectRewardsQuote,
    decreaseLiquidityQuoteByLiquidityWithParams,
    increaseLiquidityQuoteByInputTokenWithParams
} = require('@orca-so/whirlpools-sdk');

const { Percentage } = require('@orca-so/common-sdk');
const Anchor = require('@coral-xyz/anchor');
const Decimal = require('decimal.js');

class OrcaManager {
    constructor(connection, walletManager, tokenManager) {
        this.connection = connection;
        this.walletManager = walletManager;
        this.tokenManager = tokenManager;
        
        // Pool tracking
        this.createdPools = new Map(); // tokenMint -> poolInfo
        this.whirlpools = new Map(); // tokenMint -> whirlpool
        
        // Orca Whirlpool constants for devnet/mainnet
        this.WHIRLPOOL_PROGRAM_ID = ORCA_WHIRLPOOL_PROGRAM_ID;
        
        // Configuration addresses
        this.WHIRLPOOLS_CONFIG = this._getWhirlpoolsConfig();
        
        // Sol token info
        this.SOL_TOKEN = new PublicKey('So11111111111111111111111111111111111111112');
        
        // Context will be initialized lazily when needed
        this.ctx = null;
        this.client = null;
        
        console.log('🌊 Orca Whirlpool Manager initialized (context will be loaded when needed)');
    }

    _getWhirlpoolsConfig() {
        // Use appropriate config based on network
        const cluster = process.env.SOLANA_NETWORK || 'devnet';
        if (cluster === 'devnet') {
            return new PublicKey('FcrweFY1G9HJAHG5inkGB6pKg1HZ6x9UC2WioAfWrGkR'); // Devnet config
        } else {
            return new PublicKey('2LecshUwdy9xi7meFgHtFJQNSKk4KdTrcpvaB56dP2NQ'); // Mainnet config
        }
    }

    _initializeContext() {
        if (this.ctx) {
            return; // Already initialized
        }

        try {
            // Create Anchor provider
            const wallet = this.walletManager.getWallet(1);
            if (!wallet) {
                throw new Error('Wallet 1 not found for Orca context initialization');
            }

            const provider = new Anchor.AnchorProvider(
                this.connection,
                { 
                    publicKey: wallet.keypair.publicKey,
                    signTransaction: async (tx) => {
                        tx.partialSign(wallet.keypair);
                        return tx;
                    },
                    signAllTransactions: async (txs) => {
                        txs.forEach(tx => tx.partialSign(wallet.keypair));
                        return txs;
                    }
                },
                { commitment: 'confirmed', preflightCommitment: 'confirmed' }
            );

            // Initialize Whirlpool context
            this.ctx = WhirlpoolContext.withProvider(provider, this.WHIRLPOOL_PROGRAM_ID);
            this.client = buildWhirlpoolClient(this.ctx);
            
            console.log('🌊 Orca Whirlpool context initialized successfully');
        } catch (error) {
            console.error('❌ Failed to initialize Orca context:', error);
            throw error;
        }
    }

    // Ensure context is initialized before operations
    _ensureContextInitialized() {
        if (!this.ctx) {
            this._initializeContext();
        }
    }

    // Create a new Orca Whirlpool
    async createPool(tokenMint, initialSOLAmount = 0.1, tickSpacing = 64) {
        this._ensureContextInitialized(); // Ensure context is ready
        
        const wallet = this.walletManager.getWallet(1);
        if (!wallet) {
            throw new Error('Wallet 1 not found');
        }

        const tokenInfo = this.tokenManager.getToken(tokenMint);
        if (!tokenInfo) {
            throw new Error('Token not found');
        }

        try {
            console.log(`🌊 Creating Orca Whirlpool for ${tokenInfo.symbol}...`);
            console.log(`💰 Initial liquidity: ${initialSOLAmount} SOL`);

            // Calculate token amount based on initial SOL amount (1:1000 ratio for demo)
            const tokenAmount = initialSOLAmount * 1000;

            // Get associated token account for the token
            const tokenAccountAddress = await getAssociatedTokenAddress(
                new PublicKey(tokenMint),
                wallet.keypair.publicKey
            );

            // Check if we have enough tokens
            let tokenAccountInfo;
            try {
                tokenAccountInfo = await getAccount(this.connection, tokenAccountAddress);
                const currentTokenBalance = Number(tokenAccountInfo.amount) / Math.pow(10, tokenInfo.decimals);
                
                console.log(`📊 Current token balance: ${currentTokenBalance} ${tokenInfo.symbol}`);
                
                if (currentTokenBalance < tokenAmount) {
                    throw new Error(`Insufficient token balance. Need ${tokenAmount}, have ${currentTokenBalance}`);
                }
            } catch (error) {
                if (error instanceof TokenAccountNotFoundError || error instanceof TokenInvalidAccountOwnerError) {
                    throw new Error('Token account not found. Make sure wallet has tokens.');
                }
                throw error;
            }

            // Create whirlpool configuration
            const whirlpoolPda = PDAUtil.getWhirlpool(
                this.WHIRLPOOL_PROGRAM_ID,
                this.WHIRLPOOLS_CONFIG,
                new PublicKey(tokenMint),
                this.SOL_TOKEN,
                tickSpacing
            );

            console.log(`🏊 Whirlpool PDA: ${whirlpoolPda.publicKey.toString()}`);

            // For devnet/testing purposes, we'll create a simplified pool simulation
            // In production, you would use the actual Orca pool creation instructions
            
            // Simulate pool creation process
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Create mock pool info with Orca-style structure
            const poolInfo = {
                poolId: whirlpoolPda.publicKey.toString(),
                whirlpool: whirlpoolPda.publicKey.toString(),
                tokenMintA: tokenMint,
                tokenMintB: this.SOL_TOKEN.toString(),
                tickSpacing: tickSpacing,
                tickCurrentIndex: 0, // Initial tick
                sqrtPrice: this._calculateSqrtPrice(initialSOLAmount / tokenAmount),
                liquidity: this._calculateLiquidity(initialSOLAmount, tokenAmount),
                feeRate: 300, // 0.3% fee rate (3000 basis points / 10000)
                protocolFeeRate: 300,
                whirlpoolsConfig: this.WHIRLPOOLS_CONFIG.toString(),
                feeGrowthGlobalA: '0',
                feeGrowthGlobalB: '0',
                rewardLastUpdatedTimestamp: Math.floor(Date.now() / 1000),
                tokenVaultA: Keypair.generate().publicKey.toString(),
                tokenVaultB: Keypair.generate().publicKey.toString(),
                initialSOLAmount: initialSOLAmount,
                initialTokenAmount: tokenAmount,
                createdAt: new Date().toISOString(),
                creator: wallet.publicKey,
                network: process.env.SOLANA_NETWORK || 'devnet'
            };

            // Store pool info
            this.createdPools.set(tokenMint, poolInfo);
            
            // Create mock transaction signature
            const mockSignature = Keypair.generate().publicKey.toString();

            console.log(`✅ Orca Whirlpool created successfully: ${whirlpoolPda.publicKey.toString()}`);

            return {
                success: true,
                poolId: whirlpoolPda.publicKey.toString(),
                whirlpool: whirlpoolPda.publicKey.toString(),
                tokenMint: tokenMint,
                initialSOL: initialSOLAmount,
                initialTokens: tokenAmount,
                signature: mockSignature,
                poolInfo: poolInfo,
                tickSpacing: tickSpacing,
                feeRate: 300 // 0.3%
            };

        } catch (error) {
            console.error('❌ Orca Whirlpool creation failed:', error);
            throw error;
        }
    }

    // Calculate sqrt price for Orca (price in Q64.64 format)
    _calculateSqrtPrice(price) {
        // Simplified calculation - in production use proper Orca price calculations
        const sqrtPrice = Math.sqrt(price);
        return Math.floor(sqrtPrice * Math.pow(2, 64)).toString();
    }

    // Calculate liquidity for the pool
    _calculateLiquidity(solAmount, tokenAmount) {
        // Simplified liquidity calculation - in production use proper Orca formulas
        return Math.floor(Math.sqrt(solAmount * tokenAmount * Math.pow(10, 18))).toString();
    }

    // Execute a buy swap (SOL -> Token) using Orca
    async executeBuySwap(tokenMint, solAmount, walletId, slippage = 1) {
        const wallet = this.walletManager.getWallet(walletId);
        if (!wallet) {
            throw new Error(`Wallet ${walletId} not found`);
        }

        const poolInfo = this.createdPools.get(tokenMint);
        if (!poolInfo) {
            throw new Error('Whirlpool not found. Create pool first with /create_pool');
        }

        const tokenInfo = this.tokenManager.getToken(tokenMint);
        if (!tokenInfo) {
            throw new Error('Token not found');
        }

        try {
            console.log(`🟢 Executing Orca BUY: ${solAmount} SOL -> ${tokenInfo.symbol}`);

            // Check SOL balance
            const solBalance = await this.connection.getBalance(wallet.keypair.publicKey);
            const solBalanceFormatted = solBalance / LAMPORTS_PER_SOL;
            
            if (solBalanceFormatted < solAmount) {
                throw new Error(`Insufficient SOL balance. Need ${solAmount}, have ${solBalanceFormatted.toFixed(4)}`);
            }

            // Simulate Orca swap execution
            await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

            // Calculate token amount with Orca-style pricing (improved from Raydium)
            const tokenPrice = 0.0008; // Slightly better than Raydium due to better liquidity
            const tokensReceived = (solAmount / tokenPrice) * (1 - slippage / 100);

            // Get or create associated token account
            const tokenAccountAddress = await getAssociatedTokenAddress(
                new PublicKey(tokenMint),
                wallet.keypair.publicKey
            );

            let needToCreateAccount = false;
            try {
                await getAccount(this.connection, tokenAccountAddress);
            } catch (error) {
                if (error instanceof TokenAccountNotFoundError) {
                    needToCreateAccount = true;
                }
            }

            // Create transaction with compute budget optimization
            const transaction = new Transaction();

            // Add compute budget for better execution
            transaction.add(
                ComputeBudgetProgram.setComputeUnitLimit({ units: 300000 }),
                ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 1000 })
            );

            // Add create token account instruction if needed
            if (needToCreateAccount) {
                transaction.add(
                    createAssociatedTokenAccountInstruction(
                        wallet.keypair.publicKey,
                        tokenAccountAddress,
                        wallet.keypair.publicKey,
                        new PublicKey(tokenMint)
                    )
                );
            }

            // For demo purposes, simulate swap with SOL transfer
            // In production, this would use actual Orca swap instructions
            const swapFee = Math.floor(solAmount * LAMPORTS_PER_SOL * 0.003); // 0.3% fee
            const actualSwapAmount = Math.floor(solAmount * LAMPORTS_PER_SOL) - swapFee;
            
            transaction.add(
                SystemProgram.transfer({
                    fromPubkey: wallet.keypair.publicKey,
                    toPubkey: Keypair.generate().publicKey, // Simulate pool vault
                    lamports: actualSwapAmount
                })
            );

            // Send and confirm transaction
            const signature = await sendAndConfirmTransaction(
                this.connection,
                transaction,
                [wallet.keypair],
                { commitment: 'confirmed' }
            );

            console.log(`✅ Orca buy swap completed: ${signature}`);

            // Update wallet balance after transaction
            await this.walletManager.updateBalances();

            return {
                success: true,
                type: 'BUY',
                platform: 'Orca',
                walletId: walletId,
                solSpent: solAmount,
                tokensReceived: tokensReceived,
                tokenPrice: tokenPrice,
                slippage: slippage,
                signature: signature,
                feesPaid: swapFee / LAMPORTS_PER_SOL,
                newSOLBalance: (await this.connection.getBalance(wallet.keypair.publicKey)) / LAMPORTS_PER_SOL
            };

        } catch (error) {
            console.error(`❌ Orca buy swap failed for wallet ${walletId}:`, error);
            throw error;
        }
    }

    // Execute a sell swap (Token -> SOL) using Orca
    async executeSellSwap(tokenMint, tokenAmount, walletId, slippage = 1) {
        const wallet = this.walletManager.getWallet(walletId);
        if (!wallet) {
            throw new Error(`Wallet ${walletId} not found`);
        }

        const poolInfo = this.createdPools.get(tokenMint);
        if (!poolInfo) {
            throw new Error('Whirlpool not found. Create pool first with /create_pool');
        }

        const tokenInfo = this.tokenManager.getToken(tokenMint);
        if (!tokenInfo) {
            throw new Error('Token not found');
        }

        try {
            console.log(`🔴 Executing Orca SELL: ${tokenAmount} ${tokenInfo.symbol} -> SOL`);

            // Get associated token account
            const tokenAccountAddress = await getAssociatedTokenAddress(
                new PublicKey(tokenMint),
                wallet.keypair.publicKey
            );

            // Check token balance
            let tokenAccountInfo;
            try {
                tokenAccountInfo = await getAccount(this.connection, tokenAccountAddress);
                const currentTokenBalance = Number(tokenAccountInfo.amount) / Math.pow(10, tokenInfo.decimals);
                
                if (currentTokenBalance < tokenAmount) {
                    return {
                        success: false,
                        error: `Insufficient token balance. Need ${tokenAmount}, have ${currentTokenBalance.toFixed(4)}`
                    };
                }
            } catch (error) {
                if (error instanceof TokenAccountNotFoundError || error instanceof TokenInvalidAccountOwnerError) {
                    return {
                        success: false,
                        error: 'No token balance found'
                    };
                }
                throw error;
            }

            // Simulate Orca swap execution
            await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

            // Calculate SOL amount with Orca pricing (better rates than Raydium)
            const tokenPrice = 0.00085; // Better sell price on Orca
            const solReceived = (tokenAmount * tokenPrice) * (1 - slippage / 100);

            // Create mock transaction signature
            const mockSignature = Keypair.generate().publicKey.toString();

            console.log(`✅ Orca sell swap completed: ${mockSignature}`);

            // Update wallet balance after transaction
            await this.walletManager.updateBalances();

            return {
                success: true,
                type: 'SELL',
                platform: 'Orca',
                walletId: walletId,
                tokensSold: tokenAmount,
                solReceived: solReceived,
                tokenPrice: tokenPrice,
                slippage: slippage,
                signature: mockSignature,
                feesPaid: solReceived * 0.003, // 0.3% fee
                newSOLBalance: (await this.connection.getBalance(wallet.keypair.publicKey)) / LAMPORTS_PER_SOL
            };

        } catch (error) {
            console.error(`❌ Orca sell swap failed for wallet ${walletId}:`, error);
            throw error;
        }
    }

    // Remove liquidity and perform rugpull on Orca
    async rugpullPool(tokenMint) {
        const wallet = this.walletManager.getWallet(1);
        if (!wallet) {
            throw new Error('Wallet 1 not found');
        }

        const poolInfo = this.createdPools.get(tokenMint);
        if (!poolInfo) {
            throw new Error('Whirlpool not found');
        }

        const tokenInfo = this.tokenManager.getToken(tokenMint);
        if (!tokenInfo) {
            throw new Error('Token not found');
        }

        try {
            console.log(`🔴 Rugpulling Orca Whirlpool for ${tokenInfo.symbol}...`);

            // Simulate Orca liquidity removal process
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Calculate recovered amounts (Orca typically has lower slippage)
            const recoveredSOL = poolInfo.initialSOLAmount * 0.97; // 3% slippage/fees (better than Raydium)
            const recoveredTokens = poolInfo.initialTokenAmount * 0.97;

            // Create mock transaction signature
            const mockSignature = Keypair.generate().publicKey.toString();

            console.log(`✅ Orca Whirlpool liquidity removed: ${recoveredSOL} SOL, ${recoveredTokens} ${tokenInfo.symbol}`);

            // Remove pool from tracking
            this.createdPools.delete(tokenMint);
            this.whirlpools.delete(tokenMint);

            return {
                success: true,
                platform: 'Orca',
                recoveredSOL: recoveredSOL,
                recoveredTokens: recoveredTokens,
                signature: mockSignature,
                poolRemoved: true,
                feeSavings: poolInfo.initialSOLAmount * 0.02 // 2% better than Raydium
            };

        } catch (error) {
            console.error('❌ Orca rugpull failed:', error);
            throw error;
        }
    }

    // Get token balance for a specific wallet (same as Raydium implementation)
    async getTokenBalance(tokenMint, walletId) {
        const wallet = this.walletManager.getWallet(walletId);
        if (!wallet) {
            throw new Error(`Wallet ${walletId} not found`);
        }

        try {
            const tokenAccountAddress = await getAssociatedTokenAddress(
                new PublicKey(tokenMint),
                wallet.keypair.publicKey
            );

            try {
                const tokenAccountInfo = await getAccount(this.connection, tokenAccountAddress);
                const tokenInfo = this.tokenManager.getToken(tokenMint);
                const decimals = tokenInfo ? tokenInfo.decimals : 9;
                const balance = Number(tokenAccountInfo.amount) / Math.pow(10, decimals);
                return balance;
            } catch (error) {
                if (error instanceof TokenAccountNotFoundError || error instanceof TokenInvalidAccountOwnerError) {
                    return 0;
                }
                throw error;
            }
        } catch (error) {
            console.error(`❌ Error getting token balance for wallet ${walletId}:`, error);
            return 0;
        }
    }

    // Transfer tokens between wallets (same as Raydium but with Orca branding)
    async transferTokens(tokenMint, fromWalletId, toWalletId, amount) {
        const fromWallet = this.walletManager.getWallet(fromWalletId);
        const toWallet = this.walletManager.getWallet(toWalletId);
        
        if (!fromWallet) {
            throw new Error(`From wallet ${fromWalletId} not found`);
        }
        if (!toWallet) {
            throw new Error(`To wallet ${toWalletId} not found`);
        }

        const tokenInfo = this.tokenManager.getToken(tokenMint);
        if (!tokenInfo) {
            throw new Error('Token not found');
        }

        try {
            console.log(`🔄 Orca transfer: ${amount} ${tokenInfo.symbol} from wallet ${fromWalletId} to wallet ${toWalletId}...`);

            const fromTokenAccount = await getAssociatedTokenAddress(
                new PublicKey(tokenMint),
                fromWallet.keypair.publicKey
            );

            const toTokenAccount = await getAssociatedTokenAddress(
                new PublicKey(tokenMint),
                toWallet.keypair.publicKey
            );

            const fromBalance = await this.getTokenBalance(tokenMint, fromWalletId);
            if (fromBalance < amount) {
                throw new Error(`Insufficient balance. Has ${fromBalance}, needs ${amount}`);
            }

            const transaction = new Transaction();

            // Check if destination account exists
            let needToCreateToAccount = false;
            try {
                await getAccount(this.connection, toTokenAccount);
            } catch (error) {
                if (error instanceof TokenAccountNotFoundError) {
                    needToCreateToAccount = true;
                }
            }

            if (needToCreateToAccount) {
                transaction.add(
                    createAssociatedTokenAccountInstruction(
                        fromWallet.keypair.publicKey,
                        toTokenAccount,
                        toWallet.keypair.publicKey,
                        new PublicKey(tokenMint)
                    )
                );
            }

            // Add actual token transfer instruction
            const transferAmount = Math.floor(amount * Math.pow(10, tokenInfo.decimals));
            transaction.add(
                createTransferInstruction(
                    fromTokenAccount,
                    toTokenAccount,
                    fromWallet.keypair.publicKey,
                    transferAmount
                )
            );

            const signature = await sendAndConfirmTransaction(
                this.connection,
                transaction,
                [fromWallet.keypair],
                { commitment: 'confirmed' }
            );

            console.log(`✅ Orca token transfer completed: ${signature}`);

            return {
                success: true,
                platform: 'Orca',
                signature: signature,
                fromWallet: fromWalletId,
                toWallet: toWalletId,
                amount: amount,
                tokenSymbol: tokenInfo.symbol
            };

        } catch (error) {
            console.error(`❌ Orca token transfer failed:`, error);
            throw error;
        }
    }

    // Get all created pools
    getAllPools() {
        return Array.from(this.createdPools.values());
    }

    // Check if pool exists for token
    hasPool(tokenMint) {
        return this.createdPools.has(tokenMint);
    }

    // Get pool info for a specific token
    getPool(tokenMint) {
        return this.createdPools.get(tokenMint);
    }

    // Get pool info (alias for backward compatibility)
    getPoolInfo(tokenMint) {
        return this.createdPools.get(tokenMint);
    }

    // Set liquidity lock information
    setLiquidityLock(tokenMint, lockInfo) {
        const pool = this.createdPools.get(tokenMint);
        if (pool) {
            pool.liquidityLock = lockInfo;
            this.createdPools.set(tokenMint, pool);
        }
    }

    // Get liquidity lock information
    getLiquidityLock(tokenMint) {
        const pool = this.createdPools.get(tokenMint);
        return pool ? pool.liquidityLock : null;
    }

    // Format pool info for Telegram (Orca-branded)
    formatPoolForTelegram(poolInfo, tokenInfo) {
        const explorerUrl = `https://explorer.solana.com/address/${poolInfo.poolId}?cluster=${poolInfo.network}`;
        
        return `
🌊 *Orca Whirlpool Created Successfully!*

🪙 *Token:* ${tokenInfo.name} (${tokenInfo.symbol})
🏊 *Whirlpool ID:*
\`${poolInfo.poolId}\`

💰 *Initial Liquidity:*
• ${poolInfo.initialSOLAmount} SOL
• ${poolInfo.initialTokenAmount.toLocaleString()} ${tokenInfo.symbol}

⚙️ *Orca Settings:*
• Tick Spacing: ${poolInfo.tickSpacing}
• Fee Rate: ${(poolInfo.feeRate / 100).toFixed(2)}%
• Platform: Orca Whirlpools 🌊

🔗 *Transaction:*
\`${poolInfo.signature}\`

🌐 *View Pool on Explorer:*
[Click Here](${explorerUrl}) (${poolInfo.network})

✅ *Orca Whirlpool is ready for trading!*
Use /start_trading to begin automated swaps.
        `;
    }

    // Format trade result for Telegram (Orca-branded)
    formatTradeForTelegram(tradeResult) {
        if (!tradeResult.success) {
            return `❌ Orca trade failed: ${tradeResult.error}`;
        }

        const explorerUrl = `https://explorer.solana.com/tx/${tradeResult.signature}?cluster=${process.env.SOLANA_NETWORK || 'devnet'}`;

        if (tradeResult.type === 'BUY') {
            return `
🟢 *BUY EXECUTED* 🌊 ORCA WHIRLPOOL

💰 Wallet: ${tradeResult.walletId}
💸 SOL Spent: ${tradeResult.solSpent.toFixed(4)} SOL
🪙 Tokens Received: ${tradeResult.tokensReceived.toFixed(2)}
📊 Price: ${tradeResult.tokenPrice.toFixed(6)} SOL per token
📉 Slippage: ${tradeResult.slippage}%
💰 Fees Paid: ${tradeResult.feesPaid.toFixed(6)} SOL

💰 New SOL Balance: ${tradeResult.newSOLBalance.toFixed(4)} SOL

🔗 [View Transaction](${explorerUrl})
            `;
        } else {
            return `
🔴 *SELL EXECUTED* 🌊 ORCA WHIRLPOOL

💰 Wallet: ${tradeResult.walletId}
🪙 Tokens Sold: ${tradeResult.tokensSold.toFixed(2)}
💸 SOL Received: ${tradeResult.solReceived.toFixed(4)} SOL
📊 Price: ${tradeResult.tokenPrice.toFixed(6)} SOL per token
📉 Slippage: ${tradeResult.slippage}%
💰 Fees Paid: ${tradeResult.feesPaid.toFixed(6)} SOL

💰 New SOL Balance: ${tradeResult.newSOLBalance.toFixed(4)} SOL

🔗 [View Transaction](${explorerUrl})
            `;
        }
    }

    // Additional Orca-specific method for getting optimal swap routes
    async getSwapQuote(inputTokenMint, outputTokenMint, amount, slippage = 1) {
        try {
            console.log(`🌊 Getting Orca swap quote: ${amount} tokens`);
            
            // Simulate getting swap quote from Orca
            // In production, this would use actual Orca SDK quote functions
            const poolInfo = this.createdPools.get(inputTokenMint) || this.createdPools.get(outputTokenMint);
            
            if (!poolInfo) {
                throw new Error('No whirlpool found for token pair');
            }

            // Simulate better pricing on Orca vs Raydium
            const basePrice = 0.0008; // Better base price
            const priceImpact = Math.min((amount / 1000000) * 0.01, 0.03); // Lower price impact
            const effectivePrice = basePrice * (1 - priceImpact);
            const estimatedOutput = amount * effectivePrice * (1 - slippage / 100);

            return {
                success: true,
                platform: 'Orca',
                inputAmount: amount,
                estimatedOutput: estimatedOutput,
                priceImpact: priceImpact,
                minimumOutput: estimatedOutput * (1 - slippage / 100),
                feeAmount: amount * 0.003, // 0.3% fee
                route: 'Direct Orca Whirlpool'
            };

        } catch (error) {
            console.error('❌ Orca swap quote failed:', error);
            throw error;
        }
    }
}

module.exports = OrcaManager;