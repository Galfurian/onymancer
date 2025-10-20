"""Fantasy name generator module."""

from dataclasses import dataclass, field
import json
import random

# Global token map
_token_map: dict[str, list[str]] = {}


# Default tokens
_default_tokens = {
    "s": [
        "ach",
        "ack",
        "ad",
        "age",
        "ald",
        "ale",
        "an",
        "ang",
        "ar",
        "ard",
        "as",
        "ash",
        "at",
        "ath",
        "augh",
        "aw",
        "ban",
        "bel",
        "bur",
        "cer",
        "cha",
        "che",
        "dan",
        "dar",
        "del",
        "den",
        "dra",
        "dyn",
        "ech",
        "eld",
        "elm",
        "em",
        "en",
        "end",
        "eng",
        "enth",
        "er",
        "ess",
        "est",
        "et",
        "gar",
        "gha",
        "hat",
        "hin",
        "hon",
        "ia",
        "ight",
        "ild",
        "im",
        "ina",
        "ine",
        "ing",
        "ir",
        "is",
        "iss",
        "it",
        "kal",
        "kel",
        "kim",
        "kin",
        "ler",
        "lor",
        "lye",
        "mor",
        "mos",
        "nal",
        "ny",
        "nys",
        "old",
        "om",
        "on",
        "or",
        "orm",
        "os",
        "ough",
        "per",
        "pol",
        "qua",
        "que",
        "rad",
        "rak",
        "ran",
        "ray",
        "ril",
        "ris",
        "rod",
        "roth",
        "ryn",
        "sam",
        "say",
        "ser",
        "shy",
        "skel",
        "sul",
        "tai",
        "tan",
        "tas",
        "ter",
        "tim",
        "tin",
        "tor",
        "tur",
        "um",
        "und",
        "unt",
        "urn",
        "usk",
        "ust",
        "ver",
        "ves",
        "vor",
        "war",
        "wor",
        "yer",
    ],
    "v": ["a", "e", "i", "o", "u", "y"],
    "V": [
        "a",
        "e",
        "i",
        "o",
        "u",
        "y",
        "ae",
        "ai",
        "au",
        "ay",
        "ea",
        "ee",
        "ei",
        "eu",
        "ey",
        "ia",
        "ie",
        "oe",
        "oi",
        "oo",
        "ou",
        "ui",
    ],
    "c": [
        "b",
        "c",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "m",
        "n",
        "p",
        "q",
        "r",
        "s",
        "t",
        "v",
        "w",
        "x",
        "y",
        "z",
    ],
    "B": [
        "b",
        "bl",
        "br",
        "c",
        "ch",
        "chr",
        "cl",
        "cr",
        "d",
        "dr",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "ll",
        "m",
        "n",
        "p",
        "ph",
        "qu",
        "r",
        "rh",
        "s",
        "sch",
        "sh",
        "sl",
        "sm",
        "sn",
        "st",
        "str",
        "sw",
        "t",
        "th",
        "thr",
        "tr",
        "v",
        "w",
        "wh",
        "y",
        "z",
        "zh",
    ],
    "C": [
        "b",
        "c",
        "ch",
        "ck",
        "d",
        "f",
        "g",
        "gh",
        "h",
        "k",
        "l",
        "ld",
        "ll",
        "lt",
        "m",
        "n",
        "nd",
        "nn",
        "nt",
        "p",
        "ph",
        "q",
        "r",
        "rd",
        "rr",
        "rt",
        "s",
        "sh",
        "ss",
        "st",
        "t",
        "th",
        "v",
        "w",
        "y",
        "z",
    ],
    "i": [
        "big",
        "black",
        "blind",
        "bloody",
        "brave",
        "broken",
        "cold",
        "coward",
        "cowardly",
        "cunning",
        "daft",
        "dead",
        "deadly",
        "deaf",
        "dreadful",
        "evil",
        "false",
        "foul",
        "frightful",
        "ghastly",
        "grim",
        "grisly",
        "gullible",
        "hateful",
        "hearty",
        "horrible",
        "idiotic",
        "ignorant",
        "lame",
        "large",
        "lazy",
        "little",
        "lively",
        "loathsome",
        "long",
        "loud",
        "mad",
        "meek",
        "mighty",
        "miserable",
        "moronic",
        "naughty",
        "naive",
        "nimble",
        "noble",
        "old",
        "old",
        "pale",
        "petite",
        "plain",
        "poor",
        "quick",
        "quiet",
        "rash",
        "red",
        "rotten",
        "rude",
        "silly",
        "small",
        "stupid",
        "swift",
        "tall",
        "tame",
        "terrible",
        "thin",
        "tiny",
        "tough",
        "ugly",
        "vile",
        "wicked",
        "wise",
        "young",
    ],
    "m": [
        "baby",
        "dear",
        "darling",
        "love",
        "lover",
        "dearest",
        "sweet",
        "sweetie",
        "sugar",
    ],
    "M": ["boo", "kins", "pie", "poo", "tum", "ums"],
    "D": [
        "b",
        "bl",
        "br",
        "cl",
        "d",
        "f",
        "fl",
        "fr",
        "g",
        "gh",
        "gl",
        "gr",
        "h",
        "j",
        "k",
        "kl",
        "m",
        "n",
        "p",
        "th",
        "w",
    ],
    "d": [
        "el",
        "al",
        "an",
        "ar",
        "cha",
        "co",
        "el",
        "er",
        "he",
        "hi",
        "is",
        "or",
        "son",
        "ther",
        "y",
    ],
    "t": [
        "Master of",
        "Ruler of",
        "Teacher of",
        "Conqueror of",
        "Lord of",
        "Guardian of",
        "Keeper of",
        "Seeker of",
        "Bringer of",
        "Bearer of",
        "Defender of",
        "Slayer of",
        "Hunter of",
        "Watcher of",
        "Follower of",
    ],
    "T": [
        "the Endless",
        "the Sea",
        "the Fiery Pit",
        "the Mountains",
        "the Forest",
        "the Plains",
        "the Desert",
        "the Storm",
        "the Night",
        "the Day",
        "the Shadows",
        "the Light",
        "the Dark",
        "the Ancient",
        "the Forgotten",
        "the Lost",
        "the Hidden",
        "the Eternal",
        "the Mighty",
    ],
}


