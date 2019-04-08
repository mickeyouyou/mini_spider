# 设计要点
>该文档简要地说明了mini_spider.py的实现要点

在调研过程中，经常需要对一些网站进行定向抓取。由于python包含各种强大的库，使用python做定向抓取比较简单。请使用python开发一个迷你定向抓取器`mini_spider.py`，实现对种子链接的抓取，并把URL长相符合特定pattern的网页保存到磁盘上。 

## HTML请求交互与解析
- request
- based on BeautifulSoup
- urllib

## 多线程

### 数据的互斥访问
`mini_spider.py`中，在涉及到“url的去重”时，一般会使用哈希表类型的数据结构。由于这个哈希表会有多个线程同时访问的情况，所以必须做互斥保护。

此处使用python中`threading.Lock()`实现对已抓取链接的检查。将已抓取链接作为单独的数据模块，与抓取队列统一放置在`lock.acquire()`和`lock.release()`区间处理。

### 线程间的同步
在`mini_spider.py`中，涉及到两处线程间同步的处理：
- 抓取任务被分发到多个抓取线程（crawler）
- 在所有抓取任务都被执行完成后，整个程序结束退出

### 临界区内的处理
被锁保护起来的区域，被称为临界区（也就是在`lock.acquire()`和`lock.release()`之间的区域）
在临界区内的处理要非常注意，有很多禁忌。如：
- 尽量不要执行time-consuming的操作，更不要执行可能阻塞的操作（如IO读写）
- 不能出现无捕捉的exception。如果发生这样的情况，会引起lock.release()没有调用，从而导致死锁的发生
以上这些问题在以往的review中都发生过。

配置文件spider.conf:
```txt
[spider]
url_list_file: ./urls ; 种子文件路径 
output_directory: ./output ; 抓取结果存储目录 
max_depth: 1 ; 最大抓取深度(种子为0级) 
crawl_interval: 1 ; 抓取间隔. 单位: 秒 
crawl_timeout: 1 ; 抓取超时. 单位: 秒 
target_url: .*.(htm|html)$ ; 需要存储的目标网页URL pattern(正则表达式) 
thread_count: 8 ; 抓取线程数 
```

**要求和注意事项:**
- 需要支持命令行参数处理。具体包含: -h(帮助)、-v(版本)、-c(配置文件)
- 单个网页抓取或解析失败，不能导致整个程序退出。需要在日志中记录下错误原因并继续。
- 当程序完成所有抓取任务后，必须优雅退出。
- 从HTML提取链接时需要处理相对路径和绝对路径。
- 需要能够处理不同字符编码的网页(例如utf-8或gbk)。
- 网页存储时每个网页单独存为一个文件，以URL为文件名。注意对URL中的特殊字符，需要做转义。
- 要求支持多线程并行抓取。
- 代码严格遵守百度python编码规范
- 代码的可读性和可维护性好。注意模块、类、函数的设计和划分
- 完成相应的单元测试和使用demo。你的demo必须可运行，单元测试有效而且通过
- 注意控制抓取间隔和总量，避免对方网站封禁百度IP。PS Python CM委员会为大家提供测试抓取网站: http://pycm.baidu.com:8081
- 完成考试编程的一个简单指南：http://wiki.baidu.com/pages/viewpage.action?pageId=328311684