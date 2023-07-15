class GearCheck:
    def __int__(self, memjson, diskjson):
        self.memj = memjson
        self.diskj = diskjson

    def _get_refs_from_json(self, j) -> list:
        return [j['ref'] for r in j]

    def compare_jsons(self):
        oldj = self._get_refs_from_json(self.diskj)
        newj = self._get_refs_from_json(self.memj)
