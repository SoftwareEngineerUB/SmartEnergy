from app.main import app, init_mqtt_demo, socketio

if __name__ == "__main__":
    init_mqtt_demo()
    # socketio.run(app, host='localhost', port=5555, use_reloader=False, debug=True)
