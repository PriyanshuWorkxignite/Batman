#!/usr/bin/env python3
import asyncio
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from functools import wraps
import os
from dotenv import load_dotenv

from config import config
from account_manager import account_manager
from group_manager import group_manager

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'batman-secret-key-2024')
CORS(app)

# Store logs
logs = []

def add_log(message):
    """Add message to logs"""
    logs.append(message)
    if len(logs) > 1000:
        logs.pop(0)

def run_async(coro):
    """Helper to run async code"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coro)
    loop.close()
    return result

# Routes

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Check if configured"""
    return jsonify({
        'configured': config.is_configured(),
        'api_id': config.api_id if config.is_configured() else None
    })

@app.route('/api/config/save', methods=['POST'])
def save_config():
    """Save API configuration"""
    data = request.json
    api_id = data.get('api_id')
    api_hash = data.get('api_hash')

    if not api_id or not api_hash:
        return jsonify({'success': False, 'message': 'Missing API ID or Hash'}), 400

    try:
        api_id = int(api_id)
    except ValueError:
        return jsonify({'success': False, 'message': 'API ID must be a number'}), 400

    config.save_config(api_id, api_hash)
    add_log(f"✓ API Configuration saved")
    return jsonify({'success': True, 'message': 'Configuration saved'})

# Account Routes

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts"""
    accounts = account_manager.get_accounts()
    return jsonify(accounts)

@app.route('/api/accounts/add', methods=['POST'])
def add_account():
    """Add new account"""
    data = request.json
    phone = data.get('phone', '').strip()

    if not phone:
        return jsonify({'success': False, 'message': 'Phone number required'}), 400

    success, message = account_manager.add_account(phone)
    
    if success:
        add_log(f"✓ Account added: {phone}")
        # Start connection
        try:
            result = run_async(account_manager.connect_account(phone))
            success_conn, msg_conn = result
            add_log(f"→ {phone}: {msg_conn}")
            return jsonify({
                'success': True,
                'message': msg_conn,
                'phone': phone
            })
        except Exception as e:
            return jsonify({
                'success': True,
                'message': str(e),
                'phone': phone
            })
    else:
        return jsonify({'success': False, 'message': message}), 400

@app.route('/api/accounts/<phone>/verify-code', methods=['POST'])
def verify_code(phone):
    """Verify authentication code"""
    data = request.json
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'success': False, 'message': 'Code required'}), 400

    try:
        success, message = run_async(account_manager.verify_code(phone, code))
        
        if success:
            add_log(f"✓ {phone}: Code verified")
        else:
            if "2FA" in message or "password" in message.lower():
                add_log(f"→ {phone}: 2FA required")
            else:
                add_log(f"✗ {phone}: {message}")

        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/accounts/<phone>/verify-password', methods=['POST'])
def verify_password(phone):
    """Verify 2FA password"""
    data = request.json
    password = data.get('password', '')

    if not password:
        return jsonify({'success': False, 'message': 'Password required'}), 400

    try:
        success, message = run_async(account_manager.verify_password(phone, password))
        
        if success:
            add_log(f"✓ {phone}: 2FA verified")
        else:
            add_log(f"✗ {phone}: {message}")

        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/accounts/<phone>/disconnect', methods=['POST'])
def disconnect(phone):
    """Disconnect account"""
    try:
        run_async(account_manager.disconnect_account(phone))
        add_log(f"✗ Disconnected: {phone}")
        return jsonify({'success': True, 'message': 'Disconnected'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/accounts/<phone>/remove', methods=['POST'])
def remove_account(phone):
    """Remove account"""
    try:
        account_manager.remove_account(phone)
        add_log(f"✗ Account removed: {phone}")
        return jsonify({'success': True, 'message': 'Account removed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Group Routes

@app.route('/api/groups/load/<phone>', methods=['POST'])
def load_groups(phone):
    """Load groups for account"""
    try:
        add_log(f"⏳ Loading groups from {phone}...")
        
        client_coro = account_manager.get_client(phone)
        client = run_async(client_coro)
        
        if not client:
            add_log(f"✗ Error: Cannot connect to {phone}")
            return jsonify({'success': False, 'message': 'Cannot connect to account'}), 400

        groups_coro = group_manager.load_groups(client)
        groups = run_async(groups_coro)
        
        # Convert entities to serializable format
        groups_data = []
        for group in groups:
            groups_data.append({
                'id': group['id'],
                'title': group['title'],
                'type': group['type']
            })

        add_log(f"✓ Loaded {len(groups_data)} groups from {phone}")
        
        return jsonify({
            'success': True,
            'groups': groups_data,
            'message': f'Loaded {len(groups_data)} groups'
        })
    except Exception as e:
        add_log(f"✗ Error loading groups: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/groups/save/<phone>', methods=['POST'])
def save_groups(phone):
    """Save selected groups"""
    data = request.json
    groups = data.get('groups', [])

    try:
        account_manager.update_groups(phone, groups)
        add_log(f"✓ Saved {len(groups)} groups for {phone}")
        return jsonify({'success': True, 'message': f'Saved {len(groups)} groups'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Broadcast Routes

@app.route('/api/broadcast', methods=['POST'])
def broadcast():
    """Send broadcast message"""
    data = request.json
    message = data.get('message', '').strip()
    delay = data.get('delay', 3)

    if not message:
        return jsonify({'success': False, 'message': 'Message required'}), 400

    try:
        total_sent = run_async(broadcast_message_async(message, delay))
        add_log(f"\n✓✓✓ Broadcast complete! {total_sent} messages sent ✓✓✓")
        return jsonify({
            'success': True,
            'message': f'Broadcast complete! {total_sent} messages sent',
            'sent': total_sent
        })
    except Exception as e:
        add_log(f"✗ Broadcast error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

async def broadcast_message_async(message, delay):
    """Async broadcast"""
    accounts = account_manager.get_accounts()
    total_sent = 0

    for account in accounts:
        phone = account['phone']
        client = await account_manager.get_client(phone)

        if not client:
            add_log(f"⊘ Skipping {phone}: Not connected")
            continue

        for group in account.get('groups', []):
            try:
                await group_manager.send_message(client, group['entity'], message)
                total_sent += 1
                add_log(f"✓ {group['title']} ({phone})")
                await asyncio.sleep(delay)
            except Exception as e:
                add_log(f"✗ Error {group.get('title', 'Unknown')}: {str(e)}")

    return total_sent

# Logs Routes

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get all logs"""
    return jsonify({'logs': logs})

@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """Clear logs"""
    global logs
    logs = []
    return jsonify({'success': True, 'message': 'Logs cleared'})

# Status route
@app.route('/api/status', methods=['GET'])
def get_status():
    """Get application status"""
    accounts = account_manager.get_accounts()
    return jsonify({
        'status': 'ready',
        'accounts_count': len(accounts),
        'configured': config.is_configured()
    })

if __name__ == '__main__':
    print("🦇 Batman - Starting Flask Server...")
    print("Opening at http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
