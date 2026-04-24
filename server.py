from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime

print("🔥 server.py 실행됨")

app = Flask(__name__)
CORS(app)

# DB 초기화
def init_db():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        requestID TEXT,
        hospital TEXT,
        summary TEXT,
        eta TEXT,
        response TEXT,
        time TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# 🟢 요청 생성
@app.route('/request', methods=['POST'])
def create_request():
    data = request.json

    print("🔥 REQUEST 들어옴:", data)  
    print("🔥 hospitals:", data.get('hospitals'))

    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    for h in data['hospitals']:
        cur.execute("""
        INSERT INTO requests (requestID, hospital, summary, eta, response, time)
        VALUES (?, ?, ?, ?, '', ?)
        """, (
            data['requestID'],
            h,
            data.get('summary',''),
            data.get('eta',''),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# 🟢 응답 처리 (중복 방지)
@app.route('/response')
def response():
    requestID = request.args.get('requestID')
    hospital = request.args.get('hospital')
    resp = request.args.get('response')

    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    cur.execute("""
    SELECT response FROM requests
    WHERE requestID=? AND hospital=?
    """, (requestID, hospital))

    row = cur.fetchone()

    if row and row[0]:
        conn.close()
        return "already responded"

    cur.execute("""
    UPDATE requests
    SET response=?, time=?
    WHERE requestID=? AND hospital=?
    """, (
        resp,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        requestID,
        hospital
    ))

    conn.commit()
    conn.close()

    return "ok"


# 🟢 상태 조회
@app.route('/status/<requestID>')
def status(requestID):
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    cur.execute("""
    SELECT hospital, summary, eta, response
    FROM requests
    WHERE requestID=?
    """, (requestID,))

    rows = cur.fetchall()
    conn.close()

    result = [
        {
            "hospital": r[0],
            "summary": r[1],
            "eta": r[2],
            "response": r[3]
        }
        for r in rows
    ]

    return jsonify(result)


# 🟢 병원용 최신 요청
@app.route('/latest/<hospital>')
def latest(hospital):
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    cur.execute("""
    SELECT requestID, summary, eta, response
    FROM requests
    WHERE hospital=?
    ORDER BY time DESC
    LIMIT 1
    """, (hospital,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({})

    return jsonify({
        "requestID": row[0],
        "summary": row[1],
        "eta": row[2],
        "response": row[3]
    })


# 👉 여기 추가하면 됩니다 ⭐
@app.route('/hospital')
def hospital():
    return render_template('병원.html')


@app.route('/control')   # 👈 여기 추가
def control():
    return render_template('상황실.html')

@app.route('/test')
def test():
    return "test ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
print("👉 현재 실행된 server.py 맞음")

print(cur.execute("SELECT * FROM requests").fetchall())

