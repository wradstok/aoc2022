import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class File:
    name: str
    size: int

@dataclass
class Dir:
    name: str
    subdirs : dict[str, "Dir"]
    files: list[File]
    parent : Optional["Dir"]

    def get_all(self, at_most:int, found: int) -> int:
        my_size = self.get_size()
        if my_size < at_most:
            found += my_size
        
        for subdir in self.subdirs.values():
            found = subdir.get_all(at_most, found)
        return found

    def get_smallest(self, target: int, best: int) -> int:
        my_size = self.get_size()
        if my_size > target and my_size < best:
            best = my_size
        
        for subdir in self.subdirs.values():
            best = subdir.get_smallest(target, best)
        
        return best

    def get_size(self) -> int:
        return sum([file.size for file in self.files]) + sum([subdir.get_size() for subdir in self.subdirs.values()])

with open(os.getcwd() +  "/day07/input.txt") as f:
    lines = f.read().splitlines()

root = Dir("", dict(), [], None)
curr_pos = root

# Parse filestructure
for line in lines:
    if line.startswith("$"):
        if line == "$ cd ..":
            curr_pos = curr_pos.parent
        elif "cd /" in line:
            curr_pos = root
        elif "cd" in line:
            dir_name = line[5:]
            curr_pos = curr_pos.subdirs[dir_name]
    else:
        if line.startswith("dir"):
            name = line[4:]
            curr_pos.subdirs[name] = Dir(name, dict(), [], curr_pos)
        else:
            size, name = line.split(" ")
            curr_pos.files.append(File(name, int(size)))

print(f"Size of dirs on fs smaller than 100k: {root.get_all(100000, 0)}")

free = 70000000 - root.get_size()
target = 30000000 - free
print(f"Smallest to delete has size {root.get_smallest(target, 999999999999999999)}")
