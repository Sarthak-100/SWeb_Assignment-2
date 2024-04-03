class Formula:
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

def negation_normal_form(formula):
    if isinstance(formula, str):
        return formula
    elif formula.operator == '2':  # Negation
        if isinstance(formula.operands[0], Formula):
            inner_operator = formula.operands[0].operator
            if inner_operator == '2':  # Double negation
                return negation_normal_form(formula.operands[0].operands[0])
            elif inner_operator == '0':  # AND, De Morgan's laws
                return Formula('1', [negation_normal_form(Formula('2', [operand])) for operand in formula.operands[0].operands])
            elif inner_operator == '1':  # OR, De Morgan's laws
                return Formula('0', [negation_normal_form(Formula('2', [operand])) for operand in formula.operands[0].operands])
            elif inner_operator == '5':  # Existential restriction negation: ¬∃R.C becomes ∀R.¬C
                return Formula('6', [negation_normal_form(Formula('2', [operand[2]])) for operand in formula.operands[0].operands])
            elif inner_operator == '6':  # Universal restriction negation: ¬∀R.C becomes ∃R.¬C
                return Formula('5', [negation_normal_form(Formula('2', operand[2])) for operand in formula.operands[0].operands])
        return Formula('2', [formula.operands[0]])
    else:  # Other operators
        return Formula(formula.operator, [negation_normal_form(operand) for operand in formula.operands])
    

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
                
            elif code[i] in ['5','6']:
                operands.append(Formula(code[i], [code[i+1:i+4]]))
                i += 4
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
    
def print_formula2(formula):
    if isinstance(formula, str):
        return formula
    else:   
        if len(formula.operands) == 1:
            return formula.operator + "(" + print_formula2(formula.operands[0]) + ")"
        elif isinstance(formula.operands[0], str) and isinstance(formula.operands[1],Formula):
            return formula.operands[0] + formula.operator + "(" + print_formula2(formula.operands[1]) + ")"
        elif isinstance(formula.operands[0], Formula) and isinstance(formula.operands[1], str):
            return "(" + print_formula2(formula.operands[0]) + ")" + formula.operator + formula.operands[1]
        elif isinstance(formula.operands[0], str) and isinstance(formula.operands[1], str):
            return formula.operands[0] + formula.operator + formula.operands[1]
        else:
            return "(" + print_formula2(formula.operands[0]) + ")" + formula.operator + "(" + print_formula2(formula.operands[1]) + ")"









