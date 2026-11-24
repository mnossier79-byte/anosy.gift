import os
from flask import Flask, render_template_string

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE, static_url_path="/files")

# ====== عدّل هنا ======
HER_NAME = "Anosy"
TITLE = "كل سنة وانتي طيبة 🎂"
INTRO = "25 / 11 — النهارده يومك انتي"

# الكلام تحت كل صورة بالترتيب (1.jpg, 2.jpg, ...)
CAPTIONS = [
    "ضحكتنا وإحنا مش واخدين بالنا من الدنيا 😄",
    "الفيونكات دي كانت ليكي إنتي بس 🎀",
    "إنتي أكتر حد بتطلع معاه أحلى الصور 😂",
    "ولا مرة ضحكت زي ما بضحك معاكي 🔥",
    "ذكريات صغيرة بس غالية عندي 🤍",
    "ا ويلي على المززززززز 😍😍😍😍😍😍",
    "والله قمر اويييي 😍😍😍😍😍",
    "اعرعرعرعرعررعر😂😂😂",
    "يا خلاثييييي ، ورده ماسكه ورده والله 😍😍😍😍😍😘😘",
    "تتحط في متحف دي والله 😍😍😍😍😍😘",
    "أكاد من فرط الجمال اذوب 😍😍😍😍😍😍😍😍😍😍😘😘😘",
    "بغض النظر عن أنها ai بس انا بعشق الصوره دي اوييييي 😍😍😍",
    "اول مره اشوف قمر في توكتوك 😘😘😘😘😘😘😘😘",
    "I love this outfit 😍🤩😍😍😍",
]

# الرسالة جوه الإطار (كل عنصر فقرة)
MESSAGE_TITLE = "💌 رسالة ليكي يا بطه"
MESSAGE = [
    "كل سنه وانتي اجمل و احن و احلى واحده في الوجود",
    "كل سنه وانتي دايما اللي منوره حياتي و مخليه ليها شكل و معنى ، مكنتش متخيل اني اقول الكلام دا لحد بس انتي مش اي حد يا بطه ، انا ممتن للظروف اللي جمعتنا سوا يا اني ، ممتن جدا",
    "و عايزك معايا طول العمر لحد م اموت، و نتجوز و نجيب كتاكيت كدا شبهك و نعيش حياه سعيده مسالمه بعيدا عن البشر ، نعيش الباقي من عمرنا نحب بعض، عايز ابوسك دايما، مش عارف ليه",
    "بحبك اوي اوي اوي اوي اوي يا اني و بتمنى انك تكوني من نصيبي ل اخر العمر",
    "Love you awyyyyy يا بطه ، و يارب تكون سنه سعيده عليكي و تحققي كل اللي نفسك فيه ، بعشقك 😍🤩😘😘😘😘😘",
]
# ======================


def get_song():
    for f in sorted(os.listdir(BASE)):
        if f.lower().endswith((".mp3", ".m4a", ".ogg", ".wav")):
            return f
    return None


