from argparse import ArgumentParser

description = 'testing for passing multiple arguments and to get list of args'
parser = ArgumentParser(description=description)
parser.add_argument('-i', '--item', action='store', dest='alist',
                    type=str, nargs=5,
                    help='-i <<dev path(xml)>> <<prod path(xml)>> <<destination path(xml)>> <<jobs to be merged>> <<output old->new mapping path(csv)>> [python xmlparser.py C:/Users/rgu107/Desktop/comp/sample1.xml C:/Users/rgu107/Desktop/comp/sample2.xml C:/Users/rgu107/Desktop/comp/output1.xml J10,J11 C:/Users/rgu107/Desktop/comp/mapping.csv]')
opts = parser.parse_args()

print("List of items: {}".format(opts.alist))
