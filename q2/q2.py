class Node:
    def __init__(self, formula, truth_value):
        self.formula = formula
        self.truth_value = truth_value
        self.branchSiblings = []
        self.children = []

    def add_child(self, node):
        self.children.append(node)
    
    def add_branch_sibling(self, node):
        self.branchSiblings.append(node)

    def print_tree(self, level=0, is_sibling=False):
        # Print current node
        prefix = '  ' * level + ('|-' if is_sibling else '')
        print(f"{prefix}Level {level}: {self.truth_value} {decode(print_formula2(self.formula))}")
        # Print all children
        for child in self.children:
            child.print_tree(level + 1)
        # If there are branch siblings, print them as well
        for sibling in self.branchSiblings:
            sibling.print_tree(level, is_sibling=True)

class Formula:
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

def print_formula(formula):
    if isinstance(formula, Formula):
        # print("Formula")
        # print("Operator",formula.operator)
        # print("Operands",formula.operands)
        return formula.operator + '(' + ','.join(print_formula(operand) for operand in formula.operands) + ')'
    else:
        return formula

def print_formula2(formula):
    if isinstance(formula, str):
        return formula 
    else:
        if len(formula.operands) == 1:
            return formula.operator+print_formula2(formula.operands[0])
        else:
            if isinstance(formula.operands[0],str) and not isinstance(formula.operands[1],str):
                return print_formula2(formula.operands[0]) + formula.operator + "("+print_formula2(formula.operands[1])+")"
            elif not isinstance(formula.operands[0],str) and isinstance(formula.operands[1],str):
                return "("+print_formula2(formula.operands[0])+")" + formula.operator + print_formula2(formula.operands[1])
            elif not isinstance(formula.operands[0],str) and not isinstance(formula.operands[1],str):
                return "("+print_formula2(formula.operands[0])+")" + formula.operator + "(" + print_formula2(formula.operands[1])+")"
            return print_formula2(formula.operands[0]) + formula.operator + print_formula2(formula.operands[1])

def encode(encoded_formula):
    # Replace the logical constructs and quantifiers with digits
    mapping = {'⊓': '0', '⊔': '1', '¬': '2', '⊑': '3', '≡': '4', '∃': '5', '∀': '6'}
    mapped_formula = encoded_formula
    for key, value in mapping.items():
        mapped_formula = mapped_formula.replace(key, value)
    return mapped_formula

def decode(encoded_formula):
    # Replace the digits with logical constructs and quantifiers
    mapping = {' ⊓ ': '0', ' ⊔ ': '1', ' ¬ ': '2', ' ⊑ ': '3', ' ≡ ': '4', ' ∃ ': '5', ' ∀ ': '6'}
    decoded_formula = encoded_formula
    for key, value in mapping.items():
        decoded_formula = decoded_formula.replace(value, key)
    return decoded_formula

def tableau(formula, truth_value, level=0):
    node = Node(formula, truth_value)
    print('  ' * level + f'{level} {truth_value}', decode(print_formula2(formula)))
    if isinstance(formula, str):  # If the formula is a variable
        return node
    elif formula.operator == '0':  # Conjunction
        if truth_value:  # True
            child = tableau(formula.operands[0], True, level + 1)
            node.add_child(child)
            for operand_idx in range(1,len(formula.operands)):
                sibling = tableau(formula.operands[operand_idx], True, level + 1)
                child.add_branch_sibling(sibling)
        else:  # False
            for operand in formula.operands:
                child = tableau(operand, False, level + 1)
                node.add_child(child)
    elif formula.operator == '1':  # Disjunction
        if truth_value:  # True
            for operand in formula.operands:
                child = tableau(operand, True, level + 1)
                node.add_child(child)
        else:  # False
            child = tableau(formula.operands[0], False, level + 1)
            node.add_child(child)
            for operand_idx in range(1,len(formula.operands)):
                sibling = tableau(formula.operands[operand_idx], False, level + 1)
                child.add_branch_sibling(sibling)
            
    elif formula.operator == '2':  # Negation
        child = tableau(formula.operands[0], not truth_value, level + 1)
        node.add_child(child)

    return node

def parse_formula(code):
    if len(code) == 1:
        return code  # Return the concept or role
    else:
        operator = None
        operands = []
        i = 0
        while i < len(code):
            if code[i] in ['0', '1', '2']:  # If the character is an operator
                if operator is None:
                    operator = code[i]
                    i += 1
                elif int(operator) in [2]:
                    operands = [Formula(operator, operands)]
                    operator = code[i]
                    i += 1
                elif int(operator) in [0,1]:
                    operands.append(parse_formula(code[i:i+2]))
                    i+=2

            elif code[i] == '(':
                j = i
                open_brackets = 0
                while True:
                    if code[j] == '(':
                        open_brackets += 1
                    elif code[j] == ')':
                        open_brackets -= 1
                    if open_brackets == 0:
                        break
                    j += 1
                operands.append(parse_formula(code[i+1:j]))
                i = j + 1
            else:
                operands.append(code[i])
                i += 1
        return Formula(operator, operands)

# Test cases
formula = encode('(¬p ⊓ q) ⊔ (q ⊓ ¬p)')
formula = formula.replace(" ", "")
print("Encoded Formula:",formula)
formula = parse_formula(formula)
print("Parsed Formula in Interpretable Form",print_formula(formula))
print("Parsed Formula in Interpretable Form",print_formula2(formula))
root_node = tableau(formula, False)
print("\nTableau Tree:")
root_node.print_tree()
