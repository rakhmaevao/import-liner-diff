def read_report(path) -> dict:
    with open(path) as f:
        report = f.read()
    report = report.split("Broken contracts\n----------------")[-1].split("\n")
    group_errors = {}
    for i, l in enumerate(report):
        if l.startswith("---"):
            last_group_name = report[i - 1]
            group_errors[last_group_name] = {}
        if l.endswith(":"):
            last_rull_name = l.split(":")[0]
            group_errors[last_group_name][last_rull_name] = []
        if l.startswith("- "):
            error_desc = l.split("- ")[-1]
            group_errors[last_group_name][last_rull_name].append(error_desc)

    return group_errors


def compare(left_file: dict, right_file: dict):
    # Compare groups
    result = set(left_file) - (set(right_file))
    if result:
        print(f"В левом отчете есть дополнительные ошибки:\n{"\n".join(result)}\n\n")
    result = set(right_file) - (set(left_file))
    if result:
        print(f"В правом отчете есть дополнительные ошибки:\n{"\n".join(result)}\n\n")

    # Compare groups
    for group_name in left_file:
        result = set(left_file[group_name]) - (set(right_file[group_name]))
        if result:
            print(
                f"В левом отчете есть дополнительные ошибки:\n{"\n".join(result)}\n\n"
            )
        result = set(right_file[group_name]) - (set(left_file[group_name]))
        if result:
            print(
                f"В правом отчете есть дополнительные ошибки:\n{"\n".join(result)}\n\n"
            )

    # Compare rules
    for group_name in left_file:
        for rule_name in left_file[group_name]:
            result = set(left_file[group_name][rule_name]) - (
                set(right_file[group_name][rule_name])
            )
            if result:
                print(
                    f"В левом отчете есть дополнительные ошибки:\n{"\n".join(result)}\n\n"
                )

            result = set(right_file[group_name][rule_name]) - (
                set(left_file[group_name][rule_name])
            )
            if result:
                print(
                    f"В правом отчете есть дополнительные ошибки:\n{"\n".join(result)}\n\n"
                )


if __name__ == "__main__":
    left_file = read_report("left")
    right_file = read_report("right")
    compare(left_file, right_file)
