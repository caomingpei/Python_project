import MySQLdb
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

#数据库连接
conn = MySQLdb.connect(host='localhost',
                       db='sjznews',
                       user='root',
                       passwd='password',
                       charset='utf8')
cur = conn.cursor()
cur.execute('SELECT * FROM sjznewsdata ;')
rows = cur.fetchall()
conn.close()

#变量声明
wordsp_list=''
stopwords=[]

#读取停用词表
f=open('stopwords.txt')
for line in open('stopwords.txt'):
    line=f.readline()
    stopwords.append(line.rstrip('\n'))
f.close()

#生成每日词云表
for n in rows:
    str_list= n[-1]
    seg_list = jieba.cut(str_list, cut_all=False)
    for seg in seg_list:
        if seg not in stopwords:
            wordsp_list=wordsp_list+'/'.join(set(seg_list)-set(stopwords))

my_wordcloud = WordCloud( background_color='white',max_words=50,max_font_size=40).generate(wordsp_list)


'''测试部分
#显示词云图
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
'''

year = time.strftime("%Y")
month = time.strftime("%m")
day = time.strftime("%d")
file='Sjzrb'+'_'+year+'_'+month+'_'+day
my_wordcloud.to_file("%s.png"%(file))