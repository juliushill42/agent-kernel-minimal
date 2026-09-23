
from common import Store, chain_ok
CAPS={"read":True,"write":True,"net":False}
class Core:
    def __init__(self, db): self.s=Store(db)
    def submit(self, task_id, cap, payload):
        if cap not in CAPS: raise ValueError("unknown capability")
        if not CAPS[cap]: raise PermissionError("capability denied")
        return self.s.append("ak.submit", {"task":task_id,"cap":cap,"payload":payload,"state":"queued"})
    def run(self, task_id):
        import json
        recs=[json.loads(r["body"]) for r in self.s.list("ak.submit") if json.loads(r["body"])["task"]==task_id]
        if not recs: raise ValueError("unknown task")
        t=recs[-1]
        return self.s.append("ak.result", {"task":task_id,"state":"done","result":{"len":len(str(t["payload"]))}})
    def proof(self):
        self.submit("t1","read",{"q":"status"}); r=self.run("t1")
        denied="ok"
        try: self.submit("t2","net",{})
        except Exception as e: denied=str(e)
        return {"ok":chain_ok(self.s),"result":r,"net":denied}
