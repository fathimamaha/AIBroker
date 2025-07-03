from server import mcp

# Import tools so they get registered via decorators
import tools.get_listings_resource

def main():
    print("Hello from mcp-server!")
    mcp.run(transport="http", port=9000)

if __name__ == "__main__":
    main()
