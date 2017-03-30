#!/usr/bin/env python3.6
# coding: utf-8


import os
import tempfile
import unittest
from intersectshape import SpatialIndex, \
    ReverseGeolocShapefile, ReverseGeolocException


def create_tmpfn(ext=None):
    """Create temporary filename.

    :param ext: extension.
    :return: str.
    """
    return tempfile.NamedTemporaryFile(suffix=ext).name


class TestSpatialIndex(unittest.TestCase):
    def test_init(self):
        si = SpatialIndex()
        self.assertEqual(si.bboxs, list())

    def test_insert(self):
        si = SpatialIndex()
        si.insert([0, 0, 5, 5])
        self.assertEqual(si.bboxs, [[0, 0, 5, 5]])

    def test_write_1(self):
        fntmp = create_tmpfn(ext='.npy')
        si = SpatialIndex()
        si.insert([0, 10, 15, 25])
        si.insert([100, 100, 200, 200])
        si.write(fntmp)
        self.assertTrue(os.path.isfile(fntmp))

    def test_write_2(self):
        fntmp = create_tmpfn()
        si = SpatialIndex()
        si.insert([0, 10, 15, 25])
        si.insert([100, 100, 200, 200])
        si.write(fntmp)
        self.assertTrue(os.path.isfile(fntmp + '.npy'))

    def test_read(self):
        fntmp = create_tmpfn(ext='.npy')
        si1 = SpatialIndex()
        si1.insert([0, 10, 15, 25])
        si1.insert([100, 100, 200, 200])
        si1.write(fntmp)
        del si1
        si2 = SpatialIndex()
        si2.read(fntmp)
        self.assertEqual(si2.bboxs.tolist(),
                         [[0, 10, 15, 25], [100, 100, 200, 200]])

    def test_intersection(self):
        si = SpatialIndex()
        si.insert([0, 0, 10, 10])
        si.insert([5, 5, 20, 20])
        self.assertEqual(si.intersection(1, 1), [0])
        self.assertEqual(si.intersection(-1, -1), [])
        self.assertEqual(si.intersection(5, 5), [0, 1])
        self.assertEqual(si.intersection(15, 15), [1])
        self.assertEqual(si.intersection(10, 30), [])


class TestReverseGeolocShapefile(unittest.TestCase):
    def setUp(self):
        self.bn = 'data/geofla_2015_v2.1_commune'

    def test_init_ok(self):
        ReverseGeolocShapefile(self.bn + '.shp')
        self.assertTrue(os.path.isfile(self.bn + '.sidx.npy'))

    def test_init_error(self):
        pass
        # TODO: use shapefile of points

    def test_intersection_null(self):
        rgs = ReverseGeolocShapefile(self.bn + '.shp')
        ids = rgs.intersection(0, 0)
        self.assertEqual(ids, [])

    def test_intersection(self):
        rgs = ReverseGeolocShapefile(self.bn + '.shp')
        ids = rgs.intersection(525445, 6701846)
        self.assertEqual(ids, [25791])
        self.assertEqual(rgs.record(ids[0])[3], 'TOURS')


if __name__ == '__main__':
    unittest.run()
