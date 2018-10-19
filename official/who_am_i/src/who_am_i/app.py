from flask import Flask, render_template, request, make_response, url_for
app = Flask(__name__)

flag = "flag{i_canN0t_BReW_c0ffEE!}"
flag2 = "flag{delivering_tea_to_DaLa0}"
brew_url = "/the_super_great_hidden_url_for_brewing_tea/"

@app.route('/')
def index():
    return render_template("index.html"), 418

@app.route('/identity', methods=['POST'])
def identity():
    try:
        user_input_name = request.form["name"].lower()
        if "teapot" in user_input_name:
            return """
            <p>Yes, I finally realized that I am a teapot!</p>
            <p>This is my gift for you:</p>
            <p>{0}</p>
            <p>Come to <a href="{1}">This Link</a>, help me brew some tea, and you can get the 2nd FLAG!<p>""".format(flag, url_for("brew"))
        elif "coffee" in user_input_name:
            return """
            <p>You said COFFEE? You sure?</p>
            <p>Maybe you should find someone else to brew coffee for you.</p>
            """
        else:
            return """
            <p>I am not really sure whether your answer is right.</p>
            <p>You should probably try again.</p>
            """
    except (KeyError, AttributeError) as _:
        return """
        <p>You know what?</p>
        <p>Hacking this page WON'T help.</p>
        <p>After all, I am NOT written in the "best language in the world".</p>
        """

@app.route(brew_url, methods=["POST", "BREW", "GET", "WHEN"])
@app.route(brew_url + '<string:tea_type>', methods=["POST", "BREW", "GET", "WHEN"])
def brew(tea_type=None):
    if request.method == 'POST':
        return """
        <p>The method "POST" is deprecated.</p>
        <p>See RFC-7168 for more information.</p>
        """
    elif request.method == 'GET':
        return """
        <p>Brewing tea is not so easy.</p>
        <p>Try using other <i>methods</i> to request this page.</p>
        """
    elif request.method == "WHEN":
        return """
        <p>I'm NOT a coffee pot.</p>
        <p>Please, read RFC-7168, not RFC-2324.</p>
        """, 418
    try:
        header_content_type = request.headers["Content-Type"]
        if header_content_type == "message/coffeepot":
            return """
            <p>Don't you remember what's in the 1st FLAG?</p>
            """, 418
        if header_content_type != "message/teapot":
            return """
            <p>According to your header, it seems that you are not requesting for tea.</p>
            <p>Stop.</p>
            """
        if tea_type == "black_tea":
            return "Here is your tea: {}".format(flag2)
        elif tea_type != None:
            return """
            <p>Sorry, but this teapot doesn't support tea {}<p>
            """.format(tea_type)
        else:
            resp = make_response("Supported tea type:")
            resp.headers["Alternates"] = '{{"{0}" {{type message/teapot}}}}'.format(brew_url + "black_tea")
            return resp, 300

    except KeyError:
        return """
        <p>Please check if there is anything missing in your header.</p>
        """


if __name__ == '__main__':
    app.run('0.0.0.0', 5001, threaded=True)


