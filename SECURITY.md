# Security Policy

## Reporting a vulnerability

Please do not disclose suspected vulnerabilities in a public issue. Use the
repository's **Security** tab to submit a private vulnerability report. If that
option is unavailable, email `arithgeo@iwr.uni-heidelberg.de` with the subject
`Website security report`.

Include the affected URL or component, reproduction steps, likely impact, and
any suggested mitigation. Do not include unrelated personal data or attempt to
access, alter, or remove other people's content.

Maintainers should acknowledge a report within seven days. Remediation and
disclosure timing depend on severity and the availability of upstream fixes.

## Supported version

The deployed version from the default branch is supported. Older deployments,
forks, and unmerged branches are not maintained security releases.

## Deployment headers

GitHub Pages does not provide repository-level configuration for HTTP response
headers. If the site is later served through a configurable CDN or proxy, add a
tested Content Security Policy, Permissions Policy, HSTS, and MIME-sniffing
protection there. A strict Content Security Policy must account for the site's
inline structured data and scripts before enforcement; an untested policy can
break navigation, mathematics, analytics, or CMS-managed embeds.
