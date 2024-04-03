# Mapping of logical constructs and quantifiers to digits
mapping = {
    '⊓': '0',
    '⊔': '1',
    '¬': '2',
    '⊑': '3',
    '≡': '4',
    '∃': '5',
    '∀': '6'
}

def convert_biconditional_to_implication(formula):
    while '4' in formula:  # '≡' is represented as '4'
        i = formula.index('4')
        # Find the start and end of the first operand
        if formula[i-1] == ')':
            open_brackets = 0
            j = i - 1
            while True:
                if formula[j] == ')':
                    open_brackets += 1
                elif formula[j] == '(':
                    open_brackets -= 1
                if open_brackets == 0:
                    break
                j -= 1
            start1 = j
            end1 = i
        else:
            start1 = i - 1
            end1 = i
        # Find the start and end of the second operand
        if formula[i+1] == '(':
            open_brackets = 0
            j = i + 1
            while True:
                if formula[j] == '(':
                    open_brackets += 1
                elif formula[j] == ')':
                    open_brackets -= 1
                if open_brackets == 0:
                    break
                j += 1
            start2 = i + 1
            end2 = j + 1
        else:
            start2 = i + 1
            end2 = i + 2
        # Replace the biconditional with two implications
        formula = formula[:start1] + '(' + formula[start1:end1] + '3' + formula[start2:end2] + ')0(' + formula[start2:end2] + '3' + formula[start1:end1] + ')' + formula[end2:]
    return formula

def convert_implication_to_disjunction(formula):
    while '3' in formula:  # '⊑' is represented as '3'
        i = formula.index('3')
        # Find the start and end of the first operand
        if formula[i-1] == ')':
            open_brackets = 0
            j = i - 1
            while True:
                if formula[j] == ')':
                    open_brackets += 1
                elif formula[j] == '(':
                    open_brackets -= 1
                if open_brackets == 0:
                    break
                j -= 1
            start1 = j
            end1 = i
        else:
            start1 = i - 1
            end1 = i
        # Find the start and end of the second operand
        if formula[i+1] == '(':
            open_brackets = 0
            j = i + 1
            while True:
                if formula[j] == '(':
                    open_brackets += 1
                elif formula[j] == ')':
                    open_brackets -= 1
                if open_brackets == 0:
                    break
                j += 1
            start2 = i + 1
            end2 = j + 1
        else:
            start2 = i + 1
            end2 = i + 2
        # Replace the implication with a disjunction
        formula = formula[:start1] + '2' + formula[start1:end1] + '1' + formula[start2:end2] + formula[end2:]
        # Add brackets for double negations
    while '22' in formula:
        i = formula.index('22')
        formula = formula[:i] + '2(2' + formula[i+2] + ")" + formula[i+3:]
    return formula

def encode(encoded_formula):
    # Replace the logical constructs and quantifiers with digits
    mapped_formula = encoded_formula
    for key, value in mapping.items():
        mapped_formula = mapped_formula.replace(key, value)
    return mapped_formula

def decode(encoded_formula):
    # Replace the digits with logical constructs and quantifiers
    mapping = {' ⊓ ': '0', ' ⊔ ': '1', '¬': '2', ' ⊑ ': '3', ' ≡ ': '4', '∃': '5', '∀': '6'}
    decoded_formula = encoded_formula
    for key, value in mapping.items():
        decoded_formula = decoded_formula.replace(value, key)
    return decoded_formula