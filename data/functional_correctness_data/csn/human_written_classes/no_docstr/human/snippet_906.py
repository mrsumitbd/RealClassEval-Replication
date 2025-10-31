class NodeStats:

    def __init__(self, data: dict):
        self.uptime = data['uptime']
        self.players = data['players']
        self.playing_players = data['playingPlayers']
        memory = data['memory']
        self.memory_free = memory['free']
        self.memory_used = memory['used']
        self.memory_allocated = memory['allocated']
        self.memory_reservable = memory['reservable']
        cpu = data['cpu']
        self.cpu_cores = cpu['cores']
        self.system_load = cpu['systemLoad']
        self.lavalink_load = cpu['lavalinkLoad']
        frame_stats = data.get('frameStats', {})
        self.frames_sent = frame_stats.get('sent', -1)
        self.frames_nulled = frame_stats.get('nulled', -1)
        self.frames_deficit = frame_stats.get('deficit', -1)

    def __repr__(self):
        return f'<NodeStats: uptime={self.uptime}, players={self.players}, playing_players={self.playing_players}, memory_free={self.memory_free}, memory_used={self.memory_used}, cpu_cores={self.cpu_cores}, system_load={self.system_load}, lavalink_load={self.lavalink_load}>'