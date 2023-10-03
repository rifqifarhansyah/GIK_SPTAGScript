import numpy as np

def fvecs_read(filename, c_contiguous=True):
    fv = np.fromfile(filename, dtype=np.float32)
    if fv.size == 0:
        return np.zeros((0, 0))
    dim = fv.view(np.int32)[0]
    assert dim > 0
    fv = fv.reshape(-1, 1 + dim)
    if not all(fv.view(np.int32)[:, 0] == dim):
        raise IOError("Non-uniform vector sizes in " + filename)
    fv = fv[:, 1:]
    if c_contiguous:
        fv = fv.copy()
    return fv

# Nama file yang ingin Anda baca
input_filename = "sift_query.fvecs"

# Memanggil fungsi untuk membaca data dari file
array_fv = fvecs_read(input_filename)

# Menampilkan array di terminal
print("Array fv:")
print(array_fv)

# Menyimpan array ke dalam file 'array.txt'
output_filename = "array.txt"
np.savetxt(output_filename, array_fv)

print(f"Array telah disimpan dalam file {output_filename}")
