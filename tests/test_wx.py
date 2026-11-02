# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from wxcorrector import download_tle, install_tle

class WXTests(unittest.TestCase):
    def test_https_required(self):
        with self.assertRaises(ValueError):
            download_tle("http://example.com")
    def test_backup_and_write(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "weather.txt"
            path.write_bytes(b"old")
            backup = install_tle(path, b"new")
            self.assertEqual(path.read_bytes(), b"new")
            self.assertEqual(backup.read_bytes(), b"old")
    def test_symlink_rejected(self):
        with TemporaryDirectory() as folder:
            target = Path(folder) / "target"
            target.write_text("original")
            link = Path(folder) / "weather.txt"
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                install_tle(link, b"new")
            self.assertEqual(target.read_text(), "original")

if __name__ == "__main__":
    unittest.main()
