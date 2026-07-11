from .chat_styles import CSS
from .chat_script import JS

HTML = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">

<style>
{styles}
</style>

</head>

<body>

<div class="titlebar">
<div class="title">
💬 Чат
</div>

<button class="close" onclick="pywebview.api.close_chat()">
✕
</button>

</div>

<div id="chat-list" class="messages">

</div>

<div class="input">

<input
id="message"
placeholder="Напишите сообщение...">

<button
class="send"
onclick="sendMessage()">

➤

</button>

</div>

<script>

{script}

</script>

</body>
</html>
"""

HTML = HTML.format(
    styles=CSS,
    script=JS
)