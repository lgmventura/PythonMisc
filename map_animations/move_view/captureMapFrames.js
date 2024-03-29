const puppeteer = require('puppeteer');

async function captureMapFrames() {
    // Launch headless browser
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set the viewport size to the desired resolution
    const width = 1920; // Width of the viewport (in pixels)
    const height = 1080; // Height of the viewport (in pixels)
    await page.setViewport({ width, height });
    
    // Navigate to webpage with OpenLayers map
    await page.goto('http://localhost:5173/'); // Replace with your map URL

    // Wait for map to load
    await page.waitForSelector('.ol-layer');

    // Capture frames at regular intervals with a delay between each frame
    const delay = 20; // Delay in milliseconds (adjust as needed)
    const numFrames = 30; // Total number of frames to capture
    for (let i = 0; i < numFrames; i++) {
        // Capture screenshot
        await page.screenshot({ path: `frames/frame_${i}.png` });

        // Wait for the specified delay before capturing the next frame
        //await new Promise(resolve => setTimeout(resolve, delay));

        // Optionally, process or save the screenshot as needed
    }

    // Close browser
    await browser.close();
}

captureMapFrames();

