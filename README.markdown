Tornado Thread-Pool
===================

### 说明:

`我在这个版本已经修复,给作者发了pull requests`
* 以前的代码在Blocking处理阶段是有问题，首先不需要判断thread_locals.thread_pool是否存在，另外在异常处理阶段有出BUG.  

`正在写`
* ThreadPool不是预先Prefork的，是根据队列的大小来增加减少. 这样带来的问题是不断的new thread,带来不必要的系统开销.

`正在写,在保留任务异步化的基础上，加入同步非堵塞逻辑`
* thread_pool做了相当于celery那种任务推送,由线程组去消费, 而没有做到把当前用户的操作同步化,不能合理的拿到结果.

-----
#### 提供了一个tornado thread_pool的实例，可以方便的通过该实例测试线程池.

-----

Tornado Thread-Pool is a library for [Tornado](http://www.tornadoweb.org/) that lets you make sure that your blocking code and your non-blocking code don't interfere with each other.

You don't have to remember to call `IOLoop.add_callback` at the appropriate time, or worry about whether that database query will block other web requests.

Just decorate your methods with `@in_thread_pool` (for blocking methods) or `@in_ioloop` (for non-blocking methods) and let the library worry about running the method in the right place.

Usage
-----

```python
    from thread_pool import in_thread_pool, in_ioloop, blocking
    
    @blocking
    def get_thing_from_database():
        # If this method is not called from the thread pool,
        # it will result in a warning.
        return db.get('thing')

    @in_thread_pool
    def blocking_method(callback):
        # Call some blocking api, like a database driver.
        # When called, it will always return immediately,
        # and do its work at some future time in a thread pool.
        callback(get_thing_from_database())

    @in_ioloop
    def non_blocking_method(callback, data):
        # Call some non-blocking api, like AsyncHTTPClient.
        # Guarunteed to run in a tornado IOLoop.

```
