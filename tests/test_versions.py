"""Version tests."""
from __future__ import unicode_literals
import unittest
import warnings
from backrefs.__meta__ import Version, parse_version


class TestVersion(unittest.TestCase):
    """Test versions."""

    def test_version_output(self):
        """Test that versions generate proper strings."""

        assert Version(1, 0, 0, "final")._get_canonical() == "1.0"
        assert Version(1, 2, 0, "final")._get_canonical() == "1.2"
        assert Version(1, 2, 3, "final")._get_canonical() == "1.2.3"
        assert Version(1, 2, 0, "alpha", pre=4)._get_canonical() == "1.2a4"
        assert Version(1, 2, 0, "beta", pre=4)._get_canonical() == "1.2b4"
        assert Version(1, 2, 0, "candidate", pre=4)._get_canonical() == "1.2rc4"
        assert Version(1, 2, 0, "final", post=1)._get_canonical() == "1.2.post1"
        assert Version(1, 2, 3, ".dev-alpha", pre=1)._get_canonical() == "1.2.3a1.dev0"
        assert Version(1, 2, 3, ".dev")._get_canonical() == "1.2.3.dev0"
        assert Version(1, 2, 3, ".dev", dev=1)._get_canonical() == "1.2.3.dev1"

    def test_version_comparison(self):
        """Test that versions compare proper."""

        assert Version(1, 0, 0, "final") < Version(1, 2, 0, "final")
        assert Version(1, 2, 0, "alpha", pre=4) < Version(1, 2, 0, "final")
        assert Version(1, 2, 0, "final") < Version(1, 2, 0, "final", post=1)
        assert Version(1, 2, 3, ".dev-beta", pre=2) < Version(1, 2, 3, "beta", pre=2)
        assert Version(1, 2, 3, ".dev") < Version(1, 2, 3, ".dev-beta", pre=2)
        assert Version(1, 2, 3, ".dev") < Version(1, 2, 3, ".dev", dev=1)

    def test_version_parsing(self):
        """Test version parsing."""

        assert parse_version(
            Version(1, 0, 0, "final")._get_canonical()
        ) == Version(1, 0, 0, "final")
        assert parse_version(
            Version(1, 2, 0, "final")._get_canonical()
        ) == Version(1, 2, 0, "final")
        assert parse_version(
            Version(1, 2, 3, "final")._get_canonical()
        ) == Version(1, 2, 3, "final")
        assert parse_version(
            Version(1, 2, 0, "alpha", pre=4)._get_canonical()
        ) == Version(1, 2, 0, "alpha", pre=4)
        assert parse_version(
            Version(1, 2, 0, "beta", pre=4)._get_canonical()
        ) == Version(1, 2, 0, "beta", pre=4)
        assert parse_version(
            Version(1, 2, 0, "candidate", pre=4)._get_canonical()
        ) == Version(1, 2, 0, "candidate", pre=4)
        assert parse_version(
            Version(1, 2, 0, "final", post=1)._get_canonical()
        ) == Version(1, 2, 0, "final", post=1)
        assert parse_version(
            Version(1, 2, 3, ".dev-alpha", pre=1)._get_canonical()
        ) == Version(1, 2, 3, ".dev-alpha", pre=1)
        assert parse_version(
            Version(1, 2, 3, ".dev")._get_canonical()
        ) == Version(1, 2, 3, ".dev")
        assert parse_version(
            Version(1, 2, 3, ".dev", dev=1)._get_canonical()
        ) == Version(1, 2, 3, ".dev", dev=1)

    def test_asserts(self):
        """Test asserts."""

        with self.assertRaises(ValueError):
            Version("1", "2", "3")
        with self.assertRaises(ValueError):
            Version(1, 2, 3, 1)
        with self.assertRaises(ValueError):
            Version("1", "2", "3")
        with self.assertRaises(ValueError):
            Version(1, 2, 3, "bad")
        with self.assertRaises(ValueError):
            Version(1, 2, 3, "alpha")
        with self.assertRaises(ValueError):
            Version(1, 2, 3, "alpha", pre=1, dev=1)
        with self.assertRaises(ValueError):
            Version(1, 2, 3, "alpha", pre=1, post=1)
        with self.assertRaises(ValueError):
            Version(1, 2, 3, ".dev-alpha")
        with self.assertRaises(ValueError):
            Version(1, 2, 3, ".dev-alpha", pre=1, post=1)
        with self.assertRaises(ValueError):
            Version(1, 2, 3, pre=1)
        with self.assertRaises(ValueError):
            Version(1, 2, 3, dev=1)


class TestVersionDeprecations(unittest.TestCase):
    """Test general deprecations."""

    def test_version_deprecation(self):
        """Test that version is deprecated."""

        with warnings.catch_warnings(record=True) as w:
            import backrefs

            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            version = backrefs.version
            # Verify some things
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))
            self.assertEqual(version, backrefs.__version__)

    def test_version_info_deprecation(self):
        """Test that version info is deprecated."""

        with warnings.catch_warnings(record=True) as w:
            import backrefs

            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            version_info = backrefs.version_info
            # Verify some things
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))
            self.assertEqual(version_info, backrefs.__version_info__)

    def test_deprecation_wrapper_dir(self):
        """Tests the `__dir__` attribute of the class as it replaces the module's."""

        import backrefs

        dir_attr = dir(backrefs)
        self.assertTrue('version' in dir_attr)
        self.assertTrue('__version__' in dir_attr)
        self.assertTrue('version_info' in dir_attr)
        self.assertTrue('__version_info__' in dir_attr)