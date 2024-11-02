ncio - work easily with netcdf files
====================================

A small Python library providing functions to copy easily a netcdf
file while replacing and transforming variables and dimensions.

|DOI| |PyPI version| |Conda version| |License| |Build Status| |Coverage Status|


About ncio
----------

``ncio`` is a Python library that provides functions to copy
dimensions, variables, attributes, etc. from one netcdf file to a
netcdf output file. Replacements and transformations can be performed
on the copied entities such as names can be changed or variables can
be replaced with other data. It is a thin wrapper of the netCDF4_
Python package that adds no new functionality but rather provides
convenience functions to work easily with netcdf files.

The complete documentation for ``ncio`` is available at Github
pages:

   https://mcuntz.github.io/ncio/


copy_file
---------

``ncio`` provides the functions ``ncio.copy_dimensions``,
``ncio.copy_global_attributes``, and ``ncio.copy_variables`` to copy
dimensions, attributes, and variables from one netcdf file to
another. The functions have the keywords `renamedim`, `removedim`,
`changedim`, `adddim`, `renamevar`, `removevar`, `replacevar`, and
`replaceatt`, which purpose should be rather mnemonic. There is also
the function ``ncio.copy_file`` that combines the three individual
routines in a single function.

Imagine you have a netcdf file that contains the variable `gpp`, among
others. You want to have an output file, which is the same as the
input file except that `gpp` should be doubled. This could be done,
for example, as:

.. code:: python

   import ncio

   ifile = 'basic_gpp.nc'
   ofile = 'gppx2.nc'

   # read current 'gpp' array
   gpp = ncio.ncread(ifile, 'gpp')

   # copy file by replacing gpp by double its value
   ncio.copy_file(ifile, ofile, replacevar={'gpp': {'gpp': 2. * gpp}})

Here the convenience function ``ncio.ncread`` was used that simply reads
the given variable from a netcdf file.

There is also the convenience function ``ncio.ncinfo``, where one can
inquire about `dimensions` in the file, `variables`, their
`long_names` and `units` or all attributes. One could, for example,
assert that the variable gpp is present before reading it:

.. code:: python

   # read current 'gpp' array
   assert 'gpp' in ncio.ncinfo(ifile, variables=True), (
       f'Variable "gpp" not in input file {ifile}')
   gpp = ncio.ncread(ifile, 'gpp')

If you set the keyword `noclose=True` in ``ncio.copy_file``, then it
does not close the file and returns the file handle. You can then
still manipulate the contents of the file. The doubling of gpp could
hence also be done as:

.. code:: python

   import ncio

   ifile = 'basic_gpp.nc'
   ofile = 'gppx2.nc'

   # read current 'gpp' array
   assert 'gpp' in ncio.ncinfo(ifile, variables=True), (
       f'Variable "gpp" not in input file {ifile}')
   gpp = ncio.ncread(ifile, 'gpp')

   # copy file, then directly access gpp variable in putput file
   fo = ncio.copy_file(ifile, ofile, noclose=True)
   ovar = fo.variables['gpp']
   ovar[:] = ovar[:] * 2.
   fo.close()

A slightly extended example could be to produce a suite of scenarios
with respiration (resp) having global annual values between say 120
and 170 and the spatial pattern of gpp. If the input file has monthly
global gpp fields for several years, this would be:

.. code:: python

   import ncio

   ifile = 'basic_gpp.nc'

   # read current 'gpp' array
   assert 'gpp' in ncio.ncinfo(ifile, variables=True), (
       f'Variable "gpp" not in input file {ifile}')
   gpp = ncio.ncread(ifile, 'gpp')
   isglobalgpp = gpp.mean() * 12.

   for g in [140, 150, 160, 170]:
       ofile = f'resp{g}.nc'
       hist  = (f'Modified {ifile} to produce resp with the distribution'
                f' of gpp but with an annual mean of {g} PgC/a.')
       ncio.copy_file(ifile, ofile,
                      replacevar={'gpp': {'resp': gpp * (g / isglobalgpp)}},
                      replaceatt={'resp':
                                     {'long_name':
                                      'Terrestrial Ecosystem Respiration',
                                      'units': 'kg gridcell-1 s-1'}},
                       addglobalatt={'history': hist})


Individual copy routines
------------------------

