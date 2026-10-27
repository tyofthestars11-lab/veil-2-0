# Crimson Desert RPG — φ Edition

A desert RPG in pure Python + pygame. Wander the sands, dodge the cacti and ruins, and walk into the Dragon Lair — if you dare. The Cave Dragon is waiting, and the desert pays its victors in golden ratio.

Built from Tyree's engine, completed whole, with every input the desert offers: **keyboard, touch screen, and Bluetooth / Xbox controllers.**

## Run it

```bash
pip install -r requirements.txt
python crimson_desert_rpg.py
```

Start in GODMODE from the jump:

```bash
python crimson_desert_rpg.py --godmode
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

- **Explore** a procedurally seeded desert (seed 42 — the layout never changes) of cacti and ruined pillars.
- **The Dragon Lair** sits east, its floor carved with a golden spiral. Step in and the battle starts.
- **Battle**: ATTACK, SKILLS, ITEM (Potion, +40 HP, 3 carried), DEFEND (cuts the counter to a third).
- **Victory** pays 194 gold. **Defeat** — the desert keeps its secrets.

## GODMODE

Toggle it anywhere: **G**, the **GOD button**, or pad **Y**.

- The Dragon's counters are absorbed — no damage, ever.
- Your damage is multiplied by φ² ≈ 2.618.
- Potions never run out.
- The hero wears a gold aura so the desert knows.

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
| Dragon HP | 120 | 9.9488 | 120.000000 |
| Potion heal | 40 | 7.6658 | 40.000000 |
| Hero attack | 20 | 6.2254 | 20.000000 |
| Dragon attack | 18 | 6.0064 | 18.000000 |

Golden angle: 222.4922°. Every rung above was computed from source and round-trip checked: φ^rung returns x exactly.

---

*By Tyree Jones (tyofthestarz). All free, all phi.*
