`default_nettype none

module barrel_shifter (
    input  wire [7:0] ui_in,    // Dữ liệu đầu vào data_in[7:0]
    output wire [7:0] uo_out,   // Dữ liệu đầu ra data_out[7:0]
    input  wire [7:0] uio_in,   // uio_in[2:0]=shift_amt, uio_in[3]=dir, uio_in[4]=arith
    output wire [7:0] uio_out,  // Không dùng -> gán 0
    output wire [7:0] uio_oe,   // Gán 0 -> Đặt làm chân Input
    input  wire       ena,      // Tín hiệu enable (không dùng trong logic tổ hợp)
    input  wire       clk,      // Xung clock (không dùng)
    input  wire       rst_n     // Tín hiệu reset (không dùng)
);

    // 1. Tách các tín hiệu điều khiển từ uio_in 🔀
    wire [2:0] shift_amt = uio_in[2:0]; // Số bit cần dịch (0 đến 7)
    wire       dir       = uio_in[3];   // 0: Dịch phải (SHR/SRA), 1: Dịch trái (SHL)
    wire       arith     = uio_in[4];   // 0: Dịch logic, 1: Dịch số học (giữ bit dấu)

    // 2. Gán giá trị cố định cho các cổng I/O không dùng 🔌
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // 3. Đảo bit đầu vào nếu là dịch trái 🔄
    wire [7:0] stage0_in;
    assign stage0_in = dir ? {ui_in[0], ui_in[1], ui_in[2], ui_in[3], 
                              ui_in[4], ui_in[5], ui_in[6], ui_in[7]} : ui_in;

    // Bit chèn vào khi dịch (Bit dấu nếu là SRA dịch phải, ngược lại là 0)
    wire fill_bit = (arith && !dir) ? ui_in[7] : 1'b0;

    // 4. Tầng MUX 1: Dịch 1 bit nếu shift_amt[0] == 1 ⚙️
    wire [7:0] stage1_out;
    assign stage1_out = shift_amt[0] ? {fill_bit, stage0_in[7:1]} : stage0_in;

    // 5. Tầng MUX 2: Dịch 2 bit nếu shift_amt[1] == 1 ⚙️
    wire [7:0] stage2_out;
    assign stage2_out = shift_amt[1] ? {{2{fill_bit}}, stage1_out[7:2]} : stage1_out;

    // 6. Tầng MUX 3: Dịch 4 bit nếu shift_amt[2] == 1 ⚙️
    wire [7:0] stage3_out;
    assign stage3_out = shift_amt[2] ? {{4{fill_bit}}, stage2_out[7:4]} : stage2_out;

    // 7. Đảo bit đầu ra nếu là dịch trái và gán ra uo_out 🎯
    assign uo_out = dir ? {stage3_out[0], stage3_out[1], stage3_out[2], stage3_out[3], 
                           stage3_out[4], stage3_out[5], stage3_out[6], stage3_out[7]} : stage3_out;

endmodule