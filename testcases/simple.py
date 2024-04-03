import sys
from q1.q1 import convert_to_NNF

sys.path.append('..')

assert convert_to_NNF('¬(A ∧ B)') == '(¬A ∨ ¬B)'
assert convert_to_NNF('¬(A ∨ B)') == '(¬A ∧ ¬B)'
assert convert_to_NNF('¬¬A') == 'A'
assert convert_to_NNF('¬(A)') == '¬A'
assert convert_to_NNF('A') == 'A'
