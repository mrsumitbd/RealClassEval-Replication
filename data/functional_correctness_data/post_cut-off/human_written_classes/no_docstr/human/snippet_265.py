import sys
from src.common.server import mcp

class RedisMCPServer:

    def __init__(self):
        print('Starting the Redis MCP Server', file=sys.stderr)

    def run(self):
        mcp.run()