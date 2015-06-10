"""
Test Geometry 
"""

import unittest

from pypg import Geometry, InvalidGeometryError
from shapely.geometry import Point

class GeometryTestCase(unittest.TestCase):
  def test_missing_shape(self):
    """
    pypg.Geometry.__init__ missing shape
    """
    self.assertRaises(InvalidGeometryError, Geometry, None, None)

  def test_from_shape(self):
    """
    pypg.Geometry.from_shape load
    """
    point = Point(0, 0)
    geom = Geometry.from_shape(point, 4326)
    self.assertEquals(geom.srid, 4326)
    self.assertTrue(geom.as_shape().equals(point))

  def test_from_shape_nosrid(self):
    """
    pypg.Geometry.from_shape load without SRID
    """
    point = Point(0, 0)
    geom = Geometry.from_shape(point)
    self.assertEquals(geom.srid, None)
    #self.assertTrue(geom.equals(point, srid_compare = False))
    self.assertTrue(geom.as_shape().equals(point))

  def test_from_wkb_invalid(self):
    """
    pypg.Geometry.from_wkb load invalid WKB
    """
    wkb = '11110008066C00000000000000000'
    self.assertRaises(InvalidGeometryError, Geometry.from_wkb, wkb)

  def test_from_wkb(self):
    """
    pypg.Geometry.from_wkb load WKB
    """
    wkb = '0101000020E610000000000000008066C00000000000000000'
    geom = Geometry.from_wkb(wkb)
    self.assertEquals(geom.srid, 4326)
    self.assertTrue(geom.as_shape().equals(Point(-180, 0)))

  def test_from_wkt_invalid(self):
    """
    pypg.Geometry.from_wkt load invalid WKT
    """
    wkt = 'LINESTRING(-180 0)'
    self.assertRaises(InvalidGeometryError, Geometry.from_wkt, wkt)

  def test_from_wkt(self):
    """
    pypg.Geometry.from_wkt load WKB
    """
    wkt = 'POINT (-180 0)'
    geom = Geometry.from_wkt(wkt, 4326)
    self.assertEquals(geom.srid, 4326)
    self.assertTrue(geom.as_shape().equals(Point(-180, 0)))

  def test_from_ewkt(self):
    """
    pypg.Geometry.from_ewkt load EWKT
    """
    ewkt = 'SRID=4326;POINT (-180 0)'
    geom = Geometry.from_wkt(ewkt)
    self.assertEquals(geom.srid, 4326)
    self.assertTrue(geom.as_shape().equals(Point(-180, 0)))

  def test_from_ewkt_nosrid(self):
    """
    pypg.Geometry.from_ewkt load without SRID
    """
    ewkt = 'POINT (-180 0)'
    geom = Geometry.from_wkt(ewkt)
    self.assertEquals(geom.srid, None)
    self.assertTrue(geom.as_shape().equals(Point(-180, 0)))

  def test_as_ewkt(self):
    """
    pypg.Geometry.as_ewkt output EWKT
    """
    ewkt = 'SRID=4326;POINT (-180 0)'
    geom = Geometry.from_wkt(ewkt)
    self.assertEquals(geom.as_wkt(ewkt=True), ewkt)

  def test_as_wkt(self):
    """
    pypg.Geometry.as_wkt output WKT
    """
    wkt = 'POINT (-180 0)'
    geom = Geometry.from_wkt(wkt)
    self.assertEquals(geom.as_wkt(), wkt)

  def test_bounds(self):
    """
    pypg.Geometry.bounds get geometry bounds
    """
    wkb = '01020000000200000000000000000000000000000000000000000000000000F03F000000000000F03F'
    geom = Geometry.from_wkb(wkb)
    self.assertEquals(geom.bounds(), (0.0, 0.0, 1.0, 1.0))

  def test_equals(self):
    """
    pypg.Geometry.equals test geometries
    """
    wkb = '0102000020E61000000200000000000000000000000000000000000000000000000000F03F000000000000F03F'
    geom_1 = Geometry.from_wkb(wkb)
    ewkt = 'SRID=4326;LINESTRING(0 0,1 1)'
    geom_2 = Geometry.from_wkt(ewkt)
    self.assertTrue(geom_1.equals(geom_2))

  def test_wkb_srid(self):
    """
    pypg.Geometry.equals test geometries
    """
    wkb = '0102000020E61000000200000000000000000000000000000000000000000000000000F03F000000000000F03F'
    ewkt = 'SRID=4326;LINESTRING(0 0,1 1)'
    geom = Geometry.from_wkt(ewkt)
    self.assertEquals(wkb, geom.as_wkb(ewkb=True))

  def test_wkb_nosrid(self):
    """
    pypg.Geometry.equals test geometries
    """
    wkb = '01020000000200000000000000000000000000000000000000000000000000F03F000000000000F03F'
    ewkt = 'SRID=4326;LINESTRING(0 0,1 1)'
    geom = Geometry.from_wkt(ewkt)
    self.assertEquals(wkb, geom.as_wkb(ewkb=False))

  def test_equals_nosrid(self):
    """
    pypg.Geometry.equals test geometries without SRID
    """
    wkb = '0102000020E61000000200000000000000000000000000000000000000000000000000F03F000000000000F03F'
    geom_1 = Geometry.from_wkb(wkb)
    ewkt = 'LINESTRING(0 0,1 1)'
    geom_2 = Geometry.from_wkt(ewkt)
    self.assertTrue(geom_1.equals(geom_2, srid_compare = False))

  def test_equals_nosrid(self):
    """
    pypg.Geometry.equals test different geometries
    """
    wkb = '0102000020E61000000200000000000000000000000000000000000000000000000000F03F000000000000F03F'
    geom_1 = Geometry.from_wkb(wkb)
    ewkt = 'SRID=3587;LINESTRING(0 0,1 1)'
    geom_2 = Geometry.from_wkt(ewkt)
    self.assertFalse(geom_1.equals(geom_2))
