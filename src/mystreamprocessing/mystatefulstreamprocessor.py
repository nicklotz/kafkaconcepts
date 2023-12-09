import faust

app = faust.App(
    'mystatefulstreamprocessor',
    broker='kafka://localhost:9092',
    store='memory://'
)

myinputtopic = app.topic('myinputtopic', value_type=str)
myoutputtopic = app.topic('myoutputtopic', value_type=str)

wordcount_table = app.Table('wordcounts', default=int)

@app.agent(myinputtopic)
async def count_words(stream):
    async for message in stream:
        words = message.split()
        for word in words:
            wordcount_table[word] += 1
            await myoutputtopic.send(value=f"{word}: {wordcount_table[word]}")
            print(f"Count for {word}: {wordcount_table[word]}")

if __name__ == '__main__':
    app.main()
