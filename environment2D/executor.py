from environment2D.environment import Grid2D
from environment2D.parser import DSLParser
from typing import List
import pyparsing


def execute(program: str, env: Grid2D, colors, shapes,
            print_trace=False):
    parser = DSLParser(env.n, colors=colors, shapes=shapes)
    parsed_program = parser.parse_string(program)
    program_body = parsed_program[3]
    # print("program_body", program_body)
    _execute_block(env, program_body, print_trace)


def _execute_block(env: Grid2D, program: List, print_trace=False):
    assert type(program) != str, "Execution error"
    for block in program:
        # print("this block", block)
        if isinstance(block[0], pyparsing.ParseResults):
            # print("is list")
            for b in block:
                # print("b", b)
                _execute_block(env, [b], print_trace)
            continue
        if block[0] == "if":
            if print_trace:
                print(f"execute if condition {block[2]} "
                      f"= {_execute_cond(env, block[2])}")
            if _execute_cond(env, block[2]):
                # print("executing", block[5])
                _execute_block(env, [block[5]], print_trace)
        elif block[0] == "while":
            if print_trace:
                print(f"execute while condition {block[2]} = "
                      f"{_execute_cond(env, block[2])}")
            while _execute_cond(env, block[2]):
                # print("inside while")
                _execute_block(env, block[5], print_trace)
            # print("exit while")
        elif block[0] == "repeat":
            if print_trace:
                print(f"execute repeat {block[2]}")
            for i in range(int(block[2])):
                print("repeat ", i)
                _execute_block(env, block[5], print_trace)
        elif block[0] == "ifelse":
            if print_trace:
                print(f"execute ifelse condition {block[2]} == "
                      f"{_execute_cond(env, block[2])}")
            if _execute_cond(env, block[2]):
                # print("ifelse if branch")
                _execute_block(env, block[5], print_trace)
            else:
                # print("ifelse else branch")
                _execute_block(env, block[9], print_trace)
        else:
            _execute_action(env, block, print_trace)


def _execute_action(env: Grid2D, action: List[str], print_trace=False):
    if action[0] == "move(":
        env.move(int(action[1]), int(action[3]))
        if print_trace:
            print(f"performed move({int(action[1]), int(action[3])})")
    elif action[0] in ["moveUp()", "moveDown()",
                       "moveLeft()", "moveRight()",
                       "moveTop()", "moveBottom()",
                       "moveToMovableMarker()",
                       "moveLeftmost()", "moveRightmost()",
                       "pickMarker()", "putMarker()", "fixMarker()"]:
        env.__getattribute__(action[0][:-2])()
        assert len(action) == 2, f"unexpected parsing res {action}"
        if print_trace:
            print(f"perform action {action[0][:-2]}, arm loc {env.arm_loc}")
    else:
        raise AttributeError(f"Unknown action {action}")


def _execute_cond(env: Grid2D, condition):
    # print(condition)
    if isinstance(condition, str):
        if condition in ["markersPresent()", "movableMarkersPresent()",
                         "existMovableMarkers()",
                         "upperBoundary()", "lowerBoundary()",
                         "leftBoundary()", "rightBoundary()"]:
            return env.__getattribute__(condition[:-2])()
        else:
            raise AttributeError(f"unknown condition {condition}")
    if condition[0] == "not":
        return not _execute_cond(env, condition[1])
    assert condition[1] == "==", f"unrecognized condition {condition}"
    attribute1 = _get_attr(env, condition[0])
    attribute2 = _get_attr(env, condition[2])
    # print("attr1", attribute1, "attr2", attribute2, attribute1 == attribute2)
    return (attribute1 == attribute2)


def _get_attr(env: Grid2D, condition: str):
    if condition.startswith("get"):
        return env.__getattribute__(condition[:-2])()
    return condition


