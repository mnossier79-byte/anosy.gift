import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ====== عدّل هنا ======
HER_NAME = "Anosy"
TITLE = "كل سنة وانتي طيبة 🎂"
INTRO = "25 / 11 — النهارده يومك انتي"
# الكلام اللي تحت كل صورة بالترتيب (1.jpg, 2.jpg, ...)
CAPTIONS = [
    "ضحكتنا وإحنا مش واخدين بالنا من الدنيا 😄",
    "الفيونكات دي كانت ليكي إنتي بس 🎀",
    "إنتي أكتر حد بتطلع معاه أحلى الصور 😂",
    "ولا مرة ضحكت زي ما بضحك معاكي 🔥",
    "ذكريات صغيرة بس غالية عندي 🤍",
]
FINAL_MESSAGE = "ربنا يخليكي ليا ويفرحك دايمًا. كل سنة وانتي أقرب حد لقلبي ❤️"
SONG = "song.mp3"  # حطه في static/
# ======================

PHOTOS_DIR = os.path.join(app.static_folder, "photos")


def get_photos():
    if not os.path.isdir(PHOTOS_DIR):
        return []
    files = [f for f in os.listdir(PHOTOS_DIR)
             if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif"))]
    return sorted(files)


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
  body{font-family:'Cairo',sans-serif;background:linear-gradient(160deg,#ffe3ec,#e8d9ff);
       color:#4a2a3b;min-height:100vh;overflow-x:hidden}
  #overlay{position:fixed;inset:0;background:linear-gradient(160deg,#ff9ac1,#b69cff);
       display:flex;flex-direction:column;align-items:center;justify-content:center;
       z-index:100;color:#fff;text-align:center;padding:20px;transition:opacity .8s}
  #overlay h1{font-size:2rem;margin-bottom:10px}
  #overlay button{margin-top:24px;font-family:inherit;font-size:1.2rem;font-weight:700;
       padding:14px 34px;border:none;border-radius:40px;background:#fff;color:#d6457f;
       cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.2)}
  header{text-align:center;padding:50px 20px 20px}
  header h1{font-size:2.2rem;font-weight:900;color:#d6457f}
  header p{margin-top:8px;font-size:1.1rem}
  .card{max-width:480px;margin:30px auto;background:#fff;border-radius:22px;
       overflow:hidden;box-shadow:0 10px 30px rgba(150,80,130,.18);
       opacity:0;transform:translateY(30px);transition:all .8s}
  .card.show{opacity:1;transform:none}
  .card img{width:100%;display:block}
  .card p{padding:18px 20px;font-size:1.1rem;line-height:1.9;text-align:center}
  .final{max-width:480px;margin:30px auto 80px;text-align:center;font-size:1.3rem;
       font-weight:700;color:#d6457f;padding:0 20px;line-height:2}
  .heart{position:fixed;bottom:-30px;font-size:22px;animation:float 8s linear infinite;
       pointer-events:none;z-index:1}
  @keyframes float{to{transform:translateY(-110vh);opacity:0}}
</style>
</head>
<body>
<div id="overlay">
  <h1>🎁 هدية لـ {{ name }}</h1>
  <p>افتحيها بصوت مسموع 🎧</p>
  <button onclick="openGift()">افتحي الهدية</button>
</div>

{% if has_song %}<audio id="song" src="{{ url_for('static', filename=song) }}" loop></audio>{% endif %}

<header>
  <h1>{{ title }}</h1>
  <p>{{ intro }}</p>
</header>

{% for photo in photos %}
<div class="card">
  <img src="{{ url_for('static', filename='photos/' + photo) }}" alt="">
  <p>{{ captions[loop.index0] if loop.index0 < captions|length else '' }}</p>
</div>
{% endfor %}

<div class="final">{{ final }}</div>

<script>
  function openGift(){
    const s=document.getElementById('song'); if(s) s.play().catch(()=>{});
    const o=document.getElementById('overlay');
    o.style.opacity=0; setTimeout(()=>o.remove(),800);
  }
  const io=new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting)e.target.classList.add('show')}),{threshold:.2});
  document.querySelectorAll('.card').forEach(c=>io.observe(c));
  setInterval(()=>{
    const h=document.createElement('div');
    h.className='heart';h.textContent=['💖','💗','🎈','✨'][Math.floor(Math.random()*4)];
    h.style.left=Math.random()*100+'vw';
    h.style.animationDuration=(6+Math.random()*5)+'s';
    document.body.appendChild(h);
    setTimeout(()=>h.remove(),11000);
  },700);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        PAGE, name=HER_NAME, title=TITLE, intro=INTRO,
        captions=CAPTIONS, final=FINAL_MESSAGE,
        photos=get_photos(), song=SONG,
        has_song=os.path.exists(os.path.join(app.static_folder, SONG)),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
