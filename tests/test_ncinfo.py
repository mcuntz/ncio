#!/usr/bin/env python
"""
This is the unittest for ncinfo module.

python -m unittest -v tests/test_ncinfo.py
python -m pytest --cov=ncio --cov-report term-missing -v tests/test_ncinfo.py

"""
import unittest


class TestNcinfo(unittest.TestCase):
    """
    Tests for ncinfo.py
    """

    def test_ncinfo(self):
        from ncio import ncinfo

        ncfile = 'tests/test_ncread.nc'

        # variables
        fout = ncinfo(ncfile, variables=True)
        fsoll = ['is1', 'is2', 'x', 'y']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # variables, sort
        fout = ncinfo(ncfile, variables=True, sort=False)
        fsoll = ['x', 'y', 'is1', 'is2']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        fout = ncinfo(ncfile, variables=True, sort=True)
        fsoll = ['is1', 'is2', 'x', 'y']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # codes
        fout = ncinfo(ncfile, codes=True)
        fsoll = [128, 129, -1, -1]
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # codes, sort
        fout = ncinfo(ncfile, codes=True, sort=False)
        fsoll = [-1, -1, 128, 129]
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        fout = ncinfo(ncfile, codes=True, sort=True)
        fsoll = [128, 129, -1, -1]
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # units
        fout = ncinfo(ncfile, units=True)
        fsoll = ['arbitrary', 'arbitrary', 'xx', 'yy']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # units, sort
        fout = ncinfo(ncfile, units=True, sort=False)
        fsoll = ['xx', 'yy', 'arbitrary', 'arbitrary']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        fout = ncinfo(ncfile, units=True, sort=True)
        fsoll = ['arbitrary', 'arbitrary', 'xx', 'yy']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # long_names
        fout = ncinfo(ncfile, long_names=True)
        fsoll = ['all ones', 'all twos', 'x-axis', 'y-axis']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # long_names, sort
        fout = ncinfo(ncfile, long_names=True, sort=False)
        fsoll = ['x-axis', 'y-axis', 'all ones', 'all twos']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        fout = ncinfo(ncfile, long_names=True, sort=True)
        fsoll = ['all ones', 'all twos', 'x-axis', 'y-axis']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # dims, var
        fout = ncinfo(ncfile, var='is1', dims=True)
        fsoll = ('y', 'x')
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # dims, code
        fout = ncinfo(ncfile, code=128, dims=True)
        fsoll = ('y', 'x')
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # shape, var
        fout = ncinfo(ncfile, var='is1', shape=True)
        fsoll = (2, 4)
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # shape, code
        fout = ncinfo(ncfile, code=128, shape=True)
        fsoll = (2, 4)
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # variable attributes, var
        fout = ncinfo(ncfile, var='is1', attributes=True)
        fsoll = ['_FillValue', 'code', 'long_name', 'missing_value',
                 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # variable attributes, var
        fout = ncinfo(ncfile, 'is1', attributes=True)
        fsoll = ['_FillValue', 'code', 'long_name', 'missing_value',
                 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # variable attributes, code
        fout = ncinfo(ncfile, code=128, attributes=True)
        fsoll = ['_FillValue', 'code', 'long_name', 'missing_value',
                 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # file attributes
        fout = ncinfo(ncfile, attributes=True)
        fsoll = ['creator', 'history', 'NCO']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # no keyword
        fout = ncinfo(ncfile)
        fsoll = None
        assert fout is fsoll

        # errors
        # dims, no var
        self.assertRaises(ValueError, ncinfo, ncfile, dims=True)
        # dims, var does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, dims=True,
                          var='is3')
        # dims, code does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, dims=True,
                          code=130)
        # shape, no var
        self.assertRaises(ValueError, ncinfo, ncfile, shape=True)
        # shape, var does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, shape=True,
                          var='is3')
        # shape, code does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, shape=True,
                          code=130)
        # attributes, var does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, attributes=True,
                          var='is3')
        # attributes, code does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, attributes=True,
                          code=130)


if __name__ == "__main__":
    unittest.main()
