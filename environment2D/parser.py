from pyparsing import Keyword, Or, OneOrMore, Group, Forward


"""
DSL: 

Program p := def run(): s

Statement s := while(b): s 
             | repeat(r): s
             | s1; s2 
             | a 
             | if(b): s
             | ifelse(b): s1 else: s2

Condition b := markersPresent() | movableMarkersPresent()
             | existMovableMarkers()
             | upperBoundary() | lowerBoundary() 
             | leftBoundary() | rightBoundary()
             | sh1 == sh2
             | cl1 == cl2
             | not b
             | true

Action a := move(p1, p2) 
          | moveUp() | moveDown() | moveRight() | moveLeft()
          | moveTop() | moveBottom() | moveRightmost() | moveLeftmost() 
          | moveToMovableMarker()  
          | pickMarker() | putMarker() | fixMarker()

Consts r := 1 | 2 | ... | 19

Position p := 0 | 1 | ... | n - 1 width/height of the grid)

Shape sh := round | triangle | ... |
          | getMarkerShape()
                
Color cl :=  red | yellow | ... |
          | getMarkerColor()
"""


class DSLParser:
    def __init__(self, n, colors, shapes, max_constant=5):
        """
        :param n: length of side of the grids
        :param colors: list of color names
        :param shapes: list of shape names
        """

        self.colors = Or([Keyword(w) for w in colors])
        self.colors ^= Keyword("getMarkerColor()")
        self.shapes = Or([Keyword(w) for w in shapes])
        self.shapes ^= Keyword("getMarkerShape()")
        self.positions = Or([Keyword(str(i)) for i in range(n)])
        self.constants = Or([Keyword(str(i)) for i in range(1, max_constant)])
        self.actions = (
                ("move(" + self.positions + "," + self.positions + ")") |
                "moveUp()" | "moveDown()" | "moveLeft()" | "moveRight()" |
                "moveTop()" | "moveBottom()" |
                "moveLeftmost()" | "moveRightmost()" |
                "moveToMovableMarker()" |
                "pickMarker()" | "putMarker()" | "fixMarker()")

        self.conditions = (
                Group(self.shapes + "==" + self.shapes) |
                Group(self.colors + "==" + self.colors) |
                "markersPresent()" | "movableMarkersPresent()" |
                "existMovableMarkers()" |
                "upperBoundary()" | "lowerBoundary()" |
                "leftBoundary()" | "rightBoundary()" | "true")

        self.conditions = (self.conditions |
                           Group(Keyword("not") + self.conditions))
        block = Forward()
        stmt = (Group(Keyword("while") + "(" + self.conditions + ")" +
                      "{" + Group(block) + "}") |
                Group(Keyword("repeat") + "(" + self.constants + ")" +
                      "{" + Group(block) + "}") |
                Group(Keyword("if") + "(" + self.conditions + ")" +
                      "{" + Group(block) + "}") |
                Group(Keyword("ifelse") + "(" + self.conditions + ")" +
                      "{" + Group(block) + "}" +
                      Keyword("else") + "{" + Group(block) + "}") |
                Group(self.actions + ";"))
        block << OneOrMore(stmt)
        # stmt ^= block
        self.statements = block
        self.program = Keyword("def") + Keyword("run()") + "{" \
                       + Group(self.statements) + "}"

    def parse_string(self, program):
        return self.program.parseString(program, parseAll=True)


if __name__ == "__main__":
    parser = DSLParser(10, ["red", "yellow"], ["round", "square"])
    sample_program = """
    def run(){
        move(1, 2);
        if(getMarkerColor() == red){
            move(1, 2);
            move(4, 2);
            pickMarker();
            ifelse(round == getMarkerShape()){
               putMarker();
            }
            else{
                pickMarker();
                repeat(4){
                    move(1, 2);
                }
            }
        }
    }
    """
    print(parser.conditions.parseString("getMarkerColor() == red"))
    print(parser.statements.parseString("move(1, 2); move(3, 4);"))
    print(parser.statements.parseString("move(1, 2); "
                                        "repeat(10){move(1, 2);}"))
    print(parser.parse_string(sample_program))

