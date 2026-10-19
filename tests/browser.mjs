import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
const port = 18769,
  base = `http://127.0.0.1:${port}`,
  server = spawn(
    process.env.PYTHON || 'python3',
    ['-m', 'compensation_map', 'serve', String(port)],
    { stdio: ['ignore', 'pipe', 'inherit'] },
  );
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(base)).ok) break;
    } catch {}
    if (server.exitCode !== null) throw Error('server exited');
    if (i === 99) throw Error('server timeout');
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1300, height: 1200 } }),
    errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  for (const lang of ['fr', 'en', 'es']) {
    await page.goto(`${base}/?lang=${lang}`);
    await page.waitForFunction(() => document.getElementById('cost').textContent === '9');
    assert.equal(await page.locator('html').getAttribute('lang'), lang);
    assert.equal(await page.locator('#worlds').textContent(), '3');
    assert.equal(await page.locator('.branch').count(), 3);
    assert.equal(await page.locator('.replay').count(), 3);
    const event = page.waitForEvent('download');
    await page.locator('#download').click();
    assert.equal((await event).suggestedFilename(), 'compensation-plan-evidence.json');
    await page.locator('#observe').uncheck();
    await page.locator('#plan').click();
    await page.waitForSelector('.review-reason');
    assert.match(
      await page.locator('.review-reason').textContent(),
      { fr: /profondeur/, en: /depth/, es: /profundidad/ }[lang],
    );
    await page.locator('#observe').check();
    await page.locator('#irreversible').check();
    await page.locator('#plan').click();
    await page.waitForFunction(() =>
      document.getElementById('tree').textContent.includes('notification_sent'),
    );
    assert.equal(await page.locator('.branch').count(), 0);
    await page.locator('#irreversible').uncheck();
    await page.locator('#attempts').selectOption('0');
    await page.locator('#plan').click();
    await page.waitForFunction(() => document.getElementById('cost').textContent === '2');
  }
  await page.goto(`${base}/?lang=fr`);
  await page.waitForFunction(() => document.getElementById('cost').textContent === '9');
  await mkdir('.local', { recursive: true });
  await page.screenshot({ path: '.local/preview-fr.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  assert.deepEqual(errors, []);
  console.log(
    'FR/EN/ES: contingent branches, independent replay, no-observation failure, irreversible effect, export and mobile verified.',
  );
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
}
