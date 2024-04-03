x = [['b', 'c', 'a'], ['f', 'a'], ['b', 'a', 'b', 'd'], ['c', 'b', 'd', 'g']]
y = {'b': 4, 'a': 3, 'c': 2, 'd': 2, 'f': 1, 'g': 1}

# Define a function to reorder the letters in a sublist based on their frequency
def reorder_sublist(x,y):
    z = []
    for sublist in x:
        z.append(sorted(sublist, key=lambda letter: -y.get(letter, 0)))
    return z

# Apply the function to each sublist in x and create z
z = reorder_sublist(x,y)

print(z)