# Initialize with default tokens
_token_map.update(_default_tokens)


@dataclass
class _OptionT:
    """
    Struct that encapsulates all the state options.

    Attributes:
        capitalize (bool):
            Whether to capitalize the next character.
        emit_literal (bool):
            Whether to emit characters as literals.
        inside_group (bool):
            Whether currently inside a group.
        seed (int):
            The current seed for random generation.
        current_option (str):
            The current option being built.
        options (list[str]):
            The list of options in the current group.
    """

    capitalize: bool = field(
        default=False,
        metadata={"description": "Whether to capitalize the next character."},
    )
    emit_literal: bool = field(
        default=False,
        metadata={"description": "Whether to emit characters as literals."},
    )
    inside_group: bool = field(
        default=False, metadata={"description": "Whether currently inside a group."}
    )
    current_option: str = field(
        default="", metadata={"description": "The current option being built."}
    )
    options: list[str] = field(
        default_factory=list,
        metadata={"description": "The list of options in the current group."},
    )


def _capitalize_and_clear(options: _OptionT, character: str) -> str:
    """
    Capitalize the given character if capitalize is True.

    Args:
        options:
            The current state options.
        character:
            The input character.

    Returns:
        str:
            The capitalized character if capitalize is True, else the original.

    """
    if options.capitalize:
        options.capitalize = False
        return character.upper()
    return character


