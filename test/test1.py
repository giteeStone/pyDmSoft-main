answer = "11,12"
answer = answer.split(",")
answer = [int(answer[i]) for i in range(2)]
print(answer,type(answer[0]))