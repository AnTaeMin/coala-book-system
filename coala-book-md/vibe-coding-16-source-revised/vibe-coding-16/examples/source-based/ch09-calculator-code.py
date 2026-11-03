a, b = 100.0, 5.0
op = "/"
if op == "+":
    result = a + b
elif op == "-":
    result = a - b
elif op == "*":
    result = a * b
elif op == "/" and b != 0:
    result = a / b
else:
    result = "계산할 수 없습니다"
print(result)
