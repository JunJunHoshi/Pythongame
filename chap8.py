import tkinter
import time

# 解読関数
def decode_line(event):
    global current_line, bgimg, lcharimg, ccharimg, rcharimg, popularity, money, health, motibe, window, count
    if current_line >= len(scenario):
        return;
    # 1行読み込み
    line = scenario[current_line]
    current_line = current_line + 1
    
    line = line.replace("\\n", "\n").strip()
    params = line.split(" ")
    if window==1:
        canvas.create_rectangle(50, 60, 200, 230, fill='white')
        popularity_text=tkinter.Label(text="人望 "+str(popularity)+" 人 ", bg='white')
        popularity_text.place(x=60, y=70)
        money_text=tkinter.Label(text="財力 "+str(money)+" 万 ", bg='white')
        money_text.place(x=60, y=100)
        health_text=tkinter.Label(text="健康 "+str(health)+" H ", bg='white')
        health_text.place(x=60, y=130)
        motibe_text=tkinter.Label(text="モチベ "+str(motibe)+" M  ",bg='white')
        motibe_text.place(x=60, y=160)
    if popularity<0 or money<0 or health<0 or motibe<0:
        canvas.create_rectangle(0, 0, 900, 460, fill='red')
        end_text=tkinter.Label(text="「あ、あれ　そんなバカな.....」", fg='white', bg='red')
        end_text.place(x=260, y=130)
        time.sleep(3)
        gameover_text=tkinter.Label(text='GAME OVER', font=20, bg='red')
        gameover_text.place(x=350, y=170)
        count_text=tkinter.Label(text="あなたの問題解決数は"+str(count-1)+"です。", bg='red')
        count_text.place(x=300, y=210)
        message.unbind('<Button-1>')
        current_line=999999
        return;
     
    # 分岐
    if line[0] != "#":
        message["text"] = line
        button1 = tkinter.Button(text="はい")
        button2 = tkinter.Button(text="いいえ")
        button1.place(x=700, y=60)
        button2.place(x=700, y=150)
        button1["command"]= lambda: button_clk(int(params[1]),int(params[2]),int(params[3]),int(params[4]))
        button2["command"]= lambda: button_clk(int(params[5]),int(params[6]),int(params[7]),int(params[8]))
        button1["state"]="disabled"
        button2["state"]="disabled"
        return
    elif params[0] == "#back":
        canvas.delete("all")
        canvas.create_rectangle(0, 0, 900, 460, fill='black')
    elif params[0] == "#putChar":
        if params[2] == "L":
            canvas.delete("left")
            lcharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(200, 160, image=lcharimg, tag="left")
        elif params[2] == "R":
            canvas.delete("right")
            rcharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(700, 160, image=rcharimg, tag="right")
        else:
            canvas.delete("center")
            ccharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(450, 160, image=ccharimg, tag="center")
    elif params[0] == "#branch":
        message.unbind("<Button-1>")
        btn = tkinter.Button(text=params[2], width=20)
        branch.append(btn)
        btn["command"] = lambda : jump_to_line(int(params[1])-1)
        btn.place(x=300, y=60+int(params[1])*60)
        jumplabel.append(params[3])
        if params[4] == "n":
            return
    elif params[0] == "#jump":
        label = params[1].strip()
        # ジャンプ先を探す
        for l in range(len(scenario)):
            if scenario[l].strip() == "## " + label:
                current_line = l
                decode_line(None)
                return
    elif params[0].strip() == "#end":
        message["text"] = "終わり"
        message.unbind("<Button-1>")
        current_line = 999999999
    elif params[0]=="#statas":
        window=1
    elif params[0]=="#quest":
        message.unbind("<Button-1>")
        button1 = tkinter.Button(text="はい")
        button2 = tkinter.Button(text="いいえ")
        button1.place(x=700, y=60)
        button2.place(x=700, y=150)
        button1["command"]= lambda: button_clk(int(params[1]),int(params[2]),int(params[3]),int(params[4]))
        button2["command"]= lambda: button_clk(int(params[5]),int(params[6]),int(params[7]),int(params[8]))
        count=count+1
        return
    # 再帰呼び出し
    decode_line(None)
# はい、いいえ関数
def button_clk(hennkap,henkam,henkah,henkamotibe):
    global popularity, money, health, motibe 
    popularity=popularity+hennkap
    money=money+henkam
    health=health+henkah
    motibe=motibe+henkamotibe
    message.bind("<Button-1>",decode_line)
# ジャンプ関数
def jump_to_line(branchID):
    global current_line
    # ボタンを消す
    for btn in branch:
        btn.place_forget()
        btn.destroy()
    branch.clear()
    label = jumplabel[branchID]
    jumplabel.clear()
    message.bind("<Button-1>", decode_line)
    # ジャンプ先を探す
    for l in range(len(scenario)):
        if scenario[l].strip() == "## " + label:
            current_line = l
            decode_line(None)
            return

# ウィンドウ作成
root = tkinter.Tk()
root.title("IIR quest 1")
root.minsize(900, 460)
root.option_add("*font", ["メイリオ", 14])
# キャンバス作成
canvas = tkinter.Canvas(width=900, height=460)
canvas.place(x=0, y=0)
# メッセージエリア
message = tkinter.Label(width=70, height=5, wraplength=840,
    bg="white", justify="left", anchor="nw")
message.place(x=28, y=284)
message["text"] = "クリックしてスタート ⁂このゲームはフィクションですが、登場人物はバリバリ実在の人物に関係ありますw"

# ファイル読み込み
scenario = []
file = open("img8/IIRgame.txt", "r", encoding="utf-8")
while True:
    line = file.readline()
    scenario.append(line)
    if not line:
        file.close()
        break

# 現在の行数
current_line = 0
# イベント設定
message.bind("<Button-1>", decode_line)
# 画像
bgimg = None
lcharimg = None
ccharimg = None
rcharimg = None
#数値
popularity=400
money=150
health=300
motibe=500
window=0
count=0
# 選択肢
branch = []
jumplabel = []

root.mainloop()