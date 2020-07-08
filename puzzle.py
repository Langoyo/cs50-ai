from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave.

# Statement A says
AStatement = And(AKnight,AKnave)
knowledge0 = And(
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    # If A is a knight the statment must be true
    Biconditional(AKnight,AStatement),
    # If A is a knave the statement must be false
    Biconditional(AKnave,Not(AStatement))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
AStatement = And(AKnave,BKnave)
knowledge1 = And(
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),

    Biconditional(AKnight,AStatement)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
AStatement = Or(And(AKnave,BKnave),And(AKnight,BKnight))
BStatement = Or(And(AKnave,BKnight),And(AKnight,BKnave))

knowledge2 = And(
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),

    Biconditional(AKnight,AStatement),

    Biconditional(BKnight,BStatement)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."


# A is saying that he is either a knight or a knave but not both
AStatement = And(Or(AKnave, AKnight),Not(And(AKnave, AKnight)))
# B is saying that A said that B is a knave. If A is a knight it would be true and so the other way around
BStatement = And(Biconditional(AKnight, BKnave), CKnave)
CStatement = AKnight
knowledge3 = And(

    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),

    Or(CKnave, CKnight),
    Not(And(CKnave, CKnight)),

    Biconditional(AKnight, AStatement),
    Biconditional(BKnight, BStatement),
    Biconditional(CKnight, CStatement)
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
