# DouBanBook
爬取豆瓣读书的信息

## 爬取豆瓣读书时候的注意事项
- 设置User-Agent
如果不设置的话不能爬取
- 设置爬取时间间隔
由于没钱买代理ip,免费的代理存活时间很短,所以在代码中设置的时间限制,测试的时候发现,把每次爬取的时间间隔设置为**1s**,代理并不会被封.

设置如下：
```python
DOWNLOAD_DELAY = 1
```

## 难点
- 页面跳转的次数相对较多，所以对于爬取的时间来说，可能会耗时很长.
在代码设计的时候,设置了三张表进行存储.
	- 表 categories :
		存储所属的标签以及分类
	- 表 books:
		存储主要爬取的字段
	- 表 comments:
		存储评论信息

更多关于表的信息,可以通过观察**items.py**查看每个字段对应的具体功能。也可以通过**数据库建表语句查看**，这两个里面每一条语句都有相应的注释。

- summary字段解析.
这里在解析的时候花费的时间有点长,因为summary中包含了三部分内容:**内容简介**,**作者简介**,**目录**,可能对于不同的书籍只存在其中的一种或两种,也可能一种没有,所以这里对三种情况分开进行的判断,这一块代码量相对来说比较多.

- 书籍的基本信息解析.
这里其实也是一个坑,这些字段并不是每一个书籍里面都有,一般来说都是只有一部分,所以这里使用的是**xpath解析**先来获取所有的text文本,然后使用**book_info**函数根据中文字段判断.由于前端代码设计的相对比较人性化,比较好处理,所以解析写起来相对简单,只不是要想怎么去实现.

## 错误查找
在爬取过程中，发现有很大一部分书籍同时属于多个标签，而在SQL中设置唯一键是根据书籍id进行设置的，这里应该修改为根据书籍id和所属标签来设置唯一键。

这里代码中并没有进行修改，因为爬虫已经爬取了好久了，数据也获取了很大一部分。如果感兴趣的读者想进行修改的话，只需要修改下面几个地方：
- 表**categories**的唯一键，加上tag标签
- 表**comments**中添加上tag列
- 爬虫代码**doubanbook.py**中在往**parse_comment**函数中传值的时候加上**tag**这个标签即可。
(上面的问题已经进行了修改)

## star
如果感觉我的代码对你有帮助，请点击右上角的star！！！！！
