def get_gen(line):
    for num in line.rstrip().split(" "):
        yield num


if __name__ == "__main__":
    safe_reports = 0
    with open("data.txt", "r", encoding="utf-8") as f:
        while line := f.readline():
            line = line.rstrip()
            prev_elem = None
            increasing = None
            unsafe_report = False
            end_of_sequence = False
            gen = get_gen(line)
            while not unsafe_report and not end_of_sequence:
                try:
                    num = next(gen)
                except StopIteration:
                    safe_reports += 1
                    end_of_sequence = True
                else:
                    num = int(num)
                    if prev_elem is not None:
                        increasing = (
                            increasing if increasing is not None else num > prev_elem
                        )
                        if increasing and (
                            num <= prev_elem
                            or num - prev_elem < 1
                            or num - prev_elem > 3
                        ):
                            unsafe_report = True
                        elif increasing is False and (
                            num >= prev_elem
                            or prev_elem - num < 1
                            or prev_elem - num > 3
                        ):
                            unsafe_report = True
                    prev_elem = num

    print(f"number of safe reports: {safe_reports}")
