require 'aws-sdk-s3'
require 'json'

def handler(event:, context:)
    puts event
    s3 = Aws::S3::Resource.new
    bucket_name = ENV['UPLOADS_BUCKET_NAME']
    object_key = 'mock.jpg'

    obj = s3.bucket(bucket_name).object(object_key)
    url = obj.presigned_url(:put, expires_in: 300)
    url
    body = {url: url}.to_json
    {
        headers: {
            "Access-Control-Allow-Headers": "*, Authorization",
            "Acess-Control-Allow-Origin": "https://3000-vishnukumar-awsbootcamp-qcmbkxmlq35.ws-us95.gitpod.io",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
        },
        statusCode: 200, 
        body: body
        
    }
end