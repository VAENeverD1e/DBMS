import os
import pymysql
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes (no models needed since you have existing database)
from routes.music_routes import music_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'dev-secret-change-me')
    
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
    
    # Register blueprints (only music routes for now)
    app.register_blueprint(music_bp, url_prefix='/api/music')
    
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
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Music Platform API',
            'version': '1.0.0',
            'endpoints': {
                'music': '/api/music',
                'health': '/health'
            }
        })
    
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