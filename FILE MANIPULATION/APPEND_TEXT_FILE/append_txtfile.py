f = open("test.txt", "a")

for i in range(7, 13):
    data = f"Added line {i}\n"
    f.write(data)

f.close()