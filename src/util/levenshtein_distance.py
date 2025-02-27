from typing import TypeVar

T = TypeVar("T", list, str)


def edit_dist(a: T, b: T, add=1, remove=1, replace=1):
    """
    a を b に変換するための編集距離を計算するメソッド
    a       : 編集対象文字列
    b       : 目標文字列
    add     : a に一文字追加するコスト
    remove  : a から一文字削除するコスト
    replace : a を一文字置換するコスト
    """
    len_a = len(a) + 1
    len_b = len(b) + 1
    # 配列の初期化
    arr = [[-1 for col in range(len_a)] for row in range(len_b)]
    arr[0][0] = 0
    for row in range(1, len_b):
        arr[row][0] = arr[row - 1][0] + add
    for col in range(1, len_a):
        arr[0][col] = arr[0][col - 1] + remove

    # 編集距離の計算
    def go(row, col):
        if arr[row][col] != -1:
            return arr[row][col]
        else:
            dist1 = go(row - 1, col) + add
            dist2 = go(row, col - 1) + remove
            dist3 = go(row - 1, col - 1)
            arr[row][col] = min(dist1, dist2, dist3) if (b[row - 1] == a[col - 1]) else min(dist1, dist2, dist3 + replace)
            return arr[row][col]

    return go(len_b - 1, len_a - 1)


if __name__ == "__main__":
    while True:
        print("word1 word2 : ", end="")
        a, b = input().split(" ")
        print(edit_dist(a, b))
