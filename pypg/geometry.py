import shapely.wkb
import shapely.wkt
from shapely.geometry.base import BaseGeometry
from shapely.geometry import asShape
from shapely.geos import ReadingError
from shapely import geos
import re

class InvalidGeometryError(Exception):
  pass

class Geometry():
  """
  Represents a PostGIS geometry object that can be imported from or exported to
  a Shapely geometry, (E)WKB or (E)WKT.
  """
  def __init__(self, shape, srid):
    """
    Note: use one of from_shape(), from_wkb(), from_wkt() since this might change in future.
    """
    if not issubclass(type(shape), BaseGeometry):
      raise InvalidGeometryError('Geometry can not be None')
    self._shape = shape
    self._set_srid(srid)

  @classmethod
  def from_shape(cls, shape, srid=None):
    """
    Create a Geometry object from a Shapely geometry. Override the geometry's
    SRID with the optional srid parameter.
    """
    if not srid:
      srid = geos.lgeos.GEOSGetSRID(shape._geom)
    return cls(asShape(shape), srid)

  @classmethod
  def from_wkb(cls, wkb, srid=None):
    """
    Create a Geometry object from a PostGIS geometry. Override the geometry's
    SRID with the optional srid parameter.
    """
    try:
      shape = shapely.wkb.loads(wkb, hex=True)
    except ReadingError as e:
      raise InvalidGeometryError('Invalid WKB can not be loaded')
    if not srid:
      srid = geos.lgeos.GEOSGetSRID(shape._geom)
    return cls(shape, srid)

  @classmethod
  def from_wkt(cls, wkt, srid=None):
    """
    Create a Geometry object from WKT. Override the geometry's SRID with the
    optional srid parameter.
    """
    if wkt.count(';') and not srid:
      ewkt = wkt.split(';')
      wkt = ewkt[1]
      srid = re.sub(re.escape('SRID='), '', ewkt[0], flags=re.I)
      return cls.from_wkt(wkt, srid)
    else:
      try:
        shape = shapely.wkt.loads(wkt)
      except ReadingError as e:
        raise InvalidGeometryError('Invalid WKT can not be loaded')
      return cls(shape, srid)

  def _set_srid(self, srid=None):
    """
    Set the geometry's SRID.
    """
    if srid:
      self.srid = int(srid)
      geos.lgeos.GEOSSetSRID(self._shape._geom, self.srid)
    else:
      self.srid = None

  def as_shape(self):
    """
    Return the geometry as a Shapely geometry.
    """
    return self._shape

  def as_wkb(self, ewkb=True):
    """
    Return the geometry as a WKB.
    """
    if self.srid and ewkb:
      geos.WKBWriter.defaults['include_srid'] = True
    else:
      geos.WKBWriter.defaults['include_srid'] = False
    return self._shape.wkb_hex

  def as_wkt(self, ewkt=True):
    """
    Return the geometry as a WKT.
    """
    if self.srid and ewkt:
      return 'SRID=%d;%s' % (self.srid, self._shape.wkt)
    else:
      return self._shape.wkt

  def bounds(self):
    """
    Return the bounds of the geometry.
    """
    return self._shape.bounds

  def equals(self, geom, srid_compare=True):
    """
    Check if two geometries are equal.
    """
    lft_srid = geos.lgeos.GEOSGetSRID(self._shape._geom)
    rgt_srid = geos.lgeos.GEOSGetSRID(geom._shape._geom)
    if srid_compare and lft_srid != rgt_srid:
      return False
    return self._shape.equals(geom._shape)
