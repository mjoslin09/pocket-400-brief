# Pocket 400 market brief

`brief.json` is the daily market brief shown on the Brief tab of the Pocket 400 apps
(mjoslin09.github.io/pocket-400 and /pocket-400-classmates). A scheduled Claude routine rewrites it
each weekday morning by following [ROUTINE.md](ROUTINE.md), and `check_brief.py` validates it before
it is pushed. Served at https://mjoslin09.github.io/pocket-400-brief/brief.json.
