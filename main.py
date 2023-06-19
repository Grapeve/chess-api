import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import json
import time
from utils import predictAction, recordChessboardStatus

app = FastAPI()


@app.get("/")
def hello_world():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Success!"
        }
    )


@app.get("/predictChessAction/{chessboard_status}")
def read_item(chessboard_status: str):
    """
    chessboard_status: 棋子移动后的棋局状态 \n
    """
    start_time = time.time()
    possible_chess_moving = predictAction(chessboard_status)
    possible_chess_moving = [json.loads(json_str) for json_str in possible_chess_moving]
    end_time = time.time()
    print("spend_time: ", end_time - start_time)
    return JSONResponse(
        status_code=200,
        content={
            "possible_chess_moving": possible_chess_moving,
        }
    )


class ChessboardData(BaseModel):
    chessboardStatus: str
    predictAction: str
    chessboardStatusAfterPredictAction: str
    result: str


@app.post("/recordChessStatus")
def record_chess_status(data: ChessboardData):
    record_status = recordChessboardStatus(data)
    if record_status:
        return JSONResponse(
            status_code=200,
            content={
                "message": "successful",
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "message": "successful",
            }
        )


if __name__ == "__main__":
    uvicorn.run(app)
