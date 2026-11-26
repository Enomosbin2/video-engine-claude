# Hand-coded scenes (reference only)

These made the Sun Tzu and Clausewitz study videos before the script engine existed. They show how bespoke scenes are drawn: the concubine drill, the Midway intercept, Spiderweb, the Kyiv column, Napoleon's shrinking army and so on.

They use the old one-off modules and do not run on their own. To reuse an idea, copy the drawing code into a function in `vengine/customs.py`, register it, and call it from a script with `[custom: name]`. The drawing primitives they use (`ship`, `tank`, `drone`, `soldier`, `person`, `explosion`, `fire`, `panel`, `stamp`, `quote_box` ...) are all in `vengine/core.py`.
