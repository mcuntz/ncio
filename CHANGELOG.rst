Changelog
---------

v1.x (??? 2024)
   * Change build and coverage status to main branch.

v1.0 (Sep 2024)
   * First standalone release at Github.

v0.13 (Sep 2024)
   * Make `ncio` a standalone package.
   * Remove wrappers `readnetcdf` and `infonetcdf`.

v0.12 (Sep 2024)
   * Delete test for float128 because no 128-bit datatype in netcdf.

v0.11 (Dec 2023)
   * Adding global attributes (addglobalatt) in `copy_file`.

v0.10 (Sep 2023)
   * Added _FillValue and missing_value to netcdf test files.

v0.9 (Jul 2023)
   * `get_variable_definition` returns _FillValue if present and only
     missing_value if _FillValue is not present.
   * `create_variables` sets missing_value attribute if present even
     if used for _FillValue.

v0.8 (Apr 2023)
   * Make `get_variable_definition` public.

v0.6 (Dec 2022)
   * Skip test for float128 on Windows.

v0.5 (Jun 2022)
   * Delete unnecessary HDF5 filters in variable definition for
     compatibility with netcdf4 > 1.6.0.

v0.4 (May 2022)
   * Added `ncio` as submodule to `pyjams`.
   * Rename functions, e.g. `create_dimensions` -> `copy_dimensions`.
   * Add function `copy_variables`.

v0.3 (Dec 2021)
   * Add timedim in `create_variables`.

v0.2 (Mar 2021)
   * Added `get_fill_value_for_dtype`.
   * Added `create_new_variable`.
   * Make it flake8 compatible.
   * Remove keyword in `copy_global_attributes`.

v0.1 (Apr 2020)
   * Written by Matthias Cuntz (mc (at) macu (dot) de).
