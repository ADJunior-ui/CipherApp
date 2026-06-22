import io
import os
import base64
import tempfile
from flask import Flask, render_template, request, jsonify

# Force Matplotlib to run silently in the background
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from decodeApp import CipherApp

web_app = Flask(__name__)
cipher_engine = CipherApp()

def generate_graph_base64(coordinates):
    if not coordinates:
        return None
    plt.figure(figsize=(6, 4))
    plt.gcf().patch.set_facecolor('#09090b')
    ax = plt.gca()
    ax.set_facecolor('#09090b')

    x_val = [point[0] for point in coordinates]
    y_val = [point[1] for point in coordinates]

    ax.plot(x_val, y_val, color='#818cf8', marker='o', 
            markerfacecolor='#4f46e5', markeredgecolor='#818cf8', linewidth=2)

    ax.tick_params(colors='#71717a', labelsize=9)
    ax.grid(True, color='#27272a', linestyle='--', linewidth=0.5)

    # Compute axis limits from data with small margins instead of fixed limits
    x_min, x_max = min(x_val), max(x_val)
    y_min, y_max = min(y_val), max(y_val)
    x_margin = max(1, (x_max - x_min) * 0.1)
    y_margin = max(1, (y_max - y_min) * 0.1)
    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=140, facecolor=plt.gcf().get_facecolor(), edgecolor='none')
    buffer.seek(0)
    base64_string = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    return base64_string


def _atomic_write(path, text, encoding='utf-8'):
    dir_name = os.path.dirname(path) or '.'
    fd, tmp_path = tempfile.mkstemp(dir=dir_name)
    try:
        with os.fdopen(fd, 'w', encoding=encoding) as tmp:
            tmp.write(text)
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

@web_app.route('/')
def home():
    return render_template('index.html')

@web_app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()
    mode = data.get('mode', 'encode')
    user_text = data.get('text', '').strip()
    
    try:
        key_value = int(data.get('key', 0))
    except ValueError:
        key_value = 0

    # Protect against very large payloads
    if not user_text:
        return jsonify({'success': False, 'error': 'Input text field cannot be completely empty.'})

    if len(user_text) > 10000:
        return jsonify({'success': False, 'error': 'Input too large.'})

    if mode == 'encode':
        if not cipher_engine.is_valid_text(user_text):
            return jsonify({'success': False, 'error': 'Invalid characters detected.'})
        
        cipher_engine.message = user_text
        cipher_engine.key = key_value
        cipher_engine.encode_message()
        
        formatted_coordinates = " ".join([f"{x},{y}" for x, y in cipher_engine.SepSentenc])

        # Persist encoded coordinates to default.txt atomically
        try:
            _atomic_write('default.txt', formatted_coordinates, encoding='utf-8')
        except Exception:
            # fall back to best-effort write
            with open('default.txt', 'w', encoding='utf-8') as f:
                f.write(formatted_coordinates)
        graph_data = generate_graph_base64(cipher_engine.SepSentenc)
        return jsonify({'success': True, 'result': formatted_coordinates, 'graph': graph_data})

    else:
        parsed_coordinates = []
        for block in user_text.split():
            if ',' in block:
                x_str, y_str = block.split(',', 1)
                try:
                    x = int(x_str)
                    y = int(y_str)
                except ValueError:
                    return jsonify({'success': False, 'error': 'Coordinates must be integers.'})
                # Basic validation for coordinates
                if not (0 <= x <= 9) or y < 0 or y > 1000:
                    return jsonify({'success': False, 'error': 'Coordinate values out of expected range.'})
                parsed_coordinates.append((x, y))

        if not parsed_coordinates:
            return jsonify({'success': False, 'error': 'Failed to parse coordinates. Use format: X,Y X,Y'})

        cipher_engine.SepSentenc = parsed_coordinates
        cipher_engine.key = key_value
        try:
            cipher_engine.decode_message()
        except Exception:
            return jsonify({'success': False, 'error': 'Failed to decode coordinates.'})

        # Persist decoded message atomically
        try:
            _atomic_write('default.txt', cipher_engine.message, encoding='utf-8')
        except Exception:
            with open('default.txt', 'w', encoding='utf-8') as f:
                f.write(cipher_engine.message)

        graph_data = generate_graph_base64(cipher_engine.SepSentenc)
        return jsonify({'success': True, 'result': cipher_engine.message, 'graph': graph_data})

if __name__ == '__main__':
    debug_flag = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    web_app.run(host='127.0.0.1', debug=debug_flag)