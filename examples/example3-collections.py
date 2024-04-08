from collections import defaultdict

# Define a defaultdict with a default value of 0
word_count = defaultdict(int)

# Count the occurrence of each word in a list
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
for word in words:
    word_count[word] += 1

print(word_count)
