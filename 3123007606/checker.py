def lcs_length(s1, s2):
    """计算两个字符串的最长公共子序列长度"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
    return dp[m][n]

def calc_similarity(orig, plag):
    """计算重复率，基于最长公共子序列"""
    if not orig:
        return 0.0
    lcs = lcs_length(orig, plag)
    return lcs / len(orig)
