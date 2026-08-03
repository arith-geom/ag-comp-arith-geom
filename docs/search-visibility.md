# Search visibility operations

The repository generates crawl metadata automatically, but search-engine account
operations require a maintainer who can sign in to the relevant webmaster tools.

## Google Search Console

1. Open Google Search Console and select or create the URL-prefix property
   `https://arith-geom.github.io/ag-comp-arith-geom/`.
   Protocol, path, and the trailing slash are part of a URL-prefix property; a
   property for `http://`, `https://arith-geom.github.io/`, or a path without the
   final slash is not the same property.
2. Ownership can be verified by the existing HTML verification file if its token
   belongs to the Google account managing the property. Deleting a Google account
   or its Search Console access does not remove the public file from this
   repository, but the remaining file does not prove that a new account owns its
   token. If Search Console supplies a new verification file, add it alongside the
   existing file, verify the new owner, and only then remove obsolete tokens.
3. Open **Sitemaps** for that exact property. When Search Console already displays
   the property prefix before the input, enter only `sitemap.xml`. If the interface
   requests a full URL, submit
   `https://arith-geom.github.io/ag-comp-arith-geom/sitemap.xml`.
4. After favicon or important metadata deployments, inspect the homepage URL and
   request indexing. Google controls recrawl timing, so an icon change is not
   immediate.
5. Review **Page indexing**, **Core Web Vitals**, and **HTTPS** after deployment.

### If Search Console says the sitemap could not be fetched

1. Open the sitemap URL in a private browser window. It must return XML rather
   than a GitHub 404 page or HTML.
2. In **URL inspection**, inspect the full sitemap URL and run **Test live URL**.
3. Confirm that the selected property is exactly
   `https://arith-geom.github.io/ag-comp-arith-geom/` and that the submitted row
   contains the same prefix only once.
4. Delete only the failed sitemap submission from Search Console and submit it
   again as described above. This does not delete the sitemap or website content.
5. If the live test succeeds but the report still says **Couldn't fetch**, wait
   before resubmitting; Search Console can retain a temporary fetch failure.

The public sitemap currently returns HTTP 200, is valid XML, is advertised from
`robots.txt`, and contains only canonical URLs inside the project property. The
repository therefore should not be changed merely to work around a stale Search
Console status.

## Hostname root property and Google favicon

The project is hosted below `/ag-comp-arith-geom/`. The organization-wide root
`https://arith-geom.github.io/` is a separate GitHub Pages site and requires a
public repository named exactly `arith-geom.github.io` in the `arith-geom`
organization. An organization owner must create that repository or grant the
required repository-creation permission; a regular organization member cannot
assume that authority.

After the root repository exists:

1. publish a small root `index.html` that links or redirects visitors to the
   project site;
2. publish the approved favicon at `/favicon.ico` and, preferably, matching PNG
   and Apple touch icon variants;
3. add the root URL-prefix property `https://arith-geom.github.io/` to Search
   Console and place its newly issued verification file at the repository root;
4. verify ownership before removing any older verification file; and
5. inspect the root and project homepages and request indexing after deployment.

A Domain property for `github.io` is not appropriate because the organization
does not control GitHub's DNS zone. Use the two exact URL-prefix properties, or
move the site to a custom domain whose DNS the organization controls.

## Preserve historical file URLs

Some files under `assets/img/fileadmin/` are byte-identical to migrated copies but
their old public URLs are indexed and cited by external academic publications.
Treat these files as compatibility aliases, not disposable duplicates. Remove one
only with evidence that the old URL has no external consumers and with a working
replacement or redirect strategy.

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
