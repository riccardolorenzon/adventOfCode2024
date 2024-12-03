import re

if __name__ == "__main__":
    with open("data.txt") as f:
        pattern = re.compile(r"mul\((\d+),\ ?(\d+)\)|do\(\)|don\'t\(\)")
        pos = 0
        res = 0
        text = f.read()
        enabled = True
        while m := pattern.search(text, pos):
            match m[0]:
                case "do()":
                    print("enabled")
                    enabled = True
                case "don't()":
                    print("disabled")
                    enabled = False
                case _:
                    if enabled:
                        res = res + int(m[1]) * int(m[2])
            pos = m.start() + 1
        print(f"result is {res}")
