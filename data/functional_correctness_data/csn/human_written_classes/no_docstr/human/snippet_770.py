from elastic_transport import ObjectApiResponse

class CountResponseParser:

    def __init__(self, response: ObjectApiResponse) -> None:
        self.body = response.body

    @property
    def total_hits(self) -> int:
        return self.body.get('count', 0)

    @property
    def total_hits_relation(self) -> str:
        return str(SearchQuery.TotalHitsRelation.ACCURATE)