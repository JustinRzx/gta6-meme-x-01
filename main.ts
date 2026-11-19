const fs = require('fs');
const path = require('path');

const botDir = process.env.MAKEFUN_BOT_DIR || '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';

const postJsonPath = path.join(botDir, 'POST.json');
const outputPostJsonPath = path.join(outputDir, 'POST.json');

try {
    // Read POST.json from the bot directory
    const postJson = fs.readFileSync(postJsonPath, 'utf8');
    const postData = JSON.parse(postJson);

    // Validate the URL
    const urlRegex = /^https:\/\/(?:x\.com|twitter\.com)\/[a-zA-Z0-9_]+\/status\/[0-9]+$/;
    if (!urlRegex.test(postData.url)) {
        console.error('Invalid URL format');
        process.exit(1);
    }

    // Write POST.json to the output directory
    fs.writeFileSync(outputPostJsonPath, postJson);

    console.log(`Copied POST.json from ${postJsonPath} to ${outputPostJsonPath}`);

// Calculate and print the SHA-256 hash of POST.json
const crypto = require('crypto');
const hash = crypto.createHash('sha256').update(postJson).digest('hex');
console.log(`SHA-256 hash of POST.json: ${hash}`);
} catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
}