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
