# Method 1
def power2n(n):
    return 2**n

# Method 2a : Recursion
def power2n2a(n):
    if n == 0:
        return 1
    return power2n2a(n-1) + power2n2a(n-1)

# Method 2b : Recursion
def power2n2b(n):
    if n == 0:
        return 1
    return 2 * power2n2b(n-1)

# Method 3：Using recursion and memoization
def power2n3(n, memo=None):
    if memo is None:
        memo = {0: 1}
    if n in memo:
        return memo[n]
    memo[n] = 2 * power2n3(n - 1, memo)
    return memo[n]


if __name__ == '__main__':
    n = 7
    print(power2n(n))
    print(power2n2a(n))
    print(power2n2b(n))
    print(power2n3(n))
