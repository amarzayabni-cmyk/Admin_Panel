-- Supabase SQL setup for a simple registration and admin app
-- This file creates the required tables and enables RLS.

BEGIN;

CREATE TABLE IF NOT EXISTS public.content_drafts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'draft',
    excerpt TEXT,
    content TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    service_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'admin',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE public.content_drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "content_drafts_select_for_anon"
ON public.content_drafts
FOR SELECT
TO anon
USING (true);

CREATE POLICY "content_drafts_all_for_authenticated"
ON public.content_drafts
FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

CREATE POLICY "bookings_insert_for_anon"
ON public.bookings
FOR INSERT
TO anon
WITH CHECK (true);

CREATE POLICY "bookings_all_for_authenticated"
ON public.bookings
FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

CREATE POLICY "users_all_for_authenticated"
ON public.users
FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

COMMIT;
