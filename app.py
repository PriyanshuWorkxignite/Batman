#!/usr/bin/env python3
"""
Flask Web Application for Batman - Telegram Manager
Replaces PyQt6 with a web-based interface
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room
import asyncio
import json
from pathlib import Path
from config import config
from account_manager import account_manager
from group_manager import group_manager
import threading
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'batman-secret-key-change-in-production'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active connections
connected_users = {}

# Global asyncio loop for async operations
loop = None

def start_asyncio_loop():
    """Start asyncio event loop in background thread"""
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    def run_loop():
        loop.run_forever()
    
    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()
    return loop

def emit_log(message):
    """Emit log message to all connected clients"""
    socketio.emit('log', {
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, broadcast=True)

def run_async(coro):
    """Run async coroutine in the background loop"""
    return asyncio.run_coroutine_threadsafe(coro, loop)

# ==================== Routes ====================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """Get or save configuration"""
    if request.method == 'GET':
        return jsonify({
            'configured': config.is_configured(),
            'api_id': config.api_id
        })
    
    elif request.method == 'POST':
        data = request.json
        api_id = data.get('api_id')
        api_hash = data.get('api_hash')
        
        if not api_id or not api_hash:
            return jsonify({'success': False, 'error': 'Missing credentials'}), 400
        
        try:
            api_id = int(api_id)
            config.save_config(api_id, api_hash)
            emit_log(f"✓ Configuration saved")
            return jsonify({'success': True})
        except ValueError:
            return jsonify({'success': False, 'error': 'API ID must be a number'}), 400

@app.route('/api/accounts', methods=['GET', 'POST', 'DELETE'])
def api_accounts():
    """Get or manage accounts"""
    if request.method == 'GET':
        accounts = account_manager.get_accounts()
        return jsonify({'accounts': accounts})
    
    elif request.method == 'POST':
        data = request.json
        phone = data.get('phone', '').strip()
        
        if not phone:
            return jsonify({'success': False, 'error': 'Phone number required'}), 400
        
        success, message = account_manager.add_account(phone)
        if success:
            emit_log(f"✓ Account added: {phone}")
            # Start async connection
            run_async(account_manager.connect_account(phone))
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    elif request.method == 'DELETE':
        phone = request.args.get('phone')
        if phone:
            account_manager.remove_account(phone)
            emit_log(f"✗ Account removed: {phone}")
            return jsonify({'success': True})
        return jsonify({'success': False}), 400

@app.route('/api/accounts/<phone>/verify', methods=['POST'])
def verify_code(phone):
    """Verify authentication code"""
    data = request.json
    code = data.get('code', '').strip()
    
    if not code:
        return jsonify({'success': False, 'error': 'Code required'}), 400
    
    # Run async verification
    future = run_async(account_manager.verify_code(phone, code))
    try:
        success, message = future.result(timeout=30)
        if success:
            emit_log(f"✓ {phone}: {message}")
            return jsonify({'success': True, 'message': message})
        else:
            emit_log(f"✗ {phone}: {message}")
            return jsonify({'success': False, 'error': message}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/accounts/<phone>/disconnect', methods=['POST'])
def disconnect_account(phone):
    """Disconnect account"""
    run_async(account_manager.disconnect_account(phone))
    emit_log(f"✗ Disconnected: {phone}")
    return jsonify({'success': True})

@app.route('/api/groups/load', methods=['POST'])
def load_groups():
    """Load groups for an account"""
    data = request.json
    phone = data.get('phone', '').strip()
    
    if not phone:
        return jsonify({'success': False, 'error': 'Phone required'}), 400
    
    async def async_load():
        emit_log(f"⏳ Loading groups from {phone}...")
        client = await account_manager.get_client(phone)
        
        if not client:
            emit_log(f"✗ Error: Cannot connect to {phone}")
            return []
        
        groups = await group_manager.load_groups(client)
        emit_log(f"✓ Loaded {len(groups)} groups from {phone}")
        return groups
    
    future = run_async(async_load())
    try:
        groups = future.result(timeout=60)
        return jsonify({'success': True, 'groups': groups})
    except Exception as e:
        emit_log(f"✗ Error loading groups: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/groups/save', methods=['POST'])
def save_groups():
    """Save selected groups for an account"""
    data = request.json
    phone = data.get('phone', '').strip()
    groups = data.get('groups', [])
    
    if not phone:
        return jsonify({'success': False, 'error': 'Phone required'}), 400
    
    account_manager.update_groups(phone, groups)
    emit_log(f"✓ Saved {len(groups)} groups for {phone}")
    return jsonify({'success': True})

@app.route('/api/broadcast', methods=['POST'])
def broadcast():
    """Broadcast message to all selected groups"""
    data = request.json
    message = data.get('message', '').strip()
    delay = data.get('delay', 3)
    use_markdown = data.get('markdown', True)
    
    if not message:
        return jsonify({'success': False, 'error': 'Message required'}), 400
    
    async def async_broadcast():
        accounts = account_manager.get_accounts()
        total_sent = 0
        
        for account in accounts:
            phone = account['phone']
            client = await account_manager.get_client(phone)
            
            if not client:
                emit_log(f"⊘ Skipping {phone}: Not connected")
                continue
            
            for group in account.get('groups', []):
                try:
                    await group_manager.send_message(
                        client, 
                        group['entity'], 
                        message,
                        parse_mode='markdown' if use_markdown else None
                    )
                    total_sent += 1
                    emit_log(f"✓ {group['title']} ({phone})")
                    await asyncio.sleep(delay)
                
                except Exception as e:
                    emit_log(f"✗ Error {group['title']}: {str(e)}")
        
        emit_log(f"\n✓✓✓ Broadcast complete! {total_sent} messages sent ✓✓✓")
        return total_sent
    
    run_async(async_broadcast())
    return jsonify({'success': True, 'message': 'Broadcast started'})

# ==================== WebSocket Events ====================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit_log(f"🔗 Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnect"""
    emit_log(f"🔌 Client disconnected: {request.sid}")

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ==================== Main ====================

if __name__ == '__main__':
    # Start asyncio loop
    start_asyncio_loop()
    
    # Check if configured
    if not config.is_configured():
        print("⚠️  Batman not configured. Visit http://localhost:5000 and configure first.")
    
    print("🦇 Batman - Starting Flask Server")
    print("📡 Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
