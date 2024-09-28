import functions_framework
from flask import jsonify
import socket

@functions_framework.http
def connectivity_test(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    # Postされたデータを取得
    if request_json and 'host' in request_json:
        host = request_json['host']
    else:
        return "parameter 'host' is missing"
    if request_json and 'port' in request_json:
        port = request_json['port']
    else:
        return "parameter 'port' is missing"

    # 疎通テスト
    return tcp_port_test(host, port)


def tcp_port_test(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_code = sock.connect_ex((host, port))
        sock.close()

        if return_code == 0:
            result = {
                "Status": "OK(Port is open)",
                "Return Code": return_code
            }
            print(f"port: {port} is open.[return_code: {return_code}]")
        else:
            result = {
                "Status": "NG(Port is not open)",
                "Return Code": return_code
            }
            print(f"port: {port} is not open.[return_code: {return_code}]")

        result["host"] = host
        result["port"] = port

    except OSError as e:
        result = {
            "Status": "Error",
            "Message": f"[Exception]{e.__class__.__name__}: {e}"
        }
        print(f"[Exception]{e.__class__.__name__}: {e}")

    finally:
        result["host"] = host
        result["port"] = port

        return jsonify(result)
