from term_printer import Color, Format, StdText, cprint
import sys

#pip3 install term-printer

def decimal_to_binary_steps(number):
    # 整数と小数に分ける
    integer_part = int(number)
    fractional_part = number - integer_part

    print("\n=== 整数部の変換 ===")
    int_steps = []
    n = integer_part
    while n > 0:
        quotient = n // 2
        remainder = n % 2
        int_steps.append((n, remainder))
        n = quotient

    for value, remainder in int_steps:
        print(f"2 ) {value:<4} ... {StdText(remainder, Color.CYAN)}")
    print("    0")

    binary_integer = ''.join(str(r) for _, r in int_steps)[::-1] if int_steps else "0"

    print("\n=== 小数部の変換 ===")
    frac_steps = []
    view_num = []
    count = 0
    max_digits = 10  # 小数部の桁数上限（必要なら調整可）
    f = fractional_part
    while f > 0 and count < max_digits:
        init_num = f
        f *= 2
        bit = int(f)
        view_num.append((init_num, f))
        frac_steps.append((f, bit))
        f -= bit
        count += 1

    for i, (val, result) in enumerate(view_num):
        # val を小数点以下3桁で表示
        print(f"    {val}")
        print(f"x     2")
        print("----------------")
        print(f"    {StdText(result, Color.CYAN)} \n")

    binary_fraction = ''.join(str(bit) for _, bit in frac_steps)

    # 結果を表示
    print(f"\n2進数表現: {StdText(binary_integer, Color.BLUE)}.{StdText(binary_fraction, Color.BLUE)}")
    # 8進数・16進数に変換
    octal = oct(int(number))
    hexa = hex(int(number))

    print(f"\n{StdText("0oまたは0Xのあとが実際の数字  by hosshi", Color.YELLOW)}")
    print(StdText("例：0o377 → 377   0XFF → FF", Color.YELLOW))
    print(f"\n8進数表現(整数部分のみ): {StdText(octal, Color.GREEN)}")
    print(f"16進数表現(整数部分のみ): {StdText(hexa.upper(), Color.MAGENTA)}")


def decimal_to_binary_hell(number, bit_width=8):
    if number >= 0:
        print(StdText("\nこの関数は負の数専用です。", Color.YELLOW))
        return

    # 符号なしの絶対値を取得
    abs_number = abs(int(number))
    bit_width = int(input(f"{StdText("ビット幅は何ですか：", Color.CYAN)}"))

    print(StdText(f"\n{number} の2進数変換を開始します（bit幅 = {bit_width}）", Color.YELLOW))
    
    # === Step 1: 通常の2進数変換 ===
    int_steps = []
    n = abs_number
    while n > 0:
        quotient = n // 2
        remainder = n % 2
        int_steps.append((n, remainder))
        n = quotient

    for value, remainder in int_steps:
        print(f"2 ) {value:<4} ... {StdText(remainder, Color.CYAN)}")
    print("    0")

    binary_integer = ''.join(str(r) for _, r in int_steps)[::-1].zfill(bit_width)
    print(f"\n[ステップ1] 符号なし2進数（{abs_number}）: {StdText(binary_integer, Color.BLUE)}")

    # === Step 2: 1の補数 ===
    ones_complement = ''.join('1' if b == '0' else '0' for b in binary_integer)
    print(f"[ステップ2] 1の補数(1と0の入れ替え): {StdText(ones_complement, Color.GREEN)}")

    # === Step 3: 2の補数 ===
    # 1の補数に1を加える
    def add_binary_one(bin_str):
        result = list(bin_str)
        carry = 1
        for i in range(len(result)-1, -1, -1):
            if result[i] == '1' and carry == 1:
                result[i] = '0'
                carry = 1
            elif result[i] == '0' and carry == 1:
                result[i] = '1'
                carry = 0
        return ''.join(result)

    twos_complement = add_binary_one(ones_complement)
    print(f"[ステップ3] 2の補数（1を足す）: {StdText(twos_complement, Color.RED)}")
    print(f"結果：{StdText(twos_complement, Color.RED)}")
            
        
def binary_to_decimal_step(number):
    # 入力を文字列に変換（例: 1011 → "1011"）
    num = str(number)
    decimal = 0  # 結果を格納する変数
    
    print(StdText(f"2進数 {num} を 10進数に変換します。\n", Color.YELLOW))
    
    # 桁ごとに処理（左から右へ）
    for i, digit in enumerate(num[::-1]):  # 右から処理する
        if digit == "1" or digit == "0":
            value = int(digit) * (2 ** i)
            print(f"{digit} × 2^{i} = {value}")
            decimal += value
        else:
            print(StdText("エラー、二進数でない数字が入っています", Color.RED))
            return 1
            
    print(StdText(f"\n10進数の結果: {decimal}", Color.CYAN))
    octal = oct(int(decimal))
    hexa = hex(int(decimal))

    print(f"\n{StdText("0oまたは0Xのあとが実際の数字  by hosshi", Color.YELLOW)}")
    print(StdText("例：0o377 → 377   0XFF → FF", Color.YELLOW))
    print(f"\n8進数表現(整数部分のみ): {StdText(octal, Color.GREEN)}")
    print(f"16進数表現(整数部分のみ): {StdText(hexa.upper(), Color.MAGENTA)}")

    


def main():
    running =True
    while running:
        try:
            num_s = str(input("10進数の数字（例：1234 または 0.625）を入力してください: "))
            num = float(num_s.split("(")[0])
            try:
                data = int(num_s.split("(")[1])
            except IndexError:
                data = 10
                
            if data == 2:
                num = int(num)
                binary_to_decimal_step(num)
            else:
                if num < 0:
                    print("マイナスを検知しました")
                    decimal_to_binary_hell(num)
                else:
                    decimal_to_binary_steps(num)
        except ValueError:
            print("有効な数値を入力してください。")
        result = input("続けますか？[y/n]：")
        if result == "y":
            continue
        elif result ==  "n":
            running = False
        else:
            running = False
    sys.exit()

if __name__ == "__main__":
    main()