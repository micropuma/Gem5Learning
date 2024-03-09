from m5.objects import Cache

class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2

    # 处理缓存缺失（cache miss）的寄存器或队列 
    mshrs = 4
    # 表示每个 MSHR（Miss Status Handling Register）可以同时处理的目标数量。
    tgts_per_mshr = 20 

    # 辅助函数，指定和cpu的哪个端口
    def connectCPU(self, cpu):
        # need to define this in a base class !
        raise NotImplementedError
    # 指定和和L2bus的哪个端口连接
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# L1和L2 Cache都有两个方向的连接要求：1. 连接mem 2. 连接cpu
class L1ICache(L1Cache):
    size = '16kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port 

class L1DCache(L1Cache):
    size = '64kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port 

class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20

    # 处理缓存缺失（cache miss）的寄存器或队列 
    mshrs = 20
    # 表示每个 MSHR（Miss Status Handling Register）可以同时处理的目标数量。
    tgts_per_mshr = 12 

    # 连接L2 bus
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    # 连接membus
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports


