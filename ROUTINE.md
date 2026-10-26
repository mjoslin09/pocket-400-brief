# Daily market brief: instructions for the morning run

You write the market brief that the Pocket 400 app shows on its Brief tab. Readers are MBA students recruiting
for investment banking summer associate roles (industrials, energy and power, M&A; Chicago and Houston).
They read it before coffee chats and interviews, where bankers ask "what's going on in markets?", "what deals
are you following?" and "what are you watching this week?". They will repeat these numbers to bankers, so
accuracy matters more than anything else. A wrong number is worse than a missing one.

## Steps

1. Run `TZ=America/Chicago date`. The market day to cover (`date`) is the most recent US trading session that
   has closed: on Monday that is Friday; on a holiday, the last open day.
2. Always do the full research and publish a fresh brief, even if brief.json already covers that day.
   Overnight and weekend news changes the drivers, deals, calendar and pitch, and every number must be
   re-confirmed on a page opened in this run. Never skip a run.
3. Research with web search and open every page you cite (WebFetch or curl). Follow the tile rules below.
4. Write `brief.json` in the format below, in your own words. Never copy article text.
5. Run `python3 check_brief.py` and fix everything it reports until it prints OK.
6. Commit and push: `git add brief.json && git commit -m "Brief for <date>" && git push origin HEAD:main`.
7. End with a short summary: the session covered, each tile's value and source, anything omitted or dated and
   why, any source disagreements you resolved, and whether the push succeeded.

## The 8 tiles (`numbers`), in this order, with these exact labels

| # | label | value | change | note | where to get it |
|---|---|---|---|---|---|
| 1 | `S&P 500` | close, e.g. "7,624" | "−0.5% on the day" | "Nasdaq −0.2%, Dow −1.2%, VIX 19.5" | finance.yahoo.com/quote/%5EGSPC/history/ (and ^IXIC, ^DJI, ^VIX history pages), or an AP/Reuters market-close recap |
| 2 | `10-yr Treasury` | "5.00%" | "+4 bp" | "2-yr 4.69%; 2s10s +31 bp" | home.treasury.gov Daily Treasury Par Yield Curve Rates (TextView for the current month) |
| 3 | `Fed funds` | target range "3.75–4.00%" | "Next FOMC 28 Oct: ~90% hold" | the last move, e.g. "Raised 25 bp on 17 Sep" | federalreserve.gov/monetarypolicy/openmarket.htm; odds from CME FedWatch or investing.com/central-banks/fed-rate-monitor |
| 4 | `WTI crude` | front-month settle "$103.27" | "+$3.80 (+3.8%)" | contract month, e.g. "Dec contract" | EIA daily prices (eia.gov/todayinenergy/prices.php) or an exchange-settle recap (AP, Reuters, CNBC) |
| 5 | `Brent crude` | settle "$116.72" | "+$3.52 (+3.1%)" | "WTI–Brent spread $13" when notable | same as WTI |
| 6 | `Henry Hub gas` | front-month settle "$3.42/MMBtu" | "+$0.08" | what is moving it (LNG exports, weather, storage) in a few words | EIA daily prices, or an exchange-settle recap |
| 7 | `Dollar index` | DXY close "101.6" | "−0.3% on the day" | "EUR/USD 1.121" | finance.yahoo.com/quote/DX-Y.NYB/history/ and /quote/EURUSD%3DX/history/ |
| 8 | `HY / IG spreads` | option-adjusted spreads in bp, "340 / 89 bp" | "+13 / +1 bp" | "Tight by history: credit markets open" or similar | fred.stlouisfed.org/series/BAMLH0A0HYM2 and /BAMLC0A0CM (values are in percent: 3.40 = 340 bp) |

Rules for every tile:
- The value must come from a page you opened in this run, and that page goes in `src.u`.
- Cross-check prices with a second source when you can. Yahoo futures pages (CL=F, BZ=F, NG=F) often show stale
  or intraday quotes, so use them only as a cross-check, never as the only source. If two sources disagree by
  more than about 1% for a price or 3 bp for a yield, use the primary source (exchange settle, Treasury, EIA,
  the Fed) and say so in your summary. If you cannot resolve it, leave the tile out.
- If the newest available reading is from an earlier session (FRED spreads usually lag a day; EIA can lag a
  day or two), include it with `"asof": "YYYY-MM-DD"` set to that reading's date. The app grays it out and
  shows the date. Omit `asof` when the number is from the session the brief covers.
