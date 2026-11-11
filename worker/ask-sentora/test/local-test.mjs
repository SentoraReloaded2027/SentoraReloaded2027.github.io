// Local test of the Worker without a Claude key: a stand-in Claude API on localhost records what the
// Worker sends and answers with a canned message. Run: NODE_USE_ENV_PROXY=1 node test/local-test.mjs
import http from "node:http";
import worker from "../src/index.js";

let seen = [];
const fake = http.createServer((req, res) => {
  let body = ""; req.on("data", (c) => (body += c)); req.on("end", () => {
    const j = JSON.parse(body); seen.push({ path: req.url, headers: req.headers, body: j });
    const q = j.messages[0].content;
    const out = q.includes("REFUSE")
      ? { id: "msg_t", type: "message", role: "assistant", model: j.model, content: [], stop_reason: "refusal", stop_details: { type: "refusal", category: null, explanation: "" }, usage: { input_tokens: 1, output_tokens: 1 } }
      : { id: "msg_t", type: "message", role: "assistant", model: j.model, stop_reason: "end_turn", usage: { input_tokens: 10, output_tokens: 20 },
          content: [{ type: "text", text: "Run the export on the old server.\n\nRead more: https://github.com/RusTus/sentora-core-2027/blob/master2027/README.md#moving-websites-from-an-old-sentora-server" }] };
    res.writeHead(200, { "content-type": "application/json" }); res.end(JSON.stringify(out));
  });
});
await new Promise((r) => fake.listen(0, "127.0.0.1", r));
const env = { ANTHROPIC_API_KEY: "test-key", ANTHROPIC_BASE_URL: `http://127.0.0.1:${fake.address().port}`,
  MODEL: "claude-opus-5-5", ALLOWED_ORIGIN: "https://sentorareloaded2027.github.io", PER_IP_PER_HOUR: "3" };
const SITE = "https://sentorareloaded2027.github.io";
async function ask(q, origin = SITE, ip = "1.2.3.4", e = env) {
  const r = await worker.fetch(new Request("https://ask.example/ask", { method: "POST", headers: { Origin: origin, "Content-Type": "application/json", "CF-Connecting-IP": ip }, body: JSON.stringify({ question: q }) }), e);
  return [r.status, await r.json(), r.headers.get("access-control-allow-origin")];
}
let fails = 0; const check = (ok, what) => { console.log((ok ? "  ok   " : "  FAIL ") + what); if (!ok) fails++; };

let [s, j, a] = await ask("How do I move my sites from my old Sentora server?");
check(s === 200 && /export/.test(j.answer), `an answer comes back (${s})`);
check(a === SITE, "CORS allows the website");
const sent = seen[0];
check(sent && sent.path.startsWith("/v1/messages"), "it called the Messages API");
check(sent.body.model === "claude-opus-5-5" && sent.body.output_config.effort === "low", "model claude-opus-5-5, effort low");
check(/server-side-fallback-2026-07-01/.test(sent.headers["anthropic-beta"] || "") && sent.body.fallbacks === "default", "refusal fallback on (beta header + fallbacks default)");
const docs = sent.body.system[1];
check(docs.cache_control && docs.cache_control.type === "ephemeral", "the documents are a cached block");
check(docs.text.includes("## Moving websites from an old Sentora server") && docs.text.includes("- Release 2027."), `the README and changelog from GitHub are in it (${Math.round(docs.text.length / 1000)} k characters)`);
check(sent.body.system[0].text.startsWith("You answer questions about Sentora 2027"), "the instructions come first (stable, so the cache holds)");
check(sent.headers["x-api-key"] === "test-key" || sent.headers["authorization"] === "Bearer test-key", "the key goes only to the API, in its auth header");

[s, j] = await ask("hello", "https://evil.example"); check(s === 403, `another website is refused (${s})`);
[s, j] = await ask(""); check(s === 400, `an empty question is refused (${s})`);
[s, j] = await ask("x".repeat(501)); check(s === 400, `a too long question is refused (${s})`);
[s, j] = await ask("REFUSE this", SITE, "9.9.9.9"); check(s === 200 && /can't help/.test(j.answer), "a refusal gets a polite answer");
await ask("q2", SITE, "5.5.5.5"); await ask("q3", SITE, "5.5.5.5"); await ask("q4", SITE, "5.5.5.5");
[s, j] = await ask("q5", SITE, "5.5.5.5"); check(s === 429, `the fourth question in an hour from one visitor is refused at limit 3 (${s})`);
[s, j] = await ask("q", SITE, "6.6.6.6", { ...env, ANTHROPIC_API_KEY: "" }); check(s === 503, `no key set: a clear message (${s})`);
const n = seen.length;
[s, j] = await ask("Haiku?", SITE, "7.7.7.7", { ...env, MODEL: "claude-haiku-5-5" });
check(seen[n].body.model === "claude-haiku-5-5" && !seen[n].body.fallbacks, "MODEL=claude-haiku-5-5 works, without fallbacks");
const opt = await worker.fetch(new Request("https://ask.example/ask", { method: "OPTIONS", headers: { Origin: SITE } }), env);
check(opt.status === 204, "the browser's preflight is answered");
fake.close();
console.log(fails ? `ASK: ${fails} FAILED` : "ASK: PASSED");
process.exit(fails ? 1 : 0);
