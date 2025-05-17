# constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Constants used when parsing Chess Query Language (CQL) statements."""

# Patterns for piece, rank, and file, names in CQL.
PIECE_NAMES = r"QBRNKPAqbrnkpa_"
RANK_RANGE = r"1-8"
FILE_RANGE = r"a-h"

# Pattern for characters allowed in variable names.
VARIABLE_NAME_CHARS = r"[a-zA-Z0-9_$]"

# Pattern for quoted strings.
QUOTED_STRING = r'"[^\\"]*(?:\\.[^\\"]*)*"'

# File and rank names in CQL.
FILE_NAMES = "abcdefgh"  # Same as in pgn_read.core.constants module.
CQL_RANK_NAMES = "12345678"  # pgn_read.core.constants.RANK_NAMES reversed.

# Reserved prefixes for variable names.
UPPER_CASE_CQL_PREFIX = "__CQL"
LOWER_CASE_CQL_PREFIX = "cql__"

# Prefix for function body names.
# The actual arguments in a function call must form a valid function body
# when substituted for the parameter variables in the function definition.
# The first two characters of FUNCTION_BODY_PREFIX must not be characters
# allowed in variable names.
FUNCTION_BODY_PREFIX = "%%_body_"
assert (
    len([c for c in FUNCTION_BODY_PREFIX[:2] if c.isalnum() or c in "_$"]) == 0
)
