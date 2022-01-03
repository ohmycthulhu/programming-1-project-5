from src.application import Application
import json

with open('config.json') as file:
    config = json.load(file)

application = Application(
    title=config['name'],
    maps=config['maps']
)

application.mainloop()

