# Definition of the list
car = ["Brand", "Model", "Year", "Color", "Mileage", "Price"]

# Assigning values to the list
car[0] = "Toyota"
car[1] = "Corolla"
car[2] = 2023
car[3] = "White"
car[4] = 10000  # Mileage (in kilometers, assumed)
car[5] = 25000000  # Price (in Colombian pesos, assumed)

# Printing the entire list
print("Car information:", car)

# Printing a specific element (index 3)
print("Car color:", car[3])

# Printing a range of elements (index 0 to 2)
print("Brand and model:", car[0:2])

# Modifying an element (index 5)
car[5] = 24000000  # Updated price

# Printing the updated list
print("Updated car information:", car)

# Adding a new element to the end of the list
car.append("Transmission")
car[6] = "Automatic"

# Printing the list with the new element
print("Car information with new element:", car)

# Removing an element from the list (index 4)
del car[4]

# Printing the list without the removed element
print("Car information without removed element:", car)
