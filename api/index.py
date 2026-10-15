import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from supabase import create_client, Client

app = FastAPI()

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
DEFAULT_MAPEL = [
    "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "IPA", "IPS",
    "Pendidikan Pancasila", "PJOK", "Informatika", "Seni Budaya",
    "Agama", "Prakarya", "Bahasa Daerah", "Projek"
]

def client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise HTTPException(status_code=500, detail="Konfigurasi Supabase belum lengkap di Vercel.")
    return create_client(url, key)

def default_data():
    schedule = {}
    for idx, day in enumerate(HARI):
        schedule[day] = [DEFAULT_MAPEL[(idx * 3 + j) % len(DEFAULT_MAPEL)] for j in range(12)]
    return {"subjects": DEFAULT_MAPEL[:], "schedule": schedule}

def get_or_create():
    sb = client()
    result = sb.table("class_schedule").select("*").eq("id", 1).limit(1).execute()
    if result.data:
        return {"subjects": result.data[0]["subjects"], "schedule": result.data[0]["schedule"]}
    d = default_data()
    sb.table("class_schedule").insert({"id": 1, **d}).execute()
    return d

@app.get("/")
@app.get("/api")
@app.get("/schedule")
@app.get("/api/index.py")
@app.get("/api/schedule")
def get_schedule():
    try:
        return get_or_create()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membaca database: {str(e)}")

def check_admin(password: str | None):
    expected = os.getenv("ADMIN_PASSWORD")
    if not expected:
        raise HTTPException(status_code=500, detail="ADMIN_PASSWORD belum diatur di Vercel.")
    if password != expected:
        raise HTTPException(status_code=401, detail="Kata sandi admin salah.")

@app.put("/")
@app.put("/api")
@app.put("/schedule")
@app.put("/api/index.py")
@app.put("/api/schedule")
def save_schedule(payload: dict, x_admin_password: str | None = Header(default=None)):
    check_admin(x_admin_password)
    subjects = payload.get("subjects")
    schedule = payload.get("schedule")
    if not isinstance(subjects, list) or len(subjects) != 13:
        raise HTTPException(status_code=400, detail="Harus ada tepat 13 mata pelajaran.")
    subjects = [str(s).strip()[:100] or f"Mata Pelajaran {i+1}" for i, s in enumerate(subjects)]
    if len(set(subjects)) != 13:
        raise HTTPException(status_code=400, detail="Nama mata pelajaran harus unik.")
    if not isinstance(schedule, dict):
        raise HTTPException(status_code=400, detail="Format jadwal tidak valid.")
    clean_schedule = {}
    for day in HARI:
        values = schedule.get(day)
        if not isinstance(values, list) or len(values) != 12:
            raise HTTPException(status_code=400, detail=f"{day} harus memiliki 12 jam pelajaran.")
        clean_schedule[day] = [v if v in subjects else subjects[0] for v in values]
    try:
        sb = client()
        sb.table("class_schedule").upsert({
            "id": 1, "subjects": subjects, "schedule": clean_schedule,
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        return {"ok": True, "message": "Jadwal berhasil disimpan ke database cloud."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan database: {str(e)}")
