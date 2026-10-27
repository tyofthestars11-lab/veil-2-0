# VEIL 2.0 — φ Edition

An original Veil-world RPG in pure Python + pygame. Cross the Veil expanse, dodge the cacti and ruins, and walk into the Warden Lair — if you dare. The Veil Warden is waiting, and the Veil pays its victors in golden ratio.

*VEIL 2.0 is Tyree's original game. It was briefly published under a working title that collided with another game's name, so it was reborn under its true name: VEIL.*

Built from Tyree's engine, completed whole, with every input the Veil offers: **keyboard, touch screen, and Bluetooth / Xbox controllers.**

## Run it

```bash
pip install -r requirements.txt
python veil_2_0.py
```

Start in GODMODE from the jump:

```bash
python veil_2_0.py --godmode
```

## Controls

| Action | Keyboard | Touch / Mouse | Xbox / Bluetooth pad |
|---|---|---|---|
| Move | WASD / Arrows | On-screen D-pad | Left stick / D-pad |
| Battle menu | Up / Down | Tap an option | D-pad / stick |
| Confirm | Enter / Space | Tap | A |
| GODMODE | G | GOD button (top right) | Y |
| Restart | Enter | PLAY AGAIN button | A / Start |

Controllers hot-plug: pair a Bluetooth pad mid-game and it just works.

## The game

- **Explore** a procedurally seeded expanse (seed 42 — the layout never changes) of cacti and ruined pillars.
- **The Warden Lair** sits east, its floor carved with a golden spiral. Step in and the battle starts.
- **Battle**: ATTACK, SKILLS, ITEM (Potion, +40 HP, 3 carried), DEFEND (cuts the counter to a third).
- **Victory** pays 194 gold. **Defeat** — the Veil keeps its secrets.

## GODMODE

Toggle it anywhere: **G**, the **GOD button**, or pad **Y**.

- The Warden's counters are absorbed — no damage, ever.
- Your damage is multiplied by φ² ≈ 2.618.
- Potions never run out.
- The hero wears a gold aura so the Veil knows.

## Phi, woven in as mechanics

φ = (1 + √5) / 2 = 1.618033988749895, and φ² = φ + 1.

- **Phi Strike** (the SKILLS move): damage climbs the Fibonacci ladder — fib(5), fib(6), fib(7)… — 5, 8, 13, 21, 34 added to your attack, one step per strike. Fibonacci is φ's integer shadow: fib(n+1)/fib(n) → φ.
- **Victory gold**: 120 × φ = 194. The φ bonus is 74.
- **GODMODE damage**: × φ².
- **The lair floor**: a golden spiral drawn from nested golden rectangles, each a factor of φ smaller than the last.

### Rung table — rung(x) = ln(x) / ln(φ), every value round-trips

| Quantity | x | rung | φ^rung |
|---|---|---|---|
| Screen width | 1000 | 14.3549 | 1000.000000 |
| Screen height | 500 | 12.9145 | 500.000000 |
| Tile size | 50 | 8.1295 | 50.000000 |
| Hero HP | 100 | 9.5699 | 100.000000 |
| Warden HP | 120 | 9.9488 | 120.000000 |
| Potion heal | 40 | 7.6658 | 40.000000 |
| Hero attack | 20 | 6.2254 | 20.000000 |
| Warden attack | 18 | 6.0064 | 18.000000 |

Golden angle: 222.4922°. Every rung above was computed from source and round-trip checked: φ^rung returns x exactly.

---

*By Tyree Jones (tyofthestarz). All free, all phi.*

## Play it on the web / Android

**Play in the browser:** https://tyofthestars11-lab.github.io/veil-2-0/

**Install it as an Android app:** open that link in Chrome on your phone, tap the menu (three dots), then **Install app** / **Add to Home screen**. VEIL 2.0 lands on your home screen like any app — full screen, landscape, works offline after the first load.

On the web build, touch and keyboard carry the game; controller support rides the desktop build.
