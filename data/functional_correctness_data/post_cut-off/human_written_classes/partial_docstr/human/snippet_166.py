from dataclasses import dataclass

@dataclass
class MeshRank:
    """Represents a rank in the device mesh.

    This is a tuple of (DP, SP, TP, PP) ranks.
    """
    dp: int
    sp: int
    tp: int
    pp: int
    world_size: int
    dp_size: int
    pp_size: int

    def is_collection_dp_rank(self) -> bool:
        """Check if this rank is a DP rank to collect from

        This is the rank with (SP=0, TP=0, PP=pp_size-1)

        Note: double check this for ETP > 1 (but this is not a typically used case)
        """
        return self.tp == 0 and self.pp == self.pp_size - 1 and (self.sp == 0)

    def __str__(self) -> str:
        return f'MeshRank(dp={self.dp}, sp={self.sp}, tp={self.tp}, pp={self.pp}, world_size={self.world_size}, dp_size={self.dp_size}, pp_size={self.pp_size})'

    def __repr__(self) -> str:
        return self.__str__()