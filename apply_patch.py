"""apply_patch.py — áp bản vá tiếng Việt The Legend of Dragoon (USA) lên đĩa gốc.

Cách dùng:  python apply_patch.py "<đường dẫn đĩa gốc .bin>"
  - Tự nhận đĩa 1/2/3/4 theo SHA-256 của file .bin gốc (bản USA, 1 track MODE2/2352).
  - Áp file LoD-DiscN-vi.ppf nằm cùng thư mục với script này.
  - Ghi ra "The Legend of Dragoon (Disc N) (VN).bin" + ".cue" cạnh file gốc, kiểm SHA-256 kết quả.
Chỉ dùng thư viện chuẩn Python 3.
"""
import os, sys, struct, hashlib

DISCS = {
    1: ('049393ab69cfd66a12750158098358e8735628a75e2c517e0336e55bbcb67848',
        '3bca142fba929dcd9aca413cf85f0d49395ad634318475d0cae19ce41503dc3b'),
    2: ('cfbfcfda1283e85516efd73a60c74d4f44389f7dec7e1c39b6653052ab015ce8',
        '6de00991dcfbb3be3f9899f96a40d064376ccb11a80eac567db9e0a2046c7203'),
    3: ('445aa8f320b33e1703c744a63ad4efc797fa9c87bda30774f88402c0311c65ac',
        '562be3f91677d9a062c56958792db2bd801857d955d9262920c254b2796551b0'),
    4: ('205909877b0fe5fc40905f7cf6dd61dbd735f2670f3346ccf719f7fdaf3aa744',
        '80a82bbe349c04331b35a1fa969319097bf04bb6d62936081bfbaf7e93043193'),
}


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''):
            h.update(b)
    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print('Cách dùng: python apply_patch.py "<đĩa gốc .bin>"')
        return 1
    src = sys.argv[1]
    print('Đang kiểm tra đĩa gốc...')
    s = sha(src)
    dn = next((d for d, (a, b) in DISCS.items() if a == s), None)
    if dn is None:
        print('Không nhận ra đĩa (SHA-256 %s).' % s)
        print('Cần bản The Legend of Dragoon (USA) gốc, định dạng .bin 1 track (Redump).')
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    ppf = os.path.join(here, 'LoD-Disc%d-vi.ppf' % dn)
    buf = open(ppf, 'rb').read()
    if buf[:5] != b'PPF30' or buf[5] != 2:
        print('File PPF hỏng: %s' % ppf)
        return 1
    name = 'The Legend of Dragoon (Disc %d) (VN)' % dn
    outdir = os.path.dirname(os.path.abspath(src))
    dst = os.path.join(outdir, name + '.bin')
    print('Đĩa %d. Đang áp bản vá...' % dn)
    with open(src, 'rb') as fi, open(dst, 'wb') as fo:
        for b in iter(lambda: fi.read(1 << 24), b''):
            fo.write(b)
    with open(dst, 'r+b') as fo:
        p = 60
        while p < len(buf):
            off = struct.unpack_from('<Q', buf, p)[0]
            ln = buf[p + 8]
            fo.seek(off)
            fo.write(buf[p + 9:p + 9 + ln])
            p += 9 + ln
    print('Đang kiểm tra kết quả...')
    if sha(dst) != DISCS[dn][1]:
        print('LỖI: kết quả không khớp SHA-256 mong đợi. Đã xoá file hỏng.')
        os.remove(dst)
        return 1
    with open(os.path.join(outdir, name + '.cue'), 'w', encoding='ascii') as f:
        f.write('FILE "%s.bin" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n' % name)
    print('Xong! Đã tạo:\n  %s\n  %s' % (dst, os.path.join(outdir, name + '.cue')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
