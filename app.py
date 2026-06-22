import base64
import io

import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template, request

from decodeApp import CipherApp

matplotlib.use('Agg')

app = Flask(__name__)
cipher_engine = CipherApp()


def graph_to_base64(points):
    if not points:
        return None

    fig = plt.figure(figsize=(6, 4))
    fig.patch.set_facecolor('#09090b')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#09090b')

    x_vals = [point[0] for point in points]
    y_vals = [point[1] for point in points]

    ax.plot(
        x_vals,
        y_vals,
        color='#818cf8',
        marker='o',
        markerfacecolor='#4f46e5',
        markeredgecolor='#818cf8',
        linewidth=2,
    )
    ax.tick_params(colors='#71717a', labelsize=9)
    ax.grid(True, color='#27272a', linestyle='--', linewidth=0.5)

    if len(points) > 1:
        x_min = min(x_vals)
        x_max = max(x_vals)
        y_min = min(y_vals)
        y_max = max(y_vals)
        x_margin = max(1, (x_max - x_min) * 0.1)
        y_margin = max(1, (y_max - y_min) * 0.1)
        ax.set_xlim(x_min - x_margin, x_max + x_margin)
        ax.set_ylim(y_min - y_margin, y_max + y_margin)

    for side in ax.spines.values():
        side.set_visible(False)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=140, facecolor=fig.get_facecolor(), edgecolor='none')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    return encoded


def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def parse_points(text):
    points = []
    for block in text.split():
        if ',' not in block:
            continue
        x_text, y_text = block.split(',', 1)
        x = safe_int(x_text)
        y = safe_int(y_text)
        if 0 <= x <= 9 and 0 <= y <= 1000:
            points.append((x, y))
    return points


def save_result(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json(silent=True) or {}
    mode = data.get('mode', 'encode')
    text = (data.get('text') or '').strip()
    key = safe_int(data.get('key'))

    if not text:
        return jsonify({'success': False, 'error': 'Input text field cannot be completely empty.'})

    if len(text) > 10000:
        return jsonify({'success': False, 'error': 'Input is too large.'})

    if mode == 'encode':
        if not cipher_engine.is_valid_text(text):
            return jsonify({'success': False, 'error': 'Invalid characters detected.'})

        cipher_engine.set_message(text)
        cipher_engine.set_key(key)
        cipher_engine.encode_message()
        result = cipher_engine.to_coordinate_string()
        save_result('default.txt', result)
        return jsonify({
            'success': True,
            'result': result,
            'graph': graph_to_base64(cipher_engine.to_coordinate_list())
        })

    if mode == 'decode':
        points = parse_points(text)
        if not points:
            return jsonify({
                'success': False,
                'error': 'Failed to parse coordinates. Use format: X,Y X,Y'
            })

        cipher_engine.set_coordinates(points)
        cipher_engine.set_key(key)
        cipher_engine.decode_message()
        save_result('default.txt', cipher_engine.message)
        return jsonify({
            'success': True,
            'result': cipher_engine.message,
            'graph': graph_to_base64(cipher_engine.to_coordinate_list())
        })

    return jsonify({'success': False, 'error': 'Unknown mode.'})


if __name__ == '__main__':
    app.run(debug=True)

