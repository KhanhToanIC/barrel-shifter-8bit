import cocotb
from cocotb.triggers import Timer

def pack_uio(shift_amt: int, dir_val: int, arith_val: int) -> int:
    """Đóng gói các tín hiệu điều khiển vào uio_in (5 bit)
    - shift_amt: 3 bit (bit 0..2)
    - dir_val:   1 bit (bit 3) - 1: Left, 0: Right
    - arith_val: 1 bit (bit 4) - 1: SRA (Arithmetic), 0: SHR (Logic)
    """
    return ((arith_val & 0x01) << 4) | ((dir_val & 0x01) << 3) | (shift_amt & 0x07)


@cocotb.test()
async def test_barrel_shifter_main(dut):
    """Kiểm thử các ca cơ bản và nâng cao (Ca 1 - Ca 4)"""
    dut._log.info("=== BẮT ĐẦU KIỂM THỬ 4 CA CƠ BẢN ===")

    # Ca 1: Dịch 0 bit (Giữ nguyên dữ liệu)
    dut.ui_in.value = 0xA5
    dut.uio_in.value = pack_uio(shift_amt=0, dir_val=0, arith_val=0)
    await Timer(10, unit="ns")
    actual = int(dut.uo_out.value)
    expected = 0xA5
    assert actual == expected, f"Lỗi Ca 1: Kỳ vọng 0x{expected:02X} nhưng thực tế uo_out = 0x{actual:02X}"

    # Ca 2: Dịch 7 bit (SHL 7)
    dut.ui_in.value = 0x01
    dut.uio_in.value = pack_uio(shift_amt=7, dir_val=1, arith_val=0)
    await Timer(10, unit="ns")
    actual = int(dut.uo_out.value)
    expected = 0x80
    assert actual == expected, f"Lỗi Ca 2: Kỳ vọng 0x{expected:02X} nhưng thực tế uo_out = 0x{actual:02X}"

    # Ca 3: Dịch phải số học (SRA) với bit dấu = 1 (0x80 >> 2)
    dut.ui_in.value = 0x80
    dut.uio_in.value = pack_uio(shift_amt=2, dir_val=0, arith_val=1)
    await Timer(10, unit="ns")
    actual = int(dut.uo_out.value)
    expected = 0xE0
    assert actual == expected, f"Lỗi Ca 3: Kỳ vọng 0x{expected:02X} nhưng thực tế uo_out = 0x{actual:02X}"

    # Ca 4: So sánh SHR và SRA trên cùng dữ liệu 0x80 (dịch 2 bit)
    dut.ui_in.value = 0x80
    
    # 4a. SHR (Logic) -> Kỳ vọng 0x20
    dut.uio_in.value = pack_uio(shift_amt=2, dir_val=0, arith_val=0)
    await Timer(10, unit="ns")
    res_shr = int(dut.uo_out.value)

    # 4b. SRA (Số học) -> Kỳ vọng 0xE0
    dut.uio_in.value = pack_uio(shift_amt=2, dir_val=0, arith_val=1)
    await Timer(10, unit="ns")
    res_sra = int(dut.uo_out.value)

    actual = (res_shr, res_sra)
    expected = (0x20, 0xE0)
    assert actual == expected, f"Lỗi Ca 4: Phân biệt SHR/SRA không đúng"


@cocotb.test()
async def test_custom_edge_cases(dut):
    """2 ca biên bổ sung tự xây dựng (Ca 5 - Ca 6)"""
    dut._log.info("=== BẮT ĐẦU 2 CA TEST BỔ SUNG ===")

    # Ca 5: Dịch trái 4 bit (Kiểm tra riêng Tầng MUX 2)
    dut.ui_in.value = 0x0F
    dut.uio_in.value = pack_uio(shift_amt=4, dir_val=1, arith_val=0)
    await Timer(10, unit="ns")
    actual = int(dut.uo_out.value)
    expected = 0xF0
    assert actual == expected, f"Lỗi Ca 5: Kỳ vọng 0x{expected:02X} nhưng thực tế uo_out = 0x{actual:02X}"

    # Ca 6: SRA với bit dấu = 0 (Số dương, 0x7F >> 3)
    dut.ui_in.value = 0x7F
    dut.uio_in.value = pack_uio(shift_amt=3, dir_val=0, arith_val=1)
    await Timer(10, unit="ns")
    actual = int(dut.uo_out.value)
    expected = 0x0F
    assert actual == expected, f"Lỗi Ca 6: Kỳ vọng 0x{expected:02X} nhưng thực tế uo_out = 0x{actual:02X}"