# The World in One Day — Thursday 26 November 2026

[![Bounty](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/renprayoga/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/renprayoga/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image that sums up the world's news of **Thursday 26 November 2026**,
drawn as a newspaper front page: a cream masthead, one dominant lead with a
drawn refinery scene, two illustrated stories, a Trade & Markets band with
mini charts, and a two-column Day in Brief.

## The day in the picture

- **Lead — Houthis hit Saudi refinery as Brent tops $94:** Yemen's Houthis
  claim strikes on the Ras Tanura refinery and Riyadh's financial district,
  jolting oil markets and raising fears of wider disruption to Gulf energy
  supplies.
- **Tankers hit mines in the Strait of Hormuz:** two oil tankers strike naval
  mines in the world's busiest oil chokepoint as Gulf tensions climb.
- **Israel strike in Gaza strains ceasefire:** Israel kills a senior Hamas
  security official in Gaza; the fragile ceasefire comes under fresh strain.
- **Trade & Markets:** the US proposes tariffs of up to 15% on 14 trading
  partners; Taiwan shares tumble 1,927 points as the dollar passes 33;
  Nvidia is put on downgrade watch as the AI sell-off deepens.
- **Also today:** Mumbai marks 18 years since the 26/11 attacks and India
  observes Constitution Day; Pakistan's first astronaut joins China's
  Shenzhou-24 mission; Ukraine hits Russian refineries and Putin vows
  retaliation; 31 are killed in a Cairo fuel-tanker fire; North Korea
  expels a Swiss diplomat; the Solomon Islands signs a security treaty with
  Australia; 15-year-old Vaibhav Sooryavanshi smashes the fastest List A
  double century (204 off 53); the 100th Macy's Thanksgiving Day Parade
  takes to New York's streets.

Sources: Reuters, BBC, CNN, AFP, AP.

## How it runs

`main.py` (Python 3.13, standard library only) draws the page procedurally
with `render.py` — a tiny deterministic raster engine with a hand-built 5x7
pixel font and a hand-written PNG encoder — and writes `entry.png`
(1024x1024, well under 1 MiB) to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
No network, no fonts from disk, no timestamps in the output: two runs write
byte-identical files.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
