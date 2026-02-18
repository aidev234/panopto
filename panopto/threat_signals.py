"""Threat-indicator and selector parsing helpers."""

from __future__ import annotations

import re
from collections import OrderedDict
from typing import Any

# Telerecon assessment.py - capability/weapon proximity indicators.
CAPABILITY_ACTION_PHRASES: list[str] = [
    "my", "buy", "buying", "get", "getting", "got", "have", "acquire", "acquiring", "obtain", "obtaining",
    "procure", "procuring", "wanting", "want to", "want a", "going to", "own", "owning", "license", "a",
    "with", "certified", "need", "stolen", "steal a", "3d print", "3d-print", "3d printed", "3d-printed",
    "borrow", "take",
]

CAPABILITY_OBJECT_PHRASES: list[str] = [
    "gun", "rifle", "pistol", "knife", "shotgun", "revolver", "firearm", "firearms", "smg", "ar", "sawnoff",
    "sawn off", "sawn-off", "machine gun", "doublebarrel", "doublebarreled", "double-barrel", "double-barreled",
    "bolt-action", "lever-action", "lever action", "pump-action", "semi-automatic", "semiautomatic",
    "fully automatic", "ar-15", "ar15", "ak-47", "m4", "m16", "remington", "glock", "sig", "springfield",
    "ruger", "smith & wesson", "s&w", "m&p", "colt", "winchester", "benelli", "m&p15", "kel-tec", "ksg",
    "590", "870", "le6920", "ar-556", "g19", "85", "taurus", "629", ".85", ".45", ".22", "22", "9mm",
    "9 mm", ".30", "beretta", ".50", "50cal", "50 cal", "bushmaster", "m1911", "12 gauge", "12gauge",
    "12ga", "geissele", "chamber a round", "ammo", "ammunition", "caliber", "gauge", "magazine", "buck shot",
    "buckshot", "armor-piercing", "hollow point", "hollow points", "birdshot", "bird shot", "gun range",
    "rifle club", "shooting practice", "shooting range", "firearms training", "hunting", "duck shooting",
    "target shooting", "target practice", "scope", "silencer", "suppressor", "compensator", "stock", "barrel",
    "muzzle", "bipod", "firing pin", "optics", "crossbow", "compound bow", "pipe bomb", "pipebomb",
    "pipe-bomb", "pipebombs", "pipe-bombs", "grenade", "grenades", "ied", "improvised explosive device",
    "ball bearings", "molotov", "nitrate", "tnt", "landmine", "firebomb", "tannerite", "semtex", "fertilizer",
    "detonater", "detornaters", "nitroglycerin", "ammonium nitrate", "propellant", "thermalite", "thermite",
    "blasting cap", "det cord", "detcord", "boom stick", "fire bomb", "explosives", "kevlar", "body armour",
    "stab-proof vest", "stabproof vest",
]

VIOLENT_INTENT_PHRASES: list[str] = [
    "will kill", "to kill", "should kill", "fucking kill", "be killed", "get killed", "will murder", "to murder",
    "should murder", "fucking murder", "be murdered", "get murdered", "to shoot", "should shoot", "will shoot",
    "fucking shoot", "be shot", "get shot", "should stab", "will stab", "to stab", "fucking stab", "be stabbed",
    "get stabbed", "to rape", "will rape", "should rape", "get raped", "be raped", "execute them", "hang them",
    "should hang", "fucking head", "fucking neck", "fucking throat", "fucking skull", "be hanged",
    "be exterminated", "you to death", "him to death", "her to death", "them to death", "gut you", "gut him",
    "gut her", "gut them", "to gut", "rag doll", "ragdoll", "rag dolled", "ragdolled", "behead", "beheaded",
    "decapitate", "decapitated", "string them up", "string him up", "string her up", "strung up", "curb stomp",
    "curb stomped", "in the head", "in the neck", "in the throat", "by the neck", "by the throat", "lynch him",
    "lynch her", "lynch them", "to lynch", "lynched", "cable ties", "cabled tied", "hogtied", "hog tied",
    "hog tie", "hogtie", "cable tie", "in the face", "be strangled", "strangle her", "strangle him",
    "strangle them", "will strangle", "strangle you", "punch you", "punch him", "punch her", "gonna shoot",
    "gonna stab", "gonna kill", "gonna murder", "gonna execute", "gonna rape", "tar and feather", "double tap",
    "my fist", "and kill", "and shoot", "and stab", "and hang", "and lynch", "and murder", "and execute",
    "and rape", "and gut", "to attack", "should attack", "and attack", "fucking attack", "attack him",
    "attack her", "attack them", "take hostages", "take a hostage", "to exterminate", "should exterminate",
    "and exterminate", "fucking exterminate", "exterminate him", "exterminate her", "exterminate them",
    "to slaughter", "should slaughter", "and slaughter", "fucking slaughter", "slaughter him", "slaughter her",
    "slaughter them", "be slaughtered", "to die",
]

