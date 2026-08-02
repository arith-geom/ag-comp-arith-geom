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
