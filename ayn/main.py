from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import tweepy
from googletrans import Translator
from flask import *
import json





def getImage(URL) -> str:
    api_key = "FRI1LVoB1y1gJeNXa7WbNQqqn"
    api_secret_key = "tCejFVo1CdWtar4N38nSBm2TlwQKw5YDg14vEqemvNr06R0b8s"
    api_token = "AAAAAAAAAAAAAAAAAAAAAOgXlAEAAAAAbGED1kd4zP2yR58LpLx5Hd3FuGw%3DtdgSXqwVuwVapptWHiUzM137jDgWipIBeiN6HXtROQ0T0Xwq7c"
    access_token = "996911828155424768-23ZGSNuRklnJKXXGRV49z5S4gnVZcf2"
    access_secret_token = "RBkpNX9jO1jhzQ86U42GyQ2y9zccEYEsh6pGBgIChMTZU"
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(api_key, api_secret_key)

    # authentication of access token and secret
    auth.set_access_token(access_token, access_secret_token)
    api = tweepy.API(auth)
    # يتم البحث عن التغريدة من خلال URL-ها.
    tweetId = URL.split('/')[-1]

    # يتم البحث عن التغريدة من خلال ID-ها.
    tweet = api.get_status(tweetId)
    images = []
    # يتم البحث عن ملفات الوسائط في كل تعليق
    for media in tweet.extended_entities['media']:
       images.append(media['media_url'])
    return images

def getDescrption(URL) -> str:
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + "6b36710a30a0451c8736fd4f345047e7"),)

    userDataObject = resources_pb2.UserAppIDSet(user_id="hx6lt53y6p37",
                                                app_id="Ain")  # The userDataObject is required when using a PAT

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id="workflow-4cc06a",
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            url=URL
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
    results = post_workflow_results_response.results[0]
    # Each model we have in the workflow will produce one output.
    for output in results.outputs:
        model = output.model
        for concept in output.data.concepts:
            print("	%s %.2f" % (concept.name, concept.value))

    # Uncomment this line to print the full Response JSON
    return results.outputs[0].data.text.raw

def TranslateToAr(text):
    translator = Translator()
    return translator.translate(text, dest="ar").text


def runAyn(link):
    print("1")
    url = getImage(link)

    for i in url:
        desc = getDescrption(i)
        TranslateToAr(desc)
    return desc


app = Flask(__name__)


@app.route('/', methods = ["GET"])
def index():
    return "hi"

@app.route('/link/', methods = ["GET"])
def r2():
    q = str(request.args.get('link'))
    desc = runAyn(q)
    data = {"desc" : desc}
    json_dump = json.dumps(data)
    return json_dump

if __name__ == "__main__":
    print("start")
    app.run(port=7775)

