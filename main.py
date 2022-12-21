import detected_api
from PIL import Image
from flask import Flask, request, Response
from bokeh.plotting import figure, output_file, show
import math
from collections import Counter

app = Flask(__name__)


@app.route('/')
def index():
    open("static/emotions.txt", "w").close()
    return Response(open('./templates/index.html').read(), mimetype="text/html")


@app.route('/about')
def about():
    return Response(open('./templates/about.html').read(), mimetype="text/html")


@app.route('/moodDetector')
def moodDetector():
    return Response(open('./templates/services.html').read(), mimetype="text/html")


@app.route('/queries')
def queries():
    return Response(open('./templates/contact.html').read(), mimetype="text/html")


@app.route('/analysis')
def analysis():
    print("analysis")
    file1 = open('static/emotions.txt', 'r')
    count = 0
    emo = []

    for line in file1:
        if len(line.strip()) > 0:
            count += 1
            f1 = line.find('emotion": ["')
            if f1 != '-1':
                emoD = line[line.find(']', f1 + 1) - 2:line.find(']', f1 + 1)]
                emo.append(int(emoD))
            else:
                emo.append(-1)

    file1.close()

    # file to save the model
    output_file("analysis.html")

    # instantiating the figure object
    graph = figure(title="Mood distribution over Duration of call")

    emotions = dict(zip((i - 1 for i in range(9)), (
        "No person in frame", "Anger", "Contempt", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise")))

    emoDetected = [emotions[j] for j in set(emo)]
    percentages = [Counter(emo)[i] / len(emo) * 100 for i in set(emo)]

    # converting into radians
    radians = [math.radians((percent / 100) * 360) for percent in percentages]

    # starting angle values
    start_angle = [math.radians(0)]
    prev = start_angle[0]
    for i in radians[:-1]:
        start_angle.append(i + prev)
        prev = i + prev

    # ending angle values
    end_angle = start_angle[1:] + [math.radians(0)]

    # color of the wedges
    color = ["yellow", "red", "lightblue", 'pink', 'blue', 'orange', 'brown', 'green', 'purple'][:len(set(emo))]

    # plotting the graph
    for i in range(len(emoDetected)):
        graph.wedge(0, 0, 1,
                    start_angle=start_angle[i],
                    end_angle=end_angle[i],
                    color=color[i],
                    legend_label=emoDetected[i] + " : " + str(round(percentages[i], 2)) + "%"
                    )

    # saving the graph
    # show(graph)
    return Response(open('./analysis.html').read(), mimetype="text/html")


@app.route('/image', methods=['POST'])
def image():
    try:
        image_file = request.files['image']  # get the image

        # finally run the image through tensor flow object detection`
        image_object = Image.open(image_file)
        # print(image_file)
        objects = detected_api.emo(image_object)
        f = open("static/emotions.txt", "a")
        # print(objects)

        f.write(str(objects) + " \n ")

        f.close()
        return objects

    except Exception as e:
        print('POST /image error: %e' % e)
        return e


if __name__ == "__main__":
    app.run(debug=True)
