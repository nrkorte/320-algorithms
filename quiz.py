import sys
import time
tele_global = [(1, 2, 1), (1, 3, 2), (1, 4, 3), (2, 4, 5), (3, 6, 7), (4, 6, 11), (4, 7, 13), (6, 7, 17), (6, 7, 19)]
coin_global = [5,1,50,100,25,10]
matr_global = [10,4,5,60,2,12,20]
lcs_x_global = "GGTATACC"
lcs_y_global = "CCACAATTTGGG"
zero_one_s_global = [(2,1),(3,4),(7,3),(5,2)]
zero_one_w_global = 4
boyer_text_global = "cdaarbraaab"
boyer_pattern_global = "rbra"
kmp_text_global = "ABC ABCDAB ABCDABCDABDE"
kmp_pattern_global = "DABDE"


def schedule_telescope_observations(S):
    n = len(S)
    S = sorted(S, key=lambda x: x[1])
    B = [0] + [s[2] for s in S]
    M = [0] * (n + 1)
    benefit_vector = [0] * (n + 1)

    for i in range(1, n + 1):
        Si, Fi, Bi = S[i - 1]
        j = i - 1
        while j > 0 and S[j - 1][1] > Si:
            j -= 1
        M[i] = max(M[j] + B[i], M[i - 1])
        benefit_vector[i] = M[i]
    
    return M[n], benefit_vector[1:]



def coins_in_a_line(coins):
    n = len(coins)
    M = [[0]*n for _ in range(n)]
    
    # Initialize the diagonal entries
    for i in range(n):
        M[i][i] = coins[i]
        
    # Compute the maximum value table for the even diagonals
    for d in range(2, n+1, 2):
        for i in range(n-d+1):
            j = i + d - 1
            if i+2 < n:
                left = coins[i] + min(M[i+2][j], M[i+1][j-1])
            else:
                left = coins[i] + M[i+1][j-1]
            if j-2 >= 0:
                right = coins[j] + min(M[i+1][j-1], M[i][j-2])
            else:
                right = coins[j] + M[i+1][j-1]
            M[i][j] = max(left, right)
    
    # Return the maximum amount the first player can win
    return M[0][n-1], [M[0][j] for j in range(1, n, 2)], [M[i][n-1] for i in range(0, n, 2)], M



