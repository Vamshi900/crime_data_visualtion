from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
# data = pd.read_csv( ../processed_crimes_sample.csv )
# print(data.head())

# read from comments file
# #open text file in read mode
# text_file = open("./comments.txt", "r")
 
# #read whole file to a string
# data = text_file.read()
 
# #close file
# text_file.close()


with open("./comments.txt") as myfile:
    data="".join(line.rstrip() for line in myfile)

# data.replace('\n', '')

# text =   "" .join(i for i in data)
text = data.split()
text = list(set(text))

str1 = ' '.join(text)
print(text)
# text = list(set(text))
stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords, background_color= "white" ).generate(str1)
plt.figure( figsize=(15,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis( "off" )
plt.show()
plt.savefig('./wordcloud2.png')