from random import randrange, choice
from .environment import Grid2D


class Generator:
    def __init__(self, n, colors, shapes, max_constant=5):
        self.n = n
        self.max_constant = max_constant
        self.colors_list = colors
        self.shapes_list = shapes
        self.actions_list = [["move(", "position_token", ",", "position_token", ")"],
                             "moveUp()", "moveDown()", "moveLeft()", "moveRight()",
                             "moveTop()", "moveBottom()",
                             "moveLeftmost()", "moveRightmost()",
                             "moveToMovableMarker()",
                             "pickMarker()", "putMarker()", "fixMarker()"]

        self.actions_move = ["moveUp()", "moveDown()", "moveLeft()", "moveRight()",
                             "moveTop()", "moveBottom()",
                             "moveLeftmost()", "moveRightmost()"]
        self.actions_empty = [["move(", "position_token", ",", "position_token", ")"],
                              "moveToMovableMarker()",
                              "pickMarker()", "fixMarker()"]

        self.conditions_list = [["getMarkerColor() ==", "color_token"],
                                ["getMarkerShape() ==", "shape_token"],
                                "markersPresent()", "movableMarkersPresent()",
                                "existMovableMarkers()",
                                "upperBoundary()", "lowerBoundary()",
                                "leftBoundary()", "rightBoundary()"]

        self.conditions_marker = [["getMarkerColor() ==", "color_token"],
                                  ["getMarkerShape() ==", "shape_token"], "true"]
        self.statements_list = \
            [["repeat(", "const_token", ")", "{", "stmt_token", "}"],
             ["stmt_token", "stmt_token"],
             ["action_token", ";"],
             ["if(", "condition_token", ")", "{", "stmt_token", "}"],
             ["ifelse(", "condition_token", ")", "{", "stmt_token", "}",
              "else", "{", "stmt_token", "}"]]

        self.holding = False

    def random_env(self):
        env = Grid2D(self.n)
        #random amount of objects
        for i in range(randrange(self.n)):
            pos = [randrange(self.n), randrange(self.n)]
            env.set_item(choice(self.colors_list), choice(self.shapes_list), pos)
        return env

    def random_program(self, stmt_max_depth, template=None):
        # task: bin sorting
        # start: while(existMovableMarkers()), repeat, moveToMovableMarker
        # in the while loop: if, ifelse, pick, move, check, place, fix
        body = self.random_tokens(template if template else 'start', stmt_max_depth)
        program = ['def', 'run()', '{', body, '}']
        return ' '.join(program)

    def random_tokens(self, start_token='stmt', depth=1):
        if "template" in start_token:
            tokens = self.__getattribute__(start_token)()
        elif start_token == 'stmt' and depth <= 1:
            tokens = ["action_token", ";"]
        else:
            tokens = self.__getattribute__("random_" + start_token)()

        if isinstance(tokens, list):
            for i in range(len(tokens)):
                if "_token" in tokens[i]:
                    rdtk = self.random_tokens(tokens[i][:-6], depth-1)
                    tokens[i] = rdtk
            tokens = ' '.join(tokens)
        return tokens

    def random_start(self):
        # move to movable marker
        # repeat
        start_tokens = [[self.actions_list[-4], ";", "stmt_token"]] + [self.statements_list[0]] * 4 + \
                       [["while", "(", "existMovableMarkers()", ")", "{", "stmt_token", "}"]*2]  # while
        start = choice(start_tokens)
        return start

    def random_stmt(self):
        return choice(self.statements_list)

    def random_action(self):
        return choice(self.actions_list)

    def random_move(self):
        return choice(self.actions_move)

    def random_move_set(self):
        moves = ["move_token", ";"] * randrange(3)
        return moves

    def random_condition(self):
        return choice(self.conditions_list)

    def random_marker_condition(self):
        return choice(self.conditions_marker)

    def random_const(self):
        return str(randrange(1, self.max_constant))

    def random_color(self):
        return choice(self.colors_list)

    def random_shape(self):
        return choice(self.shapes_list)

    def random_position(self):
        return str(randrange(0, self.n-1))

    @staticmethod
    def sort_template():
        template_while = ["while(existMovableMarkers()){",
                          "moveToMovableMarker();",
                          "ifelse(", "marker_condition_token", "){",
                          "pickMarker();", "move_set_token",
                          "while(markersPresent()){",
                          "move_token", ";", "}",
                          "putMarker();", "}",
                          "else{", "fixMarker();", "}", "}"]

        template_repeat = ["repeat(", "const_token", "){",
                           "moveToMovableMarker();",
                           "if(", "marker_condition_token", "){",
                           "pickMarker();",
                           "move_set_token",
                           "while(markersPresent()){",
                           "move_token", ";", "}",
                           "putMarker();", "}", "}"]

        return choice([template_while, template_repeat])


if __name__ == "__main__":
    generator = Generator(10, ["red", "yellow"], ["round", "square"])
    program = generator.random_program(6)
    print(program)
    program = generator.random_program(6, template="sort_template")
    print(program)

