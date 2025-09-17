const { Keypair, PublicKey, LAMPORTS_PER_SOL, Connection, clusterApiUrl } = require('@solana/web3.js');
const { derivePath } = require('ed25519-hd-key');
const bip39 = require('bip39');

class EnhancedWalletManager {
    constructor(database) {
        this.database = database;
        this.devnetConnection = new Connection(process.env.SOLANA_RPC_URL || clusterApiUrl('devnet'), 'confirmed');
        this.mainnetConnection = new Connection(clusterApiUrl('mainnet-beta'), 'confirmed');
        this.devnetWallets = [];
        this.mainnetWallets = [];
        this.minimumReserve = database.getMinimumReserve(); // 0.05 SOL
        
        this.initializeWallets();
    }

    async initializeWallets() {
        console.log('🔄 Initializing enhanced wallet manager...');
        
        // Load or generate devnet wallets
        await this.loadOrGenerateWallets('devnet');
        
        // Load or generate mainnet wallets
        await this.loadOrGenerateWallets('mainnet');
        
        console.log(`✅ Initialized wallets: ${this.devnetWallets.length} devnet, ${this.mainnetWallets.length} mainnet`);
    }

    async loadOrGenerateWallets(network) {
        const savedWallets = this.database.getWallets(network);
        
        if (savedWallets && Object.keys(savedWallets).length === 5) {
            // Load existing wallets - NEVER regenerate if they exist
            console.log(`📂 Loading existing ${network} wallets (PERSISTENT)...`);
            await this.loadWalletsFromDatabase(network, savedWallets);
        } else if (network === 'mainnet') {
            // NEVER auto-generate mainnet wallets - they should be manually set
            console.log('⚠️ Mainnet wallets not found - using empty set (manual configuration required)');
            // Don't generate new mainnet wallets automatically
        } else {
            // Check if we have mnemonics from .env for devnet (use them for persistence)
            const envWallets = this.loadWalletsFromEnv(network);
            if (envWallets && envWallets.length === 5) {
                console.log(`📂 Loading ${network} wallets from .env (PERSISTENT)...`);
                await this.loadWalletsFromEnv(network);
                
                // Save to database for persistence
                const walletData = {};
                for (let i = 0; i < envWallets.length; i++) {
                    walletData[`wallet${i + 1}`] = {
                        mnemonic: envWallets[i].mnemonic,
                        publicKey: envWallets[i].publicKey,
                        createdAt: new Date().toISOString()
                    };
                }
                this.database.saveWallets(network, walletData);
            } else {
                // Only generate new devnet wallets if none exist
                console.log(`🆕 Generating new ${network} wallets...`);
                await this.generateNewWallets(network);
            }
        }
    }

    async loadWalletsFromDatabase(network, savedWallets) {
        const wallets = network === 'devnet' ? this.devnetWallets : this.mainnetWallets;
        
        for (let i = 1; i <= 5; i++) {
            const walletData = savedWallets[`wallet${i}`];
            if (walletData && walletData.mnemonic) {
                const seed = await bip39.mnemonicToSeed(walletData.mnemonic);
                const derivedSeed = derivePath(process.env.DERIVATION_PATH || "m/44'/501'/0'/0'", seed.toString('hex')).key;
                const keypair = Keypair.fromSeed(derivedSeed);
                
                wallets.push({
                    id: i,
                    keypair: keypair,
                    publicKey: keypair.publicKey.toString(),
                    mnemonic: walletData.mnemonic,
                    balance: 0
                });
            }
        }
        
        // Update balances
        await this.updateBalances(network);
    }

    loadWalletsFromEnv(network) {
        if (network !== 'devnet') return null;
        
        try {
            const envWallets = [];
            for (let i = 1; i <= 5; i++) {
                const mnemonic = process.env[`WALLET_${i}_MNEMONIC`];
                if (mnemonic) {
                    envWallets.push({ mnemonic, id: i });
                }
            }
            
            if (envWallets.length === 5) {
                console.log('📂 Found all 5 wallet mnemonics in .env - using for persistence');
                return envWallets;
            }
        } catch (error) {
            console.error('Error loading wallets from .env:', error);
        }
        
        return null;
    }

    async loadWalletsFromEnv(network) {
        const wallets = network === 'devnet' ? this.devnetWallets : this.mainnetWallets;
        
        for (let i = 1; i <= 5; i++) {
            const mnemonic = process.env[`WALLET_${i}_MNEMONIC`];
            if (mnemonic) {
                const seed = await bip39.mnemonicToSeed(mnemonic);
                const derivedSeed = derivePath(process.env.DERIVATION_PATH || "m/44'/501'/0'/0'", seed.toString('hex')).key;
                const keypair = Keypair.fromSeed(derivedSeed);
                
                const wallet = {
                    id: i,
                    keypair: keypair,
                    publicKey: keypair.publicKey.toString(),
                    mnemonic: mnemonic,
                    balance: 0
                };
                
                wallets.push(wallet);
                console.log(`💰 ${network.charAt(0).toUpperCase() + network.slice(1)} Wallet ${i}: ${keypair.publicKey.toString()} (FROM .ENV - PERSISTENT)`);
            }
        }
        
        // Update balances
        await this.updateBalances(network);
    }

