import os
import random
import json
from datetime import datetime

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_socketio import SocketIO, ConnectionRefusedError
from loguru import logger


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def get_settlement():
    """ This function generates test settlement data for front-end,
        current ET users are mapped as below:

        智駕車BEMS=> Carlab_BEMS
        沙崙綠能科學城C區BEMS=> SGESC_C_BEMS
        沙崙綠能科學城D區BEMS=> SGESC_D_BEMS
        歸仁校區建研所BEMS => ABRI_BEMS

        Data sample:
        {
            "date": '2019/12/09',
            "time": '15:55',
            "transactions": [
                {
                    "seller": "SGESC_C_BEMS",
                    "buyer": "SGESC_D_BEMS",
                    "achievement": 0.15
                }
            ]
        }
    """
    achievement_list = list(range(0, 105, 5))

    # Transactions are fixed for the test
    transactions = [
        {
            "seller": "Carlab_BEMS",
            "buyer": "SGESC_C_BEMS",
            "achievement": random.choice(achievement_list) / 100,
        },
        {
            "seller": "SGESC_D_BEMS",
            "buyer": "SGESC_C_BEMS",
            "achievement": random.choice(achievement_list) / 100,
        },
        {
            "seller": "SGESC_C_BEMS",
            "buyer": "ABRI_BEMS",
            "achievement": random.choice(achievement_list) / 100,
        },
    ]
    now = datetime.utcnow()
    data = {
        "date": now.strftime("%Y/%m/%d"),
        "time": now.strftime("%H:%M"),
        "transactions": transactions,
    }

    return json.dumps(data)


@socketio.on("connect")
def is_verified():
    print("here")
    verified = True
    # if verified is False:
    #     raise ConnectionRefusedError("Unauthorized access")


@app.route('/test_socket', methods=['POST'])
def post():
    socketio.emit("transaction", get_settlement())
    logger.info("[Emit Settlement Transactions]\nMessage sent")
    return jsonify({"msg": "Successfulling emitted settlement transactions"})



def main():
    socketio.run(app, host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=True)


if __name__ == "__main__":
    main()
