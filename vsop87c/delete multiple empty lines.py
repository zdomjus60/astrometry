import re
def remove_multiple_newlines(filename):
    
    readf = open (filename)
    writef = open (filename+"_cleaned.py","w")
    all_lines = readf.read()
    pattern = "(\s*\n+){3,}"
    all_split = re.split(pattern, all_lines)
    all_clean = "\n".join(all_split)
    writef.write(all_clean)
    writef.close
    readf.close
    return all_split

for i in ("earth", "mercury", "venus", "mars", "jupiter",
          "saturn", "uranus", "neptune"):
    a = remove_multiple_newlines(i+".py")
    