def _process_token(options: _OptionT, buffer: list[str], key: str) -> bool:
    """
    Process a token based on the provided key and append it to the buffer.

    Args:
        options:
            The current state options.
        buffer:
            The string buffer where the processed token will be appended.
        key:
            The key representing the type of token to process.

    Returns:
        bool:
            True on success, False otherwise.

    """
    tokens = _token_map.get(key, [])
    if not tokens:
        buffer.append(_capitalize_and_clear(options, key))
    else:
        token = random.choice(tokens)
        it = iter(token)
        first_char = next(it, "")
        buffer.append(_capitalize_and_clear(options, first_char))
        buffer.extend(it)
    return True


def _process_character(
    options: _OptionT,
    buffer: list[str],
    character: str,
) -> bool:
    """
    Process a character from the pattern and append it to the buffer.

    Args:
        options:
            The current state options.
        buffer:
            The string buffer where the processed character will be appended.
        character:
            The character to process.

    Returns:
        bool:
            True on success, False otherwise.

    """
    if character == "(":
        if options.inside_group:
            options.current_option += character
        else:
            options.emit_literal = True
    elif character == ")":
        if options.inside_group:
            options.current_option += character
        else:
            options.emit_literal = False
    elif character == "<":
        options.inside_group = True
        options.options.clear()
        options.current_option = ""
    elif character == "|":
        options.options.append(options.current_option)
        options.current_option = ""
    elif character == ">":
        options.inside_group = False
        options.options.append(options.current_option)
        options.current_option = ""
        # Ensure there's at least one option in the group.
        if not options.options:
            return False
        # Randomly pick an option.
        option = random.choice(options.options)
        # Process and append the selected option.
        for token in option:
            if not _process_character(options, buffer, token):
                return False
        # Clear options after processing the group.
        options.options.clear()
    elif character == "!":
        if options.inside_group:
            options.current_option += character
        else:
            options.capitalize = True
    elif options.inside_group:
        options.current_option += character
    elif options.emit_literal:
        buffer.append(_capitalize_and_clear(options, character))
    elif not _process_token(options, buffer, character):
        return False
    return True


def load_tokens_from_json(filename: str) -> bool:
    """
    Load tokens from a JSON file.

    Args:
        filename:
            The path to the JSON file containing the tokens.

    Returns:
        bool:
            True if the loading was successful, False otherwise.

    """
    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return False
        global _token_map
        _token_map.clear()
        _token_map.update(data)
        return True
    except (OSError, json.JSONDecodeError):
        return False


def set_token(key: str, tokens: list[str]) -> None:
    """
    Set the token list of a given key in the global token map.

    Args:
        key:
            The key for which to set the token list.
        tokens:
            The list of tokens (strings) to associate with the key.

    """
    _token_map[key] = tokens


def set_tokens(tokens: dict[str, list[str]]) -> None:
    """
    Set a given list of key-value pairs in the global token map.

    Args:
        tokens:
            A map where each key is a character and the value is a list of
            strings (tokens).

    """
    _token_map.update(tokens)


def generate(
    pattern: str,
    seed: int | None = None,
) -> str:
    """
    Generate a random name based on the provided pattern and seed.

    Args:
        pattern (str):
            The pattern defining the structure of the name.
        seed (int | None):
            The seed for random number generation.

    Returns:
        str:
            The generated name.

    """
    # If a seed is provided, seed the random generator.
    if seed is not None:
        random.seed(seed)
    options = _OptionT()
    buffer: list[str] = []
    for c in pattern:
        if not _process_character(options, buffer, c):
            return ""
    return "".join(buffer)


def generate_batch(
    pattern: str,
    count: int,
    seed: int | None = None,
) -> list[str]:
    """
    Generate multiple names using the given pattern.

    Args:
        pattern:
            The pattern to use for generation.
        count:
            Number of names to generate.
        seed:
            Optional seed for reproducibility. If provided, each name uses seed
            + i.

    Returns:
        list[str]:
            List of generated names.

    """
    # If a seed is provided, seed the random generator.
    if seed is not None:
        random.seed(seed)
    names = []
    for _ in range(count):
        # We already seeded the random generator above.
        names.append(generate(pattern, None))
    return names
