def sieve(n):
    """埃拉托斯特尼筛法，返回 <= n 的所有质数列表"""
    is_prime = [True] * (n + 1)
    is_prime[0], is_prime[1] = False, False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [p for p in range(2, n + 1) if is_prime[p]]


def is_prime(num, primes):
    """使用已知的小质数列表对 num 进行试除判断是否为质数"""
    if num < 2:
        return False
    limit = int(num**0.5)
    for p in primes:
        if p > limit:
            break
        if num % p == 0:
            return False
    return True


def is_valid_date(year, month, day):
    """判断给定的年月日是否为有效日期"""
    if not (1 <= month <= 12):
        return False
    # 各月天数（不考虑闰年，因为2025不是闰年）
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    max_day = days_in_month[month - 1]
    return 1 <= day <= max_day


if __name__ == "__main__":
    year = 2026
    MAX_N = year * 10000 + 1231
    small_primes = sieve(31622)

    start_num = year * 10000 + 101  # 以"2025"开头的最小四位数是2025，但2025本身不是质数
    # 如果只想从大于2000开始，则仍然可以从2025开始检查。

    for n in range(start_num, MAX_N + 1):
        # 仅检查前缀为 "2025" 的数字
        # 提示：由于前缀是"2025", 数字必定大于等于 2025
        s = str(n)
        if len(str(n)) == 8:
            # 解析年份、月份、日期
            month = int(s[4:6])  # MM
            day = int(s[6:8])  # DD

            if is_valid_date(year, month, day):
                # 判断质数
                if is_prime(n, small_primes):
                    print(n)
            # 如果不是有效日期则不输出
