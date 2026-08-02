const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? 'github' : 'list',
  use: {
    baseURL: 'http://127.0.0.1:4000/ag-comp-arith-geom/',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'bundle exec jekyll serve --no-watch --host 127.0.0.1 --port 4000',
    url: 'http://127.0.0.1:4000/ag-comp-arith-geom/',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
