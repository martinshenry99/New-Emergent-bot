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
            console.log(`📂 Loading existing ${network} wallets...`);
            await this.loadWalletsFromDatabase(network, savedWallets);
        } else if (network === 'mainnet') {
            // NEVER auto-generate mainnet wallets - they should be manually set
            console.log('⚠️ Mainnet wallets not found - using empty set (manual configuration required)');
            // Don't generate new mainnet wallets automatically
        } else {
            // Only generate new devnet wallets if none exist
            console.log(`🆕 Generating new ${network} wallets...`);
            await this.generateNewWallets(network);
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

    // SOL Transfer with reserve protection
    async transferSOL(network, fromWalletId, toWalletId, amount) {
        const connection = this.getConnection(network);
        const fromWallet = this.getWallet(network, fromWalletId);
        const toWallet = this.getWallet(network, toWalletId);
        
        if (!fromWallet || !toWallet) {
            throw new Error(`Wallet not found`);
        }

        // Check reserve requirement for Wallet 1
        if (fromWalletId === 1) {
            const availableBalance = fromWallet.balance - this.minimumReserve;
            if (availableBalance < amount) {
                throw new Error(`Cannot transfer: Need to keep ${this.minimumReserve} SOL reserve in Wallet 1. Available: ${availableBalance.toFixed(4)} SOL`);
            }
        }

        // Standard transfer logic here...
        console.log(`💸 Transferring ${amount} SOL from ${network} wallet ${fromWalletId} to ${toWalletId}`);
        
        // Return mock result for now
        return {
            success: true,
            signature: 'mock_signature_' + Date.now(),
            amount: amount,
            fromWallet: fromWalletId,
            toWallet: toWalletId
        };
    }

    // Equalize SOL with reserve protection
    async equalizeSOLAcrossWallets(network) {
        const wallets = this.getWallets(network);
        const wallet1 = wallets.find(w => w.id === 1);
        
        if (!wallet1) {
            throw new Error('Wallet 1 not found');
        }

        const availableForDistribution = wallet1.balance - this.minimumReserve;
        
        if (availableForDistribution <= 0) {
            throw new Error(`Wallet 1 has insufficient SOL. Current: ${wallet1.balance.toFixed(4)} SOL, Reserve needed: ${this.minimumReserve} SOL`);
        }

        const amountPerWallet = availableForDistribution / 4; // Distribute to wallets 2-5
        
        console.log(`⚖️ Equalizing ${network} wallets: ${amountPerWallet.toFixed(4)} SOL per wallet`);
        console.log(`💎 Keeping ${this.minimumReserve} SOL reserve in Wallet 1`);

        // Return mock result for now
        return {
            success: true,
            network: network,
            reserveAmount: this.minimumReserve,
            amountPerWallet: amountPerWallet,
            distributedWallets: 4
        };
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