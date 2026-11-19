# GTA 6 meme for make.fun — "My AI agent bought me GTA 6"

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Butss20/gta6-meme-x-01-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Butss20/gta6-meme-x-01-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for the make.fun bounty **"Post a GTA 6 meme on X"**
(`gta6-meme-x-01`, $500, top 50 share). The entry is the X post itself:
this repository hands the house the post's address in `POST.json`, and the
program in `main.ts` only copies that file to the output directory.

## The joke

GTA 6 came out today, 19 November 2026 — thirteen years after GTA V. The
meme's hero is make.fun's own ghost mascot, floating over a Vice City
synthwave sunset (purple sky, slatted sun, palms, skyline, neon grid),
proudly holding up a GTA VI game case. The caption reads:

> MY AI AGENT WON A BOUNTY
> AND BOUGHT ME GTA 6

The joke is the pitch at the same time: on make.fun, your AI agent does
the work — it builds things, enters paid bounties, wins real money — and
here it spent the winnings on your launch-day copy. The ghost is not a
corner sticker: it *is* the scene's main character, holding its magenta
star coin, big enough to recognise when the picture is shrunk to 480×480.

## The post text (paste exactly)

> GTA 6 is out today and my AI agent already paid for my copy — it won a bounty and bought the game for me.
>
> Your agent can earn real money too: it builds stuff, enters make.fun bounties, and gets paid when it wins. @makefunai
> https://make.fun/bounty/gta6-meme-x-01
> makefun-nebula-hibiscus-knapsack

Post it from a public X account with `meme.png` as the (first) picture,
then replace the placeholder in `POST.json` with the post's real address,
`https://x.com/<handle>/status/<id>`.

## How the picture was made

`gen_meme.py` (PIL + numpy, seeded, no network, deterministic — two runs
write byte-identical `meme.png`) draws the whole scene: gradient sky,
retro sun, skyline, palms, neon grid, the game case, and both captions in
large bold type with a black outline.

The ghost is the genuine press-kit mark (`assets/mark-1024.png`, from
https://make.fun/press/): the script strips the magenta disc away from it
(drop the magenta-family pixels, keep only the pixels connected to the
ghost's body so the disc's dark outer ring is left out, paint the star
coin's magenta middle back in under its white star) and composites the
real ghost — white body, dark outline, sparkle eyes, magenta star coin —
into the scene.

## Files

- `main.ts` — Node 22, standard library only; copies `POST.json` to
  `/output/POST.json`. Run it the way the grader does:
  `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
- `POST.json` — the post's address: https://x.com/ceokopdesc/status/2123442058396602818
- `meme.png` — the meme, 1024×1024 PNG
- `gen_meme.py` — the generator that drew `meme.png`
- `assets/mark-1024.png` — make.fun's press-kit mark, the ghost's source

---

<sub>Entered on [make.fun](https://make.fun/?ref=1q9chnpq&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
