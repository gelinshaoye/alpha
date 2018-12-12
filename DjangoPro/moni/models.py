from django.db import models

class UserInfo(models.Model):
    class Meta:
        db_table = 'userinfo_tbl'

    uname = models.CharField(max_length=20,null=False)
    upwd = models.CharField(max_length=40)

# Create your models here.
class NetInfo(models.Model):
    class Meta:
        db_table = 'netinfo_tbl'

    ip = models.CharField(max_length=20,null=True)
    time = models.CharField(max_length=20,null=True)
    status = models.IntegerField(default=0,null=True)
    recv = models.IntegerField(default=0,null=True)
    sent = models.IntegerField(default=0,null=True)


class MemInfo(models.Model):
    class Meta:
        db_table = 'meminfo_tbl'

    ip = models.CharField(max_length=45,null=True)
    time = models.CharField(max_length=60,null=True)
    active = models.IntegerField(default=0,null=True)
    available = models.IntegerField(default=0,null=True)
    used = models.IntegerField(default=0,null=True)
    total = models.IntegerField(default=0,null=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    shared = models.IntegerField(default=0,null=True)
    inactive = models.IntegerField(default=0,null=True)
    buffers = models.IntegerField(default=0,null=True)
    cached = models.IntegerField(default=0,null=True)
    free = models.IntegerField(default=0,null=True)


class PartnerInfo(models.Model):
    class Meta:
        db_table = 'partnerinfo_tbl'

    ip = models.CharField(max_length=45,null=True)
    time = models.CharField(max_length=60,null=True)
    trace = models.CharField(max_length=300,null=True)
    port_status = models.CharField(max_length=30,null=True)
    ping = models.CharField(max_length=30,null=True)
    p_ip = models.CharField(max_length=45,null=True)
    p_port = models.IntegerField(default=0,null=True)


class PlatInfo(models.Model):
    class Meta:
        db_table = 'platinfo_tbl'

    ip = models.CharField(max_length=45,null=True)
    time = models.CharField(max_length=60,null=True)
    cpu_num = models.IntegerField(default=0,null=True)
    release1 = models.CharField(max_length=120,null=True)
    dist = models.CharField(max_length=90,null=True)
    machine = models.CharField(max_length=30,null=True)
    system = models.CharField(max_length=45,null=True)
    boot_time = models.CharField(max_length=60,null=True)


class SwapInfo(models.Model):
    class Meta:
        db_table = 'swapinfo_tbl'

    ip = models.CharField(max_length=45,null=True)
    time = models.CharField(max_length=60,null=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    free = models.IntegerField(default=0,null=True)
    total = models.IntegerField(default=0,null=True)
    used = models.IntegerField(default=0,null=True)
    sin = models.IntegerField(default=0,null=True)
    sout = models.IntegerField(default=0,null=True)


class CpuInfo(models.Model):
    class Meta:
        db_table = 'cpuinfo_tbl'

    ip = models.CharField(max_length=45,null=True)
    time = models.CharField(max_length=60,null=True)
    iowait = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    guest_nice = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    user = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    system = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    guest = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    steal = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    irq = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    nice = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    idle = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    softirq = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2,null=True)


class DiskInfo(models.Model):
    class Meta:
        db_table = 'diskinfo_tbl'

    ip = models.CharField(max_length=45,null=True)
    time = models.CharField(max_length=60,null=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    free = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    used = models.DecimalField(max_digits=5, decimal_places=2,null=True)
