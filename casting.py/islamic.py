from flask import Flask, render_template, request
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
app = Flask(__name__)
surahs = [
    "Al-Fatihah",
    "Al-Baqarah",
    "Aal-e-Imran",
    "An-Nisa",
    "Al-Ma'idah",
    "Al-An'am",
    "Al-A'raf",
    "Al-Anfal",
    "At-Tawbah",
    "Yunus",
    "Hud",
    "Yusuf",
    "Ar-Ra'd",
    "Ibrahim",
    "Al-Hijr",
    "An-Nahl",
    "Al-Isra",
    "Al-Kahf",
    "Maryam",
    "Ta-Ha",
    "Al-Anbiya",
    "Al-Hajj",
    "Al-Mu'minun",
    "An-Nur",
    "Al-Furqan",
    "Ash-Shu'ara",
    "An-Naml",
    "Al-Qasas",
    "Al-Ankabut",
    "Ar-Rum",
    "Luqman",
    "As-Sajdah",
    "Al-Ahzab",
    "Saba",
    "Fatir",
    "Ya-Sin",
    "As-Saffat",
    "Sad",
    "Az-Zumar",
    "Ghafir",
    "Fussilat",
    "Ash-Shura",
    "Az-Zukhruf",
    "Ad-Dukhan",
    "Al-Jathiyah",
    "Al-Ahqaf",
    "Muhammad",
    "Al-Fath",
    "Al-Hujurat",
    "Qaf",
    "Adh-Dhariyat",
    "At-Tur",
    "An-Najm",
    "Al-Qamar",
    "Ar-Rahman",
    "Al-Waqi'ah",
    "Al-Hadid",
    "Al-Mujadilah",
    "Al-Hashr",
    "Al-Mumtahanah",
    "As-Saff",
    "Al-Jumu'ah",
    "Al-Munafiqun",
    "At-Taghabun",
    "At-Talaq",
    "At-Tahrim",
    "Al-Mulk",
    "Al-Qalam",
    "Al-Haqqah",
    "Al-Ma'arij",
    "Nuh",
    "Al-Jinn",
    "Al-Muzzammil",
    "Al-Muddaththir",
    "Al-Qiyamah",
    "Al-Insan",
    "Al-Mursalat",
    "An-Naba",
    "An-Nazi'at",
    "Abasa",
    "At-Takwir",
    "Al-Infitar",
    "Al-Mutaffifin",
    "Al-Inshiqaq",
    "Al-Buruj",
    "At-Tariq",
    "Al-A'la",
    "Al-Ghashiyah",
    "Al-Fajr",
    "Al-Balad",
    "Ash-Shams",
    "Al-Layl",
    "Ad-Duha",
    "Ash-Sharh",
    "At-Tin",
    "Al-Alaq",
    "Al-Qadr",
    "Al-Bayyinah",
    "Az-Zalzalah",
    "Al-Adiyat",
    "Al-Qari'ah",
    "At-Takathur",
    "Al-Asr",
    "Al-Humazah",
    "Al-Fil",
    "Quraysh",
    "Al-Ma'un",
    "Al-Kawthar",
    "Al-Kafirun",
    "An-Nasr",
    "Al-Masad",
    "Al-Ikhlas",
    "Al-Falaq",
    "An-Nas"
]
surah_numbers = {}

for i, surah in enumerate(surahs, start=1):
    surah_numbers[surah] = i

quran = {
    "Al-Fatihah": {
        "arabic": [
            "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
            "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
            "الرَّحْمَٰنِ الرَّحِيمِ",
            "مَالِكِ يَوْمِ الدِّينِ",
            "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
            "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
            "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"
        ]
    }
}

@app.route("/")
def home():
   
    return render_template("index.html")


@app.route("/quran")
def quran_page():
   
    return render_template("quran.html", surahs=surahs)

@app.route("/surah/<name>")
def surah(name):

    number = surah_numbers[name]

    response = requests.get(f"https://api.alquran.cloud/v1/surah/{number}")
    urdu_response = requests.get(f"https://api.alquran.cloud/v1/surah/{number}/ur.jalandhry")
    english_response = requests.get(f"https://api.alquran.cloud/v1/surah/{number}/en.asad")
    word_response = requests.get(
    f"https://api.quran.com/api/v4/verses/by_key/{number}:1?words=true&translations=131"
    )

    word_data = word_response.json()
    
    data = response.json()
    urdu_data = urdu_response.json()
    english_data = english_response.json()

    ayat = data["data"]["ayahs"]
    urdu_ayat = urdu_data["data"]["ayahs"]
    english_ayat = english_data["data"]["ayahs"]

    audio_response = requests.get(
        f"https://api.quran.com/api/v4/chapter_recitations/7/{number}"
    )

    word_response = requests.get(
        f"https://api.quran.com/api/v4/verses/by_chapter/{number}?words=true&translations=131"
    )

    word_data = word_response.json()

    print(word_data)

    word_verses = word_data["verses"]

    audio_data = audio_response.json()

    audio_url = audio_data["audio_file"]["audio_url"]
    print(audio_url)

    return render_template(
        "surah.html",
        name=name,
        ayat=ayat,
        urdu_ayat=urdu_ayat,
        english_ayat=english_ayat,
        audio_url=audio_url,
        word_verses=word_verses
    )
    word_verses=word_verses
    
   
                
@app.route("/test")
def test():
    response = requests.get("https://api.alquran.cloud/v1/surah/1")

    data = response.json()

    return data["data"]["ayahs"][1]["text"]

@app.route("/hadith")
def hadith():

    with open("data/bukhari.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    hadiths = data["hadiths"]

    return render_template(
        "hadith.html",
        hadiths=hadiths
    )
    
@app.route("/duas")
def duas():

    with open("data/duas.json", "r", encoding="utf-8") as file:
        duas = json.load(file)

    return render_template(
        "duas.html",
        duas=duas
    )
@app.route("/salah")
def salah():

    with open("data/salah.json", "r", encoding="utf-8") as file:
        salah = json.load(file)

    return render_template(
        "salah.html",
        salah=salah
    )
@app.route("/quiz")
def quiz():

    with open("data/quiz.json", "r", encoding="utf-8") as file:
        quiz = json.load(file)

    print(len(quiz))

    random_quiz = random.sample(quiz, min(10, len(quiz)))

    return render_template(
        "quiz.html",
        quiz=random_quiz
        
    )

@app.route("/prayer-times")
def prayer_times():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:
        city = "Current Location"
        url = f"https://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
    else:
        city = "Muscat, Oman"
        url = "https://api.aladhan.com/v1/timingsByCity?city=Muscat&country=Oman&method=2"

    response = requests.get(url)

    data = response.json()

    timings = data["data"]["timings"]

    return render_template(
        "prayer_times.html",
        timings=timings,
        date=data["data"]["date"]["readable"],
        city=city
    )
@app.route("/allah-names")
def allah_names():

    with open("data/allah_name.json", "r", encoding="utf-8") as file:
        names = json.load(file)

    return render_template(
        "allha_name.html",
        names=names
    )
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        sender = "nooracademyspport@gmail.com"
        password = "elgz uoad vxfj hepa"

        receiver = "nooracademyspport@gmail.com"

        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = "New Feedback - Noor Academy"

        body = f"""
Name: {name}
Email: {email}

Message:
{message}
"""

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()

        return "JazakAllah! Your feedback has been sent."

    return render_template("contact.html")
if __name__ == "__main__":
    app.run(debug=True)