Using the individual functions gives more flexibility, of
course. Imagine you have an input file that has monthly fields on a
global grid on Earth, i.e. having dimensions `(time, lon, lat)`. The
land grid cells of the vegetation variables have the extra dimension
`patch` for fractions of different plant functional types in the same
grid cell, i.e. having dimensions `(time, lon, lat, patch)` or `(time,
patch, lon, lat)`. There is an associated variable `patchfrac` that
gives the fixed relative sizes of each patch. To get the average of
the grid cell, the vegetation variables have to be multiplied by
`patchfrac` and summed over the `patch` dimension. We will first set
all metadata in the output file, then copy the variables that have no
unlimited dimension `time`, and then the variables having a `time`
dimensions. The latter will be copied timestep per timestep to avoid
Python swapping variables to disk or out-of-memory:

.. code:: python

   import sys
   import time
   import netCDF4 as nc
   import ncio

   ifile = 'patch.nc'
   ofile = 'nopatch.nc'

   # check input file
   assert 'patchfrac' in ncio.ncinfo(ifile, variables=True), (
       f'No patchfrac variable in input file {ifile}')
   assert 'patch' in ncio.ncinfo(ifile, var='patchfrac', dims=True)

   # open input and output files
   fi = nc.Dataset(ifile, 'r')
   if 'file_format' in dir(fi):
       fo = nc.Dataset(ofile, 'w', format=fi.file_format)
   else:
       fo = nc.Dataset(ofile, 'w', format='NETCDF3_64BIT_OFFSET')

   # copy global attributes, adding script
   ncio.copy_global_attributes(fi, fo,
                               add={'history': (
	                              time.asctime() + ': ' +
                                      ' '.join(sys.argv))})

   # copy dimensions
   ncio.copy_dimensions(fi, fo, removedim=['patch'])

   # create static variables (independent of time)
   ncio.create_variables(fi, fo, time=False, removedim=['patch'])

   # create dynamic variables (time dependent)
   ncio.create_variables(fi, fo, time=True, removedim=['patch'])

   # get patchfrac
   patchfrac = fi.variables['patchfrac']

   # copy static variables
   for ivar in fi.variables.values():
       if 'time' not in ivar.dimensions:
           ovar  = fo.variables[ivar.name]
           invar = ivar[:]
           if 'patch' in ivar.dimensions:
               idx = ivar.dimensions.index('patch')
	       # use patchfrac at first time step for non-time
	       # dependent variables
               out = np.sum(invar * patchfrac, axis=idx)
           else:
               out = invar
           ovar[:] = out

   # copy dynamic variables
   ntime = fi.dimensions['time'].size
   for tt in range(ntime):
       for ivar in fi.variables.values():
           if 'time' in ivar.dimensions:
               ovar = fo.variables[ivar.name]
               invar = ivar[tt, ...]
               if 'patch' in ivar.dimensions:
                   # -1 because of specific timestep
                   idx = ivar.dimensions.index('patch') - 1
                   out = np.sum(invar * patchfrac, axis=idx)
               else:
                   out = invar
               ovar[tt, ...] = out

   # finish
   fi.close()
   fo.close()


Installation
------------

The easiest way to install is via `pip`:

.. code-block:: bash

   pip install ncio

or via `conda`:

.. code-block:: bash

   conda install -c conda-forge ncio

Requirements
   * numpy_
   * netCDF4_


License
-------

``ncio`` is distributed under the MIT License. See the `LICENSE`_ file
for details.

Copyright (c) 2020- Matthias Cuntz


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.13851994.svg
   :target: https://doi.org/10.5281/zenodo.13851994
.. |PyPI version| image:: https://badge.fury.io/py/ncio.svg
   :target: https://badge.fury.io/py/ncio
.. |Conda version| image:: https://anaconda.org/conda-forge/ncio/badges/version.svg
   :target: https://anaconda.org/conda-forge/ncio
.. |License| image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/mcuntz/ncio/blob/master/LICENSE
.. |Build Status| image:: https://github.com/mcuntz/ncio/actions/workflows/main.yml/badge.svg
   :target: https://github.com/mcuntz/ncio/actions/workflows/main.yml
.. |Coverage Status| image:: https://coveralls.io/repos/github/mcuntz/ncio/badge.svg?branch=main
   :target: https://coveralls.io/github/mcuntz/ncio?branch=main

.. _LICENSE: https://github.com/mcuntz/ncio/LICENSE
.. _matplotlib: https://matplotlib.org/
.. _netCDF4: https://github.com/Unidata/netcdf4-python
.. _numpy: https://numpy.org/
