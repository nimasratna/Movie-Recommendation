import csv, random, math
import pandas

movies = {}


def prepareData():
    with open("scaledFeatures.csv", 'r', newline='') as g:
        readl= csv.reader(g, delimiter= ';')
        features = list(readl)

    train = substractY()

    __pe = [row[1] for row in train]
    person = list(set(__pe))
    g = [row[0] for row in features]
    print(features[3][1])
    datatraining = []

    for eachperson in person:
        e = []
        for row in train:
            if eachperson == row[1]:
                idmovie = g.index(row[2])
                feature = features[idmovie][1]
                grade = row[3]
                e.append([[feature],[grade]])
        datatraining.append([[eachperson], [e]])


    # with open("dataTraining.csv", 'w', newline='') as myfile:
    #     wr = csv.writer(myfile, delimiter=';')
    #     for l in datatraining:
    #         wr.writerow(l)


def prepare():

    #movie_id, budget, 1stgenre, runtime, year release, vote average, popularity
    with open("movies_1.csv", 'r') as myfile:
        reader = csv.reader(myfile)
        for row in reader:
            x = [float(y) for y in row[1:]]
            movies[row[0]] = x

    dct = {}
    for i in range(6):
        dct[i] = []

    for k, v in movies.items():
        for j in range(6):
            dct[j].append(v[j])

    for key in dct:
        high = max(dct[key])
        low = min(dct[key])
        dct[key] = []
        dct[key].append(low)
        dct[key].append(high)

    for k, v in movies.items():
        for i in range(len(v)):
            i = int(i)
            y = (2 * (v[i] - dct[i][0]) / (dct[i][1] - dct[i][0])) - 1
            movies[k][i] = y
    #print(movies)      #scaled features
    train = []
    with open('train.csv', 'r') as f:
        reader = csv.reader(f , delimiter= ';')
        train = list(reader)
   # print(train)
    train2 = train.copy()
    avgGrade = []
    print(movies)
    #take avg movie raating for each movie in train.csv
    for k, row in movies.items():
        i = int(k)
        tmp = 0
        count = 0
        r=0
        for row in train:
            if int(row[2]) == i:
                tmp += int(row[3])
                count+=1
                #train.remove(row)
        if count>0 :
            r = float(tmp/count)
        avgGrade.append([i,r])

    print(len(avgGrade))

    with open("avgMovieGrade.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, delimiter=';')
        for l in avgGrade:
            wr.writerow(l)


def avgmovie():
    with open("train.csv", 'r', newline='') as g:
        read= csv.reader(g, delimiter= ';')
        datatrain = list(read)

    for id, row in enumerate(datatrain):
        if int(row[3]) == 0:
            datatrain.pop(id)

    movie_list = []

    for idmovie in range(1,201):
        tmp=0
        c = 0
        for data in datatrain:
            if int(data[2]) == idmovie:
                tmp+=int(data[3])
                c+=1
        if c>0:
            tmp = tmp/c
        movie_list.append([idmovie, tmp])

    print(len(movie_list))

    with open("avgMovieGrade.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, delimiter=';')
        for l in movie_list:
            wr.writerow(l)


def substractY():
    with open("avgMovieGrade.csv", 'r', newline='') as g:
        readl= csv.reader(g, delimiter= ';')
        grade = list(readl)

    with open('train.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        train = list(reader)
    print(len(train))

    for id, row in enumerate(train):
        if int(row[3]) == 0:
            train.pop(id)

    g = [row[0] for row in grade]

    for row in train:
        id = g.index(row[2])
        row[3] = float(row[3])- float(grade[id][1])

    return train


def hyperN(data):
    validation, trainData = split(data)
    # g = [row[0] for row in features]
    n_max = 30
    # Qval = []
    # for i in range(10,n_max):
    #     # p = create_random_P(i+1)
    #     tablePerson, p_eachPerson , x_movie = train(trainData, i+1)
    #
    #     #validation
    #     print("Validation... n="+str(i+1))
    #     tmp = 0
    #     e=0
    #     for row in validation:
    #         y= 0
    #         pid= row[1]
    #         mid = int(row[2])-1
    #         rating = float(row[3])
    #         # pval = p_eachPerson[tablePerson.index(pid)][1]
    #         # xfeature= features[mid][1]
    #         for a in range(i+1):
    #             y+=p_eachPerson[tablePerson.index(pid)][a]* x_movie[mid][a]
    #         z=rating-y
    #         e+=(z**2)
    #     print((math.sqrt(e)/len(validation)))
    #     Qval.append((math.sqrt(e)/len(validation)))
    #
    # print(Qval)
    # n = -1
    # for i in range(1, len(Qval) - 1):
    #     if Qval[i] < Qval[i + 1] and Qval[i] < Qval[i - 1]:
    #         n = i + 1
    #         break
    # if n == -1:
    #     n = Qval.index(min(Qval))
    n = 22
    print("n final = " + str(n))

    # p = create_random_P(n)
    tablePerson, p_eachPerson, x_movie = train(data, n)

    with open("PTable.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, delimiter=';')
        for l in p_eachPerson:
            wr.writerow(l)

    print(tablePerson)
    with open("Personlist.csv", 'w', newline='') as mfile:
        wr = csv.writer(mfile)
        wr.writerow(tablePerson)

    with open("x_movieTable.csv", 'w', newline='') as mfile:
        wr = csv.writer(mfile, delimiter=';')
        for l in x_movie:
            wr.writerow(l)


def train(data_training, n):
    __pe = [row[1] for row in data_training]
    person = list(set(__pe))
    learning_step = 0.0005
    max_iteration = 1200
    e = 0.0001
    i = 0
    tmp = 0
    error = 0
    p_person = []
    x_movie = []
    t = 1
    for row in range(200):
        x_movie.append(create_random_P(n).copy())
    for row in range (len(person)):
        p_person.append(create_random_P(n).copy())

    while i < max_iteration:
        er= 0

        print("iteration...." +str(i))
        for eachperson in person:
            for trainrow in data_training:
                if eachperson == trainrow[1]:
                    movieid = int(trainrow[2])-1
                    tmp = 0
                    for j in range(n):
                        tmp += p_person[person.index(eachperson)][j] * x_movie[movieid][j]
                    delta =(tmp - trainrow[3])
                    # change p
                    for j in range(n):
                        p_person[person.index(eachperson)][j] = p_person[person.index(eachperson)][j] - (learning_step*(delta * x_movie[movieid][j])) #+ ( 0.0001 * p_person[person.index(eachperson)][j])
                        x_movie[movieid][j] = x_movie[movieid][j] - (learning_step*(delta * p_person[person.index(eachperson)][j])) #+( 0.0001 * x_movie[movieid][j])

        i+=1

    return person, p_person, x_movie


def create_random_P(p_length):
    p = []
    for i in range(p_length):
        a = random.uniform(0,1)
        p.append(a/100)
    return p



def split(data):
    print("data length: "+str(len(data)))
    val = []
    tr = data.copy()
    for i in range(int(len(data)/20)):
        id = random.randint(0, len(tr))
        val.append(tr[id])
        tr.remove(tr[id])
    print("data val length: " + str(len(val)))
    return val,tr



def itemRecom():
    trainingData = substractY()
    hyperN(trainingData)



# avgmovie()
# prepare()
itemRecom() #create PTable and people liat

def givePrediction():
    with open("x_movieTable.csv", 'r', newline='') as g:
        row= csv.reader(g, delimiter= ';')
        feature = list(row)
    # print(feature)
    with open("Ptable.csv", 'r', newline='') as g:
        row= csv.reader(g, delimiter= ';')
        Ptable = list(row)
    with open("Personlist.csv", 'r', newline='') as g:
        row= csv.reader(g)
        personlist = list(row)
    with open("avgMovieGrade.csv", 'r', newline='') as g:
        row= csv.reader(g, delimiter= ';')
        movieGrade = list(row)
    with open("task.csv", 'r', newline='') as g:
        row= csv.reader(g, delimiter= ';')
        task = list(row)

    movielist = [x[0] for x in movieGrade]
    for row in task:
        personid = row[1]
        movieid = movielist.index(row[2])
        listp = Ptable[personlist[0].index(personid)]
        n = len(listp)
        featuremovielist = feature[int(movieid)]
        avgrat = float(movieGrade[int(movieid)][1])
        y=0
        for i in range(n):
           y+=(float(listp[i]) * float(featuremovielist[i]))
        y+=avgrat
        prediction = 0
        if  y<0.2:
            prediction=int(avgrat)
            print(prediction)
        elif y>=0.2 and y<1.2:
            prediction=1
            print(prediction)
        elif y>=1.2 and y<2.2:
            prediction=2
            print(prediction)
        elif y>=2.2 and y<3.2:
            prediction=3
        elif y>=3.2 and y<4.2:
            prediction=4
            #print("4")
        elif y>=4.2:
            prediction=5
            #print('5')
        row[3] = prediction#int(y)+1
        # if row[3]> 5:
        #     row[3] = 5
        # elif row[3]<1:
        #     row[3] = int(avgrat)+1

        # prediction = int(y)
        # if prediction == 0:
        #     prediction+=avgrat
        # elif prediction >5:
        #     prediction= 5
        # row[3] = prediction

    with open("submission.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, delimiter=';')
        for l in task:
            wr.writerow(l)


givePrediction()