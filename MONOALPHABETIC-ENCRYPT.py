if __name__ == "__main__":

    print("TUGAS MONOALPHABETIC CIPHER")
    print("Enkripsi")
    print("Masukkan plain-text (plaintext hanya huruf kapital dan spasi) :")
    #input menggunakan method isupper untuk memastikan semua adalah huruf kapital
    while True :
        plain_text = input().strip()
        plain_text = plain_text.replace(" ", "")
        if plain_text.isupper() :
            break
    #jika ada yg bukan huruf kapital maka user diminta menginput ulang    
        else :
            print("Plain-text hanya boleh huruf kapital")
            print("Masukkan plain text:")

    print("Masukkan key (harus kapital dan unik sejumlah 26) :")
    while True :
        #inputan key harus kapital semua dan harus memiliki panjang 26, maka menggunakan method isupper DAN len set 26
        key = input().strip()
        if len(set(key)) == 26 and key.isupper() :
            break
        else :
            #jika tidak, user harus menginput ulang key nya
            print("Ikuti aturan. Key harus huruf kapital dan tidak ada yg boleh berulang. Sejumlah 26 :")
            print("Enter a valid key:")
            
    #dibuat asumsi perulangan 10 supaya fungsi didalamnya berjalan, sebenarnya dibuat angka lain pun tidak masalah 
    for j in range(10) : 
        #inisiasi cipher text sebelum mengisi
        cipher_text = []
        #METHOD ord untuk mengetahui value ascii pada karakter, untuk mencocokkannya
        for i in plain_text.upper() :
            cipher_text.append(key[ord(i) - ord('A')])

    print("Cipher-text nya adalah :", end = ' ')
    print("".join(cipher_text))