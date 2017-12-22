input_file = open("train", "r+")
Email_ID={}
Email_Data={}
words={}
words_ham={}
words_spam={}
word_in_no_ham = {}
word_in_no_spam = {}
for line in input_file:
    data=line.split(" ")
    Email_ID[data[0]]=data[1]
    temp={}
    temp_num=None
    for i in range(2,len(data)-1,2):
        temp_num=int(data[i+1])
        if i==len(data)-2:
            temp_num = int(data[i + 1][:-1])
            temp[data[i]]=data[i+1][:-1]
        else:
            temp_num = int(data[i + 1])
            temp[data[i]]=data[i+1]
        if data[i] not in words:
            words[data[i]] = temp_num
        else:
            words[data[i]] += temp_num
        if Email_ID[data[0]]=="ham":
            if data[i] not in words_ham:
                words_ham[data[i]] = temp_num
            else:
                words_ham[data[i]] += temp_num
        if Email_ID[data[0]]=="spam":
            if data[i] not in words_spam:
                words_spam[data[i]] = temp_num
            else:
                words_spam[data[i]] += temp_num
        """if Email_ID[data[0]] == "ham":
            if data[i] not in word_in_no_ham:
                word_in_no_ham[data[i]] = 1
            else:
                word_in_no_ham[data[i]] += 1
            if data[i] not in words_ham:
                words_ham[data[i]] = temp_num
            else:
                words_ham[data[i]] += temp_num
        if Email_ID[data[0]] == "spam":
            if data[i] not in word_in_no_spam:
                word_in_no_spam[data[i]] = 1
            else:
                word_in_no_spam[data[i]] += 1
            if data[i] not in words_spam:
                words_spam[data[i]] = temp_num
            else:
                words_spam[data[i]] += temp_num"""



    Email_Data[data[0]]=temp

    # print Email_ID,Email_Data,temp_num
    # break
print 667,words["share"],words_spam["share"],words_ham["share"]
print len(Email_Data)
prob_ham=0.0
prob_spam=0.0
for Id in Email_ID.keys():
    if Email_ID[Id]=="ham":
        prob_ham+=1
    if Email_ID[Id]=="spam":
        prob_spam+=1

# print prob_ham,prob_spam

# print prob_ham,prob_spam
prob_word_given_spam={}
prob_word_given_ham={}
for w in words.keys():
    if w not in words_spam.keys():
        #prob_word_given_spam[w] = float(1) / float(prob_spam + 1*sum(words_spam.values()))
        #prob_word_given_spam[w] = float(17.35) / float(prob_spam + 17.35*len(words_spam))
        #prob_word_given_spam[w] = float(2.5) / float(prob_spam + 2.5* len(word_in_no_spam))
        prob_word_given_spam[w] = float(100)/float(sum(words_spam.values()) + 100*len(words))
        # prob_word_given_spam[w] = float(1)/float(sum(words.values()))
    else:
        #prob_word_given_spam[w] = float(words_spam[w] + 1) / float(prob_spam + 1 * sum(words_spam.values()))
        #prob_word_given_spam[w] = float(words_spam[w]+1)/float(sum(words.values()))
        #import pdb;pdb.set_trace()
        prob_word_given_spam[w] = float(words_spam[w] + 1) / float(sum(words_spam.values()) + 1*len(words))
        #prob_word_given_spam[w] = float(word_in_no_spam [w] + 2.5) / float(prob_spam + 2.5* len(word_in_no_spam))
        #prob_word_given_spam[w] = float(words_spam[w] + 17.35) / float(prob_spam + 17.35*len(words_spam))
        #prob_word_given_spam[w] = float(word_in_no_spam [w]) / float(prob_spam + 1* len(words))

    if prob_word_given_spam[w] >= 1:
        print prob_word_given_spam[w]
for w in words.keys():
    if w not in words_ham.keys():
        #prob_word_given_ham[w] = float(1) / float(prob_ham + 1 * sum(words_ham.values()))
        # prob_word_given_ham[w] = float(1)/float(sum(words.values()))
        #prob_word_given_ham[w] = float(2 / words[w]) * prob_ham
        #prob_word_given_ham[w] = float(2.5) / float(prob_ham + 2.5*len(word_in_no_ham))
        prob_word_given_ham[w] = float(1) / float(sum(words_ham.values()) + 1*len(words))
    else:
        #prob_word_given_ham[w] = float(words_ham[w] + 1) / float(prob_ham + 1 * sum(words_ham.values()))
        # prob_word_given_ham[w] = float(words_ham[w])/float(sum(words.values()))
        prob_word_given_ham[w] = float(words_ham [w] + 1) / float(sum(words_ham.values()) + 1*len(words))
        #prob_word_given_ham[w] = float((words_ham[w]+2) / words[w]) * prob_ham
        #prob_word_given_ham[w] = float(word_in_no_ham[w] + 2.5) / float(prob_ham + 2.5*len(word_in_no_ham))
        #prob_word_given_ham[w] = float(word_in_no_ham[w]) / float(prob_ham + 1 * len(words))
    if prob_word_given_ham[w] >= 1:
        print prob_word_given_ham[w]

prob_ham/=len(Email_ID)
prob_spam/=len(Email_ID)


test_file=open("test","r+")
Email_ID_test={}
test_data={}
for line in test_file:
    data = line.split(" ")
    # print data
    Email_ID_test[data[0]] = data[1]
    temp = {}
    temp_num = 0
    for i in range(2, len(data) - 1, 2):
        temp_num = int(data[i + 1])
        if i == len(data) - 2:
            temp_num = int(data[i + 1][:-1])
            temp[data[i]] = data[i + 1][:-1]
        else:
            temp_num = int(data[i + 1])
            temp[data[i]] = data[i + 1]
    test_data[data[0]]=temp
    # break

Pr_w_s=1
Pr_n_w_s=1
Pr_w_h=1
Pr_n_w_h=1
# for w in words:
    # Pr_w_s*=prob_word_given_spam[w]
    # Pr_n_w_s *= prob_word_given_spam[w]
    # Pr_w_h *= prob_word_given_ham[w]
    # Pr_n_w_h *= prob_word_given_ham[w]
Prb_spam={}
Prb_ham={}
corRes=0
c=len(Email_ID_test)
for a in Email_ID_test.keys():
    Pr_w_s = 1
    Pr_w_h = 1
    for w in test_data[a]:
        Pr_w_s *= prob_word_given_spam[w]
        Pr_w_h *= prob_word_given_ham[w]

    Prb_spam[a] = Pr_w_s*prob_spam
    Prb_ham[a] = Pr_w_h*prob_ham

    if Prb_spam[a] > 1 or Prb_ham[a] > 1:
        print Prb_spam[a], Prb_ham[a]
    if Prb_ham[a] > Prb_spam[a]:
        if "ham" == Email_ID_test[a]:
            corRes += 1
    else:
        if "spam" == Email_ID_test[a]:
            corRes += 1

# print Prb_spam,Prb_ham
corRes=float(corRes)
c=float(c)
accuracy=float(corRes/c)
# print "accuracy : ",accuracy
accuracy=accuracy*100
print "accuracy : ",accuracy
# print Pr_w_s,Pr_n_w_s,Pr_w_h,Pr_n_w_h

# print Prb_spam,Prb_ham
