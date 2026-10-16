"""Isolated source guard checks; never launches the application."""
import ast, hashlib, os, unittest
from pathlib import Path
from unittest.mock import patch

class PasswordGuards(unittest.TestCase):

    def test_video_missing_empty_correct_incorrect(self):
        source = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text())
        fn = next((n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'check_password'))
        env = {'os': os, 'hashlib': hashlib, 'ROOM_PASSWORD_ENV': 'CODEX_TEST_ROOM_PASSWORD'}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<video-check-password>', 'exec'), env)
        fn = env['check_password']
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(fn(''))
            self.assertFalse(fn('irrelevant'))
            os.environ['CODEX_TEST_ROOM_PASSWORD'] = ''
            self.assertFalse(fn(''))
            os.environ['CODEX_TEST_ROOM_PASSWORD'] = 'synthetic-only-test-value'
            self.assertTrue(fn('synthetic-only-test-value'))
            self.assertFalse(fn('incorrect'))
