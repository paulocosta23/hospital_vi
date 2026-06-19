from supabase import create_client

from config.settings import SUPABASE_KEY, SUPABASE_URL

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)