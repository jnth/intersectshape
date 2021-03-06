==============
Intersectshape
==============

Reverse geocoding from a shapefile of polygons.


How ?
-----


The ``ReverseGeolocShapefile`` class improves the ``shapefile.Reader`` class by
adding a ``intersection`` method to find polygons that intersects with a single
point.

I use a simple spatial index that store the bounding box of each polygons.
I save these informations into a ``.sidx.npy`` file next to the ``.dbf``/``.shp``
files.

Works with Python 3.6+ (I'm using f-string).


Documentation
-------------

The ``intersection`` method of the ``ReverseGeolocShapefile`` class return a list
of row index.


Usage
-----

::

    import intersectshape

    shp = intersectshape.ReverseGeolocShapefile('/path/of/shapefile.shp')

    # You can use all methods of shapefile.Reader object like...
    row = shp.record(5)
    geo = shp.shape(2)

    # Find polygons that intersects a point
    x, y = 200, 500  # must be at the same projection system
    ids = shp.intersection(x, y)
    print(ids)
    # return [] or [0, 5, 9, 7] for example.


License
-------

This code are under the `GNU GPL v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_ licence.

Data of French communal polygons (Geofla shapefile located in the `data`
folder) are under `Etalab Open License <https://www.etalab.gouv.fr/licence-ouverte-open-licence>`_.
