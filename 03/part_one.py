import re

if __name__ == "__main__":
    with open("data.txt") as f:
        pattern = re.compile(r"mul\((\d+),\ ?(\d+)\)")
        pos = 0
        res = 0
        text = f.read()
        while m := pattern.search(text, pos):
            pos = m.start() + 1
            res = res + int(m[1]) * int(m[2])
        print(f"result is {res}")
