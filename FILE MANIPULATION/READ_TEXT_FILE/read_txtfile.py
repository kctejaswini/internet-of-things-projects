# Read text file using different methods

# Method 1: readline()
f = open("test.txt", "r")
print("readline() method")
print(f.readline())
print(f.readline())
f.close()

# Method 2: readlines()
f = open("test.txt", "r")
print("readlines() method")
lines = f.readlines()
for line in lines:
    print(line.strip())
f.close()

# Method 3: read()
f = open("test.txt", "r")
print("read() method")
data = f.read()
print(data)
f.close()