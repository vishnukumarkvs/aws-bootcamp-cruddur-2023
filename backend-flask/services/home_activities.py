from datetime import datetime, timedelta, timezone
from opentelemetry import trace
import json
from flask import jsonify

from lib.db import pool
from lib.db import query_wrap_array

tracer = trace.get_tracer("home.activities")


class HomeActivities:
  def run(logger):
    logger.info("HomeActivities")
    with tracer.start_as_current_span("home-activities-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now",now.isoformat())
      
      sql = query_wrap_array("""
      SELECT * FROM activities
      """)
      with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            json = cur.fetchone()
            
    # Return JSON response with 200 status code
    return json[0]
      
