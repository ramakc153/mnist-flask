# Suggested code may be subject to a license. Learn more: ~LicenseLog:2466795690.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:2223421549.
from flask import Flask, render_template, request,jsonify
import flask
import tensorflow
from PIL import Image
import numpy as np
import base64
from io import BytesIO

app = Flask(__name__)
model = tensorflow.keras.models.load_model("mnist.h5")

label = ["kucing", "anjing"]
label_map ={
    0 : "anjing",
    1: "kucing"
}

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
@app.route("/predict/json", methods=["GET", "POST"])
def predictjson():
    if request.method == "GET":
        return render_template("predictjson.html")
    elif request.method == "POST":
        print("function triggered")
        try:
            # Get JSON data from the request
            data = request.get_json()
            if 'image' not in data:
                return jsonify({"error": "No image data provided"}), 400
            
            # Decode the Base64 string
            base64_image = data['image']
            image_data = base64.b64decode(base64_image)
            
            # Optionally, open it with PIL for further processing
            prediction = predict_image(BytesIO(image_data))
            
            # Here you can apply your model prediction logic
            # Example placeholder for prediction result
            prediction_result = "Sample Prediction Result"
            print(prediction)

            return jsonify({"prediction": str(prediction[0])})
        
        except Exception as e:
            print(str(e))
            return jsonify({"error": str(e)}), 500
        # file = request.files["file"]
        # # print(type(file))
        # prediction = predict_image(file)
        # # print(prediction)
        # return render_template("predict.html", prediction=prediction)

@app.route("/json", methods=["GET", "POST"])
def json():
    return jsonify({
        "hello": "Hello"
    })
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
