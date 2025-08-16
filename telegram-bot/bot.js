require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const { Connection, PublicKey, clusterApiUrl } = require('@solana/web3.js');
const WalletManager = require('./wallet-manager');
const TokenManager = require('./token-manager');
const AIIntegrations = require('./ai-integrations');
const MetadataManager = require('./metadata-manager');

// Initialize Telegram Bot with new token
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: true });

// Initialize Solana Connection
const connection = new Connection(process.env.SOLANA_RPC_URL || clusterApiUrl('devnet'), 'confirmed');

// Initialize managers
const walletManager = new WalletManager(connection);
const tokenManager = new TokenManager(connection, walletManager);
const aiIntegrations = new AIIntegrations();
const metadataManager = new MetadataManager();

// User sessions for multi-step wizards
const userSessions = new Map();

console.log('🚀 Simplified Meme Bot Starting...');
console.log(`📡 Connected to Solana ${process.env.SOLANA_NETWORK || 'devnet'}`);

// Test connections
(async () => {
    try {
        const version = await connection.getVersion();
        console.log('✅ Solana connection successful:', version);
        console.log('📱 Bot is ready - Send /start to begin');
    } catch (error) {
        console.error('❌ Connection failed:', error);
    }
})();

// Start command
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const welcomeMessage = `🚀 Welcome to Simplified Meme Token Creator

Create your own meme token on Solana with just 2 simple commands:

🛠️ Manual Setup:
/launch - Step-by-step token creation wizard

🤖 AI-Powered:
/auto_brand - AI creates everything for you

Ready to launch your meme coin? 🚀`;

    bot.sendMessage(chatId, welcomeMessage, {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: '🛠️ Manual Launch', callback_data: 'manual_launch' },
                    { text: '🤖 AI Auto-Brand', callback_data: 'ai_auto_brand' }
                ],
                [
                    { text: '💰 Check Wallets', callback_data: 'show_wallets' }
                ]
            ]
        }
    });
});

// Help command
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, `📋 **Available Commands:**

🛠️ **/launch** - Manual token creation wizard
• Step-by-step setup
• Full control over all settings
• Perfect for custom tokens

🤖 **/auto_brand** - AI-powered automatic branding
• Trending meme analysis
• AI-generated names, descriptions, images
• Quick and easy token creation

💰 **/wallets** - View wallet balances
📊 **/status** - Check bot status

Choose your preferred method and start creating! 🚀`, { parse_mode: 'Markdown' });
});

// Manual Launch Command - Step-by-step wizard
bot.onText(/\/launch/, (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    startManualLaunch(chatId, userId);
});

function startManualLaunch(chatId, userId) {
    userSessions.set(userId, {
        type: 'manual_launch',
        step: 1,
        data: {}
    });

    bot.sendMessage(chatId, `🛠️ Manual Token Creation Wizard

Step 1/9: Token Name

Choose something catchy and relevant to your meme.

Examples: "Doge Killer", "Moon Rocket", "Diamond Hands"

💡 Tip: Keep it memorable and under 32 characters

Please enter your token name:`, {
        reply_markup: {
            inline_keyboard: [
                [{ text: '❌ Cancel', callback_data: 'cancel_wizard' }]
            ]
        }
    });
}

// Auto Brand Command - AI-powered creation
bot.onText(/\/auto_brand/, (msg) => {
    const chatId = msg.chat.id;
    startAutoBrand(chatId, msg.from.id);
});

function startAutoBrand(chatId, userId) {
    bot.sendMessage(chatId, `🤖 AI-Powered Token Branding

Choose your AI branding mode:

🔥 Trending Meme Mode
• Scan trending Twitter memes
• Extract popular themes
• Create based on current trends

🎯 Pure AI Mode
• Generate unique concept from scratch
• Creative AI-driven ideas
• Completely original branding

Which mode would you prefer?`, {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: '🔥 Trending Mode', callback_data: 'ai_trending' },
                    { text: '🎯 Pure AI Mode', callback_data: 'ai_pure' }
                ],
                [
                    { text: '❌ Cancel', callback_data: 'cancel_wizard' }
                ]
            ]
        }
    });
}

