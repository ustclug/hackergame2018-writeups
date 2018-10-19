f = open("gift", "rb")

binary = f.read()
f.close()

binary = binary.replace(b'Obfuscator', bytes("Naive-doki"))
binary = binary.replace(b'4.0.1', bytes("9.1.0"))

f = open("gift", "wb")
f.write(binary)
f.close()
