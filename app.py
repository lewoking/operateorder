from flask import Flask,request,render_template
from generateticket import transaction
import webbrowser
app = Flask(__name__)

#返回相应页面结果
@app.route('/')
def hello_world():
    return render_template('test.html')  

#从test页面获取输入并传入字符替换函数得到结果
@app.route('/test/', methods=['GET', 'POST'])
def test():
    target = {}
    if request.method == 'POST':
        postData = request.form
        DataA = postData['bh']
        DataB = postData['operate']
        target = transaction(str(DataA),str(DataB))
    return render_template('result.html',result = target)

#自动打开浏览器
webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    app.run(debug=True)
    