# Telerecon indicators.py - ideological indicator categories.
IDEOLOGICAL_CATEGORY_PHRASES: dict[str, list[str]] = {
    "Racism/Hate Speech": [
        "moslem", "mulatto", "sand nigger", "sandnig", "nigger", "mogger", "negroid", "jew", "kike", "zogbot",
        "chink", "paki", "mudslime", "mudshit", "femoid", "foid", "mongrel", "towelhead", "muzzies",
        "shit skin", "shitskin", "spics", "gooks", "rapefugees", "fag", "fags", "faggot", "faggots", "groomer",
        "groomers", "tranny", "trannys", "jewish", "gibsmedat", "goy", "soyboy", "soyboys",
    ],
    "Indicators - White Identity Motivated Extremism": [
        "white genocide", "cultural marxism", "the great replacement", "white race", "demographic replacement",
        "white lives matter", "white pride", "ethnostate", "hitler", "tarrant", "brevik", "white nationalist",
        "ethno-nationalist", "kebab removalist", "remove kebab", "aryan", "1488", "14-88", "14/88", "1788",
        "88/hh", "blood and soil", "race war now", "rahowa", "racial holy war", "fgrn", "gtkrwn", "iotbw",
        "jewish question", "accelerate", "accelerationist", "sieg heil", "siege pill", "white power", "goyim",
        "zyklon b", "14 words", "race traitor", "race traitors", "day of the rope", "waffen", "iron pill",
        "zog", "terrorgram", "national socialist", "national socialism", "khazarian", "ashkenazis", "tradwife",
        "tradthot", "cultural jihad", "pro western values", "western culture", "kek", "did nothing wrong",
        "its okay to be white", "it's okay to be white", "white is right", "pro-white activism", "coal burner",
        "6mwne", "holocauster", "holohoax", "clown world", "james mason", "accelerationism",
    ],
    "Indicators - Faith Motivated Extremism": [
        "jihad", "holy war", "apostate", "the apostates", "tyrants", "the crusader coalition",
        "soldiers of the caliphate", "lions of the islamic state", "in the shadow of the caliphate",
        "remaining and expanding", "encyclopedia of jihad", "mujahad", "rawafidh", "istishaadi",
        "baqiya wa tatamaddad", "al-tawaghit", "shariyah", "amaq agency", "al-hayat", "al-emarah", "dabiq",
    ],
    "Indicators - Conspiratorial Ideation": [
        "great awakening", "globalist", "globalists", "new world order", "wwg1wga", "the storm", "chemtrails",
        "freemasons", "illuminati", "deep state", "adrenochrome", "cabal", "rothschilds", "nuremberg",
        "nuremburg", "crimes against humanity", "great reset", "agenda 2030", "agenda 21", "world economic forum",
        "false flag", "microchipped", "microchips", "pizzagate", "sheeple", "geotus",
    ],
    "Indicators - Sovereign Citizen": [
        "sovereign citizen", "sovreign citizen", "free man", "free woman", "flesh and blood", "common law",
        "admiralty law", "non-resident alien", "14th amendment", "legal fiction", "affidavit of truth",
        "birth certificate bond", "non-domiciled resident", "natural law", "freeman passport",
        "constitutional sheriff", "nontaxpayer", "informed consent", "commercial redemption",
        "freemen standby act", "strawman", "man on the land", "in admiralty", "living soul", "letters of marque",
        "settlor", "quantum grammar", "magna carta", "maritime law", "policy officer", "postmaster",
        "artificial construct", "lawful dissent", "in the private", "living man", "living woman",
        "maxim of law", "uniform commercial code", "corpus juris", "sui juris",
    ],
    "Indicators - Involuntary Celibate": [
        "foid", "femoid", "dog pill", "dog pilled", "red pill", "red pilled", "going er", "truecel", "incel",
        "chad", "fakecel", "black pilled", "blackpilled", "ragefuel", "rape fuel", "ropefuel",
        "supreme gentleman", "elliot rodger", "braincels", "genetically inferior", "roasties", "smv",
        "sexual market value", "cucks", "manosphere", "incels", "mens rights activists", "mgtow",
        "men going their own way", "alpha male", "beta male", "omega male", "gamma male",
    ],
    "Indicators - Dehumanizing Rhetoric": [
        "parasite", "scum", "demon", "demonic", "soulless", "vermin", "parasites", "mongrel", "mongrels",
        "leeches", "leech", "maggot", "maggots", "sub-human",
    ],
}

