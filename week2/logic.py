''' Logic to hold Knowledge Base '''

import math


class Sentence:
    def symbols(self, sentence) -> set:
        return set()

    def evaluate(self, model) -> bool:
        raise Exception("Nothing to evaluate !!")

    @classmethod
    def validate(self, s) -> bool:
        if not isinstance(s, Sentence):
            raise TypeError("This is not a valid sentence.")

    @classmethod
    def parenthesize(cls, s) -> str:
        def balanced(s):
            count = 0

            for ch in s:
                if ch == '(':
                    count += 1
                elif ch == ')':
                    if count <= 0:
                        return False
                    count -= 1
            
            return count == 0

        if not len(s) or s.isalpha() or (s[0] == '(' and s[-1] == ')' and balanced(s[1:-1])):
            return s
        
        else:
            return f"({s})" 


class Symbol:
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    # Returns the value held by the symbol in the given model.
    def evaluate(self, model) -> bool:
        if self.name in model:
            return model[self.name]
        raise KeyError('Symbol does not exits.')

    def formula(self) -> str:
        return self.name

    def symbols(self) -> set:
        return {self.name}


''' Logic to implement different logical operators '''
class And(Sentence):
    def __init__(self, *conjuncts) -> None:
        super().__init__()
        self.conjuncts = list(conjuncts)

    def __repr__(self) -> str:
        operands = ', '.join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({operands})"
    
    def evaluate(self, model) -> bool:
        for conjunction in self.conjuncts:
            if not conjunction.evaluate(model):
                return False
        return True

    def formula(self) -> str:
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " & ".join([Sentence.parenthesize(conjunct.formula()) 
        for conjunct in self.conjuncts])

    def symbols(self) -> set:
        return set.union(*[conjunct.symbols() 
        for conjunct in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts) -> None:
        super().__init__()
        self.disjuncts = list(disjuncts)

    def __repr__(self) -> str:
        operands = ', '.join([str(disjunct) 
        for disjunct in self.disjuncts])
        return f"Or({operands})"
    
    def evaluate(self, model) -> bool:
        for disjunction in self.disjuncts:
            if disjunction.evaluate(model):
                return True
        return False

    def formula(self) -> str:
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return "|| ".join([Sentence.parenthesize(disjunct.formula()) 
        for disjunct in self.disjuncts])

    def symbols(self) -> set:
        return set.union(*[disjunct.symbols() 
        for disjunct in self.disjuncts])

class Not(Sentence):
    def __init__(self, operand) -> None:
        super().__init__()
        self.operand = operand

    def __repr__(self) -> str:
        return f"Not({self.operand})"
    
    def evaluate(self, model) -> bool:
        return not self.operand.evaluate(model)

    def formula(self) -> str:
        return f"!({self.operand.formula()})"

    def symbols(self) -> set:
        return self.operand.symbols()

class Implication(Sentence):
    def __init__(self, antecedent, consequent) -> None:
        super().__init__()
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self) -> str:
        return f"Implication({self.antecedent}, {self.consequent})"
    
    def evaluate(self, model) -> bool:
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def formula(self) -> str:
        antecedent = self.antecedent.formula()
        consequent = self.consequent.formula()
        return f"{antecedent} -> {consequent}"

    def symbols(self) -> set:
        return set.union(self.antecedent.symbols(), 
        self.consequent.symbols())

class Biconditional(Sentence):
    def __init__(self, antecedent, consequent) -> None:
        super().__init__()
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self) -> str:
        return f"Biconditional({self.antecedent}, {self.consequent})"
    
    def evaluate(self, model) -> bool:
        return not (self.antecedent.evaluate(model) ^ 
        self.consequent.evaluate(model)) 

    def formula(self) -> str:
        antecedent = self.antecedent.formula()
        consequent = self.consequent.formula()
        return f"{antecedent} <-> {consequent}"

    def symbols(self) -> set:
        return set.union(self.antecedent.symbols(), 
        self.consequent.symbols())


def model_check(knowledge, query):
    symbols = set.union(knowledge.symbols(), query.symbols())
    model = dict()
    size = len(symbols)
    preposition_result = False
    for i in range(int(math.pow(2, size))):
        for symbol in symbols:
            model[symbol] =  (int(i) & 1 == 1)
            i = i >> 1
        if knowledge.evaluate(model):
            preposition_result =  query.evaluate(model)

        if preposition_result:
            return True

    return False
