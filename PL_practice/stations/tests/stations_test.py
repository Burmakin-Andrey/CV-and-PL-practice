
import pytest
from plib import Point, PointError, Stations

class TestPoint:

    def test_for_init(self):
        Stations("stations.json")

    def test_min_tri(self):
        assert Stations("stations.json").find_min_tri() == 9.387585278839446e-07