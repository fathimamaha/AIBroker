from server import app

def main():
    print("Hello from backend-server!")
    app.run(host='0.0.0.0',port=9001,debug=True)

if __name__ == "__main__":
    main()
