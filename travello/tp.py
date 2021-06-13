import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("student_data.csv")

#create a dataframe
df=pd.DataFrame(df)
print("display dataframe")
print(df)


#bargraph
x=df.sname
y=df.marks

plt.bar(x,y,label="Student data",color="Orange")

plt.xlabel("Student Name")
plt.ylabel("Marks Obtained")

plt.title("Test Marks")
plt.show()

#histogram
plt.hist(df.marks,histtype="bar",rwidth=0.8,color="red")
plt.show()

#pie
marksp=[5,3]
plt.title("Test Marks")
plt.pie(marksp,)
plt.show()










