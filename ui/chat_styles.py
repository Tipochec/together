CSS = r"""
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    background:#0f0f13;
    color:#fff;
    font-family:-apple-system,'Segoe UI',sans-serif;
    height:100vh;
    overflow:hidden;
}

.titlebar{
    height:40px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 14px;
    border-bottom:.5px solid rgba(255,255,255,.06);
}

.title{
    color:#d4537e;
    font-size:14px;
}

.close{
    width:28px;
    height:28px;
    border:none;
    border-radius:6px;
    background:transparent;
    color:rgba(255,255,255,.4);
    cursor:pointer;
}

.close:hover{
    background:rgba(255,255,255,.08);
}

.messages{
    height:calc(100vh - 95px);
    overflow-y:auto;
    padding:14px;
}

.input{
    height:55px;
    border-top:.5px solid rgba(255,255,255,.06);
    display:flex;
    gap:8px;
    padding:10px;
}

.input input{
    flex:1;
    background:#1a1820;
    border:none;
    outline:none;
    border-radius:10px;
    padding:0 12px;
    color:white;
}

.send{
    width:42px;
    border:none;
    border-radius:10px;
    background:#534ab7;
    color:white;
    cursor:pointer;
}

.message{
    max-width:75%;
    padding:10px 14px;
    border-radius:14px;
    margin-bottom:8px;
    word-break:break-word;
    font-size:13px;
}

.message.me{
    margin-left:auto;
    background:#534ab7;
}

.message.partner{
    margin-right:auto;
    background:#1a1820;
}

.time{
    margin-top:4px;
    font-size:10px;
    opacity:.5;
}
"""