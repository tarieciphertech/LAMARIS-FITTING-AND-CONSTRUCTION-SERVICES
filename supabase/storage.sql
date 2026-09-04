-- Run this once in the Supabase SQL Editor.
-- The FastAPI backend uses the service-role key for uploads/deletes.
-- Keep SUPABASE_SERVICE_ROLE_KEY on Render only; never expose it to React.

insert into storage.buckets (id, name, public)
values ('property-images', 'property-images', true)
on conflict (id) do update set public = excluded.public;

-- Public property photos are intentionally readable without authentication.
-- Writes remain server-side through the FastAPI service-role key.
