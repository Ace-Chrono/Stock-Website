from website import create_app

app = create_app()

if __name__ == '__main__': #Only runs the app if we run this file, not if we import it
    app.run(debug=True) #Runs flask application, any time we make change to code it will rerun app because of debug=True. Turn off debug=True in production