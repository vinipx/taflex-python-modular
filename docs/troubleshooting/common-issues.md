# Troubleshooting

## Common Issues

### Invalid URL Error in API Strategy
Ensure that `API_BASE_URL` is set in your `.env` file and starts with `http://` or `https://`.

### Locators not found
Verify the hierarchy in `src/resources/locators`. Remember the resolution order: Page > Mode > Global.

### Playwright Browser missing
Run `playwright install` to download required binaries.
