"""Tests for name generator."""


import json
import tempfile
import os

from onymancer import generate, generate_batch, load_language_from_json, set_token, set_tokens


def test_generate_simple() -> None:
    """Test simple name generation."""
    name = generate("s", seed=42)
    assert isinstance(name, str)
    assert len(name) > 0


def test_generate_with_literal() -> None:
    """Test generation with literals."""
    name = generate("s(dim)", seed=42)
    assert "dim" in name


def test_generate_with_capitalization() -> None:
    """Test generation with capitalization."""
    name = generate("!s", seed=42)
    assert name[0].isupper()


def test_generate_with_groups() -> None:
    """Test generation with groups."""
    name = generate("<s|v>", seed=42)
    assert isinstance(name, str)


def test_generate_empty_pattern() -> None:
    """Test generation with empty pattern."""
    name = generate("", seed=42)
    assert name == ""


def test_set_token() -> None:
    """Test setting a token."""
    set_token("x", ["test"])
    name = generate("x", seed=42)
    assert name == "test"


def test_set_tokens() -> None:
    """Test setting multiple tokens."""
    tokens = {"y": ["hello"], "z": ["world"]}
    set_tokens(tokens)
    name1 = generate("y", seed=42)
    name2 = generate("z", seed=42)
    assert name1 == "hello"
    assert name2 == "world"


def test_generate_reproducibility() -> None:
    """Test that same seed produces same result."""
    name1 = generate("s!v", seed=123)
    name2 = generate("s!v", seed=123)
    assert name1 == name2


def test_generate_complex_pattern() -> None:
    """Test complex pattern generation."""
    pattern = "!s<v|c>!C"
    name = generate(pattern, seed=456)
    assert isinstance(name, str)
    assert len(name) > 0


def test_generate_batch_basic() -> None:
    """Test basic batch generation."""
    names = generate_batch("s", count=3, seed=42)
    assert isinstance(names, list)
    assert len(names) == 3
    for name in names:
        assert isinstance(name, str)
        assert len(name) > 0


def test_generate_batch_reproducibility() -> None:
    """Test batch generation reproducibility with seed."""
    names1 = generate_batch("s!v", count=5, seed=123)
    names2 = generate_batch("s!v", count=5, seed=123)
    assert names1 == names2


def test_generate_batch_no_seed() -> None:
    """Test batch generation without seed."""
    names = generate_batch("s", count=2)
    assert len(names) == 2
    for name in names:
        assert isinstance(name, str)


def test_generate_batch_count_zero() -> None:
    """Test batch generation with count 0."""
    names = generate_batch("s", count=0, seed=42)
    assert names == []


def test_generate_elvish() -> None:
    """Test generation with Elvish language."""
    name = generate("s!v!c", seed=42, language="elvish")
    assert isinstance(name, str)
    assert len(name) > 0
    # Elvish names should contain more liquid consonants
    assert any(char in name.lower() for char in "lr")


def test_generate_elvish_batch() -> None:
    """Test batch generation with Elvish language."""
    names = generate_batch("s!v", count=3, seed=123, language="elvish")
    assert len(names) == 3
    for name in names:
        assert isinstance(name, str)
        assert len(name) > 0


def test_generate_default_language() -> None:
    """Test that default language works."""
    name1 = generate("s", seed=42, language="default")
    name2 = generate("s", seed=42)  # Should be same as default
    assert name1 == name2


def test_generate_unknown_language() -> None:
    """Test generation with unknown language falls back to default."""
    name = generate("s", seed=42, language="unknown")
    assert isinstance(name, str)
    assert len(name) > 0


def test_load_language_from_json() -> None:
    """Test loading a custom language from JSON."""
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"s": ["test"]}, f)
        temp_file = f.name
    
    try:
        success = load_language_from_json("test_lang", temp_file)
        assert success
        name = generate("s", seed=42, language="test_lang")
        assert name == "test"
    finally:
        os.unlink(temp_file)


def test_load_language_from_json_invalid() -> None:
    """Test loading invalid JSON for language."""
    result = load_language_from_json("test", "nonexistent.json")
    assert result is False
