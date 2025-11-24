import os
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_S3_REGION', 'ap-southeast-2')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

    def upload_file(self, file_obj, folder_name, file_name=None):
        """
        Upload a file to S3 bucket
        
        Args:
            file_obj: File object from request.files
            folder_name: Folder path in S3 (e.g., 'uploads/songs')
            file_name: Optional custom file name. If not provided, uses original filename
        
        Returns:
            dict: {
                'success': bool,
                'url': str (S3 URL if successful),
                'error': str (error message if failed)
            }
        """
        try:
            # Use provided filename or get from file object
            if file_name is None:
                file_name = secure_filename(file_obj.filename)
            else:
                file_name = secure_filename(file_name)
            
            # Create full S3 key path
            s3_key = f"{folder_name}/{file_name}"
            
            # Upload file to S3
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': file_obj.content_type or 'application/octet-stream'
                }
            )
            
            # Generate S3 URL
            url = f"https://{self.bucket_name}.s3.{os.getenv('AWS_S3_REGION', 'ap-southeast-2')}.amazonaws.com/{s3_key}"
            
            return {
                'success': True,
                'url': url,
                'key': s3_key
            }
        
        except ClientError as e:
            return {
                'success': False,
                'error': f"AWS S3 Error: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Upload failed: {str(e)}"
            }

    def delete_file(self, s3_key):
        """
        Delete a file from S3 bucket
        
        Args:
            s3_key: Full path to file in S3
        
        Returns:
            dict: {'success': bool, 'error': str}
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return {'success': True}
        except ClientError as e:
            return {
                'success': False,
                'error': f"AWS S3 Error: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Delete failed: {str(e)}"
            }

    def get_file_url(self, s3_key):
        """
        Generate a public URL for a file in S3
        
        Args:
            s3_key: Full path to file in S3
        
        Returns:
            str: Public URL
        """
        return f"https://{self.bucket_name}.s3.{os.getenv('AWS_S3_REGION', 'ap-southeast-2')}.amazonaws.com/{s3_key}"

# Singleton instance
s3_service = S3Service()
