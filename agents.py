"""Transparent, modular agents for JalSakhi AI. Shared state is passed through each stage."""
from datetime import datetime
import uuid

def new_id(prefix): return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

class CommunicationAgent:
    name="Community Communication Agent"
    def process(self,message,language="English",source_id=None):
        m=message.lower()
        if any(w in m for w in ["safe","पिण्यायोग्य","safe आहे","is my water"]): intent="safety_query"
        elif any(w in m for w in ["repair","leak","गळती","tank","टाकी"]): intent="maintenance"
        elif any(w in m for w in ["smell","dirty","muddy","गढूळ","दुर्गंध","taste","colour","color"]): intent="water_complaint"
        else: intent="general"
        return {"case_id":new_id("JS"),"message":message,"language":language,"source_id":source_id,
                "intent":intent,"created_at":datetime.now().isoformat(timespec="minutes"),
                "status":"Open","priority":"Normal","assigned_to":"VWSC"}

class TestingAgent:
    name="Local Testing Agent"
    def assess(self,case,source,test_record=None):
        case["source_name"]=source.get("name","Unknown source")
        case["testing_recommendation"]="Field verification"
        case["test_record"]=test_record
        if case["intent"]=="water_complaint":
            case["priority"]="High"
            case["testing_recommendation"]="Arrange a field check; consider lab testing based on VWSC review"
        return case

class AlertAgent:
    name="Alert Agent"
    def create(self,case):
        case["alert"]={"required":case["priority"]=="High","acknowledged":False,
                       "message":f'{case["priority"]} priority concern for {case.get("source_name","source")}' }
        return case

class EscalationAgent:
    name="Escalation & Lab Coordination Agent"
    def route(self,case):
        case["escalation"]={"required":case["priority"]=="High","destination":"VWSC testing member",
                           "status":"Pending review" if case["priority"]=="High" else "Not required"}
        return case

class RecordAgent:
    name="Village Water Record Agent"
    def attach(self,case,records):
        case["history_count"]=sum(1 for r in records if r.get("source_id")==case.get("source_id"))
        return case

class Pipeline:
    def __init__(self):
        self.communication=CommunicationAgent(); self.testing=TestingAgent()
        self.alert=AlertAgent(); self.escalation=EscalationAgent(); self.record=RecordAgent()
    def run(self,message,language,source_id,source,records,test_record=None):
        case=self.communication.process(message,language,source_id)
        case=self.testing.assess(case,source,test_record)
        case=self.alert.create(case)
        case=self.escalation.route(case)
        case=self.record.attach(case,records)
        return case
