# Jadwal Kelas Digital — Vercel + Supabase

Proyek ini mengadaptasi notebook Google Colab Anda (Python + Gradio + Google Drive) menjadi website untuk Vercel dengan database Supabase.

Fitur:
- Jadwal hari ini otomatis (Senin–Jumat).
- 5 hari × 12 jam pelajaran.
- 13 mata pelajaran yang dapat diubah.
- Edit jadwal dan simpan ke database cloud.
- Desain biru futuristik dan responsif.

## 1. Buat database Supabase
1. Buat proyek di https://supabase.com/
2. Buka **SQL Editor** → **New query**.
3. Salin isi file `supabase_setup.sql`, jalankan dengan **Run**.
4. Buka **Project Settings → API** dan salin:
   - Project URL
   - `service_role` key (jaga rahasia; jangan pernah masukkan ke file frontend/GitHub)

## 2. Unggah proyek ke GitHub
1. Ekstrak ZIP ini.
2. Buat repositori baru di https://github.com/
3. Unggah semua file dan folder proyek ke repositori tersebut.

## 3. Deploy ke Vercel
1. Buka https://vercel.com/ dan pilih **Add New → Project**.
2. Impor repositori GitHub Anda.
3. Di bagian **Environment Variables**, tambahkan:
   - `SUPABASE_URL` = Project URL Supabase
   - `SUPABASE_SERVICE_ROLE_KEY` = service_role key Supabase
   - `ADMIN_PASSWORD` = kata sandi admin yang kuat untuk menyimpan perubahan
4. Deploy.
5. Buka URL website yang diberikan Vercel.

## 4. Cara menggunakan
- Tab **Jadwal Hari Ini** menampilkan jadwal sesuai hari saat ini.
- Tab **Atur Jadwal**: pilih hari, ubah 12 pilihan, tekan **Simpan Jadwal**. Masukkan kata sandi admin.
- Tab **Mata Pelajaran**: ubah 13 nama, tekan **Simpan Mata Pelajaran**. Masukkan kata sandi admin.
- Data dibaca dari Supabase sehingga jadwal yang disimpan bisa dilihat dari perangkat lain.

## Catatan penting
- Kata sandi admin dikirim hanya saat melakukan penyimpanan, dan diverifikasi di backend.
- Jangan menaruh `SUPABASE_SERVICE_ROLE_KEY` pada file `public/` atau kode JavaScript browser.
- Untuk aplikasi sekolah yang lebih besar, sebaiknya tambahkan akun admin per pengguna dan kebijakan akses yang lebih terperinci.
- Ini adalah proyek awal hasil adaptasi fitur notebook; UI dibuat ulang sebagai website, bukan menjalankan Gradio di Vercel.
