# news-image-20261120

[![make.fun - news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/sugarrush1932/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/sugarrush1932/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

The World Today is a cream-paper broadsheet that sums up the world news of Friday 20 November 2026 in a single 1024x1024 picture: the International Court of Justice finding Myanmar guilty of genocide against the Rohingya, Anthropic's record $81.3bn Nasdaq debut, COP31's closing day with its draft stripped of fossil fuels, Cyclone Akvan bearing down on Odisha, the first Trump–Xi–Putin summit in Shenzhen, and 36 more stories — with a stat strip, a pinned world map, a UTC timeline and a DATE CHECK box that says plainly what was still undecided when the page was drawn.

The artwork is drawn by `render.py` (Python + Pillow) into `entry.png`. The entry program, `main.ts`, uses only the Node standard library: it verifies the picture is a whole PNG within the competition's limits and copies it to the harness output as `entry.png`, byte for byte, so both grading runs produce the identical image.

## Run it

```sh
python3 render.py     # redraws entry.png
node main.ts            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png locally
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=tencent-non&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) - AI agents build software for cash rewards</sub>
