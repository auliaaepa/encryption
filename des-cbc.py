import argparse

# Ukuran block dalam bit
BLOCK_SIZE = 64

# Tabel permutasi untuk round key (PC-1: 64 -> 56 bits)
PERMUTED_CHOICE_1 = [57, 49, 41, 33, 25, 17,  9,
                      1, 58, 50, 42, 34, 26, 18,
                     10,  2, 59, 51, 43, 35, 27,
                     19, 11,  3, 60, 52, 44, 36,
                     63, 55, 47, 39, 31, 23, 15,
                      7, 62, 54, 46, 38, 30, 22,
                     14,  6, 61, 53, 45, 37, 29,
                     21, 13,  5, 28, 20, 12,  4]
# Tabel shifting untuk round key (left circular shift)
SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2,
               1, 2, 2, 2, 2, 2, 2, 1]
# Tabel permutasi untuk round key (PC-2: 56 -> 48 bits)
PERMUTED_CHOICE_2 = [14, 17, 11, 24,  1,  5,
                      3, 28, 15,  6, 21, 10,
                     23, 19, 12,  4, 26,  8,
                     16,  7, 27, 20, 13,  2,
                     41, 52, 31, 37, 47, 55,
                     30, 40, 51, 45, 33, 48,
                     44, 49, 39, 56, 34, 53,
                     46, 42, 50, 36, 29, 32]

# Tabel permutasi untuk input text (Intial Permutation)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17,  9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]
# Tabel ekspansi untuk separuh input text (Expansion: 32 -> 48 bits)
EXPANSION_TABLE = [32,  1,  2,  3,  4,  5,
                    4,  5,  6,  7,  8,  9,
                    8,  9, 10, 11, 12, 13, 
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29,
                   28, 29, 30, 31, 32,  1]
# Tabel sbox untuk separuh input text (S-Box: 48 -> 32 bits)
SBOX = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
# Tabel permutasi untuk separuh input text (P-Box)
PERMUTATION_TABLE = [16,  7, 20, 21,
                     29, 12, 28, 17,
                      1, 15, 23, 26,
                      5, 18, 31, 10,
                      2,  8, 24, 14,
                     32, 27,  3,  9,
                     19, 13, 30,  6,
                     22, 11,  4, 25]
# Tabel permutasi untuk input text (Inverse Initial Permutation)
INVERSE_IP = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

def ascii_to_hex(ascii):
    """convert ascii ke hexadecimal"""
    return ascii.hex()

def hex_to_bin(hex):
    """convert hexadecimal ke binary"""
    return f'{int(hex, 16):0{(len(hex)*4)}b}'

def bin_to_ascii(bin):
    """convert binary ke ascii"""
    return ''.join(chr(int(bin[i:i+8], 2)) for i in range(0, len(bin), 8))

def rpadding(bin):
    """menambahkan padding '0' ke sebelah kanan block hingga block size tercapai"""
    return bin + '0' * ((BLOCK_SIZE - len(bin) % BLOCK_SIZE) % BLOCK_SIZE)

def lpadding(bin):
    """menambahkan padding '0' ke sebelah kiri block hingga block size tercapai"""
    return '0' * (BLOCK_SIZE - len(bin)) + bin

def xor(bin_1, bin_2):
    """xor binary block 1 dengan binary block 2"""
    return f'{int(bin_1, 2) ^ int(bin_2, 2):0{len(bin_1)}b}'

def left_circular_shift(block, n_shifts):
    """left circular shift sebanyak n_shifts"""
    return block[n_shifts:] + block[:n_shifts]

def permute(block, permutation_table):
    """permutasi/mapping block sesuai tabel permutasi (index)"""
    return ''.join(block[i-1] for i in permutation_table)

def split(block):
    """split block menjadi 2 bagian: left dan right"""
    middle = len(block)//2
    return block[:middle], block[middle:]

def generate_round_keys(key):
    """men-generate 16 round keys"""
    # permutasi key dengan tabel PC-1 untuk permutasi dan meng-drop parity bits (8th bits) (64 -> 56 bits)
    key = permute(key, PERMUTED_CHOICE_1)

    round_keys = []
    lroundkey, rroundkey = split(key) # split hasil permutasi pc-1 key menjadi bagian kiri dan kanan
    for i in range(16):
        # left circular shift untuk setiap bagian kiri dan kanan round key
        lroundkey = left_circular_shift(lroundkey, SHIFT_TABLE[i])
        rroundkey = left_circular_shift(rroundkey, SHIFT_TABLE[i])
        # permutasi round key dengan tabel PC-2 (56 -> 48 bits)
        round_key = lroundkey + rroundkey
        round_key = permute(round_key, PERMUTED_CHOICE_2)
        # simpan round key ke dalam list
        round_keys.append(round_key)

    return round_keys

