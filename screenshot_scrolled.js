const { chromium } = require('playwright');
const subprocess = require('child_process');

// Start http.server in background
const PORT = 8999;
const server = subprocess.spawn('python3', ['-m', 'http.server', PORT.toString()], {
  cwd: '/root/NovaGenAI'
});

console.log('Started local server on port', PORT);

setTimeout(async () => {
  try {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1280, height: 1024 });
    await page.goto(`http://localhost:${PORT}/enterprise-ai-company-malaysia.html`);
    await page.waitForTimeout(3000);
    
    // Find the infographic section heading and scroll to it
    const heading = await page.locator('text=THE ENTERPRISE AI OPERATING LAYER');
    if (await heading.count() > 0) {
      console.log('Scrolling to infographic heading...');
      await heading.scrollIntoViewIfNeeded();
      await page.waitForTimeout(1000);
    } else {
      console.log('Heading not found, capturing default fold');
    }
    
    await page.screenshot({ path: 'screenshots/aeo-infographic.png' });
    console.log('Saved screenshot to screenshots/aeo-infographic.png');
    await browser.close();
  } catch (err) {
    console.error('Error during capture:', err);
  } finally {
    server.kill();
    console.log('Stopped local server.');
    process.exit(0);
  }
}, 2000);
