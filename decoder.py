import argparse
import sys

from hash import create_hashfile, md5, check_hash
from huffman import HuffmanArchiver


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['encode', 'decode', 'hashcheck'])
    parser.add_argument('-fn', '--filename', type=str, required=True)
    parser.add_argument('-to', type=argparse.FileType("w"))
    parser.add_argument('-cto', type=argparse.FileType())

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.filename is None:
        print('Error: no input file. Use -fn or --filename to specify input file')
        exit(1)
    filename = namespace.filename

    if namespace.action == 'encode':
        try:
            with open(filename, 'r') as f:
                bitstring = HuffmanArchiver().encode_string(f.read())
            with open(filename.split('.')[0] + '.huf', 'wb') as f:
                f.write(bitstring)
            create_hashfile(md5(filename), filename)
        except FileNotFoundError as e:
            print('Error: no such input file')
    elif namespace.action == 'decode':
        if namespace.to is None:
            print('Error: no output file')
            exit(1)
        with open(filename, 'rb') as file:
            string = HuffmanArchiver().decode_string(file.read())
        namespace.to.write(string)
    elif namespace.action == 'hashcheck':
        tr = check_hash(md5(filename), namespace.cto.name)
        if tr:
            print("{}".format('Hashes are the same'))
        else:
            print("{}".format('Hashes are different'))