def matrix_chain_order(p):
    n = len(p) - 1
    m = [[0] * n for _ in range(n)]
    s = [[0] * n for _ in range(n)]

    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i + l - 1
            m[i][j] = sys.maxsize
            for k in range(i, j):
                q = m[i][k] + m[k+1][j] + p[i] * p[k+1] * p[j+1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s

def lcs(X, Y):
    m, n = len(X), len(Y)
    # Initialize the table with 0s
    table = [[0] * (n+1) for _ in range(m+1)]
    # Fill in the table using dynamic programming
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                table[i][j] = table[i-1][j-1] + 1
            else:
                table[i][j] = max(table[i-1][j], table[i][j-1])
    # Backtrack through the table to find the LCS
    lcs = ''
    i, j = m, n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs += X[i-1]
            i -= 1
            j -= 1
        elif table[i-1][j] >= table[i][j-1]:
            i -= 1
        else:
            j -= 1
    # Generate the bottom row and rightmost column of the table
    bottom_row = table[-1][1:]
    right_col = [table[i][-1] for i in range(m+1)][1:]
    return lcs[::-1], bottom_row, right_col, table


def zero_one_knap(S, W):
    n = len(S)
    table = [[0] * (W+1) for _ in range(n+1)]

    for i in range(1, n+1):
        for j in range(1, W+1):
            if S[i-1][1] <= j:
                table[i][j] = max(table[i-1][j], S[i-1][0] + table[i-1][j-S[i-1][1]])
            else:
                table[i][j] = table[i-1][j]

    max_benefit = table[n][W]
    last_row = table[-1]
    last_col = [table[i][-1] for i in range(n+1)]

    last_col[0] = 0  # add 0 to the beginning of the last column

    return max_benefit, last_row, last_col, table


def build_mismatch(pattern):
    table = {}
    for i in range(0, len(pattern)):
        if table.get(pattern[i]) == None:
            table[pattern[i]] = max([1, len(pattern) - i - 1])
        else:
            table.update({pattern[i] : max([1, len(pattern) - i - 1])})
    return table

def boyer_moore(text, pattern):
    table = build_mismatch(pattern)
    i = len(pattern)
    comps = 0
    start = True
    while i < len(text):
        if not start:
            if table.get(text[i - 1]) == None:
                i += len(pattern)
            else:
                i += table.get(text[i - 1])
                
                
        start = False
        j = 1
        while j < len(pattern):
            comps += 1
            print ("checking to see if", text[i-j], "is equal to ", pattern[len(pattern) - j], "at positon (i, j) ==> (", str(i-j), ",", str(len(pattern) - j), ")")
            if text[i - j] == pattern[len(pattern) - j]:
                j += 1
                if j == len(pattern):
                    comps += 1
                    print ("checking to see if", text[i-j], "is equal to ", pattern[len(pattern) - j], "at positon (i, j) ==> (", str(i-j), ",", str(len(pattern) - j), ")")
                    return i - len(pattern), comps, table
            else:
                break
    return -1, comps, table

def reverse(x):
  return x[::-1]

def kmp(text, pattern):
    i = 0
    j = 0
    comps = 0
    while i < len(text):
        if text[i] != pattern[j] and j > 0:
            comps += 1
            j = 0
            continue
        elif text[i] != pattern[j] and j == 0:
            comps += 1
            i += 1
            continue
        comps += 1
        i += 1
        j += 1
        if (j == len(pattern)):
            break
    
    position = (i - j) + 1
    yn = j != len(pattern)
    # build failure function
    failure = [0] * len(pattern)
    i = 1
    j = 0
    for d in range (len(pattern) - 1):
        if (pattern[j] == pattern[i]):
            failure[i] = j + 1
            i += 1
            j += 1
        else:
            if j != 0:
                j = failure[j - 1]
            i += 1


    if yn:
        return -1, comps
    return position - 1, comps, failure



# ================================================================================================================================================




def a_to_s(arr):
    return str(arr).replace(" ", "")

def build_matr_string():
    ret = str(matr_global[0])
    for i in range (1, len(matr_global) - 1):
        ret += "x" + str(matr_global[i]) + " " + str(matr_global[i])
    ret += "x" + str(matr_global[len(matr_global) - 1])
    return ret

if __name__ == "__main__":
    print_param = 32
    print ("=====================")
    print ("Telescope scheduling problem\n")
    max_benefit, benefit_vector = schedule_telescope_observations(tele_global)
    print(f'{"Maximum total benefit": <{print_param}} ==> ', max_benefit)
    print(f'{"Benefit vector": <{print_param}} ==> ', a_to_s(benefit_vector), "\n")

    print ("=====================")
    print ("Coins in a line problem\n")
    max_amount, top_row, right_col, coins_table= coins_in_a_line(coin_global)
    print(f'{"Max amount possible": <{print_param}} ==> ', max_amount)
    print(f'{"Top row": <{print_param}} ==> ', a_to_s(top_row))
    print(f'{"Rightmost column": <{print_param}} ==> ', a_to_s(right_col), "\n")

    print ("=====================")
    print ("Matrix Chain Problem\n")
    M, S = matrix_chain_order(matr_global)
    print(f'{"Minimum number of operations": <{print_param}} ==> ', M[0][len(matr_global) - 2])
    print (f'{"Top row": <{print_param}} ==> ', a_to_s(M[0]))
    print (f'{"Rightmost column": <{print_param}} ==> ', a_to_s([row[-1] for row in M]), "\n")

    print ("=====================")
    print ("Longest Common Substring Problem\n")
    lcs_final, b_row, r_col, lcs_table = lcs(lcs_x_global, lcs_y_global)
    print (f'{"Longest common substring": <{print_param}} ==> ', lcs_final)
    print (f'{"Bottom row": <{print_param}} ==> ', a_to_s(b_row))
    print (f'{"Rightmost column": <{print_param}} ==> ', a_to_s(r_col), "\n")

    print ("=====================")
    print ("0-1 Knapsack Problem\n")
    knap_ben, knap_row, knap_col, tb = zero_one_knap(zero_one_s_global, zero_one_w_global)
    print (f'{"Max benefit": <{print_param}} ==> ', knap_ben)
    print (f'{"Bottom row": <{print_param}} ==> ', a_to_s(knap_row))
    print (f'{"Rightmost column": <{print_param}} ==> ', a_to_s(knap_col), "\n")

    print ("=====================")
    print ("Boyer-moore problem\n")
    bm_start, bm_num_comp, bm_table = boyer_moore(boyer_text_global, boyer_pattern_global)
    print (f'{"Start": <{print_param}} ==> ', bm_start)
    print (f'{"Comparison count": <{print_param}} ==> ', bm_num_comp)

    print ("=====================")
    print ("KMP problem\n")
    kmp_start, kmp_num_comp, kmp_fail = kmp(kmp_text_global, kmp_pattern_global)
    print (f'{"Start": <{print_param}} ==> ', kmp_start)
    print (f'{"Comparison count": <{print_param}} ==> ', kmp_num_comp)
    print (f'{"Failure function": <{print_param}} ==> ', a_to_s(kmp_fail))


# ================================================================================================================================================

    if len(sys.argv) == 2 and sys.argv[1] == "table":
        print ("=====================")
        print ("\nTable information\n")
        print ("=====================") # Coins table
        print (f'{"Coins table": <{print_param}} ==> ', a_to_s(coin_global), "\n")
        for i in range(len(coins_table)):
            for j in range(len(coins_table[i])):
                print(coins_table[i][j], end="\t")
            print()
        print()
        print ("=====================") # Matrix table
        print(f'{"Matrix table": <{print_param}} ==> ', build_matr_string(), "\n")
        for i in range(len(M)):
            for j in range(len(M[i])):
                print(M[i][j], end="\t")
            print()
        print()
        print ("=====================") # Lcs table
        print (f'{"LCS table": <{print_param}} ==> ', lcs_x_global, "vs", lcs_y_global, "\n")
        for i in range(len(lcs_table)):
            for j in range(len(lcs_table[i])):
                print(lcs_table[i][j], end="\t")
            print()
        print()
        print ("=====================") # Knapsack table
        print (f'{"Knapsack table": <{print_param}} ==> ', zero_one_s_global, "with max benefit", zero_one_w_global, "\n")
        for i in range(len(tb)):
            for j in range(len(tb[i])):
                print(tb[i][j], end="\t")
            print()

        print()
        print ("=====================") # Knapsack table
        print (f'{"Boyer-Moore table": <{print_param}} ==> ', boyer_text_global, "\twith pattern\t\"", end="")
        print(boyer_pattern_global, end="")
        print("\"\n")
        for var in bm_table.keys():
            print (var, end="\t")
        print ("*")
        for var in bm_table.values():
            print (var, end="\t")
        print (len(boyer_pattern_global))
        


