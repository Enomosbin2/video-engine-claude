# Script guide

A script is a plain text file. Narration lines are spoken one at a time, and the animation is timed to each line. Visual tags in square brackets go on the line before the narration they belong to, or at the start of the same line.

## Header (top of file, all optional)

```
TITLE: Clausewitz in Two Minutes     shown on the opening card
VOICE: bm_george                     bm_george, bm_lewis, bf_emma, bf_isabella, am_michael, af_heart
SPEED: 0.95
PLACE: Wu = 120.6, 31.3              any place the map can't find (lon, lat)
SAY: Milošević = Milo-sheh-vitch     pronunciation fix (screen keeps the original)
MARKING: RESTRICTED                  printed top and bottom of every frame
```

## Scenes

```
## The Trinity                  plain section; name shows top-left
## IDEA 2 | The Trinity         same, plus a 3-second title card ("IDEA 2", "The Trinity")
```

## Narration

Each non-empty line that isn't a tag or header is one narration cue. Write numbers as figures. The voice says "431 BC" as "four thirty-one B.C.", "1812" as "eighteen twelve" and "97%" as "97 per cent". Use `[pause: 2]` on its own line for a 2-second silent beat.

## Boards (the main picture; a new board cross-fades in)

| Tag | What it shows |
|---|---|
| `[map: Kuwait, Baghdad, Riyadh]` | Map framed to fit the places, labelled. Options: `span=20` (degrees wide), `center=47,29`, `pad=0.5` |
| `[quote: text \| source]` | Quote card |
| `[bullets: #Heading \| point \| point \| step]` | Numbered list. Without `step`, points appear across the line; with `step`, one per narration line |
| `[timeline: 1792 = joins army \| 1806 = Jena \| step]` | Horizontal timeline |
| `[compare: Policy ; sets the aim \| War ; serves the aim \| arrow]` | Two panels (`;` separates title and lines) |
| `[text: BIG STATEMENT \| smaller line]` | Big centred words |
| `[title: KICKER \| Title \| subtitle]` | Dark title card |
| `[image: photo.jpg]` | Your picture (next to the script), slow zoom |
| `[custom: name \| args]` | Special animation (see below) |
| `[blank]` / `[dark]` | Empty parchment / dark background |

The first scene opens on a title card using TITLE unless it starts with a board.

## Map overlays (only on a map board; they stay until the board changes)

Places are names (cities and countries are built in), `PLACE:` names, or `lon,lat`.

| Tag | Effect |
|---|---|
| `[place: Mosul, Raqqa \| blue]` | Add labelled dots |
| `[pulse: Moscow \| red]` | Pulsing highlighted place |
| `[arrow: Kuwait > Basra > Baghdad \| blue \| thick \| dashed \| text=100 hours]` | Animated arrow along a route |
| `[move: tanks \| Rostov > Moscow \| brown \| n=4]` | Units travel the route: `tanks`, `ships`, `troops`, `drones`, `missiles`. `loop` repeats |
| `[boom: Belgrade \| n=5]` | Explosions |
| `[area: Crimea \| red \| r=80 \| text=Annexed 2014]` | Shaded circle |
| `[label: Text @ Kyiv \| red \| dy=40]` | Text near a place (or top-centre with no @) |
| `[zoom: Kyiv \| span=6]` | Camera moves to fit the places |

## Overlays on any board

| Tag | Effect |
|---|---|
| `[stamp: Missiles removed \| green \| bottom/middle/left/right]` | Rubber stamp (default near top) |
| `[year: 1991]` | Year badge top-right |
| `[counter: 0-100 \| hours]` | Number counting up during the line |
| `[note: Drone: thousands \| Interceptor: millions]` | Small panel, top-right (`left` for top-left) |

Colours: red, blue, green, gold, ink, purple, grey, brown, orange, olive, white.

## Custom animations (`vengine/customs.py`)

| Tag | Animation |
|---|---|
| `[custom: magnets \| Passion ; the people \| Chance ; army \| Reason ; government \| pull=1 \| object=WAR]` | Object pulled between three magnets; `pull=` makes one win |
| `[custom: gears \| FRICTION \| danger \| fatigue \| weather]` | Gears jamming with grit |
| `[custom: hub \| CoG \| army \| capital \| alliance \| collapse]` | Hub and spokes; `collapse` knocks out the hub |
| `[custom: water \| STRENGTH]` | Water flowing round a rock |
| `[custom: curve \| CULMINATING POINT \| attacker \| defender]` | Strength falling with distance |
| `[custom: ladder \| Order of strategy \| best \| ... \| worst]` | Ranked options |
| `[custom: scales \| Left \| Right \| tip=left]` | Balance tipping |

A new animation is one Python function in `customs.py` plus one line in `REGISTRY`. `examples/handcoded/` holds the hand-coded Sun Tzu and Clausewitz videos (the drill, Midway, Spiderweb and so on) to borrow from.

## Commands

```
./setup.sh                                   once per session or machine
python3 make_video.py script.txt --check     narration + plan + contact sheets (script_work/sheet_*.jpg)
python3 make_video.py script.txt             full video -> script.mp4
python3 make_video.py script.txt --scene 3   re-render scene 3 only and rejoin
```

Narration is cached, so unchanged lines are not re-voiced. Unknown place names stop the run and are listed, so add them with `PLACE:`.

## Rules for Claude when making a video

1. Run `./setup.sh` first.
2. If the user's script has no tags, write the tagged version and show the plan before rendering. Keep their narration wording.
3. Run `--check` and look at the contact sheets. Fix these before the full render:
   - text hidden under the caption bar;
   - labels colliding;
   - maps that don't show every named place;
   - a stamp covering the action.
4. Render once, then send the MP4 with its duration and scene start times.
5. About 140 spoken words is one minute. If it runs long, tighten or cut lines; never speed up the voice without asking.
6. Keep examples factually accurate, quote real translations and name them, and flag errors in the user's script before building.
7. Don't put classified material into a session. MARKING is for training-level content only.
