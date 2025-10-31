from graphistry.plugins_types.embed_types import XSymbolic, ProtoSymbolic, TT

class EmbedDistScore:

    @staticmethod
    def TransE(h: TT, r: TT, t: TT) -> TT:
        return (h + r - t).norm(p=1, dim=1)

    @staticmethod
    def DistMult(h: TT, r: TT, t: TT) -> TT:
        return (h * r * t).sum(dim=1)

    @staticmethod
    def RotatE(h: TT, r: TT, t: TT) -> TT:
        return -(h * r - t).norm(p=1, dim=1)