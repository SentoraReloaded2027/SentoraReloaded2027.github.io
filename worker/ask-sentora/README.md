# Ask Sentora

A small Cloudflare Worker that answers questions about Sentora 2027 on the website. It reads the panel's
README, the installers' README and the changelog from GitHub, asks Claude to answer **only from them**, and
returns the answer with links to the README sections it used. The website's "Find an answer" search stays as
it is; the **Ask Sentora** button appears under it once the Worker's address is set in `index.html`.

## What it costs

- **Cloudflare:** nothing on the free plan (100,000 requests a day; waiting for Claude does not count
  toward the 10 ms of CPU per request).
- **Claude:** paid on your Anthropic account. The documents (about 95,000 tokens) are sent as a cached block,
  so a question costs roughly 2 cents with Claude Opus 5.5 (the first one after a quiet spell, about 40 cents),
  or a small fraction of a cent with Claude Haiku 5.5 (`MODEL` in `wrangler.toml`). **Set a monthly spending
  limit in the Anthropic Console first**: it is the hard cap.

## Guards

- Only the website may ask (`ALLOWED_ORIGIN`); questions up to 500 characters.
- `PER_IP_PER_HOUR` questions per visitor and hour (default 20; kept per Worker instance, so it is a first line
  of defence: the spending limit is the real cap).
- Claude answers only from the documents, says so when they do not answer, and declines anything else.
- The Claude key is a Cloudflare secret: never in the website, in GitHub or in this folder.

## Set it up (once)

1. **Anthropic:** console.anthropic.com > Settings > Limits: set a monthly spending limit. Then API keys >
   Create key; copy it.
2. **Cloudflare:** sign up at dash.cloudflare.com (free). Workers & Pages > Create > Create Worker, name it
   `ask-sentora`, Deploy (the hello-world it makes is replaced in step 4).
3. In that Worker: Settings > Variables and Secrets > Add > type **Secret**, name `ANTHROPIC_API_KEY`, paste
   the key, Deploy.
4. **Deploy this code**, either way:
   - **From GitHub (nothing to install):** in Cloudflare, My Profile > API Tokens > Create Token > template
     "Edit Cloudflare Workers"; copy the token. In this repository on GitHub: Settings > Secrets and variables >
     Actions > New repository secret: `CLOUDFLARE_API_TOKEN` (the token) and `CLOUDFLARE_ACCOUNT_ID` (shown on
     Cloudflare's Workers & Pages page). Then Actions > **Deploy Ask Sentora** > Run workflow.
   - **From a PC with Node.js:** in this folder, `npm ci`, then `npx wrangler login`, then `npx wrangler deploy`.
5. Cloudflare shows the Worker's address, like `https://ask-sentora.<your-name>.workers.dev`. Put it in the
   website's `index.html` as `ASK_URL` (search for `var ASK_URL`), with `/ask` on the end. The **Ask Sentora**
   button then appears under the search.

## Test

`npm ci`, then `NODE_USE_ENV_PROXY=1 node test/local-test.mjs`: 17 checks against a stand-in Claude API on
this computer (no key, no cost): the documents arrive from GitHub and are cached, the model, effort and refusal
fallback, other websites refused, the length and per-visitor limits, the messages when the key is missing or
Claude declines. The GitHub workflow runs it before every deploy.
