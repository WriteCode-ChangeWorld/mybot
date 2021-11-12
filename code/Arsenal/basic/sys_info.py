import psutil


class SysInfo:
    def size2Mb(self,size,key=0):
        unit = ["KB","MB","GB","TB"]
        if size/1024 > 1024:
            return self.size2Mb(size/1024,key=key+1)
        else:
            return "%.2f%s" %(size/1024,unit[key])

    def get_cpu_info(self):
        cpuper = psutil.cpu_percent(interval=1)
        # text
        CPU_TEXT = "CPU: {}% (In 1s)".format(cpuper)
        return CPU_TEXT

    def get_mem_info(self):
        # 获取内存的完整信息
        mem = psutil.virtual_memory()
        # 总内存大小 -- MB
        max_mem = self.size2Mb(mem.total)
        # 已使用内存 -- MB
        used_mem = self.size2Mb(mem.used)
        # 内存占用率
        mem_percent = mem.percent
        # text
        MEM_TEXT = "MEM: {}% {}/{}".format(mem_percent,used_mem,max_mem)
        return MEM_TEXT

    def get_disk_info(self):
        # 获取磁盘完整信息
        disk = psutil.disk_partitions(all=False)
        disk_info = []
        for d in disk:
            # 获取分区状态
            name = d[0]
            try:
                info = { 
                    "name":name.split(":")[0],
                    "disk_usage":str(psutil.disk_usage(name)[-1]),
                    "total":self.size2Mb(psutil.disk_usage(name)[0])
                }
            except PermissionError as e:
                name = name.split(":")[0],
                disk_info.append("磁盘:{}|{} 使用率: {}".format(name,"设备未就绪","设备未就绪"))
            else:
                disk_info.append("磁盘:{}|{} 使用率: {}%".format(info["name"],info["total"],info["disk_usage"]))

        DISK_TEXT = "DISK:\n" + "\n".join(disk_info)
        return DISK_TEXT

    def main(self):
        return self.get_cpu_info() + "\n" +\
                self.get_mem_info() + "\n" +\
                self.get_disk_info()

sysinfo = SysInfo()

if __name__ == "__main__":
    sysinfo = SysInfo()
    print(sysinfo.main())