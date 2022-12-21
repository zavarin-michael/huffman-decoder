import argparse
import sys

from huffman import HuffmanArchiver


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['encode', 'decode'])
    parser.add_argument('-fn', '--filename', type=str, required=True)
    parser.add_argument('-to', type=argparse.FileType("w"))

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
        except FileNotFoundError as e:
            print('Error: no such input file')

    else:
        if namespace.to is None:
            print('Error: no output file')
            exit(1)
        with open(filename, 'rb') as file:
            string = HuffmanArchiver().decode_string(file.read())
        namespace.to.write(string)