// Message handler for wizard steps
bot.on('message', (msg) => {
    const userId = msg.from.id;
    const chatId = msg.chat.id;
    const text = msg.text;

    // Skip if it's a command
    if (text && text.startsWith('/')) return;

    const session = userSessions.get(userId);
    if (!session) return;

    if (session.type === 'manual_launch') {
        handleManualLaunchStep(chatId, userId, text, session);
    }
});

function handleManualLaunchStep(chatId, userId, text, session) {
    const step = session.step;
    const data = session.data;

    switch (step) {
        case 1: // Token Name
            if (!text || text.length > 32) {
                bot.sendMessage(chatId, '❌ Please enter a valid token name (1-32 characters)');
                return;
            }
            data.name = text;
            session.step = 2;
            bot.sendMessage(chatId, `✅ Token Name: ${text}

Step 2/9: Token Description

Briefly describe the vibe or joke behind your token.

Examples: "The ultimate meme coin for diamond hands 💎", "Community-driven dog coin with a twist 🐕"

💡 Tip: Make it engaging and under 200 characters

Please enter your token description:`);
            break;

        case 2: // Token Description
            if (!text || text.length > 200) {
                bot.sendMessage(chatId, '❌ Please enter a valid description (1-200 characters)');
                return;
            }
            data.description = text;
            session.step = 3;
            bot.sendMessage(chatId, `✅ Description: ${text}

Step 3/9: Ticker Symbol

3-6 uppercase letters, e.g., DOGE, PEPE, MOON

💡 Tip: Keep it short, memorable, and related to your token name

Please enter your ticker symbol:`);
            break;

        case 3: // Ticker Symbol
            const ticker = text.toUpperCase();
            if (!ticker || ticker.length < 3 || ticker.length > 6 || !/^[A-Z]+$/.test(ticker)) {
                bot.sendMessage(chatId, '❌ Please enter a valid ticker symbol (3-6 uppercase letters, A-Z only)');
                return;
            }
            data.symbol = ticker;
            session.step = 4;
            bot.sendMessage(chatId, `✅ Ticker Symbol: ${ticker}

Step 4/9: Total Supply

Total number of tokens to mint.

Examples: 1000000 (1M), 100000000 (100M), 1000000000 (1B)

💡 Tip: Popular supplies are 1M, 100M, or 1B tokens

Please enter total supply (numbers only):`);
            break;

        case 4: // Total Supply
            const supply = parseInt(text.replace(/,/g, ''));
            if (!supply || supply < 1000 || supply > 1000000000000) {
                bot.sendMessage(chatId, '❌ Please enter a valid supply (1,000 to 1,000,000,000,000)');
                return;
            }
            data.totalSupply = supply;
            session.step = 5;
            bot.sendMessage(chatId, `✅ Total Supply: ${supply.toLocaleString()} tokens

Step 5/9: Liquidity Lock

Should we lock the liquidity to prevent rug pulls?

🔒 Liquidity Lock means the liquidity tokens are locked for a specific period, making it impossible for creators to remove liquidity (prevents rug pulls).

💡 Tip: Locking builds trust with your community`, {
                reply_markup: {
                    inline_keyboard: [
                        [
                            { text: '🔒 Yes, Lock It', callback_data: `step5_yes_${userId}` },
                            { text: '🚫 No Lock', callback_data: `step5_no_${userId}` }
                        ]
                    ]
                }
            });
            break;

        case 6: // Network Selection (after liquidity lock decision)
            session.step = 7;
            bot.sendMessage(chatId, `**Step 7/9: Blockchain Network**

Choose which network to deploy on:

🧪 **Devnet** - Free testing network (recommended for testing)
🌐 **Mainnet** - Live network (real SOL required)

💡 *Tip: Start with devnet to test everything first*`, {
                parse_mode: 'Markdown',
                reply_markup: {
                    inline_keyboard: [
                        [
                            { text: '🧪 Devnet (Free)', callback_data: `network_devnet_${userId}` },
                            { text: '🌐 Mainnet (Live)', callback_data: `network_mainnet_${userId}` }
                        ]
                    ]
                }
            });
            break;

        default:
            // Handle other steps...
            break;
    }

    userSessions.set(userId, session);
}

