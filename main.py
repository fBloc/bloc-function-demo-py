import asyncio

from bloc_client import BlocClient

from bloc_node.sleep import SleepNode
from bloc_node.phone_sms import SMSNode
from bloc_node.new_stock import NewStockNode
from bloc_node.stock_price_monitor import StockPriceMonitorNode

async def main():
    client_name = "stock_py"
    bloc_client = BlocClient(name=client_name)

    bloc_client.get_config_builder(
    ).set_server(
		"127.0.0.1", 8080,
    ).set_rabbitMQ(
        user="blocRabbit", password='blocRabbitPasswd',
        host="127.0.0.1", port=5672
    ).build_up()

    stock_function_group = bloc_client.register_function_group("Stock Monitor")
    stock_function_group.add_function("PriceMonitor", "stock absolute price change monitor", StockPriceMonitorNode())
    stock_function_group.add_function("NewStockMonitor", "certain exchange & industry new stock monitor", NewStockNode())

    notice_function_group = bloc_client.register_function_group("Notify")
    notice_function_group.add_function("Sms", "phone short message notice", SMSNode())

    tool_function_group = bloc_client.register_function_group("Tool")
    tool_function_group.add_function("Sleep", "do sleep between nodes", SleepNode())

    await bloc_client.run()


if __name__ == "__main__":
    asyncio.run(main())
