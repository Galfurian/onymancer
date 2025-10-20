#!/usr/bin/env python3
"""Command-line name generator for Onymancer.

This script provides a convenient way to generate fantasy names using various patterns.
Use --help to see all available options.
"""

import argparse
import sys

from onymancer import generate_batch, load_language_from_json

# Predefined patterns with descriptions
PREDEFINED_PATTERNS = {
    "simple": {
        "pattern": "s(dim)",
        "language": "default",
        "description": "Simple name with literal suffix",
        "example": "thor(dim)",
    },
    "fantasy": {
        "pattern": "!s!v!c",
        "language": "default",
        "description": "Classic fantasy name with capitalization",
        "example": "Elira",
    },
    "elven": {
        "pattern": "!s<v|l>!c!v",
        "language": "elvish",
        "description": "Elven-style name with liquid consonants",
        "example": "Lirael",
    },
    "dwarven": {
        "pattern": "!s!c!c<v|>",
        "language": "default",
        "description": "Dwarven name with hard consonants",
        "example": "Thrain",
    },
    "title": {
        "pattern": "!t !T",
        "language": "default",
        "description": "Random title",
        "example": "Master of The Mountains",
    },
    "place": {
        "pattern": "!s<v|c><ford|ham|ton|ville|burg>",
        "language": "default",
        "description": "Place name",
        "example": "Riverton",
    },
    "insult": {
        "pattern": "!i !s",
        "language": "default",
        "description": "Humorous insult",
        "example": "Bigheaded Thor",
    },
    "mushy": {
        "pattern": "!m !M",
        "language": "default",
        "description": "Affectionate term",
        "example": "Sweetie Pie",
    },
}


def load_custom_tokens(filepath: str) -> bool:
    """Load custom tokens from a JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        True if loaded successfully, False otherwise

    """
    try:
        success = load_language_from_json("custom", filepath)
        if success:
            print(f"✓ Loaded custom tokens from {filepath}")
        else:
            print(f"✗ Failed to load tokens from {filepath}")
        return success
    except Exception as e:
        print(f"✗ Error loading tokens: {e}")
        return False


def print_patterns() -> None:
    """
    Print all available predefined patterns.
    """
    print("Available predefined patterns:")
    print("-" * 50)
    for name, info in PREDEFINED_PATTERNS.items():
        print(f"{name:<15} {info['description']} (e.g., {info['example']})")
    print("\nUse --preset <name> to use a predefined pattern")


def main() -> None:
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Generate fantasy names using Onymancer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --pattern "!s!v!c" --count 5
  %(prog)s --preset fantasy --count 3 --seed 42
  %(prog)s --preset elven --language elvish --count 5 --min-length 4 --max-length 8
  %(prog)s --pattern "!s!v!c" --count 3 --starts-with "A" --ends-with "n" --contains "e"
  %(prog)s --list-patterns

Pattern Syntax:
  s: syllable    v: vowel    V: vowel combo    c: consonant
  B: begin cons  C: any cons i: insult         m: mushy name
  M: mushy end   D: dumb cons d: dumb syllable t: title begin
  T: title end   !: capitalize  (): literals   <>: groups
        """,
    )

    parser.add_argument(
        "-p",
        "--pattern",
        help="Pattern to use for name generation",
    )

    parser.add_argument(
        "--preset",
        choices=list(PREDEFINED_PATTERNS.keys()),
        help="Use a predefined pattern",
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="Number of names to generate (default: 1)",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=42,
        help="Seed for reproducible generation",
    )
    parser.add_argument(
        "-l",
        "--list-patterns",
        action="store_true",
        help="List available predefined patterns",
    )
    parser.add_argument(
        "-t",
        "--custom-tokens",
        help="Load custom tokens from JSON file",
    )
    parser.add_argument(
        "--language",
        default="default",
        choices=["default", "elvish"],
        help="Language token set to use (default: auto for presets, 'default' for custom patterns)",
    )
    parser.add_argument(
        "--min-length",
        type=int,
        help="Minimum length constraint for generated names",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum length constraint for generated names",
    )
    parser.add_argument(
        "--starts-with",
        help="String that generated names must start with",
    )
    parser.add_argument(
        "--ends-with",
        help="String that generated names must end with",
    )
    parser.add_argument(
        "--contains",
        help="String that generated names must contain",
    )

    args = parser.parse_args()

    # Handle custom tokens first
    if args.custom_tokens:
        if not load_custom_tokens(args.custom_tokens):
            sys.exit(1)

    # List patterns if requested
    if args.list_patterns:
        print_patterns()
        return

    if args.language not in ["default", "elvish"]:
        print(f"✗ Unknown language: {args.language}")
        sys.exit(1)

    # Determine pattern and language to use
    if args.preset and args.pattern:
        print("✗ Cannot use both --preset and --pattern")
        sys.exit(1)

    if not args.preset and not args.pattern:
        print("✗ Must specify either --pattern or --preset")
        print("Use --list-patterns to see available presets")
        sys.exit(1)

    if args.preset:
        args.pattern = PREDEFINED_PATTERNS[args.preset]["pattern"]
        args.language = PREDEFINED_PATTERNS[args.preset]["language"]

    # Generate names
    try:
        names = generate_batch(
            args.pattern,
            args.count,
            args.seed,
            args.language,
            args.min_length,
            args.max_length,
            args.starts_with,
            args.ends_with,
            args.contains,
        )

        print(
            f"Generated {args.count} name(s) "
            f"using pattern '{args.pattern}', language '{args.language}', "
            f"and seed '{args.seed}'."
        )

        print("\nNames:")
        for i, name in enumerate(names, 1):
            print(f"{i:2d}. {name}")

    except Exception as e:
        print(f"✗ Error generating names: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
