import re


def is_password(p):
    if not ''.join(sorted(p)) == p:
        return False

    groups = [m.group(0) for m in re.finditer(r"(\d)\1*", p)]
    return next((g for g in groups if len(g) > 1), False)


def is_password2(p):
    if not ''.join(sorted(p)) == p:
        return False

    groups = [m.group(0) for m in re.finditer(r"(\d)\1*", p)]
    return next((g for g in groups if len(g) == 2), False)


assert is_password("111111")
assert not is_password("223450")
assert not is_password("123789")

test_range = range(124075, 580769+1)

count = sum(1 for i in test_range if is_password(str(i)))

assert count == 2150
print(count)

assert is_password2("112233")
assert not is_password2("123444")
assert is_password2("111122")

count = sum(1 for i in test_range if is_password2(str(i)))

assert count == 1462
print(count)
