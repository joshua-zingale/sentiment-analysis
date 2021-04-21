import extensionModel
model = models.StringModel()
model.load('saved_model')
text = input("Enter Text to Analyze")
metrics = model.predict([text][0])
rating = metrics[1:-5]
if rating > 0.8:
    print("great review...")
elif rating > 0.51:
    print("average review...")
elif rating> 0.3:
    print("poor review...")
else:
    print("terrible review...")
