from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run
from drizm_commons.sqla import Database, Base
import sqlalchemy as sqla
from typing import List

app = FastAPI()
db = Database(
    dialect="sqlite"
)


class MyBase(BaseModel):
    class Config:
        orm_mode = True


class MyTable(Base):
    title = sqla.Column(sqla.String(50))
    author = sqla.Column(sqla.String(50))


class MyTableSchema(MyBase):
    pk: int
    title: str
    author: str


@app.get("/my_table", response_model=List[MyTableSchema])
def get_item():
    with db.Session() as sess:

        return sess.query(MyTable).all()


@app.post("/my_table", response_model=MyTableSchema)
def post_item():
    with db.Session() as sess:
        t = MyTable(title= "newtitle", author= "hahah")
        sess.add(t)

    return t


@app.put("/my_table", response_model=MyTableSchema)
def put_item():
    with db.Session() as sess:
        new = sess.query(MyTable).get(1)
        new.title = "Pls work"
        new.author = "Stalin v.2"

    return new

@app.delete("/my_table", response_model=MyTableSchema)
def delete_item():
    with db.Session() as sess:
        table = sess.query(MyTable).filter(MyTable.pk==1).one()
        sess.delete(table)
    return table

if __name__ == '__main__':
    db.create()

    with db.Session() as sess:
        t = MyTable(
            title="Hallo",
            author="Stalin"
        )
        sess.add(t)

    run(app)