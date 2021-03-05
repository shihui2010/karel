from environment2D.environment import Grid2D
from environment2D.parser import DSLParser
from environment2D.executor import execute

parser = DSLParser(10, ["red", "yellow"], ["round", "square"])
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
env.set_items("yellow", "round", [2, 3])
print("input: ")
print(env)
execute(straight_program, env,
        colors=["red", "yellow"],
        shapes=["round", "square"])
print("output: ")
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

"""
# sort to right as a straight line
def run(){
    while(existUnfixedMarker()){
        moveToUnfixedMarker();
        ifelse(getMarkerColor() == red){
            pickMarker();
            move(0,0);
            while(markersPresent()){
                moveDown();
            }
            putMarker();
            fixMarker();
        }
        else{
            fixMarker();
        }
}
"""
