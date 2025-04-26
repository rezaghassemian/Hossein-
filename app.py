from flask import Flask, request, render_template_string, session
import re
import sympy
from sympy import symbols, solve, Eq
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

def normalize_persian(text):
    persian_chars = {'ك':'ک', 'ي':'ی', 'ة':'ه', 'أ':'ا'}
    return ''.join(persian_chars.get(c, c) for c in text.strip())

FAQ = {
    "ساخته شدی؟": "من در سال 2024 ساخته شدم!",
    "کمک می‌کنی؟": "بله! سوالات ریاضی بپرسید مثل: 'مساحت مربع با ضلع ۵' یا 'حل کن ۲x=۱۰'"
}

HTML = '''
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>چت‌بات حسین</title>
    <style>
        body { font-family: 'Vazir', sans-serif; background: #f0f0f0; padding: 30px; direction: rtl; }
        .chat-box { max-width: 600px; background: white; padding: 20px; border-radius: 10px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .msg { margin: 10px 0; }
        .user { text-align: right; color: #333; }
        .bot { text-align: left; color: #006600; }
    </style>
</head>
<body>
    <div class="chat-box">
        <h2>سلام! من حسین هستم، چت‌بات فارسی شما.</h2>
        <form method="post">
            <input name="msg" type="text" style="width:90%; padding:8px" autofocus/>
            <button type="submit">ارسال</button>
        </form>
        {% if user_msg %}
            <div class="msg user"><strong>شما:</strong> {{ user_msg }}</div>
            <div class="msg bot"><strong>حسین:</strong> {{ response }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

def get_response(text):
    text = normalize_persian(text)
    if text in FAQ:
        return FAQ[text]
    if 'مساحت مربع' in text:
        nums = re.findall(r'\d+', text.replace('۰','0').replace('۱','1').replace('۲','2'))
        return f"مساحت: {int(nums[0])**2}" if nums else "لطفاً عدد ضلع را بگویید."
    if 'حل کن' in text and '=' in text:
        try:
            x = symbols('x')
            left, right = text.split('حل کن')[-1].split('=')
            eq = Eq(eval(left.strip()), eval(right.strip()))
            return f"پاسخ: x = {solve(eq, x)[0]}"
        except:
            return "معادله نامعتبر است"
    return "متوجه نشدم. مثال: 'مساحت مربع با ضلع ۵' یا 'حل کن ۲x=۱۰'"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_msg = request.form.get("msg", "")
        response = get_response(user_msg)
        return render_template_string(HTML, user_msg=user_msg, response=response)
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)