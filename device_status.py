from zk import ZK

def device_info(ip) :
    from device_info import Device_Info
    conn = None
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try:
        conn = zk.connect()
        conn.disable_device()
        conn.read_sizes()
        device_info = Device_Info(
            ip, conn.get_device_name(), conn.get_serialnumber(), conn.get_mac(), conn.users, conn.fingers, conn.records
        )
        conn.enable_device()
        return device_info
    except Exception as e:
        print ('Process Terminate : {}'.format(e))
    finally:
        if conn :
            conn.disconnect()