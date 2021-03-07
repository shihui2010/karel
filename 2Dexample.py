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
env.set_item("yellow", "round", [2, 3])
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
    move(1, 2);
    putMarker();
    while(getMarkerColor() == red){
        pickMarker();
        ifelse(not leftBoundary()){
           moveLeft();
        }
        else{
           moveTop();
        }
    }
    putMarker();
    if(markersPresent()){
        move(0, 0);
    }
}
"""

env.set_item("red", "round", [0, 0])
execute(nested_program, env,
        colors=["red", "yellow"], shapes=["round", "square"])
print(env)

print("===========Sort red markers to upper left===========")
program = """
def run(){
    while(existMovableMarkers()){
        moveToMovableMarker();
        ifelse(getMarkerColor() == red){
            pickMarker();
            move(0,0);
            while(markersPresent()){
                moveDown();
            }
            putMarker();
        }
        else{
            fixMarker();
        }
    }
}
"""

env = Grid2D(10)
items = [['red', 'round', (5, 0)],
         ['yellow', 'round', (8, 1)],
         ['red', 'square', (2, 2)]]
for obj in items:
        env.set_item(*obj)
print("unsorted")
print(env)
execute(program, env, colors=["red", "yellow"], shapes=["round", "square"], print_trace=True)
print("sorted")
print(env)

print("===========Sort to lower right===========")
program = """
def run(){
    repeat(3){
        moveToMovableMarker();
        pickMarker();
        moveRightmost();
        moveBottom();
        while(markersPresent()){
           moveUp();
        }
        putMarker();
        move(0, 0);
    }
}
"""

env = Grid2D(10)
items = [['red', 'round', (1, 0)],
         ['yellow', 'round', (0, 1)],
         ['red', 'square', (2, 2)]]
for obj in items:
        env.set_item(*obj)
print("unsorted")
print(env)
execute(program, env, colors=["red", "yellow"], shapes=["round", "square"], print_trace=True)
print("sorted")
print(env)


print("==========PutMarker Conflict=========")
program = """
def run(){
     pickMarker();
     move(2, 4);
     putMarker();
}
"""
env = Grid2D(20)
env.set_item('red', 'round', [0, 0])
env.set_item('red', 'round', [2, 4])
try:
    execute(program, env, colors=['red'], shapes=['round'])
except Exception as e:
    print(e)


print("___________test____________")
program = """
def run() { repeat( 4 ){ moveToMovableMarker(); if( true ){ pickMarker(); moveLeftmost() ; while(markersPresent()){ moveLeftmost() ; } putMarker(); } } }
"""
env = Grid2D(20)
env.set_item('red', 'round', [1, 0])
env.set_item('red', 'round', [2, 4])
print("unsorted")
print(env)
execute(program, env, colors=["red", "yellow"], shapes=["round", "square"], print_trace=True)
print("sorted")
print(env)

