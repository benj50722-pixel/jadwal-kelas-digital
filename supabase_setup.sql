create table if not exists public.class_schedule (
  id integer primary key check (id = 1),
  subjects jsonb not null,
  schedule jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.class_schedule enable row level security;

-- Browser tidak mendapat akses langsung ke tabel. Backend Vercel menggunakan service role.
-- Buat satu baris awal; API akan membaca baris ini.
insert into public.class_schedule (id, subjects, schedule)
values (
  1,
  '["Matematika","Bahasa Indonesia","Bahasa Inggris","IPA","IPS","Pendidikan Pancasila","PJOK","Informatika","Seni Budaya","Agama","Prakarya","Bahasa Daerah","Projek"]'::jsonb,
  '{
    "Senin":["Matematika","Bahasa Indonesia","Bahasa Inggris","IPA","IPS","Pendidikan Pancasila","PJOK","Informatika","Seni Budaya","Agama","Prakarya","Bahasa Daerah"],
    "Selasa":["Pendidikan Pancasila","PJOK","Informatika","Seni Budaya","Agama","Prakarya","Bahasa Daerah","Projek","Matematika","Bahasa Indonesia","Bahasa Inggris","IPA"],
    "Rabu":["Agama","Prakarya","Bahasa Daerah","Projek","Matematika","Bahasa Indonesia","Bahasa Inggris","IPA","IPS","Pendidikan Pancasila","PJOK","Informatika"],
    "Kamis":["Bahasa Inggris","IPA","IPS","Pendidikan Pancasila","PJOK","Informatika","Seni Budaya","Agama","Prakarya","Bahasa Daerah","Projek","Matematika"],
    "Jumat":["Seni Budaya","Agama","Prakarya","Bahasa Daerah","Projek","Matematika","Bahasa Indonesia","Bahasa Inggris","IPA","IPS","Pendidikan Pancasila","PJOK"]
  }'::jsonb
)
on conflict (id) do nothing;
