import os
import pymysql
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

# Import routes
from app.auth import auth_bp
from app.users import users_bp
from app.subscriptions import subscriptions_bp
from services.s3_service import s3_service

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'mp3', 'wav', 'flac'}

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'dev-secret-change-me')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session expires after 7 days
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Store database config for direct PyMySQL connections
    app.config['DB_CONFIG'] = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'ssl_disabled': False,  # Aiven requires SSL
        'charset': 'utf8mb4'
    }
    
    # Enable CORS for frontend
    CORS(app, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(subscriptions_bp)

    
    # Health check endpoint with database connection test
    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            connection = pymysql.connect(**app.config['DB_CONFIG'])
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            connection.close()
            
            return jsonify({
                'status': 'healthy',
                'service': 'music-platform-api',
                'database': 'connected',
                'aiven_mysql': 'accessible'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'service': 'music-platform-api',
                'database': 'disconnected',
                'error': str(e)
            }), 500
    
    # S3 Health check endpoint
    @app.route('/health/s3')
    def s3_health_check():
        try:
            # Test S3 connection by listing bucket contents (limited to 1 object)
            response = s3_service.s3_client.list_objects_v2(
                Bucket=s3_service.bucket_name,
                MaxKeys=1
            )
            
            return jsonify({
                'status': 'connected',
                'service': 'AWS S3',
                'bucket': s3_service.bucket_name,
                'region': os.getenv('AWS_S3_REGION', 'ap-southeast-2')
            })
        except Exception as e:
            return jsonify({
                'status': 'disconnected',
                'service': 'AWS S3',
                'error': str(e),
                'bucket': s3_service.bucket_name
            }), 500
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Music Platform API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'music': '/api/music',
                'upload': '/api/upload',
                'health': '/health'
            }
        })
    
    # S3 Upload endpoint - Example for uploading media files
    @app.route('/api/upload', methods=['POST'])
    def upload_file():
        """
        Upload a file to AWS S3
        
        Expected request:
        - file: File object (form-data)
        - folder: Target folder in S3 (e.g., 'uploads/songs')
        - filename: (Optional) Custom filename
        
        Returns:
            - success: True/False
            - url: S3 URL of uploaded file
            - error: Error message if failed
        """
        try:
            # Check if file is present
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Get folder path (default to 'uploads')
            folder = request.form.get('folder', 'uploads')
            custom_filename = request.form.get('filename')
            
            # Upload to S3
            result = s3_service.upload_file(file, folder, custom_filename)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'url': result['url'],
                    'key': result['key']
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': result['error']
                }), 500
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f"Upload error: {str(e)}"
            }), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    # Test database connection on startup
    print("🔗 Testing Aiven MySQL connection...")
    try:
        connection = pymysql.connect(**app.config['DB_CONFIG'])
        print("✅ Successfully connected to Aiven MySQL!")
        connection.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your .env file and Aiven credentials")
    
    print("🚀 Starting Flask server...")
    app.run(debug=True, port=5000, host='0.0.0.0')