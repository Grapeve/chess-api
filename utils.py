from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, count, lit
from pyspark.sql.window import Window
import csv


def predictAction(chessboardStatus):
    # 创建SparkSession
    spark = SparkSession.builder.appName("predictAction").getOrCreate()
    # 读取数据
    df_chess = spark.read.csv("chessboard.csv", header=False)
    df_chess = df_chess.withColumnRenamed("_c0", "chessboardStatus") \
        .withColumnRenamed("_c1", "predictAction") \
        .withColumnRenamed("_c2", "chessboardStatusAfterPredictAction") \
        .withColumnRenamed("_c3", "result")
    # 根据输入的棋局状态和棋子移动状态去查找
    filtered_df_chess = df_chess.filter(
        (col("chessboardStatus") == chessboardStatus))
    # 统计重复数据出现次数
    result_df_chess = filtered_df_chess.groupBy(filtered_df_chess.columns).agg(count("*").alias("count"))
    # 排序
    result_df_chess = result_df_chess.orderBy(col("count").desc())
    # 添加一个名为"key"的列，包含按顺序递增的数字
    df_with_key = result_df_chess.select(lit(1).alias("key"), "*")
    return result_df_chess.toJSON().collect()


def recordChessboardStatus(chessboardData):
    try:
        with open('recordChessboard.csv', 'a', newline='') as f:
            csvwriter = csv.writer(f)
            row_data = [
                chessboardData.chessboardStatus,
                chessboardData.predictAction,
                chessboardData.chessboardStatusAfterPredictAction,
                chessboardData.result
            ]
            csvwriter.writerow(row_data)
            return True
    except Exception as e:
        print(f'An error occurred: {e}')
        return False


if __name__ == "__main__":
    chessboard_status = "0919293949596979891747062646668600102030405060708012720323436383"
    possible_chess_moving = predictAction(chessboard_status)
    print(possible_chess_moving)
