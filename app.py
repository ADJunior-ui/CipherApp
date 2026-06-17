import io
import base64
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

    # Lock axis frames to prevent auto-scaling illusions
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 16)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=140, facecolor=plt.gcf().get_facecolor(), edgecolor='none')
    buffer.seek(0)
    base64_string = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    return base64_string

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

    if not user_text:
        return jsonify({'success': False, 'error': 'Input text field cannot be completely empty.'})

    if mode == 'encode':
        if not cipher_engine.is_valid_text(user_text):
            return jsonify({'success': False, 'error': 'Invalid characters detected.'})
        
        cipher_engine.message = user_text
        cipher_engine.key = key_value
        cipher_engine.encode_message()
        
        formatted_coordinates = " ".join([f"{x},{y}" for x, y in cipher_engine.SepSentenc])
        
        # 📁 RESTORED FEATURE: Write encoded coordinates directly to default.txt
        with open('default.txt', 'w', encoding='utf-8') as f:
            f.write(formatted_coordinates)
            
        graph_data = generate_graph_base64(cipher_engine.SepSentenc)
        return jsonify({'success': True, 'result': formatted_coordinates, 'graph': graph_data})

    else:
        try:
            parsed_coordinates = []
            for block in user_text.split():
                if ',' in block:
                    x_str, y_str = block.split(',', 1)
                    parsed_coordinates.append((int(x_str), int(y_str)))
            
            if not parsed_coordinates:
                raise ValueError()
                
            cipher_engine.SepSentenc = parsed_coordinates
            cipher_engine.key = key_value
            cipher_engine.decode_message()
            
            # 📁 RESTORED FEATURE: Write decoded plain text directly to default.txt
            with open('default.txt', 'w', encoding='utf-8') as f:
                f.write(cipher_engine.message)
                
            graph_data = generate_graph_base64(cipher_engine.SepSentenc)
            return jsonify({'success': True, 'result': cipher_engine.message, 'graph': graph_data})
            
        except Exception:
            return jsonify({'success': False, 'error': 'Failed to parse coordinates. Use format: X,Y X,Y'})

if __name__ == '__main__':
    web_app.run(debug=True)