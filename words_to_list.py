with open('positive_words.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

other = open("list.txt",'w')
other.write(str(content))
other.close()
