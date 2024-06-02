import threading
import sys
from .app import create_app
from .db.db_ops import run_periodic_db_refresh
from .extensions import output_buffer

app, socketio = create_app()

refresh_interval = 600  # 10 minutes in seconds
db_refresh_thread = threading.Thread(target=run_periodic_db_refresh, args=(app, refresh_interval))
db_refresh_thread.daemon = True  # This makes the thread exit when the main program exits
db_refresh_thread.start()

# Redirect output to buffer which is shown in the admin panel
sys.stdout = output_buffer
#sys.stderr = output_buffer # Comment this to get debug in console

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
    
