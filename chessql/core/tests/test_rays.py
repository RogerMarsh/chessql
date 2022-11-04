# test_rays.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Tests for chessql.core.rays."""

import unittest
import re

from .. import rays


class GetRay(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_get_ray_001(self):
        ae = self.assertEqual
        ae(rays.get_ray(), None)

    def test_001_get_ray_002(self):
        ae = self.assertEqual
        ae(rays.get_ray(None, None, None, None), None)

    def test_001_get_ray_003(self):
        self.assertRaisesRegex(
            KeyError,
            "None",
            rays.get_ray,
            *(None, None, None),
            **dict(direction_name=None),
        )

    def test_001_get_ray_004(self):
        ae = self.assertEqual
        ae(rays.get_ray(None, None, None, direction_name="up"), None)

    def test_001_get_ray_005(self):
        ae = self.assertEqual
        ae(rays.get_ray("d3", "f5", None, direction_name="up"), None)

    def test_001_get_ray_006(self):
        ae = self.assertEqual
        ae(rays.get_ray("d3", "f5", direction_name="up"), None)

    def test_001_get_ray_007(self):
        ae = self.assertEqual
        ae(rays.get_ray("d3", "d5", None, direction_name="up"), None)

    def test_001_get_ray_008(self):
        ae = self.assertEqual
        ae(rays.get_ray("d3", "d5", direction_name="up"), ("d3", "d4", "d5"))

    def test_001_get_ray_009(self):
        ae = self.assertEqual
        ae(rays.get_ray("d5", "d3", None, direction_name="up"), None)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(GetRay))