// Callback query handler
bot.on('callback_query', async (callbackQuery) => {
    const data = callbackQuery.data;
    const chatId = callbackQuery.message.chat.id;
    const userId = callbackQuery.from.id;

    console.log(`🔔 Callback received: "${data}" from user ${userId} in chat ${chatId}`);

    if (data === 'manual_launch') {
        startManualLaunch(chatId, userId);
    } else if (data === 'ai_auto_brand') {
        startAutoBrand(chatId, userId);
    } else if (data === 'ai_trending') {
        await executeAIBranding(chatId, userId, 'trending');
    } else if (data === 'ai_pure') {
        await executeAIBranding(chatId, userId, 'pure');
    } else if (data.startsWith('step5_')) {
        const [, decision, sessionUserId] = data.split('_');
        if (sessionUserId === userId.toString()) {
            const session = userSessions.get(userId);
            if (session) {
                session.data.liquidityLock = decision === 'yes';
                session.step = 6;
                // Continue to mint authority step
                bot.sendMessage(chatId, `✅ Liquidity Lock: ${decision === 'yes' ? 'Enabled' : 'Disabled'}

Step 6/9: Mint Authority Revoke

Should we revoke mint authority after creation?

🔒 Mint Authority Revoke prevents creating more tokens after initial mint, ensuring fixed supply forever.

💡 Tip: Revoking shows commitment to tokenomics`, {
                    reply_markup: {
                        inline_keyboard: [
                            [
                                { text: '🔒 Yes, Revoke', callback_data: `step6_yes_${userId}` },
                                { text: '🔄 Keep Authority', callback_data: `step6_no_${userId}` }
                            ]
                        ]
                    }
                });
                userSessions.set(userId, session);
            }
        }
    } else if (data.startsWith('step6_')) {
        // Handle mint authority decision in manual launch
        console.log(`📝 Processing step6 callback: ${data}`);
        const parts = data.split('_');
        const decision = parts[1]; // 'yes' or 'no' 
        const sessionUserId = parts[2]; // user ID
        
        console.log(`📝 Step6 decision: ${decision}, sessionUserId: ${sessionUserId}, currentUserId: ${userId}`);
        
        if (sessionUserId === userId.toString()) {
            const session = userSessions.get(userId);
            if (session) {
                session.data.revokeMint = decision === 'yes';
                session.step = 7;
                console.log(`✅ Step6 processed: revokeMint = ${session.data.revokeMint}`);
                
                bot.sendMessage(chatId, `✅ Mint Authority: ${decision === 'yes' ? 'Will be revoked' : 'Keep authority'}

Step 7/9: Network Selection

Choose which network to deploy on:

🧪 Devnet - Free testing network (recommended)
🌐 Mainnet - Live network (real SOL required)`, {
                    reply_markup: {
                        inline_keyboard: [
                            [
                                { text: '🧪 Devnet (Free)', callback_data: `network_devnet_${userId}` },
                                { text: '🌐 Mainnet (Live)', callback_data: `network_mainnet_${userId}` }
                            ]
                        ]
                    }
                });
                userSessions.set(userId, session);
            } else {
                console.log(`❌ No session found for user ${userId}`);
            }
        } else {
            console.log(`❌ Session userId mismatch: ${sessionUserId} vs ${userId}`);
        }
    } else if (data.startsWith('network_')) {
        const [, network, sessionUserId] = data.split('_');
        if (sessionUserId === userId.toString()) {
            const session = userSessions.get(userId);
            if (session) {
                session.data.network = network;
                session.step = 8;
                showFinalSummary(chatId, userId, session.data);
            }
        }
    } else if (data.startsWith('ai_continue_')) {
        const sessionUserId = data.replace('ai_continue_', '');
        if (sessionUserId === userId.toString()) {
            const session = userSessions.get(userId);
            if (session && session.data) {
                // Continue with AI branding settings
                bot.sendMessage(chatId, `🤖 AI Branding: ${session.data.name} (${session.data.symbol})

Now let's configure the remaining settings:

Step 1: Liquidity Lock
Should we lock the liquidity to prevent rug pulls?`, {
                    reply_markup: {
                        inline_keyboard: [
                            [
                                { text: '🔒 Yes, Lock It', callback_data: `ai_lock_yes_${userId}` },
                                { text: '🚫 No Lock', callback_data: `ai_lock_no_${userId}` }
                            ]
                        ]
                    }
                });
            }
        }
    } else if (data.startsWith('ai_lock_')) {
        const [, decision, sessionUserId] = data.split('_');
        if (sessionUserId === userId.toString()) {
            const session = userSessions.get(userId);
            if (session) {
                session.data.liquidityLock = decision === 'yes';
                bot.sendMessage(chatId, `✅ Liquidity Lock: ${decision === 'yes' ? 'Enabled' : 'Disabled'}

Step 2: Mint Authority Revoke
Should we revoke mint authority after creation?

🔒 Mint Authority Revoke prevents creating more tokens after initial mint, ensuring fixed supply forever.`, {
                    reply_markup: {
                        inline_keyboard: [
                            [
                                { text: '🔒 Yes, Revoke', callback_data: `ai_mint_yes_${userId}` },
                                { text: '🔄 Keep Authority', callback_data: `ai_mint_no_${userId}` }
                            ]
                        ]
                    }
                });
                userSessions.set(userId, session);
            }
        }
    } else if (data.startsWith('ai_mint_')) {
        const [, decision, sessionUserId] = data.split('_');
        if (sessionUserId === userId.toString()) {
            const session = userSessions.get(userId);
            if (session) {
                session.data.revokeMint = decision === 'yes';
                bot.sendMessage(chatId, `✅ Mint Authority: ${decision === 'yes' ? 'Will be revoked' : 'Keep authority'}

Step 3: Network Selection
Choose which network to deploy on:`, {
                    reply_markup: {
                        inline_keyboard: [
                            [
                                { text: '🧪 Devnet (Free)', callback_data: `ai_network_devnet_${userId}` },
                                { text: '🌐 Mainnet (Live)', callback_data: `ai_network_mainnet_${userId}` }
                            ]
                        ]
                    }
                });
                userSessions.set(userId, session);
            }
        }
    } else if (data.startsWith('ai_network_')) {
        const [, , network, sessionUserId] = data.split('_');
        if (sessionUserId === userId.toString()) {
            const session = userSessions.get(userId);
            if (session) {
                session.data.network = network;
                session.data.totalSupply = 1000000; // Default 1M supply for AI tokens
                showFinalSummary(chatId, userId, session.data);
            }
        }
    } else if (data === 'show_wallets') {
        await showWallets(chatId);
    } else if (data === 'cancel_wizard') {
        userSessions.delete(userId);
        bot.sendMessage(chatId, '❌ Wizard cancelled. Use /start to begin again.');
    }

    bot.answerCallbackQuery(callbackQuery.id);
});

