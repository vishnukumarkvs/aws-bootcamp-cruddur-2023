-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Andrew Brown','anndrew@exampro.co', 'andrewbrown' ,'MOCK'),
  ('Bayko', 'bayko@exampro.co','bayko' ,'MOCK'),
  ('Vishnu Kvs', 'kvs.vishnu23@gmail.com','Kavali Vignesh Sai' ,'MOCK'),
  ('Vishnu Kumar', 'kvsvishnukumar@gmail.com','vvvv' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )