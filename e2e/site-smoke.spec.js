const { expect, test } = require('@playwright/test');

const criticalRoutes = [
  { label: '/', path: './' },
  { label: '/members/', path: 'members/' },
  { label: '/publications/', path: 'publications/' },
  { label: '/teaching/', path: 'teaching/' },
  { label: '/research/', path: 'research/' },
  { label: '/links/', path: 'links/' },
  { label: '/contact/', path: 'contact/' },
];

for (const route of criticalRoutes) {
  test(`${route.label} renders the shared page shell`, async ({ page }) => {
    const browserProblems = [];
    page.on('console', (message) => {
      if (message.type() === 'error') browserProblems.push(`console: ${message.text()}`);
    });
    page.on('pageerror', (error) => browserProblems.push(`page: ${error.message}`));
    page.on('requestfailed', (request) => {
      const failure = request.failure();
      browserProblems.push(`request: ${request.url()} (${failure?.errorText || 'failed'})`);
    });
    const response = await page.goto(route.path);

    expect(response?.ok()).toBeTruthy();
    await expect(page).toHaveTitle(/AG Computational Arithmetic Geometry/);
    await expect(page.locator('.header-main')).toBeVisible();
    await expect(page.locator('#main-content')).toBeVisible();
    await expect(page.locator('.footer')).toBeVisible();

    const emptyResourceAttributes = await page
      .locator('a[href=""], img[src=""], script[src=""]')
      .count();
    expect(emptyResourceAttributes).toBe(0);

    const horizontalOverflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(horizontalOverflow).toBeLessThanOrEqual(1);
    expect(browserProblems).toEqual([]);
  });
}

test('CMS-backed overview pages contain generated entries', async ({ page }) => {
  await page.goto('members/');
  expect(await page.locator('.member-card').count()).toBeGreaterThan(0);

  await page.goto('publications/');
  expect(await page.locator('.publication-card').count()).toBeGreaterThan(0);

  await page.goto('teaching/');
  expect(await page.locator('.course-card').count()).toBeGreaterThan(0);
});

test('site search returns readable results and an empty state', async ({ page }) => {
  await page.goto('./');
  await page.keyboard.press('/');

  const dialog = page.locator('#site-search-dialog');
  const input = page.locator('#site-search-input');
  await expect(dialog).toBeVisible();
  await expect(input).toBeFocused();

  await input.fill('arithmetic');
  await expect(page.locator('#site-search-results > li').first()).toBeVisible();
  await expect(page.locator('.site-search-result-type').first()).not.toBeEmpty();

  await input.fill('definitely-no-result-xyz');
  await expect(page.locator('.site-search-empty')).toBeVisible();
  await expect(page.locator('#site-search-status')).toHaveText('No results found.');

  await page.keyboard.press('Escape');
  await expect(dialog).not.toBeVisible();
});

test('publication search filters and clears without changing source content', async ({ page }) => {
  await page.goto('publications/');
  const cards = page.locator('#publication-grid > .publication-card');
  const total = await cards.count();

  await page.locator('#publication-search-input').fill('arithmetic');
  const filtered = await page.locator('#publication-grid > .publication-card:visible').count();
  expect(filtered).toBeGreaterThan(0);
  expect(filtered).toBeLessThan(total);
  await expect(page).toHaveURL(/\?q=arithmetic$/);

  await page.locator('.publication-search-clear').click();
  expect(await page.locator('#publication-grid > .publication-card:visible').count()).toBe(total);
  await expect(page).not.toHaveURL(/\?q=/);
});

test.describe('mobile navigation', () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test('opens, exposes state, and closes with Escape', async ({ page }) => {
    await page.goto('./');

    const toggle = page.locator('.nav-toggle');
    const sidebar = page.locator('#sidebar-navigation');

    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(sidebar).toHaveAttribute('aria-hidden', 'false');

    await page.keyboard.press('Escape');
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(sidebar).toHaveAttribute('aria-hidden', 'true');
  });

  test('hands off cleanly from navigation to site search', async ({ page }) => {
    await page.goto('./');

    const toggle = page.locator('.nav-toggle');
    const sidebar = page.locator('#sidebar-navigation');
    await toggle.click();
    await page.locator('#sidebar-navigation [data-site-search-open]').click();

    await expect(sidebar).toHaveAttribute('aria-hidden', 'true');
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(page.locator('#site-search-dialog')).toBeVisible();
    await expect(page.locator('#site-search-input')).toBeFocused();
  });
});

test('representative generated detail pages resolve', async ({ page }) => {
  await page.goto('members/');
  const memberPath = await page.locator('.member-card a').first().getAttribute('href');
  expect(memberPath).toBeTruthy();
  await page.goto(memberPath);
  await expect(page.locator('.member-profile-page')).toBeVisible();

  await page.goto('publications/');
  const publicationPath = await page.locator('.publication-card a').first().getAttribute('href');
  expect(publicationPath).toBeTruthy();
  await page.goto(publicationPath);
  await expect(page.locator('.publication-page')).toBeVisible();
});
