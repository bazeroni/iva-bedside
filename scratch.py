import re

string = "This is a [string] with [brackets]"

new_string = re.sub(r'\[.*?\]', '', string)

print(new_string)

############################################

# compile regular expression pattern to match contents of brackets '[]'
pattern = re.compile(r'\[(.*?)\]')

# input string with bracketed contents
string = "The colors of the rainbow are [red], [orange], [yellow], [green], [blue], [indigo], and [violet]"

# find all occurrences of pattern in string and save as list
bracketed_contents = pattern.findall(string)

# loop through list and assign each element to separate variable
red = bracketed_contents[0]
orange = bracketed_contents[1]
yellow = bracketed_contents[2]
green = bracketed_contents[3]
blue = bracketed_contents[4]
indigo = bracketed_contents[5]
violet = bracketed_contents[6]