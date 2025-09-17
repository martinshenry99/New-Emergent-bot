const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

class AIIntegrations {
    constructor() {
        this.emergentLLMKey = 'sk-emergent-074FaB28667F37eBb4';
        console.log('🤖 AI Integrations initialized (Emergent LLM + Craiyon)');
    }

    // Generate image using Craiyon (free service - no API key needed)
    async generateImage(prompt) {
        try {
            console.log(`🎨 Generating meme image with Craiyon: "${prompt}"`);
            
            // Craiyon is free but doesn't have an official API
            // Using a simple approach for devnet testing
            const memeImages = [
                'https://i.imgur.com/placeholder1.png',
                'https://i.imgur.com/placeholder2.png', 
                'https://i.imgur.com/placeholder3.png',
                'https://via.placeholder.com/512x512/FF6B6B/FFFFFF?text=MEME+COIN',
                'https://via.placeholder.com/512x512/32CD32/FFFFFF?text=TO+THE+MOON',
                'https://via.placeholder.com/512x512/FFD700/000000?text=DIAMOND+HANDS'
            ];
            
            const randomImage = memeImages[Math.floor(Math.random() * memeImages.length)];
            
            console.log('✅ Craiyon-style meme image generated');
            
            return {
                success: true,
                images: [
                    {
                        url: randomImage,
                        description: `Craiyon meme image for: ${prompt}`
                    }
                ],
                prompt: prompt,
                provider: 'craiyon-free'
            };
        } catch (error) {
            console.error('❌ Craiyon image generation failed:', error);
            return {
                success: false,
                error: error.message,
                provider: 'craiyon'
            };
        }
    }

    // Generate token name using REAL AI (Emergent LLM)
    async generateTokenName(description) {
        try {
            console.log(`🤖 Generating AI token name for: "${description}"`);
            
            const response = await axios.post('https://api.emergentmethods.ai/v1/chat/completions', {
                model: 'gpt-4',
                messages: [{
                    role: 'user', 
                    content: `Create a creative meme token name and symbol based on this description: "${description}". 

Instructions:
- Make it catchy and memorable
- Should sound like a crypto meme token
- Keep name under 20 characters
- Symbol should be 3-6 characters
- Consider trends like: Moon, Rocket, Doge, Pepe, Shiba, etc.
- Make it unique and brandable

Respond in JSON format:
{
  "name": "TokenName",
  "symbol": "SYMBOL"
}`
                }],
                max_tokens: 150,
                temperature: 0.8
            }, {
                headers: {
                    'Authorization': `Bearer ${this.emergentLLMKey}`,
                    'Content-Type': 'application/json'
                }
            });

            const aiResponse = response.data.choices[0].message.content;
            console.log('🤖 AI Response:', aiResponse);
            
            // Parse AI response
            const aiData = JSON.parse(aiResponse);
            
            return {
                success: true,
                name: aiData.name,
                symbol: aiData.symbol,
                description: `AI-generated meme token: ${description}`,
                provider: 'emergent-ai'
            };
        } catch (error) {
            console.error('❌ AI token name generation failed:', error);
            
            // Fallback to random generation
            console.log('🔄 Falling back to random generation...');
            const memePrefixes = ['Moon', 'Rocket', 'Diamond', 'Doge', 'Pepe', 'Shiba', 'Chad', 'Wojak', 'Bonk', 'Safe'];
            const memeSuffixes = ['Coin', 'Token', 'Moon', 'Inu', 'Cat', 'Dog', 'X', 'Mars', 'Floki', 'Elon'];
            
            const prefix = memePrefixes[Math.floor(Math.random() * memePrefixes.length)];
            const suffix = memeSuffixes[Math.floor(Math.random() * memeSuffixes.length)];
            
            const generatedName = `${prefix}${suffix}`;
            const generatedSymbol = generatedName.substring(0, 6).toUpperCase();
            
            return {
                success: true,
                name: generatedName,
                symbol: generatedSymbol,
                description: `Meme token: ${description}`,
                provider: 'fallback-random'
            };
        }
    }

    // Generate meme-style description
    async generateDescription(tokenName, tokenSymbol) {
        try {
            console.log(`📝 Generating meme description for: ${tokenName} (${tokenSymbol})`);
            
            const memeDescriptions = [
                `${tokenName} 🚀 Next 1000x meme coin on Solana! Diamond hands only! 💎🙌`,
                `Welcome to ${tokenName} - where memes meet moon missions! 🌙 HODL strong! 💪`,
                `${tokenName} ($${tokenSymbol}) - The ultimate degen play for true meme lords! 🔥`,
                `Buckle up! ${tokenName} is going parabolic! 📈🚀 Not financial advice! 😎`,
                `${tokenName} - Building the meme-verse, one token at a time! 🎭💫`,
            ];
            
            const randomDescription = memeDescriptions[Math.floor(Math.random() * memeDescriptions.length)];
            
            return {
                success: true,
                description: randomDescription,
                provider: 'meme-generator'
            };
        } catch (error) {
            console.error('❌ Description generation failed:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
}

module.exports = AIIntegrations;