    async generateNewWallets(network) {
        const wallets = network === 'devnet' ? this.devnetWallets : this.mainnetWallets;
        const walletData = {};
        
        for (let i = 1; i <= 5; i++) {
            // Generate new mnemonic for each wallet
            const mnemonic = bip39.generateMnemonic();
            const seed = await bip39.mnemonicToSeed(mnemonic);
            const derivedSeed = derivePath(process.env.DERIVATION_PATH || "m/44'/501'/0'/0'", seed.toString('hex')).key;
            const keypair = Keypair.fromSeed(derivedSeed);
            
            const wallet = {
                id: i,
                keypair: keypair,
                publicKey: keypair.publicKey.toString(),
                mnemonic: mnemonic,
                balance: 0
            };
            
            wallets.push(wallet);
            walletData[`wallet${i}`] = {
                mnemonic: mnemonic,
                publicKey: keypair.publicKey.toString(),
                createdAt: new Date().toISOString()
            };
            
            console.log(`💰 ${network.charAt(0).toUpperCase() + network.slice(1)} Wallet ${i}: ${keypair.publicKey.toString()}`);
        }
        
        // Save to database
        await this.database.saveWallets(network, walletData);
        
        // Update balances
        await this.updateBalances(network);
    }

    getConnection(network) {
        return network === 'devnet' ? this.devnetConnection : this.mainnetConnection;
    }

    getWallets(network) {
        return network === 'devnet' ? this.devnetWallets : this.mainnetWallets;
    }

    getWallet(network, walletId) {
        const wallets = this.getWallets(network);
        return wallets.find(w => w.id === walletId);
    }

    async updateBalances(network) {
        const connection = this.getConnection(network);
        const wallets = this.getWallets(network);
        
        for (const wallet of wallets) {
            try {
                const balance = await connection.getBalance(wallet.keypair.publicKey);
                wallet.balance = balance / LAMPORTS_PER_SOL;
            } catch (error) {
                console.error(`❌ Error updating balance for ${network} wallet ${wallet.id}:`, error.message);
                wallet.balance = 0;
            }
        }
    }

    async formatWalletsForTelegram(network) {
        await this.updateBalances(network);
        const wallets = this.getWallets(network);
        const networkName = network.charAt(0).toUpperCase() + network.slice(1);
        
        let message = `💰 **${networkName} Wallet Balances**\n\n`;
        let totalBalance = 0;
        
        for (const wallet of wallets) {
            const balanceStr = wallet.balance.toFixed(4);
            totalBalance += wallet.balance;
            
            message += `**Wallet ${wallet.id}:** ${balanceStr} SOL\n`;
            message += `\`${wallet.publicKey}\`\n\n`;
        }
        
        message += `**📊 Total Balance:** ${totalBalance.toFixed(4)} SOL`;
        message += `\n🌐 **Network:** ${networkName}`;
        message += `\n💎 **Reserve Required:** ${this.minimumReserve} SOL (Wallet 1)`;
        
        return message;
    }

    // SOL Transfer with reserve protection - REAL IMPLEMENTATION
    async transferSOL(network, fromWalletId, toWalletId, amount) {
        const connection = this.getConnection(network);
        const fromWallet = this.getWallet(network, fromWalletId);
        const toWallet = this.getWallet(network, toWalletId);
        
        if (!fromWallet || !toWallet) {
            throw new Error(`Wallet not found`);
        }

        // Update balances first
        await this.updateBalances(network);

        // Check reserve requirement for Wallet 1
        if (fromWalletId === 1) {
            const availableBalance = fromWallet.balance - this.minimumReserve;
            if (availableBalance < amount) {
                throw new Error(`Cannot transfer: Need to keep ${this.minimumReserve} SOL reserve in Wallet 1. Available: ${availableBalance.toFixed(4)} SOL`);
            }
        }

        // Check if from wallet has enough balance
        if (fromWallet.balance < amount) {
            throw new Error(`Insufficient balance. Need ${amount} SOL, have ${fromWallet.balance.toFixed(4)} SOL`);
        }

        try {
            console.log(`💸 REAL TRANSFER: ${amount} SOL from ${network} wallet ${fromWalletId} to ${toWalletId}`);

            // Create and send real transaction
            const { Transaction, SystemProgram, sendAndConfirmTransaction, LAMPORTS_PER_SOL } = require('@solana/web3.js');
            
            const transaction = new Transaction().add(
                SystemProgram.transfer({
                    fromPubkey: fromWallet.keypair.publicKey,
                    toPubkey: toWallet.keypair.publicKey,
                    lamports: Math.floor(amount * LAMPORTS_PER_SOL)
                })
            );

            // Sign and send transaction
            const signature = await sendAndConfirmTransaction(
                connection,
                transaction,
                [fromWallet.keypair],
                { commitment: 'confirmed' }
            );

            console.log(`✅ REAL SOL transfer completed: ${signature}`);

            // Update balances after transfer
            await this.updateBalances(network);

            return {
                success: true,
                signature: signature,
                fromWallet: fromWalletId,
                toWallet: toWalletId,
                amount: amount,
                newFromBalance: fromWallet.balance,
                newToBalance: toWallet.balance
            };

        } catch (error) {
            console.error(`❌ REAL SOL transfer failed:`, error);
            throw new Error(`Transfer failed: ${error.message}`);
        }
    }

