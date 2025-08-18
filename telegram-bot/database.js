// Database manager for persistent storage of wallets and token data
const fs = require('fs').promises;
const path = require('path');

class DatabaseManager {
    constructor() {
        this.dbPath = path.join(__dirname, 'bot_database.json');
        this.data = {
            devnetWallets: {},
            mainnetWallets: {},
            tokens: {},
            settings: {
                lockDuration: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
                minimumReserveSol: 0.05
            }
        };
        this.loadDatabase();
    }

    async loadDatabase() {
        try {
            const fileExists = await fs.access(this.dbPath).then(() => true).catch(() => false);
            if (fileExists) {
                const data = await fs.readFile(this.dbPath, 'utf8');
                this.data = { ...this.data, ...JSON.parse(data) };
                console.log('✅ Database loaded successfully');
            } else {
                console.log('📄 Creating new database file');
                await this.saveDatabase();
            }
        } catch (error) {
            console.error('❌ Database load error:', error);
        }
    }

    async saveDatabase() {
        try {
            await fs.writeFile(this.dbPath, JSON.stringify(this.data, null, 2));
            console.log('💾 Database saved successfully');
        } catch (error) {
            console.error('❌ Database save error:', error);
        }
    }

    // Wallet Management
    async saveWallets(network, wallets) {
        if (network === 'devnet') {
            this.data.devnetWallets = wallets;
        } else if (network === 'mainnet') {
            this.data.mainnetWallets = wallets;
        }
        await this.saveDatabase();
    }

    getWallets(network) {
        return network === 'devnet' ? this.data.devnetWallets : this.data.mainnetWallets;
    }

    // Token Data Management
    async saveTokenData(tokenMint, tokenData) {
        this.data.tokens[tokenMint] = {
            ...tokenData,
            createdAt: new Date().toISOString(),
            lastUpdated: new Date().toISOString()
        };
        await this.saveDatabase();
    }

    getTokenData(tokenMint) {
        return this.data.tokens[tokenMint];
    }

    getAllTokens() {
        return Object.values(this.data.tokens);
    }

    // Settings
    getLockDuration() {
        return this.data.settings.lockDuration; // 24 hours
    }

    getMinimumReserve() {
        return this.data.settings.minimumReserveSol; // 0.05 SOL
    }

    // Liquidity & Market Cap Data
    async saveLiquidityData(tokenMint, realSol, displayedLiquidity, realMarketCap, displayedMarketCap) {
        if (!this.data.tokens[tokenMint]) {
            this.data.tokens[tokenMint] = {};
        }
        
        this.data.tokens[tokenMint].liquidityData = {
            realSol: realSol,
            displayedLiquidity: displayedLiquidity,
            realMarketCap: realMarketCap,
            displayedMarketCap: displayedMarketCap,
            updatedAt: new Date().toISOString()
        };
        
        await this.saveDatabase();
    }

    getLiquidityData(tokenMint) {
        const token = this.data.tokens[tokenMint];
        return token ? token.liquidityData : null;
    }
}

module.exports = DatabaseManager;