from flask import Flask, render_template, request, send_file
import qrcode
import io
import pandas as pd

app = Flask(__name__)


# Route for the main page to input user's name and generate QR code
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']  # Get the name from the form
        qr_img = qrcode.make(name)  # Generate the QR code from the name
        buffer = io.BytesIO()  # Create an in-memory buffer for the image
        qr_img.save(buffer, 'PNG')  # Save the QR code image to the buffer
        buffer.seek(0)  # Go back to the beginning of the buffer

        # Return the QR code image for download
        return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f'{name}_qrcode.png')

    return render_template('index.html')  # Render the input form


if __name__ == '__main__':
    app.run(debug=True)