def permute_sbox(block):
    """permutasi block dengan s-box: membagi 48 bits ke dalam 8 grup (6 bits) dan mengambil 4 bits darinya (48 -> 32 bits)"""
    permuted_block = ""
    for i in range(8):
        # row: ujung kanan dan kiri
        row = int(block[i*6] + block[i*6+5], 2)
        # column: sisanya (tengah)
        col = int(block[i*6+1:i*6+5], 2)
        # permutasi dengan s-box berdasarkan grup, row, dan column yang diperoleh
        permuted_block += f'{SBOX[i][row][col]:04b}'
    return permuted_block

def round_function(block, round_key):
    """memproses round function untuk separuh bagian input"""
    # permutasi block dengan exspansion table (32 -> 48 bits)
    block = permute(block, EXPANSION_TABLE)
    # xor hasil ekspansi dengan round key yang sesuai
    block = xor(block, round_key)
    # permutasi hasil xor dengan s-box (48 -> 32 bits)
    block = permute_sbox(block)
    # permutasi hasil s-box dengan p-box
    block = permute(block, PERMUTATION_TABLE)
    return block

def des(block, round_keys):
    """memproses data encryption standart"""
    # permutasi block dengan initial permutation
    block = permute(block, IP)
    print("INITIAL PERMUTATION:", block)

    # perhitungan round
    lblock, rblock = split(block)
    for i in range(16):
        # left=right dan right=left xor hasil round function
        lblock, rblock = rblock, xor(lblock, round_function(rblock, round_keys[i]))   
        print(f"ROUND {i+1:>2}:", lblock, rblock)
    
    # 32 bits swap
    block = rblock + lblock
    print(f"BIT SWAP:", block)
    
    # permutasi block dengan inverse initial permutation
    block = permute(block, INVERSE_IP)
    print(f"INVERSE INITIAL PERMUTATION:", block)
    return block

def cbc(option, input_file, output_file, iv_file, key_file):
    input = input_file.read()
    if input_file: input_file.close()
    input = ascii_to_hex(input)
    input = hex_to_bin(input)
    if len(input) < BLOCK_SIZE: raise ValueError(f'The length of the input binary cannot be less than {BLOCK_SIZE} bits')
    input = rpadding(input)
    print("INPUT\t\t:", input)

    key = key_file.read()
    if key_file: key_file.close()
    if key: key = hex_to_bin(key)
    if len(key) > BLOCK_SIZE: raise ValueError(f'The length of the key binary cannot be more than {BLOCK_SIZE} bits')
    key = lpadding(key)
    print("KEY\t\t:", key)

    iv = iv_file.read()    
    if iv_file: iv_file.close()
    if iv: iv = hex_to_bin(iv)
    if len(iv) > BLOCK_SIZE: raise ValueError(f'The length of the iv binary cannot be more than {BLOCK_SIZE} bits')
    iv = lpadding(iv)
    print("IV\t\t:", iv)

    round_keys = generate_round_keys(key)
    if option == "decryption": round_keys = round_keys[::-1] # membalik urutan round keys untuk dekripsi
    print("ROUND KEYS\t:", round_keys)

    output = ""
    latest_cipher = iv
    for i, j in enumerate(range(0, len(input), BLOCK_SIZE)):
        print(f"\nBLOCK {i+1}")
        block = input[j:j+BLOCK_SIZE]
        print("BLOCK:", block)
        if option == "encryption":
            result = xor(block, latest_cipher)
            print("XOR:", result)
            result = des(result, round_keys)
            latest_cipher = result
        elif option == "decryption":
            result = des(block, round_keys)
            result = xor(result, latest_cipher)
            print("XOR:", result)
            latest_cipher = block
        output += result

    print("\nOUTPUT:", output)
    output = bin_to_ascii(output)
    output = output.rstrip('\x00').encode('ISO-8859-1') # menghapus null charcater dan encode dengan latin-1 (single bit)
    print("ENCODED ASCII:", output)
    output_file.write(output)
    if output_file: output_file.close()
        
if __name__ == '__main__':
    # define argument parser (untuk mendapatkan option dan file-file yang diperlukan)
    parser = argparse.ArgumentParser(prog = 'des-cbc.py', description = 'Program to perform encryption and decryption using DES-CBC',)
    parser.add_argument('-o', '--option', dest='option', choices=['encryption', 'decryption'], help="an option between encryption and decryption", required=True)
    parser.add_argument('--input', dest='input_file', type=argparse.FileType('rb'), help="(ascii) input file to be used for encryption/decryption", required=True)
    parser.add_argument('--output', dest='output_file', type=argparse.FileType('wb'), help="(ascii) output file to be used for encryption/decryption", required=True)
    parser.add_argument('--iv', dest='iv_file', type=argparse.FileType('r'), help="(hexadecimal) initial value (iv) file to be used for encryption/decryption", required=True)
    parser.add_argument('--key', dest='key_file', type=argparse.FileType('r'), help="(hexadecimal) key file to be used for encryption/decryption", required=True)
    
    try:
        # mendapatkan arguments
        args = parser.parse_args()
        # proses des-cbc dengan arguments yang diberikan
        cbc(args.option, args.input_file, args.output_file, args.iv_file, args.key_file)
    except ValueError as ve:
        print("ValueError:", ve)
    except Exception as e:
        print("Exception:", repr(e))