def read(i):
    with open("cle"+str(i),"rb") as f:
        out = f.read()
        print(out.hex())

for i in range(1,5):
    read(i)