    // Equalize SOL with reserve protection - REAL IMPLEMENTATION
    async equalizeSOLAcrossWallets(network) {
        const wallets = this.getWallets(network);
        const wallet1 = wallets.find(w => w.id === 1);
        
        if (!wallet1) {
            throw new Error('Wallet 1 not found');
        }

        // Update balances first
        await this.updateBalances(network);

        const availableForDistribution = wallet1.balance - this.minimumReserve;
        
        if (availableForDistribution <= 0) {
            throw new Error(`Wallet 1 has insufficient SOL. Current: ${wallet1.balance.toFixed(4)} SOL, Reserve needed: ${this.minimumReserve} SOL`);
        }

        const amountPerWallet = availableForDistribution / 4; // Distribute to wallets 2-5

        if (amountPerWallet < 0.001) {
            throw new Error(`Not enough SOL to distribute meaningfully. Available: ${availableForDistribution.toFixed(4)} SOL would give ${amountPerWallet.toFixed(6)} SOL per wallet`);
        }
        
        console.log(`⚖️ REAL EQUALIZATION: ${amountPerWallet.toFixed(4)} SOL per wallet on ${network}`);

        const results = [];

        // Transfer to wallets 2-5 with REAL transactions
        for (let walletId = 2; walletId <= 5; walletId++) {
            try {
                const result = await this.transferSOL(network, 1, walletId, amountPerWallet);
                results.push({
                    walletId: walletId,
                    success: true,
                    amount: amountPerWallet,
                    signature: result.signature,
                    newBalance: result.newToBalance
                });
                console.log(`✅ REAL transfer to wallet ${walletId}: ${result.signature}`);
            } catch (error) {
                console.error(`❌ Failed REAL transfer to wallet ${walletId}:`, error.message);
                results.push({
                    walletId: walletId,
                    success: false,
                    error: error.message,
                    amount: amountPerWallet
                });
            }
        }

        // Final balance update
        await this.updateBalances(network);

        const successfulTransfers = results.filter(r => r.success).length;
        const totalDistributed = successfulTransfers * amountPerWallet;

        return {
            success: true,
            network: network,
            reserveAmount: this.minimumReserve,
            amountPerWallet: amountPerWallet,
            totalDistributed: totalDistributed,
            successfulTransfers: successfulTransfers,
            results: results,
            finalWallet1Balance: wallet1.balance
        };
    }

    // REAL AIRDROP IMPLEMENTATION
    async requestDevnetAirdrop(walletId) {
        const connection = this.getConnection('devnet');
        const wallet = this.getWallet('devnet', walletId);
        
        if (!wallet) {
            throw new Error(`Wallet ${walletId} not found`);
        }

        try {
            console.log(`🪂 REAL AIRDROP: Requesting 1 SOL for wallet ${walletId}`);
            
            // Real Solana devnet airdrop
            const { LAMPORTS_PER_SOL } = require('@solana/web3.js');
            const signature = await connection.requestAirdrop(
                wallet.keypair.publicKey,
                LAMPORTS_PER_SOL
            );

            // Confirm the transaction
            await connection.confirmTransaction(signature, 'confirmed');

            // Update balance
            await this.updateBalances('devnet');

            console.log(`✅ REAL AIRDROP completed: ${signature}`);

            return {
                success: true,
                signature: signature,
                walletId: walletId,
                amount: 1,
                newBalance: wallet.balance
            };

        } catch (error) {
            console.error(`❌ REAL AIRDROP failed:`, error);
            throw new Error(`Airdrop failed: ${error.message}. The devnet faucet might be rate-limited or unavailable.`);
        }
    }

    // Get wallet mnemonics for backup
    getWalletMnemonics(network) {
        const wallets = this.getWallets(network);
        return wallets.map(wallet => ({
            id: wallet.id,
            mnemonic: wallet.mnemonic,
            publicKey: wallet.publicKey
        }));
    }
}

module.exports = EnhancedWalletManager;