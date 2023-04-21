CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;

CREATE TABLE IF NOT EXISTS public.schema_information (
    last_successful_run text
);

CREATE TABLE public.users(
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    display_name text,
    email text NOT NULL,
    handle text NOT NULL,
    cognito_user_id text NOT NULL,
    created_at TIMESTAMP default current_timestamp NOT NULL
);

CREATE TABLE public.activities(
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_uuid UUID NOT NULL,
    message text NOT NULL,
    replies_count INTEGER DEFAULT 0,
    reposts_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    reply_to_activity_uuid INTEGER,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT current_timestamp NOT NULL
);