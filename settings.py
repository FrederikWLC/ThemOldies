from os import getenv
from dotenv import load_dotenv

from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Accessing variables.
stripe_public_key = getenv("STRIPE_PUBLIC_KEY")
stripe_secret_key = getenv("STRIPE_SECRET_KEY")
stripe_plan_id = getenv("STRIPE_PLAN_ID")