THREAT_SIGNAL_SUBCATEGORY_CAPABILITY = "Possible Indicators of Capability"
THREAT_SIGNAL_SUBCATEGORY_VIOLENT_INTENT = "Possible Indicators of Violent Intent"

SELECTOR_PHRASES: list[str] = [
    "where i work", "where i live", "where i grew up", "my wife", "my husband", "my children", "my kids", "my kid",
    "my child", "my sibling", "my siblings", "my significant other", "my so", "my partner", "getting married",
    "getting engaged", "got married", "got engaged", "got divorced", "getting divorced", "my family", "my spouse",
    "my little ones", "my little one", "our children", "our kid", "our son", "our daughter", "my son", "my daughter",
    "my birthday", "born in", "my phone number", "my email", "my address", "my home address", "my house",
    "my school", "my university", "my job", "my profession", "work at", "new job", "job interview", "to school at",
    "to university at", "just visited", "went down to", "just visiting", "going down to", "went up to", "my hometown",
    "living in", "live in", "moved to", "my home", "my mother", "my father", "my stepmother", "my stepfather",
    "my grandchildren", "my grandchild", "my grandson", "my granddaughter", "my brother", "my sister", "my nephew",
    "my niece", "my uncle", "my aunty", "my parents",
]

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{6,}\d)(?!\w)")


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def _compile_phrase_pattern(phrase: str) -> re.Pattern[str]:
    escaped = re.escape(phrase)
    if re.search(r"\w", phrase):
        return re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE)
    return re.compile(escaped, re.IGNORECASE)


def _unique_preserve_order(items: list[str]) -> list[str]:
    return list(OrderedDict((item.lower(), item) for item in items if item).values())


def _find_phrase_matches(text: str, phrases: list[str]) -> list[str]:
    output: list[str] = []
    for phrase in phrases:
        pattern = _compile_phrase_pattern(phrase)
        if pattern.search(text):
            output.append(phrase)
    return _unique_preserve_order(output)


def _find_phrase_spans(text: str, phrases: list[str]) -> list[tuple[str, int, int]]:
    spans: list[tuple[str, int, int]] = []
    for phrase in phrases:
        pattern = _compile_phrase_pattern(phrase)
        for match in pattern.finditer(text):
            spans.append((phrase, match.start(), match.end()))
    return spans


def _word_gap_between_spans(text: str, span_a: tuple[int, int], span_b: tuple[int, int]) -> int:
    a_start, a_end = span_a
    b_start, b_end = span_b
    if a_end <= b_start:
        segment = text[a_end:b_start]
    elif b_end <= a_start:
        segment = text[b_end:a_start]
    else:
        return 0
    return len(re.findall(r"\b\w+\b", segment))


def _find_capability_proximity_matches(text: str, *, max_gap_words: int = 5) -> tuple[list[str], list[str]]:
    action_hits: list[str] = []
    object_hits: list[str] = []
    sentences = [segment for segment in re.split(r"(?<=[.!?])\s+", text) if segment.strip()]
    for sentence in sentences:
        action_spans = _find_phrase_spans(sentence, CAPABILITY_ACTION_PHRASES)
        object_spans = _find_phrase_spans(sentence, CAPABILITY_OBJECT_PHRASES)
        if not action_spans or not object_spans:
            continue
        for action_phrase, action_start, action_end in action_spans:
            for object_phrase, object_start, object_end in object_spans:
                gap = _word_gap_between_spans(sentence, (action_start, action_end), (object_start, object_end))
                if gap > max_gap_words:
                    continue
                action_hits.append(action_phrase)
                object_hits.append(object_phrase)

    return _unique_preserve_order(action_hits), _unique_preserve_order(object_hits)


