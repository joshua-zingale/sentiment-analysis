import models

model = models.StringModel()

model.load("models/SM_LSTM_90")

model.predict(["a"])



text = input("Enter a body of text to be evaluated.\n>> ")

while True:

	prediction = model.predict([text])

	print("Prediction: "  + str(prediction[0]))
	
	text = input("Enter a body of text to be evaluated. Enter -1 to exit.\n>> ")

	if text == "-1":
		break


