import faust

app = faust.App(
    'mystatelessstreamprocessor',
    broker='kafka://localhost:9092',
    store='memory://'
)

myinputtopic = app.topic('myinputtopic', value_type=str)
myoutputtopic = app.topic('myoutputtopic', value_type=str)

@app.agent(myinputtopic)
async def process(stream):
    async for message in stream:
        if 'important' in message:
            # Send the message to myoutputtopic if the string 'important' is in message
            await myoutputtopic.send(value=f"Processed: {message}")
            print(f"Processed message: {message}")

if __name__ == '__main__':
    app.main()
