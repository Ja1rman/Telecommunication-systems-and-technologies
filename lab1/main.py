def text_to_bits(text: str) -> list[int]:
    return [int(bit) for char in text for bit in format(ord(char), '08b')]


def bits_to_text(bits: list[int]) -> str:
    return ''.join(chr(int(''.join(map(str, bits[i:i+8])), 2)) for i in range(0, len(bits), 8))


def uolsh_codes_gen(n: int) -> list[list[int]]:
    r = range(2**n)
    return [[int(bin(x & y), 13) % 2 or -1 for x in r] for y in r]


def encode_cdma(bits: list[int], code: list[int]) -> list[int]:
    signal = []
    for bit in bits:
        b = 1 if bit else -1
        signal.extend([b * c for c in code])
    return signal


def decode_cdma(signal: list[int], code: list[int]) -> list[int]:
    n = len(code)
    bits = []
    for i in range(0, len(signal), n):
        chunk = signal[i:i+n]
        s = sum(chunk[j] * code[j] for j in range(n))
        bits.append(1 if s > 0 else 0)
    return bits


stations = {
    "A": "GOD",
    "B": "CAT",
    "C": "HAM",
    "D": "SUN"
}

walsh = uolsh_codes_gen(3)
print("Walsh codes:")
for i, code in enumerate(walsh):
    print(f"Code {i+1}:\t", end="")
    for c in code:
        print(c, end="\t")
    print()

codes = [walsh[i] for i in range(4)]

# Кодирование сигналов каждой станции
signals = []
for i, key in enumerate(stations):
    bits = text_to_bits(stations[key])
    sig = encode_cdma(bits, codes[i])
    signals.append(sig)

# Суммарный сигнал
combined_signal = [sum(x) for x in zip(*signals)]
print("Combined signal:", combined_signal)
# Декодирование
for i, key in enumerate(stations):
    decoded_bits = decode_cdma(combined_signal, codes[i])
    decoded_text = bits_to_text(decoded_bits)
    print(f"Station {key} transmits: {decoded_text}")
