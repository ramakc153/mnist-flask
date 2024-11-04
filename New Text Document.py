# Suggested code may be subject to a license. Learn more: ~LicenseLog:2466795690.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:2223421549.
from flask import Flask, render_template, request
import tensorflow
from PIL import Image
import numpy as np

app = Flask(__name__)

model = tensorflow.keras.models.load_model("mnist.h5")

def load_image_into_numpy_array(file):
    # Open the file directly as a PIL image
    img = Image.open(file)
    # Resize to (28, 28) if needed
    img = img.resize((28, 28))
    # Convert image to RGB if it isn't already
    img = img.convert("L")
    # Convert the image to a NumPy array
    img_array = np.array(img)
    return img_array

def predict_image(file):
    
    img = load_image_into_numpy_array(file)
    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0
    prediction = model.predict(img)
    prediction = np.argmax(prediction, axis=1)
    return prediction



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")
    elif request.method == "POST":
        file = request.files["file"]
        # print(type(file))
        prediction = predict_image(file)
        # print(prediction)
        return render_template("predict.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)