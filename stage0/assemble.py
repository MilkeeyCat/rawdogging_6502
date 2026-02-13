#!/bin/env python3

import subprocess

# assembling an assembler, haha

# each mnemonic table row takes 16 bytes, there're 150ish opcodes but I rounded
# up a bit
TABLE_SIZE = 200 * 8 * 2
FN_SIZE = 128
PARTS: list[tuple[str, None | int]] = [
    ("main", None),
    ("mnemonics_table", FN_SIZE),
    ("assembler", FN_SIZE * 2 + TABLE_SIZE),
    ("find_table_entry", FN_SIZE * 3 + TABLE_SIZE),
    ("am_implied", FN_SIZE * 4 + TABLE_SIZE),
    ("str_cmp", FN_SIZE * 5 + TABLE_SIZE),
    ("add_byte_to_word", FN_SIZE * 6 + TABLE_SIZE),
    ("inc_word", FN_SIZE * 7 + TABLE_SIZE),
    ("parse_char_to_nibble", FN_SIZE * 8 + TABLE_SIZE),
    ("parse_hex_byte", FN_SIZE * 9 + TABLE_SIZE),
    ("assembler_process_hex_byte", FN_SIZE * 10 + TABLE_SIZE),
    ("am_x_indirect", FN_SIZE * 11 + TABLE_SIZE),
    ("assembler_process_hex_word", FN_SIZE * 12 + TABLE_SIZE),
    ("am_absolute", FN_SIZE * 13 + TABLE_SIZE),
    ("am_immediate", FN_SIZE * 14 + TABLE_SIZE),
    ("am_relative", FN_SIZE * 15 + TABLE_SIZE),
    ("am_indirect_y", FN_SIZE * 16 + TABLE_SIZE),
    ("am_zeropage", FN_SIZE * 17 + TABLE_SIZE),
    ("am_indirect", FN_SIZE * 18 + TABLE_SIZE),
]
ASM_SOURCE_OFFSET = 0x8000 - 0x0800


def assemble():
    result = bytes()

    for path, offset in PARTS:
        if offset != None:
            assert offset >= len(result), "invalid offset for " + path
            result += bytes([0x00] * (offset - len(result)))

        completed_process = subprocess.run(["xxd", "-r", path], capture_output=True)
        result += completed_process.stdout

    assert ASM_SOURCE_OFFSET >= len(
        result
    ), "invalid offset, can't insert assembly input"
    result += bytes([0x00] * (ASM_SOURCE_OFFSET - len(result)))

    with open("input.asm", "rb") as file:
        result += file.read()

    with open("assembler.bin", "wb") as file:
        _ = file.write(result)


if __name__ == "__main__":
    assemble()
