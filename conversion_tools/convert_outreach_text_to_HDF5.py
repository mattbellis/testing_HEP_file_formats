import ryans_code as rt

import sys

infile = sys.argv[1]

#outfilebase = infile.split('.')[0]
#hdf5out = rt.create_file(outfilebase)

rt.cms_conversion(infile)
