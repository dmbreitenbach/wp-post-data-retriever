# wp-post-date-retriever
Gets post dates from WordPress REST API and saves to CSV.

This script was created to GET **post publication** and **last modified dates** for WordPress websites with the [REST API](https://developer.wordpress.org/rest-api/) enabled. This is particularly useful for websites where the post dates are not published in the URL or HTML. Even if posts dates are accessible through other means, using the API with this script will be more efficient and more respectful than crawling and scraping.

## Use cases
Post dates are useful for a variety of content strategy and SEO application, especially when combined with analytics:
- Content audits
- SEO blog updates/refreshes
- Determining content "shelf life"

## Other uses
With some knowledge of the API, this script can be modified to get a variety of data. 

### SEO
Some SEO plugins may surface other useful data in the API. For example, on a website running Yoast SEO, you could get:
- **Canonical URLs** - add `yoast_head_json.canonical` to the `fields` variable
- **Schema markup** - add `yoast_head_json.canonical` to the `fields` variable

### Other endpoints
You could get pubication and last modified dates for pages by changing the `path` variable from `/wp-json/wp/v2/posts` to `/wp-json/wp/v2/pages`. More possibilities are listed at the [API Endpoint Reference](https://developer.wordpress.org/rest-api/reference/), but most data are not public, so you'll need to add [authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/) to your request.

## Potential issues
- **Empty User Agent** Some hosts will block requests without a valid user agent. If you get a 403 error, check that the `user_agent` variable is set appropriately. If you're not sure, Google "what is my user agent" and copy the result into the `user_agent = ''` between the quotes.
- Not all WordPress websites have the API enabled, some require authentication for all requests, including for public data. Further testing is required to better handle these cases.
