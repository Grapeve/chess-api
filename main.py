import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

import json
import time
from utils import predictAction

app = FastAPI()


@app.get("/")
def hello_world():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Success!"
        }
    )


@app.get("/chess/{chessboard_status}")
def read_item(chessboard_status: str, move_status: str):
    """
    chessboard_status: 棋子移动前的棋局状态 \n
    move_status: 棋子移动状态
    """
    start_time = time.time()
    possible_chess_moving = predictAction(chessboard_status, move_status)
    possible_chess_moving = [json.loads(json_str) for json_str in possible_chess_moving]
    end_time = time.time()
    print("spend_time: ", end_time - start_time)
    return JSONResponse(
        status_code=200,
        content={
            "possible_chess_moving": possible_chess_moving,
        }
    )


if __name__ == "__main__":
    uvicorn.run(app)
