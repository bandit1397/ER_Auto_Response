WebSocket + PWA + polling + 사이렌 + 알림
http://localhost:5000/hospital/B
http://localhost:5000/control


pyinstaller --onefile --noconsole ^
--hidden-import=engineio.async_drivers.threading ^
--hidden-import=socketio.async_drivers.threading ^
--add-data "templates;templates" ^
--add-data "static;static" ^
server.py
