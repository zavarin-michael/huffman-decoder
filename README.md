# Huffman decoder
- To encode a file, run:
```
python decoder.py encode -fn <file>
```
>where `<file>` is the path to the file to be encoded. For example run `python decoder.py encode -fn vim.txt`

-To decode file, run:
```
python decoder.py decode -fn <file>.huf -to <decoded_file>
```
>where `<file>` is the path to the file to be decoded and `<decoded_file>` is the path to the decoded file. For example run `python decoder.py decode -fn vim.huf -to vim_decoded.txt`

-To check hashes, run:
```
python decoder.py hashcheck -fn <file> -cto <file>.hash
```
>where `<file>` is the path to the file to take hash and `<file>.hash` is the path to the comparing hash. For example run `python decoder.py hashcheck -fn vim_decoded.txt -cto vim.hash`
