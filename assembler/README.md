## Zero page layout

Zero page is used to pass parameters to functions.

| Bytes  | Purpose                                                    |
|--------|------------------------------------------------------------|
|  0-1   | `assembler`s 1st parameter(source pointer)                 |
|  2-3   | `assembler`s 2nd parameter(output pointer)                 |
|  4-5   | `str_cmp` 1st parameter(lhs)                               |
|  6-7   | `str_cmp` 2nd parameter(rhs)                               |
|  8-9   | generic word 1 used for indirect reads/writes              |
|  10-11 | `find_table_entry`s 1st parameter(source mnemonic pointer) |
|  12-13 | generic word 2 used for indirect reads/writes              |

## Functions

Each function is in a separate file.

`assembler` takes 3 parameters: input and output pointer parameters are passed
using zero page, source code size parameter is passed in `XR`.

`str_cmp` takes 3 parameters: lhs and rhs pointer parameters are passed using
zero page, number of bytes to compare is passed in `XR`. Returns `0` if strings
are not equal, `1` otherwise(in `AC` register).

`find_table_entry` takes 1 parameter, pointer to source mnemonic string, passed
using zero page. Returns a pointer to table row(low-byte in `XR`, high-byte in
`YR`).

`add_byte_to_word` adds addend to a memory in zero page. The
function takes 2 parameters, zero page address in `XR` and addend in `YR`.

`inc_word` increments word in zero page. The function takes 1 parameters, zero
page address in `XR`.

Each addressing mode has a separate `am_*` file. Each addressing mode function
returns how many characters it read in `AC`.
- `am_implied` "noop" handler, the operand is implied, there's nothing to do to
handle the operand.

## Mnemonics table

`mnemonics_table` defines, well, mnemonics table. It has following columns:
- `mnemonic_len` 1 byte long, specifies how long the mnemonic string is
- `mnemonic_str` 5 bytes long, mnemonic string, if the string is < 5, pad with
`0x00`
- `address_mode_handler` 2 bytes long, pointer to the addressing mode handler

Example of the table:

| len |      mnemonic    | handler |
|-----|------------------|---------|
|  3  |   LDA#\x00\x00   | 0xff00  |
|  5  |      ORAxi       | 0xf001  |
