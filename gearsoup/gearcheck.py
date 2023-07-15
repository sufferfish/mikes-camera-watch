from typing import Any

class GearCheck():
    def __init__(self, memjson: dict, diskjson: dict) -> None:
        self.memj = memjson
        self.diskj = diskjson

    def _get_refs_from_json(self, jdict) -> list:
        return [j['ref'] for j in jdict if isinstance(j['ref'], int)]

    def compare_jsons(self) -> list|None:
        oldj = self._get_refs_from_json(jdict=self.diskj)
        newj = self._get_refs_from_json(jdict=self.memj)

        res = [x for x in oldj + newj if x not in oldj and x not in newj]

        if not res:
            return False
        else:
            self.new_listings = res
            return True

    def get_new_listings(self) -> list[dict[str, Any]]:
        if self.new_listing is not None:
            ref_dict = {d['ref']: d for d in self.memj}
            # self.new_gear = [ref_dict[k] for k in self.new_listing if k in ref_dict]
            return [ref_dict[k] for k in self.new_listing if k in ref_dict]