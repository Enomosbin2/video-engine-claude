from script import spoken as _sp
import re
def spoken(s):
    s = s.replace("500 BC", "five hundred B.C."); s = _sp(s)
    s = re.sub(r"\b(1[0-9]\d\d|20\d\d)\b", lambda m: yr(int(m.group(1))), s)
    return s
ONES = "zero one two three four five six seven eight nine".split()
TEENS = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
def two(n):
    if n < 10: return "oh " + ONES[n]
    if n < 20: return TEENS[n - 10]
    return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
def yr(y):
    if 2000 <= y < 2010: return "two thousand" + ("" if y == 2000 else " and " + ONES[y - 2000])
    if y >= 2010: return "twenty " + two(y - 2000)
    return two(y // 100) + " " + (two(y % 100) if y % 100 else "hundred")

SUNZI = [
 ("open", [
  "Around 500 BC, China was a land of rival kingdoms, almost always at war.",
  "In the southern state of Wu, a general named Sun Tzu offered his services to King Helü.",
  "The king tested him. Could he drill the palace women like soldiers?",
  "Sun Tzu formed two companies, with the king's two favourite concubines as captains. When he gave orders, the women laughed.",
  "He explained the orders again. They laughed again. So he had the two captains executed, appointed new ones, and gave the orders a third time. This time, they were obeyed perfectly.",
  "The book attributed to him, The Art of War, has thirteen short chapters. Two and a half thousand years later, armies still study it.",
 ]),
 ("p1", [
  "His most famous idea is the highest of all.",
  "\"Supreme excellence consists in breaking the enemy's resistance without fighting.\"",
  "He ranked the methods: first, balk the enemy's plans; next, break up his alliances; then attack his army; and worst of all, besiege his cities.",
  "In October 1962, the Soviet Union placed nuclear missiles in Cuba.",
  "President Kennedy did not invade. He ordered a naval quarantine, and bargained in secret. Within two weeks, the missiles went home, without a shot exchanged between the superpowers.",
  "In 2014, Russia took Crimea with unmarked troops, information operations and a staged referendum. Ukraine lost the peninsula almost without a fight.",
  "Winning without fighting works best when real force stands behind the threat.",
 ]),
 ("p2", [
  "\"All warfare is based on deception.\"",
  "\"When able to attack, we must seem unable. When we are near, we must make the enemy believe we are far away.\"",
  "In 1944, the Allies built a fake army in England, the First United States Army Group, with inflatable tanks, dummy landing craft and false radio traffic, all aimed at Calais.",
  "On the sixth of June, the real landings came in Normandy. Germany held its Fifteenth Army at Calais for weeks, waiting for an attack that never came.",
  "In September 2022, Ukraine openly prepared an offensive in the south, towards Kherson.",
  "Russia moved troops south. Then Ukraine struck in the north-east, at Kharkiv, and broke through.",
  "Today, deception also runs through code and screens: malware that shows normal readings while destroying machines, and deepfake videos of leaders.",
  "But satellites and open-source analysts now watch everything, so deception must be faster and more layered than ever.",
 ]),
 ("p3", [
  "\"If you know the enemy and know yourself, you need not fear the result of a hundred battles.\"",
  "\"If you know neither the enemy nor yourself, you will succumb in every battle.\"",
  "He insisted that this knowledge comes from people: spies and agents, not spirits or guesswork.",
  "In 1942, American codebreakers learned that Japan's next target was Midway. The US Navy laid an ambush, and sank four Japanese aircraft carriers.",
  "In 2022, Russia invaded Ukraine expecting Kyiv to fall in days.",
  "It misjudged Ukraine's will, and also its own army's logistics and morale. It knew neither the enemy nor itself.",
  "The hardest half of the principle is often the second: knowing yourself.",
 ]),
 ("p4", [
  "\"Military tactics are like unto water. Water runs away from high places and hastens downwards.\"",
  "\"So in war, the way is to avoid what is strong, and to strike at what is weak.\"",
  "Since 2023, the Houthis in Yemen have attacked shipping in the Red Sea with cheap drones and missiles.",
  "They never fight warships head on. They strike trade, and force navies to spend costly interceptors on cheap threats.",
  "In April 2022, Ukraine, with almost no navy, sank the Russian cruiser Moskva with missiles fired from the shore.",
  "Sea drones then pushed Russia's Black Sea Fleet away from Ukraine's coast.",
  "This is the logic of every weaker side: refuse the enemy's strength, and attack his weak points.",
 ]),
 ("p5", [
  "\"Rapidity is the essence of war: take advantage of the enemy's unreadiness, make your way by unexpected routes, and attack unguarded spots.\"",
  "On the first of June 2025, in Operation Spiderweb, Ukraine hid drones inside trucks deep in Russia, and struck strategic bombers at airbases thousands of kilometres from the front.",
  "Unexpected routes, unguarded spots, and complete surprise.",
  "But Sun Tzu also warned: \"There is no instance of a country having benefited from prolonged warfare.\"",
  "The war in Ukraine became a long war of shells, drones and factories, draining both sides.",
 ]),
 ("p6", [
  "For Sun Tzu, the commander stands for five virtues: wisdom, sincerity, benevolence, courage and strictness.",
  "And he preached restraint: \"Move not unless you see an advantage; use not your troops unless there is something to be gained; fight not unless the position is critical.\"",
  "In May 2025, India and Pakistan, two nuclear-armed states, exchanged strikes for four days, then stopped once each had shown its resolve.",
  "Restraint is not weakness. It is strategy.",
 ]),
 ("close", [
  "Sun Tzu's lessons endure.",
  "Win without fighting where you can.",
  "Deceive, and expect to be deceived.",
  "Know the enemy, and above all, know yourself.",
  "Avoid strength, and strike weakness.",
  "Move fast, and avoid long wars.",
  "He did not foresee nuclear weapons, the laws of war, or artificial intelligence. But his principles about people, judgement and economy still hold.",
  "As he wrote: \"The art of war is of vital importance to the State.\"",
 ]),
]

CLAUSE = [
 ("open", [
  "Carl von Clausewitz joined the Prussian army in 1792. He was twelve years old.",
  "In 1806, he watched Napoleon destroy the Prussian army at Jena and Auerstedt, and was taken prisoner.",
  "In 1812, rather than serve as Napoleon's ally, he joined the Russian army, and saw the French invasion of Russia collapse.",
  "In 1815, he fought again in the campaign that ended at Waterloo.",
  "He spent his last years directing Prussia's war college, writing a great book on war.",
  "He died of cholera in 1831, with the book unfinished. His widow, Marie, published it the next year. Its title: On War.",
 ]),
 ("p1", [
  "His most famous line:",
  "\"War is a mere continuation of policy by other means.\"",
  "War has no purpose of its own. It serves a political aim, and that aim decides how far it should go.",
  "In 1991, a coalition freed Kuwait from Iraq. After one hundred hours of ground war, it stopped. The aim was to free Kuwait, not to occupy Iraq.",
  "In 2003, a new invasion toppled Saddam Hussein in three weeks. But there was no clear policy for what came after, and an insurgency followed.",
  "Clausewitz warned that the first task of statesmen and generals is to understand what kind of war they are entering.",
 ]),
 ("p2", [
  "Clausewitz called war a \"wonderful trinity\".",
  "Passion: the violence, hatred and animosity of the people.",
  "Chance: the play of probability and courage, the realm of the commander and the army.",
  "And reason: war as an instrument of government policy.",
  "He compared war to an object suspended between three magnets, pulled one way, then another.",
  "In Vietnam, after the Tet Offensive of 1968, American public support collapsed, even though the army was winning battles. Passion broke away from reason.",
  "In June 2023, the Wagner group marched on Moscow against Russia's own defence ministry. The army and the government split apart.",
 ]),
 ("p3", [
  "\"Everything is very simple in War, but the simplest thing is difficult.\"",
  "Clausewitz called these accumulated difficulties friction: the force that separates real war from war on paper.",
  "Danger, exhaustion, weather, broken equipment, and human error, each small, all adding up.",
  "And uncertainty: \"A great part of the information obtained in War is contradictory, a still greater part is false.\"",
  "In February 2022, a Russian column about forty miles long stalled north of Kyiv. Fuel ran short, vehicles broke down, and Ukrainian units ambushed it.",
  "Drones and satellites now see more than ever. But jamming, information overload and deepfakes create new fog.",
  "Clausewitz's answer was the commander's judgement and determination. Today we call it mission command: subordinates acting on intent when the plan breaks.",
 ]),
 ("p4", [
  "Clausewitz described the centre of gravity: \"the centre of power and movement, on which everything depends.\"",
  "Against it, he argued, the whole weight of the attack should be directed.",
  "It might be an army, a capital, an alliance, or in a popular uprising, its leader and public opinion.",
  "In 1999, NATO bombed Serbian forces in Kosovo for weeks with little effect. Then it struck the power and industry around Belgrade, the real centre of Milošević's power. Within weeks, he gave in.",
  "In 2017, coalition forces retook Mosul and Raqqa. The Islamic State's territory was its centre of gravity, and its so-called caliphate collapsed.",
  "But in Iraq in 2003, the capital fell and the war went on. The real centre of gravity was the people's consent.",
 ]),
 ("p5", [
  "Clausewitz also warned of the culminating point: the moment when an attacker's strength is spent, and every further step makes him weaker.",
  "He had seen it himself. In 1812, Napoleon marched more than four hundred thousand men into Russia, and reached Moscow.",
  "But his supply lines stretched, winter came, and the retreat destroyed the Grande Armée. Only a fraction returned.",
  "For the same reason, he called defence the stronger form of war. The defender has time, terrain, and supplies close at hand.",
  "In 2022, Russia's drive on Kyiv passed its culminating point within weeks, and its forces withdrew from the north.",
 ]),
 ("close", [
  "Clausewitz's lessons endure.",
  "War serves policy, so know your aim.",
  "Keep passion, chance and reason in balance.",
  "Expect friction, and train leaders to overcome it.",
  "Find what truly holds the enemy together.",
  "And know when to stop.",
  "Two centuries on, On War remains the most studied book on the nature of war.",
 ]),
]
