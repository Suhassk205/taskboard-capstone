import os
from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy import select, func, text, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from prometheus_fastapi_instrumentator import Instrumentator
from .db import get_db
from .models import Ticket
from .schemas import TicketCreate, TicketUpdate, TicketOut

app = FastAPI(title="CampusDesk API", version="1.0.0")
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"service":"CampusDesk", "version":os.getenv("APP_VERSION","local")}

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(503,"Database is unavailable")
    return {"status":"ready"}

@app.get("/api/tickets", response_model=list[TicketOut])
def tickets(status: str | None = None, search: str = "", db: Session = Depends(get_db)):
    query = select(Ticket)
    if status:
        query = query.where(Ticket.status == status)
    if search:
        query = query.where(or_(Ticket.title.ilike(f"%{search}%"),Ticket.requester.ilike(f"%{search}%")))
    return list(db.scalars(query.order_by(Ticket.id.desc()).limit(200)))

@app.get("/api/tickets/stats")
def stats(db: Session = Depends(get_db)):
    counts = dict(db.execute(select(Ticket.status,func.count(Ticket.id)).group_by(Ticket.status)).all())
    urgent = db.scalar(select(func.count(Ticket.id)).where(Ticket.priority=="urgent",Ticket.status!="resolved"))
    return {"total":sum(counts.values()), "open":counts.get("open",0), "in_progress":counts.get("in_progress",0), "resolved":counts.get("resolved",0), "urgent":urgent}

def find(db, ticket_id):
    ticket = db.get(Ticket,ticket_id)
    if not ticket:
        raise HTTPException(404,"Ticket not found")
    return ticket

@app.get("/api/tickets/{ticket_id}",response_model=TicketOut)
def detail(ticket_id:int,db:Session=Depends(get_db)):
    return find(db,ticket_id)

@app.post("/api/tickets",response_model=TicketOut,status_code=201)
def create(payload:TicketCreate,db:Session=Depends(get_db)):
    ticket=Ticket(**payload.model_dump());db.add(ticket);db.commit();db.refresh(ticket)
    return ticket

@app.put("/api/tickets/{ticket_id}",response_model=TicketOut)
def update(ticket_id:int,payload:TicketUpdate,db:Session=Depends(get_db)):
    ticket=find(db,ticket_id)
    for key,value in payload.model_dump().items():setattr(ticket,key,value)
    db.commit();db.refresh(ticket)
    return ticket

@app.delete("/api/tickets/{ticket_id}",status_code=204)
def delete(ticket_id:int,db:Session=Depends(get_db)):
    db.delete(find(db,ticket_id));db.commit()
    return Response(status_code=204)