def _extract_phones(text: str) -> list[str]:
    phones: list[str] = []
    for match in PHONE_RE.finditer(text):
        raw = match.group(0).strip()
        digits = re.sub(r"\D", "", raw)
        if len(digits) < 7 or len(digits) > 15:
            continue
        phones.append(raw)
    return _unique_preserve_order(phones)


def _extract_ideological_indicator_matches(text: str) -> tuple[list[str], list[str]]:
    categories: list[str] = []
    matches: list[str] = []
    for category, phrases in IDEOLOGICAL_CATEGORY_PHRASES.items():
        hits = _find_phrase_matches(text, phrases)
        if not hits:
            continue
        categories.append(category)
        matches.extend(hits)
    return _unique_preserve_order(categories), _unique_preserve_order(matches)


def extract_threat_and_selector_signals(text: str) -> dict[str, Any]:
    content = str(text or "")
    if not content.strip():
        return {
            "threat_matches": [],
            "threat_signal_matches": [],
            "selector_matches": [],
            "threat_categories": [],
            "threat_signal_categories": [],
            "ideological_matches": [],
            "emails": [],
            "phones": [],
        }

    threat_signal_matches: list[str] = []
    threat_signal_categories: list[str] = []

    capability_actions, capability_objects = _find_capability_proximity_matches(content)
    if capability_actions and capability_objects:
        threat_signal_categories.append(THREAT_SIGNAL_SUBCATEGORY_CAPABILITY)
        threat_signal_matches.extend(capability_actions)
        threat_signal_matches.extend(capability_objects)

    violent_matches = _find_phrase_matches(content, VIOLENT_INTENT_PHRASES)
    if violent_matches:
        threat_signal_categories.append(THREAT_SIGNAL_SUBCATEGORY_VIOLENT_INTENT)
        threat_signal_matches.extend(violent_matches)

    ideological_categories, ideological_matches = _extract_ideological_indicator_matches(content)

    selector_phrase_matches = _find_phrase_matches(content, SELECTOR_PHRASES)
    emails = _unique_preserve_order(EMAIL_RE.findall(content))
    phones = _extract_phones(content)
    selector_matches = _unique_preserve_order(selector_phrase_matches + emails + phones)

    threat_signal_matches = _unique_preserve_order(threat_signal_matches)
    return {
        # Backward-compatible name used by highlighting and threat-signal panel.
        "threat_matches": threat_signal_matches,
        "threat_signal_matches": threat_signal_matches,
        # Ideological categories for the "Ideological Indicators" panel.
        "threat_categories": ideological_categories,
        "threat_signal_categories": threat_signal_categories,
        "ideological_matches": ideological_matches,
        "selector_matches": selector_matches,
        "emails": emails,
        "phones": phones,
    }


def build_signal_tags(signal_payload: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    threat_signal_matches = signal_payload.get("threat_signal_matches")
    if threat_signal_matches is None:
        threat_signal_matches = signal_payload.get("threat_matches") or []
    selector_matches = signal_payload.get("selector_matches") or []
    ideological_categories = signal_payload.get("threat_categories") or []
    threat_signal_categories = signal_payload.get("threat_signal_categories") or []

    if threat_signal_matches:
        tags.extend(["threat:indicator", "indicator:match"])
    for category in threat_signal_categories:
        tags.append(f"threat:{_slugify(str(category))}")
        tags.append(f"indicator:{_slugify(str(category))}")
    for category in ideological_categories:
        tags.append(f"indicator:{_slugify(str(category))}")

    if selector_matches:
        tags.append("selector:match")
    if signal_payload.get("emails"):
        tags.append("selector:email")
    if signal_payload.get("phones"):
        tags.append("selector:phone")

    return _unique_preserve_order(tags)
