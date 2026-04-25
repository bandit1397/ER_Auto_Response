WebSocket + PWA + polling + 사이렌 + 알림
http://localhost:5000/hospital/B
http://localhost:5000/control


#pyinstaller --onefile --noconsole ^
--hidden-import=engineio.async_drivers.threading ^
--hidden-import=socketio.async_drivers.threading ^
--add-data "templates;templates" ^
--add-data "static;static" ^
server.py

# “경찰 실전 배포용 100% 안정 버전” (로그 + 장애복구 + 자동재시작)
# taskkill /F /IM server.exe
taskkill /F /IM python.exe  // DIST 삭제/ CMD 에서 작업
