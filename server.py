from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
	<title>Login</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="/css/font.css">
<!--===============================================================================================-->
</head>
<body>
<ul>
  <li><a class="active" href="#home">Home</a></li>
  <li><a href="#contact">Contact</a></li>
  <li><a href="#about">About</a></li>
</ul>
  <div class="form">
    <form class="login-form">
      <input type="text" placeholder="username"/>
      <input type="password" placeholder="password"/>
      <button>LOGIN</button>
      <p class="message">Not registered? <a href="#">Create an account</a></p>
    </form>
  </div>
</body>
</html>"""


if __name__ == "__main__":
    app.run()
