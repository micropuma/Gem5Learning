import m5
from m5.objects import *
from caches import *
system = System()

# 设定时钟信号阈以及电压阈
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# 定义内存类型
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# CPU类型是TimingSimpleCPU
system.cpu = TimingSimpleCPU()

# 构建缓存模型
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# 利用辅助函数连接端口
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# 由于L2Cache只有一个端口，因此需要先实现L2Cache的bus
system.l2bus = L2XBar()

# icache和dcache连接该bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# 构建L2Cache，并连接port
# 1. 连接L2Bus
# 2. 连接membus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
#system.cpu.interrupts[0].pio = system.membus.master
#system.cpu.interrupts[0].int_master = system.membus.slave
#system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.cpu_side_ports

# 设定mem参数
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

binary = 'tests/test-progs/hello/bin/riscv/linux/hello'

# for gem5 V21 and beyond
# 定义工作负载
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

# gem5的模拟方式是事件触发
print("Begginning simulation")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))