from environment2D.environment import Grid2D
from environment2D.parser import DSLParser
from typing import List
import pyparsing


def execute(program: str, env: Grid2D, colors, shapes):
    parser = DSLParser(env.n, colors=colors, shapes=shapes)
    parsed_program = parser.parse_string(program)
    program_body = parsed_program[3]
    # print("program_body", program_body)
    _execute_block(env, program_body)


def _execute_block(env: Grid2D, program: List):
    assert type(program) != str, "Execution error"
    for block in program:
        # print("this block", block)
        if isinstance(block[0], pyparsing.ParseResults):
            # print("is list")
            for b in block:
                # print("b", b)
                _execute_block(env, [b])
            continue
        if block[0] == "if":
            # print("execute if", "condi", block[2], "body", block[5])
            if _execute_cond(env, block[2]):
                # print("executing", block[5])
                _execute_block(env, [block[5]])
        elif block[0] == "while":
            # print("execute while", "condi", block)
            while _execute_cond(env, block[2]):
                # print("inside while")
                _execute_block(env, block[5])
            # print("exit while")
        elif block[0] == "repeat":
            # print("execute repeat")
            for i in range(int(block[2])):
                # print("repeat ", i)
                _execute_block(env, block[5])
        elif block[0] == "ifelse":
            # print("execute ifelse", block)
            if _execute_cond(env, block[2]):
                # print("ifelse if branch")
                _execute_block(env, block[5])
            else:
                # print("ifelse else branch")
                _execute_block(env, block[9])
        else:
            # print("execute action")
            _execute_action(env, block)


def _execute_action(env: Grid2D, action: List[str]):
    if action[0] == "move(":
        env.move(int(action[1]), int(action[3]))
        # print(action, "performed move")
    elif action[0] == "pickMarker()":
        env.pickMarker()
        # print("perform pickMarker")
    elif action[0] == "putMarker()":
        env.putMarker()
        # print("perform putMarker")
    else:
        raise AttributeError(f"Unknown action {action}")


def _execute_cond(env: Grid2D, condition):
    if condition[0] == "markersPresent()":
        return env.markersPresent()
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


if __name__ == "__main__":
    parser = DSLParser(10, ["red", "yellow"], ["round", "square"])
    # print(parser.parse_string("red yellow getMarkerColor() round"))
    straight_program = """
    def run(){
        if(not getMarkerColor() == red){
            move(1, 2);
            pickMarker();
            repeat(3){
                putMarker();
            }
        }
    }
    """
    env = Grid2D(10)
    execute(straight_program, env,
            colors=["red", "yellow"],
            shapes=["round", "square"])
    print(env)

    print("=============program 2===========")

    nested_program = """
    def run(){
        move(0, 0);
        putMarker();
        while(getMarkerColor() == red){
            pickMarker();
            ifelse(red == yellow){
               putMarker();
               move(1, 1);
            }
            else{
               move(2, 2);
            }
        }
        putMarker();
        move(0, 0);
    }
    """
    env.set_items("red", "round", [0, 0])
    execute(nested_program, env,
            colors=["red", "yellow"], shapes=["round", "square"])
    print(env)