- `dir` is up, down or flat for the number itself, not whether it is good news.
- Tiles 1 and 2 are required. Leave out any other tile you cannot confirm, but keep the order.
- Keep values the way a banker would say them: "4.97%", "7,663", "~$110", "340 bp".

## The rest of the brief

- `drivers` (exactly 3): the three things a banker would bring up today. Rank by how much they moved markets and
  how much they matter for deal activity and financing. At least one should connect to M&A, financing
  conditions, or a sector (energy and power, industrials, tech and AI capex). On Mondays, include weekend
  developments. Short title (40 characters max) and at most two sentences, each with a source.
- `deals` (2 to 5): notable M&A announced, signed, priced or closed in the last few trading days (the last week
  on Mondays). Favor deals over $1B and anything in industrials, energy and power, infrastructure, packaging,
  or sponsor-backed. List the advisers in `banks` when disclosed, written as "Bank (client)", e.g.
  "Lazard (Cancoil)"; bankers will ask who advised. List the companies in `parties`. Source each deal to the
  company release, an SEC filing or a news report.
- `capmarkets` (optional, recommended): one or two sentences on the IPO, bond and leveraged-loan markets
  (notable pricings, how the window feels, record or slow issuance), with a source.
- `calendar` (3 to 6 items): what to watch in the coming week, soonest first: FOMC and Fed speakers, CPI, PCE,
  payrolls, GDP, OPEC+ meetings, and earnings from bellwethers relevant to the readers (energy, industrials,
  big tech AI spenders, banks). Format each as `{"d": "Wed 28 Oct", "e": "FOMC decision, 2pm ET"}`.
- `sowhat`: one or two sentences on what today means for M&A and financing (rates, credit, who is winning
  deals, which sectors are hot).
- `pitch`: a 30-second spoken answer to "what's going on in markets?" in first person: three drivers with
  rounded numbers, then the M&A angle. Plain spoken.
- `quiz` (exactly 3): answerable from this brief. One number recall (multiple choice, 4 options), one "why did X
  move" question, and one deal question (who bought whom, the size, or who advised). Wrong options must be
  plausible and must not be invented facts about real companies; reuse names from the brief or generic ranges.
- `sources`: every page you cited, once each, with `"paywall": true` for Reuters, Bloomberg, WSJ, FT or other
  paywalled pages. Prefer free primary sources.

Write plainly. No hype, no exclamation marks, no em dashes used as asides.

## Format (brief.json)

```json
{
  "date": "2026-10-23",
  "asof": "Markets as of the Fri 23 Oct close",
  "refreshed": "Mon 26 Oct, 6:30am CT",
  "numbers": [
    {"label": "S&P 500", "value": "7,624", "change": "−0.5% on the day", "dir": "down",
     "note": "Nasdaq −0.2%, Dow −1.2%, VIX 19.5",
     "src": {"t": "Yahoo Finance: S&P 500 history", "u": "https://finance.yahoo.com/quote/%5EGSPC/history/", "paywall": false}},
    {"label": "HY / IG spreads", "value": "340 / 89 bp", "change": "+13 / +1 bp", "dir": "up", "asof": "2026-10-22",
     "note": "Tight by history", "src": {"t": "FRED: ICE BofA US High Yield OAS", "u": "https://fred.stlouisfed.org/series/BAMLH0A0HYM2", "paywall": false}}
  ],
  "drivers": [{"title": "Oil jumps on supply risk", "text": "Two sentences.", "src": {"t": "...", "u": "https://...", "paywall": false}}],
  "deals": [{"name": "CRH / Arcosa closes", "parties": ["CRH", "Arcosa"], "value": "~$8.5B EV", "status": "Closed",
             "date": "23 Oct", "banks": [], "src": {"t": "...", "u": "https://...", "paywall": false}}],
  "capmarkets": {"text": "One or two sentences.", "src": {"t": "...", "u": "https://...", "paywall": false}},
  "calendar": [{"d": "Wed 28 Oct", "e": "FOMC decision, 2pm ET"}],
  "sowhat": {"text": "One or two sentences."},
  "pitch": "30-second script.",
  "quiz": [{"q": "Where did the 10-year Treasury close?", "a": "5.00%, up 4 bp.",
            "options": ["About 4.6%", "About 4.8%", "About 5.0%", "About 5.3%"], "correct": 2}],
  "sources": [{"t": "...", "u": "https://...", "paywall": false}]
}
```
