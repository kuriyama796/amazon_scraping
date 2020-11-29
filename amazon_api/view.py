import eel
import amazon_api
import desktop

app_name="web"
end_point="index.html"
size=(1500,1000)

@eel.expose
def set_genre(genre):
    result = amazon_api.main(genre)
    print(result)
    return result

desktop.start(app_name,end_point,size)

# eel.init("web")
# eel.start("index.html")