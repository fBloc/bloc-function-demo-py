# bloc-function-demo-python
此仓库的存在有两个意义：
1. 是[部署本地demo进行试用](https://fbloc.github.io/docs/runDemo/Python)中的预置函数
2. 开发者可以通过查看此中的`bloc function`是如何开发的来进行学习开发`bloc function`

## 如何通过此仓库进行学习开发`bloc function`
### 入口
- 此项目的所有`bloc function`都可以在`main.py`中找到：
    ```python
    import asyncio

    from bloc_client import BlocClient
    
    # below are all bloc functions
    from bloc_node.sleep import SleepNode
    from bloc_node.phone_sms import SMSNode
    from bloc_node.new_stock import NewStockNode
    from bloc_node.stock_price_monitor import StockPriceMonitorNode

    async def main():
        client_name = "stock_py"
        bloc_client = BlocClient(name=client_name)

        # 如果你是按照[教程](https://fbloc.github.io/docs/runDemo/Python)部署的bloc环境
        # 那么下面的地址是正确的，否则请替换为你自己部署的对应地址
        bloc_client.get_config_builder(
        ).set_server(
            "127.0.0.1", 8080,  # bloc-server address
        ).set_rabbitMQ(  # bloc use rabbitMQ address
            user="blocRabbit", password='blocRabbitPasswd',
            host="127.0.0.1", port=5672
        ).build_up()

        # 建议将你的functions按照一定的方式进行分组
        # 就像下面一样，将所有和股票监控相关的function都放到同一个function group中
        # (当然你也可以不按用处分，比如按照团队/代码仓库划/...等进行划分)
        stock_function_group = bloc_client.register_function_group("Stock Monitor")
        # 每个 add_function 方法都将一个 bloc function 注册到对应的group下
        # 这里你可以跳转到对应的 bloc function 对应的实现去看其到底是怎么开发的
        stock_function_group.add_function("PriceMonitor", "stock absolute price change monitor", StockPriceMonitorNode())
        stock_function_group.add_function("NewStockMonitor", "certain exchange & industry new stock monitor", NewStockNode())

        notify_function_group = bloc_client.register_function_group("Notify")
        notify_function_group.add_function("Sms", "phone short message notify", SMSNode())

        tool_function_group = bloc_client.register_function_group("Tool")
        tool_function_group.add_function("Sleep", "do sleep between nodes", SleepNode())

        await bloc_client.run()


    if __name__ == "__main__":
        asyncio.run(main())
    ```

### 从此项目的demo functions中，可以学到什么
> 请先确保你已经看过了关于`bloc function`的[基础文档](https://github.com/fBloc/bloc-client-python#readme)，再继续下面的内容

首先，每个 `bloc function` 都实现了 - [FunctionInterface](https://github.com/fBloc/bloc-client-python/blob/main/bloc_client/function_interface.py#L10) 并且编写了 单元测试

其次，此项目的 `function node` 节点开发的目的是用于演示如何进行开发`bloc function`, 故其并不会有真正的、有外部依赖的访问（比如访问股票实际数据...）

下面列出了每个 function 的特点（都相同的将不会被列出）：
1. sleep function。[代码](/bloc_node/sleep/node.py); [单元测试](/bloc_node/sleep/node_test.py)
    - 此函数是用于模拟长运行函数的。也就是说其应该尽量上报足够多的实时日志 & 进度信息，使得用户可以在 bloc 用户端就能够看到函数的运行进度。在其实现的 `run` 方法中，你可以看到：
        - 上报log & 上报进度百分比
        - 上报进度里程碑情况
    - 如何定义[进度里程碑](/bloc_node/sleep/milestone.py) 以及如何回报里程碑（在run()函数里)
2. stock_price_monitor function。[代码](/bloc_node/stock_price_monitor/node.py); [单元测试](/bloc_node/stock_price_monitor/node_test.py)
    - 你可以了解到为什么把入参设计成了两层嵌套的 - 这里我们将设置“股票价格监控”条件的入参放到了第一个参数里，且其下还有3个参数, 入参数据举例：[tsla_stock_code, >, 700]，这三个一起构成了第一个参数
    - ipt_config() 方法支持设置的多种数据类型（设置 string、int、 float 值类型 & 设置input、select 前端组件类型)
    - opt_config() 方法支持设置的多种数据类型（设置 string、int、json 值类型）
3. new_stock function。[代码](/bloc_node/new_stock/node.py); [单元测试](/bloc_node/new_stock/node_test.py)
    - 在ipt_config() 方法中你可以看到如何构建SelectOptions
    - opt_config() 方法中你可以看到支持多选的Select
