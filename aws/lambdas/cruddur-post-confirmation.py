import json
import os
import psycopg2

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('User Metadata')
    print(user)
    user_display_name = user['name']
    user_email = user['email']
    user_handle = user['preferred_username']
    user_cognito_id = user['sub']
    conn = None
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()

        sql = """
        INSERT INTO users(
            display_name,
            email,
            handle,
            cognito_user_id
        )
        VALUES(%s, %s, %s, %s)
        """
        values = (user_display_name, user_email, user_handle, user_cognito_id)
        cur.execute(sql, values)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database Connection closed')
    
    return event