def get_photos():
    files = [f for f in os.listdir(BASE)
             if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif"))]

    def key(f):
        stem = os.path.splitext(f)[0]
        return (0, int(stem)) if stem.isdigit() else (1, f)
    return sorted(files, key=key)


PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Cairo',sans-serif;color:#5a2347;min-height:100vh;overflow-x:hidden;
       background:
         radial-gradient(circle at 15% 10%, rgba(255,255,255,.7), transparent 40%),
         radial-gradient(circle at 85% 30%, rgba(255,214,236,.8), transparent 45%),
         radial-gradient(circle at 20% 80%, rgba(220,200,255,.8), transparent 45%),
         linear-gradient(160deg,#ffc2dd,#ffd9ec 40%,#e3ccff);
       background-attachment:fixed}
  #overlay{position:fixed;inset:0;background:linear-gradient(160deg,#ff7fb2,#a98bff);
       display:flex;flex-direction:column;align-items:center;justify-content:center;
       z-index:100;color:#fff;text-align:center;padding:20px;transition:opacity .8s}
  #overlay h1{font-size:2rem;margin-bottom:10px}
  #overlay .big{font-size:3rem;margin-bottom:10px}
  #overlay button{margin-top:24px;font-family:inherit;font-size:1.2rem;font-weight:700;
       padding:14px 34px;border:none;border-radius:40px;background:#fff;color:#d6457f;
       cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.2)}
  header,.card,.frame{position:relative;z-index:2}
  header{text-align:center;padding:50px 20px 20px}
  header h1{font-size:2.2rem;font-weight:900;color:#d6336c;text-shadow:0 2px 0 #fff}
  header p{margin-top:8px;font-size:1.1rem}
  .card{max-width:480px;margin:30px auto;background:#fff;border-radius:22px;
       overflow:hidden;box-shadow:0 10px 30px rgba(214,51,108,.22);
       border:3px solid #ffd0e4;opacity:0;transform:translateY(30px);transition:all .8s}
  .card.show,.frame.show{opacity:1;transform:none}
  .card img{width:100%;display:block}
  .card p{padding:18px 20px;font-size:1.1rem;line-height:1.9;text-align:center}
  .frame{max-width:520px;margin:50px auto 100px;padding:10px;border-radius:30px;
       background:linear-gradient(135deg,#ff7fb2,#c9a6ff,#ff7fb2);
       box-shadow:0 14px 40px rgba(214,51,108,.35);
       opacity:0;transform:translateY(30px);transition:all .9s;width:calc(100% - 32px)}
  .frame-inner{background:linear-gradient(#fffafd,#fff0f7);border-radius:22px;
       border:3px dashed #ff9cc4;padding:34px 22px 28px;text-align:center;position:relative}
  .frame-inner::before,.frame-inner::after{position:absolute;font-size:30px}
  .frame-inner::before{content:'🦋';top:-18px;right:14px}
  .frame-inner::after{content:'🌸';bottom:-18px;left:14px}
  .frame h2{font-size:1.6rem;font-weight:900;color:#d6336c;margin-bottom:18px}
  .frame p{font-size:1.1rem;line-height:2.1;margin-bottom:16px;color:#5a2347}
  .frame p:last-child{margin-bottom:0;font-weight:700;color:#c2255c}
  .heart{position:fixed;bottom:-40px;pointer-events:none;z-index:1;
       animation:rise linear forwards}
  @keyframes rise{to{transform:translateY(-115vh)}}
  .bfly{position:fixed;bottom:-50px;pointer-events:none;z-index:3;
       animation:rise linear forwards}
  .bfly span{display:inline-block;animation:sway 2.6s ease-in-out infinite alternate}
  @keyframes sway{from{transform:translateX(-35px) rotate(-18deg)}
                  to{transform:translateX(35px) rotate(18deg)}}
</style>
</head>
<body>
<div id="overlay">
  <div class="big">🦋💖🦋</div>
  <h1>🎁 هدية لـ {{ name }}</h1>
  <p>افتحيها بصوت مسموع 🎧</p>
  <button onclick="openGift()">افتحي الهدية</button>
</div>

{% if song %}<audio id="song" src="{{ url_for('static', filename=song) }}" loop></audio>{% endif %}

<header>
  <h1>{{ title }}</h1>
  <p>{{ intro }}</p>
</header>

{% for photo in photos %}
<div class="card">
  <img src="{{ url_for('static', filename=photo) }}" alt="">
  <p>{{ captions[loop.index0] if loop.index0 < captions|length else '' }}</p>
</div>
{% endfor %}

<div class="frame">
  <div class="frame-inner">
    <h2>{{ msg_title }}</h2>
    {% for para in message %}<p>{{ para }}</p>{% endfor %}
  </div>
</div>

<script>
  function openGift(){
    const s=document.getElementById('song'); if(s) s.play().catch(()=>{});
    const o=document.getElementById('overlay');
    o.style.opacity=0; setTimeout(()=>o.remove(),800);
  }
  const io=new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting)e.target.classList.add('show')}),{threshold:.15});
  document.querySelectorAll('.card,.frame').forEach(c=>io.observe(c));

  const hearts=['💖','💗','💕','💘','🌸','✨'];
  setInterval(()=>{
    const h=document.createElement('div');
    h.className='heart';
    h.textContent=hearts[Math.floor(Math.random()*hearts.length)];
    h.style.left=Math.random()*100+'vw';
    h.style.fontSize=(16+Math.random()*20)+'px';
    h.style.animationDuration=(7+Math.random()*6)+'s';
    document.body.appendChild(h);
    setTimeout(()=>h.remove(),14000);
  },500);

  const bf=['🦋','🦋','🦋'];
  setInterval(()=>{
    const b=document.createElement('div');
    b.className='bfly';
    b.style.left=(5+Math.random()*85)+'vw';
    b.style.fontSize=(24+Math.random()*16)+'px';
    b.style.animationDuration=(9+Math.random()*6)+'s';
    b.innerHTML='<span>'+bf[Math.floor(Math.random()*bf.length)]+'</span>';
    document.body.appendChild(b);
    setTimeout(()=>b.remove(),16000);
  },1800);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        PAGE, name=HER_NAME, title=TITLE, intro=INTRO,
        captions=CAPTIONS, msg_title=MESSAGE_TITLE, message=MESSAGE,
        photos=get_photos(), song=get_song(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
