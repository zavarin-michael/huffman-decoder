import hashlib
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_hashfile(hash, filename):
    with open(f"{filename.split('.')[0]}.hash", "w") as f:
        f.write(hash)


def check_hash(hash, filename):
    with open(filename, "r") as f:
        s = f.readline()
        print(hash, s)
        if hash == s:
            return True
        else:
            return False



