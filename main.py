from fastapi import FastAPI
from pydantic import BaseModel


class BaseResponse(BaseModel):
    user_name: str


app = FastAPI()


@app.get("/", response_model=BaseResponse)
def hello():
    pass

"The man didn't eat anything because he is doing fast"

[
    vectors,
    vectors
]

now when it goest to he

Query(he)

Key(All Words)
[
    "the"=>0.33,
    "man"=>0.73,
]

Value("man")