async function executeAIBranding(chatId, userId, mode) {
    bot.sendMessage(chatId, `🤖 **AI Branding in Progress...**

Mode: ${mode === 'trending' ? '🔥 Trending Memes' : '🎯 Pure AI'}

🧠 Analyzing meme trends...
🎨 Generating token concept...
🖼️ Creating logo with Craiyon...

This may take 30-45 seconds...`, { parse_mode: 'Markdown' });

    try {
        let brandingResult;
        
        if (mode === 'trending') {
            // Simulate trending meme analysis
            brandingResult = await generateTrendingMemeToken();
        } else {
            // Pure AI generation
            brandingResult = await metadataManager.autoGenerateTokenBranding('unique creative meme concept');
        }

        if (brandingResult.success) {
            userSessions.set(userId, {
                type: 'ai_branding',
                data: {
                    name: brandingResult.name,
                    symbol: brandingResult.symbol,
                    description: brandingResult.description,
                    imageUrl: brandingResult.imageUrl,
                    mode: mode
                }
            });

            bot.sendMessage(chatId, `🎉 AI Branding Complete!

🪙 Token Name: ${brandingResult.name}
🔤 Symbol: ${brandingResult.symbol}
📝 Description: ${brandingResult.description}
🖼️ Logo: ${brandingResult.imageUrl ? 'Generated' : 'Placeholder'}
🤖 Mode: ${mode === 'trending' ? 'Trending Memes' : 'Pure AI'}

Settings Still Needed:`, {
                reply_markup: {
                    inline_keyboard: [
                        [
                            { text: '✅ Looks Great - Continue', callback_data: `ai_continue_${userId}` }
                        ],
                        [
                            { text: '🔄 Try Again', callback_data: mode === 'trending' ? 'ai_trending' : 'ai_pure' },
                            { text: '❌ Cancel', callback_data: 'cancel_wizard' }
                        ]
                    ]
                }
            });
        } else {
            bot.sendMessage(chatId, '❌ AI branding failed. Please try again.');
        }
    } catch (error) {
        console.error('AI branding error:', error);
        bot.sendMessage(chatId, '❌ AI branding failed. Please try again.');
    }
}

