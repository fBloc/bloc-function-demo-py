# bloc-function-demo-python
[中文版](/README.zh-CN.md)

## Project mission
This project has 2 missions：
1. Used by [run a local demo doc](https://fbloc.github.io/docs/runDemo/Python) which take you to deploy a bloc environment locally with some preset functions to let you try bloc. Those preset functions are provided by this project
2. Bloc functions under this project are used as model for developer to learn how to deploy bloc function.

## How to learn develop bloc function by this project
### Entrance
- Entrance content is in main.py:
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

        # below address is address if you deploy bloc by tutorial https://fbloc.github.io/docs/runDemo/Python
        # if you deploy bloc by yourself, you should change it to your own address
        bloc_client.get_config_builder(
        ).set_server(
            "127.0.0.1", 8080,  # bloc-server address
        ).set_rabbitMQ(  # bloc use rabbitMQ address
            user="blocRabbit", password='blocRabbitPasswd',
            host="127.0.0.1", port=5672
        ).build_up()

        # Recommend group bloc functions, like below put all stock monitor about bloc functions into one group
        # (of course you can split function in other way, like by team/code repo/language...)
        stock_function_group = bloc_client.register_function_group("Stock Monitor")
        # Every add_function method added a bloc function to register
        # so you can jump to each of it to learn how the bloc function is developed
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


## What you can learn from each demo function
> Please make sure you have already read [the basic doc](https://github.com/fBloc/bloc-client-python#readme) about bloc function before continue

First of all, every bloc function implemented [FunctionInterface](https://github.com/fBloc/bloc-client-python/blob/main/bloc_client/function_interface.py#L10) And have unittest code. 

Second, project's function node is developed only to demonstrate how to develope bloc function. So will not visit real data (like stock price...)

Below list each function's unique features，all in common features will not be listed.
1. sleep function. [code](/bloc_node/sleep/node.py); [unittest](/bloc_node/sleep/node_test.py)
    - this function is used to simulate a long run function。which means it should report more enough live log & progress msg to let user know the progress of it. In run() method you can see
        - report log & progress percent
        - report progress_milestone
    - see how to [define](/bloc_node/sleep/milestone.py) and report progress milestone(in run() method)
2. stock_price_monitor function. [code](/bloc_node/stock_price_monitor/node.py); [unittest](/bloc_node/stock_price_monitor/node_test.py)
    - you can see why input param's definition are nested - here we set stock's absolute_price_monitor condition into 3 input components under single one input param. e.g: [tsla_stock_code, >, 700];
    - you can see how to define a multi kind of input in ipt_config() method (string、int、 float value type & input、select frontend form type)
    - you can see how to define a multi kind of output in opt_config() method (string、bool、json value type)
3. new_stock function. [code](/bloc_node/new_stock/node.py); [unittest](/bloc_node/new_stock/node_test.py)
    - in ipt_config() method, you can see how to build SelectOptions from Enum.
    - in opt_config() method, new_stock_codes field defined a List[str] type
4. phone_sms function. [code](/bloc_node/phone_sms/node.py); [unittest](/bloc_node/phone_sms/node_test.py)
    - in ipt_config() method, you can see support multi value Select.
