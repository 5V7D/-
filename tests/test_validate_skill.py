import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "skill-builder" / "scripts"))
import validate_skill


class SkillNameTests(unittest.TestCase):
    def test_valid_names(self):
        for name in ("skill-builder", "résumé-helper", "данные-анализ", "a1-b2"):
            with self.subTest(name=name):
                self.assertTrue(validate_skill.valid_skill_name(name))

    def test_invalid_names(self):
        for name in ("", "-bad", "bad-", "bad--name", "UPPER", "a" * 65, "two words"):
            with self.subTest(name=name):
                self.assertFalse(validate_skill.valid_skill_name(name))


class FrontmatterTests(unittest.TestCase):
    def test_valid_frontmatter(self):
        fields, errors = validate_skill.parse_frontmatter(
            "---\nname: skill-builder\ndescription: Build skills.\n---\n# Body\n"
        )
        self.assertEqual(errors, [])
        self.assertEqual(fields["name"], "skill-builder")
        self.assertEqual(fields["description"], "Build skills.")

    def test_missing_closing_delimiter(self):
        _, errors = validate_skill.parse_frontmatter("---\nname: skill-builder\n")
        self.assertTrue(errors)

    def test_duplicate_field(self):
        _, errors = validate_skill.parse_frontmatter(
            "---\nname: first\nname: second\n---\n# Body\n"
        )
        self.assertTrue(any("Duplicate" in error for error in errors))


class SkillFileTests(unittest.TestCase):
    def test_valid_skill_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "skill-builder"
            skill_dir.mkdir()
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(
                "---\nname: skill-builder\ndescription: Build skills.\n---\n# Title\nBody\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_skill.validate(skill_file), [])

    def test_directory_name_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "wrong-directory"
            skill_dir.mkdir()
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(
                "---\nname: skill-builder\ndescription: Build skills.\n---\n# Title\nBody\n",
                encoding="utf-8",
            )
            self.assertTrue(any("must match" in error for error in validate_skill.validate(skill_file)))


if __name__ == "__main__":
    unittest.main()