async function generateTrendingMemeToken() {
    // Simulate trending meme analysis
    const trendingThemes = [
        { name: 'ElonDogeMars', symbol: 'EDMARS', theme: 'Elon Musk + Doge + Mars exploration' },
        { name: 'PepePump', symbol: 'PEPUMP', theme: 'Pepe frog pumping weights' },
        { name: 'ShibaBoss', symbol: 'SHIBOSS', theme: 'Shiba Inu as a business executive' },
        { name: 'DiamondApe', symbol: 'DIAPE', theme: 'Diamond hands meets ape strong' },
        { name: 'MoonLambo', symbol: 'MLAMBO', theme: 'Moon mission with Lamborghini' }
    ];

    const selected = trendingThemes[Math.floor(Math.random() * trendingThemes.length)];
    
    return {
        success: true,
        name: selected.name,
        symbol: selected.symbol,
        description: `🔥 Trending meme token based on ${selected.theme}! Join the community and ride the wave! 🚀💎`,
        imageUrl: 'https://via.placeholder.com/512x512/FF6B6B/FFFFFF?text=' + selected.symbol
    };
}

function showFinalSummary(chatId, userId, data) {
    const summary = `📋 **Final Token Summary**

🪙 **Name:** ${data.name}
🔤 **Symbol:** ${data.symbol}
📝 **Description:** ${data.description}
🔢 **Total Supply:** ${data.totalSupply?.toLocaleString() || 'Not set'}
🔒 **Liquidity Lock:** ${data.liquidityLock ? 'Yes' : 'No'}
🔒 **Revoke Mint:** ${data.revokeMint ? 'Yes' : 'No'}  
🌐 **Network:** ${data.network || 'Not set'}

**Ready to create your token?**`;

    bot.sendMessage(chatId, summary, {
        parse_mode: 'Markdown',
        reply_markup: {
            inline_keyboard: [
                [
                    { text: '🚀 Create Token', callback_data: `create_final_${userId}` }
                ],
                [
                    { text: '✏️ Edit Settings', callback_data: 'manual_launch' },
                    { text: '❌ Cancel', callback_data: 'cancel_wizard' }
                ]
            ]
        }
    });
}

async function showWallets(chatId) {
    try {
        const walletInfo = await walletManager.formatAllWalletsForTelegram();
        bot.sendMessage(chatId, walletInfo, { parse_mode: 'Markdown' });
    } catch (error) {
        bot.sendMessage(chatId, '❌ Error fetching wallet information.');
    }
}

// Error handling
bot.on('error', (error) => {
    console.error('Bot error:', error);
});

bot.on('polling_error', (error) => {
    console.error('Polling error:', error);
});

console.log('✅ Simplified Meme Bot loaded successfully!');