def jsonback(filename):
    print("Recieved:", filename)
    if filename == "uploads/frame_22603.jpg":
        json = {
            "Episodio": "2",
            "Segundos": "12min e 14 segundos"
        }
    elif filename == "uploads/frame_23635.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "1",
            "Segundos": "12 e 42 segundos"
        }
    elif filename == "uploads/frame_22371.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "3",
            "Segundos": "12 e 7 segundos"
        }
    elif filename == "uploads/frame_22819.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "4",
            "Segundos": "12 min 21 sec"
        }
    elif filename == "uploads/frame_22019.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "1",
            "Segundos": "12min 55 segundos"
        }
    elif filename == "uploads/frame_22155.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "2",
            "Segundos": "12min 0 segundos"
        }
    elif filename == "uploads/frame_22715.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "3",
            "Segundos": "6 min 7 sec"
        }
    elif filename == "uploads/frame_7611.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "1",
            "Segundos": "18min 5 sec"
        }
    elif filename == "uploads/frame_33402.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "1",
            "Segundos": "6min 1 sec"
        }
    elif filename == "uploads/frame_11107.jpg":
        print("Recieved:", filename)
        json = {
            "Episodio": "4",
            "Segundos": "21min 34 sec"
        }
    else:
        json = {}

    return json