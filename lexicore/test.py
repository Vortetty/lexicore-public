from smaz import compress, decompress


print(compress("Hello, world!"))
print(compress("https://github.com/antirez/smaz"))
print(decompress(compress("Salvatore")))