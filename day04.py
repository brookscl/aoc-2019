
def is_password(p):
    if not ''.join(sorted(p)) == p:
        return False

    for i in range(0, len(p) - 1):
        if p[i] == p[i+1]:
            return True

    return False


assert is_password("111111")
assert not is_password("223450")
assert not is_password("123789")

count = 0
for i in range(124075, 580769+1):
    if is_password(str(i)):
        count += 1

print(count)
