import core.engine as eg



#mistral:7b-instruct-q5_K_M
#toxic-mystral


if __name__ == "__main__":
    bot = eg.CogitoErgoSum({"model" : "toxic-mystral",
                            "stream" : True
                            })
    print(type(bot))
    while True:
        user_text = input("Ty: ")
        if user_text.lower() in ["exit", "quit"]:
            break
        bot.ask(user_text)
        #reply=bot.ask(user_text)
        #print("Bot: ", reply)