# coding=utf-8
from flask import Flask
from flask import request
from concurrent.futures import ThreadPoolExecutor
from requests_handler import *
from pepper_handler import *
import json
#----------------------------------------------------------------------------------------------------------------------#
app = Flask(__name__)
executor = ThreadPoolExecutor(1)

SERVER_IP = "192.168.1.106"
SERVER_PORT = "5000"
#----------------------------------------------------------------------------------------------------------------------#
@app.route('/connect', methods=["POST"])
def connect():
    result = handle_connect_request(request.json)
    return result

@app.route('/logger', methods=["GET"])
def logger():
    result = handle_logger_request()
    return result

@app.route('/scenarios', methods=["GET"])
def get_scenarios_list():
    result = handle_scenarios_list_request()
    return result

@app.route('/scenarios', methods=["POST"])
def create_new_scenario():
    result = handle_creating_new_scenario_request(request.json)
    return result

@app.route('/scenarios/remove', methods=["GET"])
def delete_scenario():
    result = handle_deleting_scenario_request(request.args.get['name'])
    return result

@app.route('/scenarios', methods=["GET"])
def scenarios_get_details_and_run():
    result = handle_scenario_run_request(request.args.get['name'], request.args.get['run'], request.args.get['start'], request.args.get['end'])
    return result

@app.route('/scenarios', methods=["PUT"])
def modify_scenario():
    result = handle_modify_scenario_request(request.args.get['name'], request.json)
    return result

@app.route('/sequences', methods=["GET"])
def get_sequences_list():
    result = handle_sequences_list_request()
    return result

@app.route('/media', methods=["GET"])
def get_media_list():
    result = handle_media_list_request()
    return result

@app.route('/record', methods=["GET"])
def start_stop_recording():
    result = handle_recording_toggle_request(request)
    return result

@app.route('/recordings', methods=["GET"])
def get_recordings_list():
    result = handle_recordings_list_request()
    return result

@app.route('/recordings', methods=["GET"])
def play_recording():
    result = handle_play_recording_request(request.args.get['name'])
    return result

@app.route('/settings', methods=["GET"])
def get_settings():
    result = handle_get_settings_request()  #ta metoda ma zostać niezaimplementowana, bo uznaliśmy, że nie ma ustawień robota, które chcielibyśmy uzyskiwać, ale perspektywicznie można to zostawić
    return result

@app.route('/settings', methods=["POST"])
def set_settings():
    result = handle_set_settings_request(request.json)  #ta metoda ma zostać niezaimplementowana, bo uznaliśmy, że nie ma ustawień robota, które chcielibyśmy uzyskiwać, ale perspektywicznie można to zostawić
    return result

@app.route('/clear_queue', methods=["GET"])
def clear_queue():
    result = handle_clear_queue_request()
    return result

@app.route('/add_action', methods=["POST"])
def add_action():
    result = handle_add_action_request(request.json)
    return result
#----------------------------------------------------------------------------------------------------------------------#
@app.before_first_request
def initialize():
    executor.submit(initialize_queue)
    executor.submit(establish_connection)
#----------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(threaded=True, processes=2, host=SERVER_IP, port=SERVER_PORT)
