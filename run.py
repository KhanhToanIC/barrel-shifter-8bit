from pathlib import Path
from cocotb_tools.runner import get_runner

def test_runner():
    sim = "questa"
    proj_path = Path(__file__).resolve().parent
    runner = get_runner(sim)
    
    runner.build(
        verilog_sources=[proj_path / "project.v"],
        hdl_toplevel="barrel_shifter",  # 📝 Đã đổi tên toplevel thành barrel_shifter
        always=True,
    )
    
    runner.test(
        hdl_toplevel="barrel_shifter",  # 📝 Đã đổi tên toplevel thành barrel_shifter
        test_module="test",
        gui=True,  # 🌊 Bật giao diện GUI QuestaSim
    )

if __name__ == "__main__":
    test_runner()