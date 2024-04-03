import sys
sys.path.append('.')
from utlis import convert_biconditional_to_implication, convert_implication_to_disjunction, encode, decode
from nnf_rules import negation_normal_form, parse_formula, print_formula2

def apply_nnf_rules(expression):
    parsed_expression = parse_formula(expression)
    print("Parsed Expression",parsed_expression)
    print("Understandable Expression",decode(print_formula2(parsed_expression)))
    negation_normal_form_expression = negation_normal_form(parsed_expression)
    return negation_normal_form_expression

def compute(expression):
    # Remove spaces
    preprocessed_expression = expression.replace(" ", "")
    print("Preprocessed Expression",preprocessed_expression)

    # encode the expression
    encoded_expression = encode(preprocessed_expression)
    print("Encoded Expression",encoded_expression)

    # Convert biconditional to implication
    expression_1 = convert_biconditional_to_implication(encoded_expression)
    print("Result after Step 1:", expression_1)
    print("Decoded Result after Step 1:",decode(expression_1))

    # Replace 'A ⊑ B' with '¬A⊔B'
    expression_2 = convert_implication_to_disjunction(expression_1)
    print("Result after Step 2:", expression_2)
    print("Decoded Result after Step 2:",decode(expression_2))

    final_expression = apply_nnf_rules(expression_2)
    print("Result after Step 3:", final_expression)

    # decode the expression
    pre_decoded_expression = print_formula2(final_expression)
    print("Predecoded Expression",pre_decoded_expression)
    decoded_expression = decode(print_formula2(final_expression))
    print("Decoded Expression",decoded_expression)
    
if __name__ == "__main__":
    test_case = '(¬A ⊑ ∃S.B) ≡ (B ⊑ ¬C)'
    compute(test_case) 

