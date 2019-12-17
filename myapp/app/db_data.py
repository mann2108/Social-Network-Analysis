from app.models import Relationship,Tweeter
readData = open('app/17IT1 DataSet.txt', 'r')

people = []

for line in readData:
    people.append((line.split()))
readData.close()

for i in people:
    newUser = Tweeter()
    newUser.user_name=i[0]
    newUser.first_name=i[2]
    newUser.last_name=i[1]
    newUser.password=i[0].lower()
    newUser.email=i[0].lower()+"@charusat.edu.in"
    newUser.save()