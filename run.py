import os
from pathlib import Path
from cocotb_tools.runner import get_runner

def test_runner():
    sim = os.environ.get("SIM", "questa")
    proj_path = Path(__file__).resolve().parent
    runner = get_runner(sim)
    
    runner.build(
        verilog_sources=[proj_path / "project.v"],
        hdl_toplevel="barrel_shifter",
        always=True,
        waves=True,  # 🌊 Bật tạo file dạng sóng khi build
    )
    
    runner.test(
        hdl_toplevel="barrel_shifter",
        test_module="test",
        waves=True,  # 🌊 Bật lưu dạng sóng khi chạy kiểm thử
    )

if __name__ == "__main__":
    test_runner()