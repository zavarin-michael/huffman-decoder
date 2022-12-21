import bisect

def bits(f):
    bytes = f
    for b in bytes:
        for i in range(8):
            yield (b >> i) & 1

class HuffmanNode:

    def __init__(self, s=None, left=None, right=None, c=None, parent=None):
        self.s = s
        self.left = left
        self.right = right
        self.parent = parent
        self.c = c

    def get_code(self, fr=None):
        parent_code = "" if self.parent is None else self.parent.get_code(self)
        if parent_code is None:
            return parent_code

        if fr is not None:
            if fr == self.left:
                return parent_code + "1"
            if fr == self.right:
                return parent_code + "0"
            return None
        return parent_code


    def build_tree_by_code(self, code, i, c):
        if i == len(code):
            self.c = c
            return

        if code[i] == '1':
            if self.left is None:
                self.left = HuffmanNode()
            self.left.build_tree_by_code(code, i + 1, c)
            return
        if code[i] == '0':
            if self.right is None:
                self.right = HuffmanNode()
            self.right.build_tree_by_code(code, i + 1, c)
            return


    def get_c(self, iterator):
        if self.c is not None:
            return self.c

        c = next(iterator)
       # print(c, end="")

        if c == 1:
            if self.left is None:
                raise Exception
            return self.left.get_c(iterator)
        if c == 0:
            if self.right is None:
                raise Exception
            return self.right.get_c(iterator)


class HuffmanArchiver:
    start_end_symbol = 255
    separator = 254

    def __init__(self):
        pass

    def encode_string(self, s):
        dictionary = self.form_dictionary(s)
        codes = self.create_tree(dictionary)
        return self.encode_with_format(codes, s)


    def encode_with_format(self, codes, s):
        output_b = HuffmanArchiver.start_end_symbol.to_bytes(4, 'little')
        for i in codes:
            output_b += ord(i).to_bytes(4, 'little')
            for j in codes[i]:
                output_b += int(j, 2).to_bytes(1, 'little')
            output_b += HuffmanArchiver.separator.to_bytes(1, 'little')
        output_b += HuffmanArchiver.start_end_symbol.to_bytes(4, 'little')

        output = []
        length = len(s)
        percent = 0
        for i in range(len(s)):
            if i / length * 100 > percent:
                percent += 1
                print(f"{percent}%")
            output.append(codes[s[i]])
        output = "".join(output)

        output_b += len(s).to_bytes(8, 'little')

        output += "1"
        output = output[::-1]
        output = int(output, 2)

        # bits_iter = iter(bits(output.to_bytes((output.bit_length() + 7) // 8, 'little')))
        # while (b := next(bits_iter, None)) is not None:
        #     print(b, end="")
        # print()

        output_b += output.to_bytes((output.bit_length() + 7) // 8, 'little')
        return output_b


    def form_dictionary(self, s):
        dictionary = {}
        for i in s:
            if i in dictionary:
                dictionary[i] += 1
            else:
                dictionary[i] = 1
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}

    def create_tree(self, dictionary):
        l = [HuffmanNode(v, c=k) for k, v in sorted(dictionary.items(), key=lambda item: item[1])]
        if len(l) == 0:
            return None
        elif len(l) == 1:
            return {l[0].c: "0"}

        k = {i.c: i for i in l}
        while len(l) >= 2:
            new = HuffmanNode(l[0].s + l[1].s, l[0], l[1])
            l[0].parent = new
            l.pop(0)
            l[0].parent = new
            l.pop(0)
            bisect.insort(l, new, key=lambda x: x.s)

        return {key: k[key].get_code() for key in k}


    def restore_codes(self, bitstring):
        if int.from_bytes(bitstring[0: 4], byteorder='little') != HuffmanArchiver.start_end_symbol:
            raise Exception
        i = 4
        codes = {}

        while int.from_bytes(bitstring[i: i+4], byteorder='little') != HuffmanArchiver.start_end_symbol:
            k = bitstring[i:i+4].decode("utf-32")
            i += 4
            v = ""
            while bitstring[i] != HuffmanArchiver.separator:
                v += str(bitstring[i])
                i += 1
            codes[k] = v
            i += 1

        i += 4

        length = int.from_bytes(bitstring[i: i + 8], byteorder='little')
        i += 8

        return codes, i, length


    def restore_tree(self, codes):
        root = HuffmanNode()
        for k, v in codes.items():
            root.build_tree_by_code(v, 0, k)
        return root


    def restore_string_by_codes(self, codes, bitstring, tree, length):
        output = []
        percent = 0
        bits_iter = iter(bits(bitstring))
        i = 0
        while i < length:
            if i / length * 100 > percent:
                percent += 1
                print(f"{percent}%")
            i += 1
            output.append(tree.get_c(bits_iter))

        return "".join(output)


    def decode_string(self, bitstring):
        codes, i, length = self.restore_codes(bitstring)
        tree = self.restore_tree(codes)
        return self.restore_string_by_codes(codes, bitstring[i::], tree, length)


