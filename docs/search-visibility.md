# Search visibility operations

The repository generates crawl metadata automatically, but search-engine account
operations require a maintainer who can sign in to the relevant webmaster tools.

## Google Search Console

1. Open Google Search Console and select or create the URL-prefix property
   `https://arith-geom.github.io/ag-comp-arith-geom/`.
2. Ownership can be verified by the existing HTML verification file if it matches
   the Google account managing the property. Do not replace that file without
   checking the property's verification method.
3. Submit
   `https://arith-geom.github.io/ag-comp-arith-geom/sitemap.xml` under **Sitemaps**.
4. After favicon or important metadata deployments, inspect the homepage URL and
   request indexing. Google controls recrawl timing, so an icon change is not
   immediate.
5. Review **Page indexing**, **Core Web Vitals**, and **HTTPS** after deployment.

## Deployment checks

Verify these public URLs after the relevant pull requests are merged and Pages has
finished deploying:

- `/robots.txt` returns HTTP 200 and references the sitemap.
- `/sitemap.xml` returns HTTP 200 and contains canonical HTTPS URLs.
- `/favicon.ico`, `/favicon-32x32.png`, and `/apple-touch-icon.png` return their
  expected image types rather than an HTML error document.
- The homepage contains one canonical URL, one description, and Organization
  structured data.

The repository's SEO, generated-site, Lighthouse, and browser workflows cover the
build-side requirements. Search Console remains the source of truth for Google's
actual crawl and indexing state.

## Other engines

The same sitemap can be submitted to Bing Webmaster Tools. Do not use deprecated
anonymous sitemap-ping endpoints; use an authenticated webmaster account instead.
