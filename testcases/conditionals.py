import sys
from q1.utlis import convert_implication_to_disjunction
sys.path.append('..')

assert convert_implication_to_disjunction('A ⊑ B') == ''
assert convert_implication_to_disjunction('(A ⊑ B) ⊑ C') == ''
assert convert_implication_to_disjunction('A ⊑ (B ⊑ C)') == ''
assert convert_implication_to_disjunction('A ⊑ (B ⊑ (C ⊑ D))') == ''

