import datetime

class Host:

    def __init__(self, dns, id, ip, last_scan, netbios, os, tracking_method):
        self.dns = str(dns)
        self.id = int(id)
        self.ip = str(ip)
        try:
            last_scan = str(last_scan).replace('T', ' ').replace('Z', '').split(' ')
            date = last_scan[0].split('-')
            time = last_scan[1].split(':')
            self.last_scan = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
        except IndexError:
            self.last_scan = 'never'
        self.netbios = str(netbios)
        self.os = str(os)
        self.tracking_method = str(tracking_method)

    def __repr__(self):
        return f'ip: {self.ip}, qualys_id: {self.id}, dns: {self.dns}'