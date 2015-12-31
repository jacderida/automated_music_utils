import unittest
from amu.parsing import replace_forbidden_characters


class TestReplaceForbiddenCharacters(unittest.TestCase):
    def test_forward_slash_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor/Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_back_slash_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor\Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_question_mark_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor?Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_left_arrow_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor<Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_right_arrow_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor>Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_colon_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor:Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_asterisk_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor*Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_pipe_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor|Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)

    def test_double_quote_is_replaced(self):
        replaced = replace_forbidden_characters('Backdoor"Spyboter.A')
        self.assertEqual('Backdoor Spyboter.A', replaced)
