import Training
import Testing
import Init

while False:
    var = input("What do you want to do? Training, Testing or Exiting?\n")

    if var.capitalize() == "Training":
        try:
            Training.training(int(input("How much do you want to train? ")))
        except ValueError:
            Training.training()
    elif var.capitalize() == "Testing":
        if "Yes" in input("Do you want to see every single result?").capitalize():
            pass
        else:
            Testing.testing()
    elif var.capitalize() == "Exiting":
        if "Yes" in input("Really? Why already now?").capitalize():
            exit()
        else:
            pass
    else:
        print("I didn't understand you.")
        print("Did you really say: " + str(var.capitalize()) + "?")
