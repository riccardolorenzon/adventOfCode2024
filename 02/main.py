def is_safe(line):
    prev_elem = None
    increasing = None
    unsafe_report = False
    for num in line:
        num = int(num)
        if prev_elem is not None:
            increasing = increasing if increasing is not None else num > prev_elem
            if increasing and (
                num <= prev_elem or num - prev_elem < 1 or num - prev_elem > 3
            ):
                unsafe_report = True
            elif increasing is False and (
                num >= prev_elem or prev_elem - num < 1 or prev_elem - num > 3
            ):
                unsafe_report = True
        prev_elem = num
    return not unsafe_report


if __name__ == "__main__":
    safe_reports = 0
    with open("data.txt", "r", encoding="utf-8") as f:
        while line := f.readline():
            line = line.rstrip().split(" ")
            if is_safe(line):
                safe_reports += 1
            else:
                safe_alternative = False
                for i in range(len(line)):
                    if is_safe(line[:i] + line[i + 1 :]):
                        safe_alternative = True
                        break
                if safe_alternative:
                    safe_reports += 1

    print(f"number of safe reports: {safe_reports}")
