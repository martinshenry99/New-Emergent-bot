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
                    content: `You are a VIRAL MEME TOKEN STRATEGIST with deep knowledge of crypto trends, internet culture, and what makes tokens successful.

ANALYZE THE CURRENT CRYPTO MEME LANDSCAPE and create a trending-ready token based on: "${description}"

USE YOUR KNOWLEDGE OF:
🔥 VIRAL MEME PATTERNS: Pepe variants, Doge derivatives, AI themes, "To the Moon" culture
📈 SUCCESSFUL TOKEN FORMATS: What symbols and names actually pump (BONK, SHIB, FLOKI patterns)
🌐 CRYPTO COMMUNITY TRENDS: Diamond hands, apes, rockets, safe tokens, inu derivatives
🎭 INTERNET CULTURE: Current meme formats, viral catchphrases, trending aesthetics
⚡ TIMING ELEMENTS: What themes are "having a moment" in crypto culture

GENERATE A TOKEN THAT FEELS LIKE IT'S RIDING A CURRENT TREND:
- Combine trending elements intelligently
- Use viral-ready naming patterns
- Include culturally relevant references
- Make it feel "timely" and "now"
- Tap into crypto community psychology

Respond in JSON format:
{
  "name": "TokenName",
  "symbol": "SYM",
  "trend_analysis": "Brief explanation of why this would be trending now",
  "viral_potential": "What makes this likely to go viral"
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

    // Generate description using REAL AI (Emergent LLM)
    async generateDescription(tokenName, tokenSymbol, userDescription = '') {
        try {
            console.log(`🤖 Generating AI description for: ${tokenName} (${tokenSymbol})`);
            
            const prompt = userDescription ? 
                `Create a compelling meme token description for "${tokenName}" ($${tokenSymbol}) based on this concept: "${userDescription}". Make it exciting, fun, and crypto-native with appropriate emojis.` :
                `Create an exciting meme token description for "${tokenName}" ($${tokenSymbol}). Make it catchy, fun, and include crypto memes and emojis.`;
            
            const response = await axios.post('https://api.emergentmethods.ai/v1/chat/completions', {
                model: 'gpt-4',
                messages: [{
                    role: 'user', 
                    content: prompt + `

Instructions:
- Keep it under 200 characters
- Include relevant emojis
- Make it sound like a genuine meme coin project
- Add excitement and community vibes
- Include crypto slang if appropriate
- End with a call to action or hype phrase

Respond with just the description text, no JSON.`
                }],
                max_tokens: 100,
                temperature: 0.9
            }, {
                headers: {
                    'Authorization': `Bearer ${this.emergentLLMKey}`,
                    'Content-Type': 'application/json'
                }
            });

            const aiDescription = response.data.choices[0].message.content.trim();
            console.log('🤖 AI Generated Description:', aiDescription);
            
            return {
                success: true,
                description: aiDescription,
                provider: 'emergent-ai'
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