from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

'''
Puzzle 0 is the puzzle from the Background. It contains a single character, A.
A says "I am both a knight and a knave."
'''
knowledge0 = And(
    # A is a knight only if it is not a knave and
    Biconditional(AKnight, Not(AKnave)),
    # if and only if the statement made by A i.e "I am both knight and a knave is true"
    Biconditional(AKnight, And(AKnight, AKnave)),
)

'''
Puzzle 1 has two characters: A and B.
A says "We are both knaves."
B says nothing.
'''
knowledge1 = And(
    # A is a knight only if it is not a knave and
    Biconditional(AKnight, Not(AKnave)),
    # if the statment is true.
    Biconditional(AKnight, And(AKnave, BKnave)),
    # B is a knight if it it not a knave.
    Biconditional(BKnight, Not(BKnave))
)

'''
Puzzle 2 has two characters: A and B.
A says "We are the same kind."
B says "We are of different kinds."
'''
knowledge2 = And(
    # A is a knight only if it is not a knave and
    Biconditional(AKnight, Not(AKnave)),
    # if B and A are alike
    Biconditional(AKnight, Or(And(BKnight, AKnight), And(AKnave, BKnave))),
    # B is a knight if B is not a knave and 
    Biconditional(BKnight, Not(BKnave)),
    # if A and B are differnt.
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave)))
)

'''
Puzzle 3 has three characters: A, B, and C.
A says either "I am a knight." or "I am a knave.", but you don't know which.
B says "A said 'I am a knave.'"
B then says "C is a knave."
C says "A is a knight."
'''
knowledge3 = And(
    # A is a knight only if it is not a knave and
    Biconditional(AKnight, Not(AKnave)),
    # if A is either a knight or a knave.
    Biconditional(AKnight, Or(AKnight, BKnave)),
    # B is a knight if B is not a knave and 
    Biconditional(BKnight, Not(BKnave)),
    # if A says it's a knave (making it a knight, hypothetically) and c is a knave
    Biconditional(BKnight, And(Biconditional(AKnight, AKnave), CKnave)),
    # C is a knight if C is not a knave and 
    Biconditional(CKnight, Not(CKnave)),
    # if A is a Knight
    Biconditional(CKnight, AKnight)
)

def main():
    puzzles = [
        ("Puzzle 0", knowledge0, (AKnight, AKnave)),
        ("Puzzle 1", knowledge1, (AKnight, AKnave, BKnight, BKnave)),
        ("Puzzle 2", knowledge2, (AKnight, AKnave, BKnight, BKnave)),
        ("Puzzle 3", knowledge3, (AKnight, AKnave, BKnight, BKnave,CKnight, CKnave))
    ]
    for puzzle, knowledge, symbols in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")

if __name__ == "__main__":
    main()