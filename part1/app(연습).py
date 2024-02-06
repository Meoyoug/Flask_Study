from flask import Flask, request, Response
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, This is Main Page"

@app.route('/about')
def about():
    return "Hello, This is About Page"

# 동적으로 URL 파라미터 값을 받아서 처리하기
@app.route('/user/<username>')
def user_profile(username):
    return f"Username : {username}"

# requests 라이브러리를 활용해서 post 날려보기
@app.route('/test')
def test():
    url = 'http://127.0.0.1:5000/submit'
    data = 'test data'
    requests.post(url=url, data=data)

    return Response("Successfully post", status=200)

@app.route('/submit', methods= ["GET", "POST", "DELETE", "PUT"])
def submit():
    print(request.method)

    if request.method == 'GET':
        print("GET Method")
    if request.method == 'POST':
        print("POST Method",request.data)

    return 'success'

if __name__ == "__main__":
    app.run()

