# tokenmap.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) names mapped to classes.

Map token names found in a CQL query by the pattern.CQL_TOKENS pattern
to classes mostly defined in filters module.

The filters module has most of the classes representing CQL filters and
parameters.

The 'hhdb' filter is in the hhdb module because it represents a resource
external to CQL.

The base class for all the filters, the class representing the query, and
other classes representing shared behaviour of various sets of filters,
are in the structure module.

A few filters are in a module which would not be regarded as their proper
location because they reference other classes and functions in the body
of their code.

This module has the classes involved in expanding function definitions at
the point of function call.  These belong in the filters module but make
direct use of the class_from_token_name dict defined in this module.

"""
import re

from . import basenode
from . import filters
from . import hhdb
from . import structure
from . import cql

# This gives misleading information about variable name derivation but
# fits the pattern to detect 'function call' variable names.
# Defined in cql, rather than filters, module because it is referred
# to by the FunctionCallEnd class.
_function_call_variable_re = re.compile(r"(?P<variable>.*)")

# This gives misleading information about assign derivation but fits the
# pattern to assign actual parameters to instantiated fuunction formal
# parameters.
# Defined in cql, rather than filters, module because it is referred
# to by the FunctionCallEnd class.
_function_call_assign_re = re.compile(r"(?P<assign>)=")


class ReservedVariable(filters.Variable):
    """Represent the name of a reserved variable filter of various types.

    Variable names starting with a reserved string are allowed when
    representing function call arguments which are not variables.

    This class is in cql, rather than structure, module because it refers
    to class filters.Variable yet does not itself belong in
    filters.  The alternative is to put class Variable in structure
    module though it does not belong there.
    """

    def _raise_if_name_invalid(self, type_):
        """Raise NodeError if conditions are met.

        Reserved CQL variable names are allowed.

        """
        self._raise_if_characters_invalid(type_)


class FunctionCallEnd(filters.RightCompoundPlace):
    """Delegate then close FunctionCall and include function body.

    This class is in cql, rather than filters, module because it
    refers to class_from_token_name dict.

    """

    def place_node_in_tree(self):
        """Delegate then add function body to container cursor."""
        super().place_node_in_tree()
        container = self.container
        assert isinstance(container.cursor, filters.FunctionCall)
        if container.function_body_cursor is None:
            cursor = container.cursor
            formal = {}
            parameters = container.definitions[cursor.name].parameters
            cursor.completed = False
            body = container.definitions[container.cursor.name].body
            filters.BraceLeft(
                match_=body[0], container=container
            ).place_node_in_tree()
            for item, child in enumerate(cursor.children[:-1]):
                name = (
                    child.name if isinstance(child, structure.Name) else None
                )
                if name is not None:
                    # Associate actual function call argument variable name
                    # with formal variable name and remove it from function
                    # call children.
                    formal[parameters[item]] = name
                    cursor.children.pop(0)
                    continue
                formal[parameters[item]] = container.get_next_variable_id(
                    parameters[item]
                )
                # Add 'cql__*' variables at start of '{}' block.
                functioncall_variable = ReservedVariable(
                    match_=_function_call_variable_re.match(
                        formal[parameters[item]]
                    ),
                    container=container,
                )
                functioncall_variable.place_node_in_tree()
                filters.Assign(
                    match_=_function_call_assign_re.match("="),
                    container=container,
                ).place_node_in_tree()
                # Allocate the function call argument to the variable and
                # remove it from function call children.
                container.cursor.children.append(cursor.children.pop(0))
                container.cursor.children[-1].parent = container.cursor
            for token in body:
                classes = {
                    key: class_from_token_name[key]
                    # pylint R0801 duplicate code.  Ignored.
                    # See cql.CQL.place_node_in_tree().
                    # Shortening the 'raise_...' function name enough would
                    # remove the pylint report after black reformatting.
                    for key, value in token.groupdict().items()
                    if value is not None
                }
                structure.raise_if_not_single_match_groupdict_entry(
                    self, token, classes
                )
                for value in classes.values():
                    # Rename formal variable instances as they appear.
                    body_item = value(match_=token, container=container)
                    if isinstance(body_item, structure.Name):
                        if body_item.name in formal:
                            body_item.replace_formal_name(formal)
                    body_item.place_node_in_tree()
            filters.BraceRight(
                match_=body[-1], container=container
            ).place_node_in_tree()
            cursor.completed = True
            container.cursor = cursor


def parenthesis_right(match_=None, container=None):
    """Return ParenthesisRight or ConstituentParenthesisRight instance.

    This function is in cql, rather than filters, module because it
    refers to FunctionCallEnd class.

    """
    node = container.cursor
    while node:
        if node.complete():
            node = node.parent
            continue
        if isinstance(node, filters.ParenthesisLeft):
            return filters.ParenthesisRight(match_=match_, container=container)
        if isinstance(node, filters.ConstituentParenthesisLeft):
            return filters.ConstituentParenthesisRight(
                match_=match_, container=container
            )
        if isinstance(node, filters.LineConstituentParenthesisLeft):
            return filters.LineConstituentParenthesisRight(
                match_=match_, container=container
            )
        if isinstance(node, filters.FunctionCall):
            return FunctionCallEnd(match_=match_, container=container)
        if isinstance(node, structure.ParenthesizedArguments):
            return filters.ParenthesizedArgumentsEnd(
                match_=match_, container=container
            )
        if isinstance(node, filters.TargetParenthesisLeft):
            return filters.TargetConditionsEnd(
                match_=match_, container=container
            )
        if isinstance(node, filters.BraceLeft):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close a '{' compound filter with ')'"
            )
        if isinstance(node, filters.ConstituentBraceLeft):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close a '{' constituent filter with ')'"
            )
        if isinstance(node, filters.BracketLeft):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close a '[' string index with ')'"
            )
        node = node.parent
    raise basenode.NodeError(
        node.__class__.__name__
        + ": cannot find a '(' phrase to close with ')'"
    )


class_from_token_name = {
    "ascii": filters.ASCII,
    "abs": filters.Abs,
    "after_eq": filters.AfterEq,
    "after_ne": filters.AfterNE,
    "all": filters.All,
    "ancestor": filters.Ancestor,
    "and": filters.And,
    "anydirection": filters.anydirection,
    "any_square": filters.AnySquare,
    "anything_else": filters.AnythingElse,
    "keyword_anything_else": filters.AnythingElse,
    "arrow_backward": filters.arrow_backward,
    "arrow_forward": filters.ArrowForward,
    "assert": filters.Assert,
    "assign": filters.assign,
    "assign_divide": filters.AssignDivide,
    "assign_if": filters.AssignIf,
    "assign_minus": filters.AssignMinus,
    "assign_modulus": filters.AssignModulus,
    "assign_multiply": filters.AssignMultiply,
    "assign_plus": filters.AssignPlus,
    "atomic": filters.Atomic,
    "attack_arrow": filters.AttackArrow,
    "attacked_arrow": filters.AttackedArrow,
    "attackedby": filters.AttackedBy,
    "attacks": filters.Attacks,
    "btm": filters.BTM,
    "backslash": filters.Backslash,
    "before_eq": filters.BeforeEq,
    "before_ne": filters.BeforeNE,
    "between": filters.Between,
    "black": filters.Black,
    filters.BLOCK_COMMENT: filters.BlockComment,
    "brace_left": filters.brace_left,
    filters.BRACE_RIGHT: filters.brace_right,
    "bracket_left": filters.bracket_left,
    filters.BRACKET_RIGHT: filters.bracket_right,
    "cql": cql.CQL,
    "capture": filters.Capture,
    "captures": filters.Captures,
    "captures_p": filters.Captures,
    "captures_l": filters.CapturesL,
    "captures_l_p": filters.CapturesL,
    "captures_l_br": filters.CapturesL,
    "captures_bl": filters.Captures,
    "captures_bl_p": filters.Captures,
    "captures_br": filters.Captures,
    "captures_blbr": filters.Captures,
    "captures_lr": filters.CapturesLR,
    "captures_lr_p": filters.CapturesLR,
    "captures_bl_r": filters.CapturesR,
    "captures_bl_r_p": filters.CapturesR,
    "captures_r": filters.CapturesR,
    "captures_r_p": filters.CapturesR,
    "castle": filters.castle,
    "check": filters.Check,
    "child_parentheses": filters.ChildParentheses,
    "child": filters.Child,
    "colon": filters.colon,
    "colortype": filters.ColorType,
    "comment": filters.comment,
    "comment_parentheses": filters.comment_parentheses,
    "comment_symbol": filters.CommentSymbol,
    "complement": filters.Complement,
    "connectedpawns": filters.ConnectedPawns,
    "consecutivemoves": filters.ConsecutiveMoves,
    "count": filters.Count,
    "countmoves": filters.CountMoves,
    "count_filter": filters.CountFilter,
    "currentmove": filters.CurrentMove,
    "currentposition": filters.CurrentPosition,
    "currenttransform": filters.CurrentTransform,
    "dark": filters.Dark,
    "date": filters.Date,
    "depth": filters.Depth,
    "descendant": filters.Descendant,
    "diagonal": filters.diagonal,
    "dictionary": filters.Dictionary,
    "distance": filters.Distance,
    "divide": filters.Divide,
    "doubledpawns": filters.DoubledPawns,
    "down": filters.down,
    "eco": filters.ECO,
    "echo": filters.Echo,
    "element": filters.Element,
    "elo": filters.Elo,
    "else": filters.Else,
    "empty_squares": filters.EmptySquares,
    "enpassant": filters.enpassant,
    "enpassantsquare": filters.enpassantsquare,
    filters.END_OF_LINE: filters.end_of_line,
    filters.END_OF_STREAM: filters.end_of_stream,
    "eq": filters.Eq,
    "event": filters.Event,
    "eventdate": filters.EventDate,
    "fen": filters.FEN,
    "false": filters.False_,
    "file": filters.File,
    "find": filters.Find,
    "firstmatch": filters.FirstMatch,
    "flip": filters.Flip,
    "flipcolor": filters.FlipColor,
    "fliphorizontal": filters.FlipHorizontal,
    "flipvertical": filters.FlipVertical,
    "focus_capture": filters.FocusCapture,
    "focus": filters.Focus,
    "existential_square_variable": filters.ExistentialSquareIterator,
    "existential_piece_variable": filters.ExistentialPieceIterator,
    "universal_square_variable": filters.UniversalSquareIterator,
    "universal_piece_variable": filters.UniversalPieceIterator,
    "from": filters.from_,
    "function": filters.Function,
    "function_call": filters.function_call,
    "ge": filters.GE,
    "gt": filters.GT,
    "gamenumber": filters.GameNumber,
    "hhdb": hhdb.hhdb_not_implemented,  # hhdb.HHDB,
    "hascomment": filters.OriginalComment,
    "horizontal": filters.horizontal,
    "idealmate": filters.IdealMate,
    "idealstalemate": filters.IdealStaleMate,
    "if": filters.If,
    "in": filters.in_,
    "in_all": filters.InAll,
    "indexof": filters.IndexOf,
    "initial": filters.Initial,
    "initialposition": filters.InitialPosition,
    "int": filters.Int,
    "integer": filters.integer,
    "intersection": filters.Intersection,
    "isbound": filters.IsBound,
    "isunbound": filters.IsUnbound,
    "isolatedpawns": filters.IsolatedPawns,
    "keepallbest": filters.KeepAllBest,
    "lca": filters.LCA,
    "le": filters.LE,
    "lt": filters.LT,
    "lastgamenumber": filters.LastGameNumber,
    "lastposition": filters.LastPosition,
    "left": filters.left,
    "legal": filters.legal,
    "light": filters.Light,
    "line": filters.Line,
    filters.LINE_COMMENT: filters.line_comment,
    "local": filters.Local,
    "loop": filters.Loop,
    "lowercase": filters.LowerCase,
    "maindiagonal": filters.main_diagonal,
    "mainline": filters.mainline,
    "makesquare_parentheses": filters.MakeSquareParentheses,
    "makesquare_string": filters.MakeSquareString,
    "mate": filters.Mate,
    "max": filters.max_,
    "max_parameter": filters.MaxParameter,
    "message": filters.Message,
    "message_parentheses": filters.MessageParentheses,
    "min": filters.min_,
    "minus": filters.minus,
    "modelmate": filters.ModelMate,
    "modelstalemate": filters.ModelStalemate,
    "modulus": filters.Modulus,
    "move": filters.Move,
    "movenumber": filters.MoveNumber,
    "ne": filters.NE,
    "nestban": filters.NestBan,
    "notransform": filters.NoTransform,
    "northeast": filters.northeast,
    "northwest": filters.northwest,
    "not": filters.Not,
    "null": filters.Null,
    "nullmove": filters.NullMove,
    "oo": filters.o_o,
    "ooo": filters.o_o_o,
    "offdiagonal": filters.off_diagonal,
    "or": filters.Or,
    "originalcomment": filters.OriginalComment,
    "orthogonal": filters.orthogonal,
    "parent": filters.Parent,
    "parenthesis_left": filters.parenthesis_left,
    filters.PARENTHESIS_RIGHT: parenthesis_right,
    "passedpawns": filters.PassedPawns,
    "path": filters.Path,
    "pathcount": filters.PathCount,
    "pathcountunfocused": filters.PathCountUnfocused,
    "pathlastposition": filters.PathLastPosition,
    "pathstart": filters.PathStart,
    "persistent": filters.Persistent,
    "persistent_quiet": filters.PersistentQuiet,
    "piece": filters.piece,
    "piece_variable": filters.PieceVariable,
    "piece_designator": filters.PieceDesignator,
    "pieceid": filters.PieceId,
    "piecename": filters.PieceName,
    "piecepath": filters.PiecePath,
    "pin": filters.Pin,
    "player": filters.Player,
    "plus": filters.plus,
    "ply": filters.Ply,
    "position": filters.Position,
    "positionid": filters.PositionId,
    "power": filters.Power,
    "previous": filters.Previous,
    "primary": filters.primary,
    "promote": filters.Promote,
    "pseudolegal": filters.pseudolegal,
    "puremate": filters.PureMate,
    "purestalemate": filters.PureStalemate,
    "quiet": filters.Quiet,
    "rank": filters.Rank,
    "ray": filters.Ray,
    "readfile": filters.ReadFile,
    "regex_match": filters.RegexMatch,
    "regex_captured_group": filters.RegexCapturedGroup,
    "regex_captured_group_index": filters.RegexCapturedGroupIndex,
    "regex_repeat": filters.regex_repeat,
    "removecomment": filters.RemoveComment,
    "repeat_0_or_1": filters.RepeatZeroOrOne,
    "result": filters.Result,
    "result_argument": filters.ResultArgument,
    "reversecolor": filters.ReverseColor,
    "right": filters.right,
    "rotate45": filters.Rotate45,
    "rotate90": filters.Rotate90,
    "sqrt": filters.Sqrt,
    "secondary": filters.secondary,
    "settag": filters.SetTag,
    "shift": filters.Shift,
    "shifthorizontal": filters.ShiftHorizontal,
    "shiftvertical": filters.ShiftVertical,
    "sidetomove": filters.SideToMove,
    "singlecolor": filters.SingleColor,
    "single_move": filters.SingleMove,
    "single_move_p": filters.SingleMove,
    "single_move_l": filters.SingleMoveL,
    "single_move_l_p": filters.SingleMoveL,
    "single_move_l_br": filters.SingleMoveL,
    "single_move_bl": filters.SingleMove,
    "single_move_bl_p": filters.SingleMove,
    "single_move_br": filters.SingleMove,
    "single_move_blbr": filters.SingleMove,
    "single_move_lr": filters.SingleMoveLR,
    "single_move_lr_p": filters.SingleMoveLR,
    "single_move_bl_r": filters.SingleMoveR,
    "single_move_bl_r_p": filters.SingleMoveR,
    "single_move_r": filters.SingleMoveR,
    "single_move_r_p": filters.SingleMoveR,
    "site": filters.Site,
    "sort": filters.sort,
    "southeast": filters.southeast,
    "southwest": filters.southwest,
    "square": filters.square,
    "stalemate": filters.Stalemate,
    "star": filters.star,
    "str_parentheses": filters.StrParentheses,
    "str": filters.Str,
    "string": filters.string,
    "tag": filters.Tag,
    "terminal": filters.Terminal,
    "then": filters.Then,
    "through": filters.Through,
    "title": filters.Title,
    "to": filters.to,
    "true": filters.True_,
    "try": filters.Try,
    "type": filters.Type,
    "typename": filters.TypeName,
    "unbind": filters.Unbind,
    "union": filters.Union,
    "up": filters.Up,
    "uppercase": filters.UpperCase,
    "variable": filters.variable,
    "variable_assign": filters.variable_assign,
    "variation": filters.variation,
    "verbose": filters.Verbose,
    "vertical": filters.vertical,
    "virtualmainline": filters.VirtualMainLine,
    "wtm": filters.WTM,
    "while": filters.While,
    "white": filters.White,
    filters.WHITESPACE: filters.WhiteSpace,
    "wildcard_plus": filters.WildcardPlus,
    "wildcard_star": filters.WildcardStar,
    "writefile": filters.WriteFile,
    "xray": filters.XRay,
    "year": filters.Year,
}
