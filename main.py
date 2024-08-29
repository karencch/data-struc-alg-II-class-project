# Student ID: 0
import csv
from datetime import datetime, timedelta

from hashtable import Hashtable
from package import Package
from truck import Truck


# Create instance of Hashtable
mainHashtable = Hashtable()


# Method to load all packages from csv into hashtable
def loadPackageData(filename):
    with open(filename) as packages_csv:
        packageData = csv.reader(packages_csv, delimiter=",")
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = int(package[6])
            pStatus = "At the hub"

            # Create package object
            p = Package(pID, pAddress, pDeadline, pCity, pZip, pWeight, pStatus)

            # Insert each package object into hashtable
            mainHashtable.insert(pID, p)

# Load packages from csv into table
loadPackageData("table_packages.csv")


# Create dictionary of distances
def loadDistanceData(filename):
    with open(filename) as distances_csv:
        distanceData = csv.reader(distances_csv, delimiter=",")
        count_line = 0
        distance_dictionary = {}
        for line in distanceData:
            count_elem = 0
            for elem in line:
                if elem != "":
                    # Add from the other direction too since both directions have the same distance
                    distance_dictionary[f"{count_line},{count_elem}"] = elem
                    distance_dictionary[f"{count_elem},{count_line}"] = elem
                    count_elem += 1
            count_line += 1
        return distance_dictionary

# Load distances from csv into dictionary
# Dictionary key-value example is '2,0': '3.8'
# Key is loc to loc. Value is distance in miles.
symmetrical_distance_dict = loadDistanceData("table_distances.csv")


# Create dictionary of addresses
def loadAddressData(filename):
    with open(filename) as addresses_csv:
        addressData = csv.reader(addresses_csv, delimiter=",")
        addr_dict = {}
        for line in addressData:
            addr_dict[f"{line[0]}"] = f"{line[1]}"
    return addr_dict


# Load addresses from csv into dictionary
# Dictionary key-value example is '0': '4001 South 700 East'
address_dict = loadAddressData("table_addresses.csv")


# Method to find address ID in address_dict using address string
def findAddressID(address_string):
    search_string = address_string
    for k, v in address_dict.items():
        if v == search_string:
            return k


# Method to return distance (in float type) between 2 string addresses
def distanceBetween(address1, address2):
    address_id_1 = findAddressID(address1)
    address_id_2 = findAddressID(address2)
    distance = float(symmetrical_distance_dict[f"{address_id_1},{address_id_2}"])
    return distance


# Method to convert string timepoint to datetime object
def convert_str_time_to_datetimeobj(timepoint_str):
    time_concat = "2024-04-01 " + timepoint_str
    timepoint_format = "%Y-%m-%d %I:%M %p"
    # Convert to datetime object:
    datetimeobj = datetime.strptime(time_concat, timepoint_format)
    return datetimeobj


# Method to convert string timepoint to float-hours with respect to a starting time
def convert_str_time_to_floathrs(starttime_str,endtime_str):
    # Convert string times to datetime objects
    start_time = datetime.strptime(starttime_str, "%I:%M %p")
    end_time = datetime.strptime(endtime_str, "%I:%M %p")

    # Calculate the time difference
    time_difference = end_time - start_time

    # Convert the time difference to hours in float
    hours_float = time_difference.total_seconds() / 3600.0

    return hours_float


# Method to calculate datetime obj from float-hours
def accumulated_hrs_as_datetimeobj(starttime_datetimeobj, accumulatedhrsfloat):
    tm_delta = convert_float_hrs_to_timedeltaobj(accumulatedhrsfloat)

    accumulated_as_datetimeobj = starttime_datetimeobj + tm_delta
    return accumulated_as_datetimeobj


# Method to convert miles to hours
def convert_miles_to_floathours(miles):
    hrs = float(miles/18.0)
    return hrs


# Method to convert hours to miles
def convert_floathours_to_miles(float_hrs):
    miles = float(float_hrs * 18.0)
    return miles


# Method to convert float-hours to timedelta
def convert_float_hrs_to_timedeltaobj(float_hrs):
    # Split hours into integer and partial hours
    whole_hours = int(float_hrs)
    fractional_hours = float_hrs - whole_hours
    # Convert partial hours to minutes
    minutes = int(fractional_hours * 60)
    # Create a timedelta object
    tdelta = timedelta(hours=whole_hours, minutes=minutes)
    return tdelta


# Method to convert timedelta to float-hours
def convert_timedeltaobj_to_float_hrs(timedeltaobj):
    float_hrs = timedeltaobj.total_seconds() / 3600.0
    return float_hrs


# Method to convert float hours to a timepoint i.e, datetime
def convert_floathours_to_datetime(starttime_str, float_hrs):
    # Define starting datetime
    start_time = datetime.strptime(starttime_str, "%I:%M %p")

    # Calculate timedelta
    time_delta = timedelta(hours=float_hrs)

    # Add timedelta to starttime
    timedelta_result = start_time + time_delta

    return timedelta_result


# Method to return the package object (based on the truck package list) that
#  is shortest distance from start address.
def closestPackageObj(startAddress, truck_pkgObj_list):
    minDist = 0
    closestPackageID = 0
    for pkg in truck_pkgObj_list:
        dist = distanceBetween(startAddress, pkg.address)
        if minDist == 0:
            minDist = dist
            closestPackageID = pkg.package_id
        if dist < minDist:
            minDist = dist
            closestPackageID = pkg.package_id
    return mainHashtable.get_item(closestPackageID)


# LOAD TRUCKS MANUALLY WITH PACKAGE ID'S (157.2 miles at lowest):
# Note: 9:00 AM package is 15
# Note: 10:30AM id's are 13, 14, 16, 20, 6, 25, // 1, 29, 30, 31, 34, 37, 40
truck_1_packages = [14, 15, 16, 20, 19, 29, 30, 37, 13, 1, 27, 35]
truck_2_packages = [34, 31, 6, 28, 40, 7, 10, 8, 5, 38, 3, 4, 17, 32, 39, 36]
truck_3_packages = [9, 2, 33, 11, 12, 18, 21, 22, 23, 24, 25, 26]

# CREATE TRUCK 1 and 2 OBJECTS
truck1_obj = Truck("1", truck_1_packages, "8:00 AM")
truck2_obj = Truck("2", truck_2_packages,  "9:05 AM")


# METHOD TO DELIVER PACKAGES IN EACH TRUCK
# TAKES IN A TRUCK OBJECT and the STRING USER INPUT OF TIME
def deliverPackagesInTruck(truckobj, user_timept_str):
    # Consider if user input time is before designated truck leave time...
    if convert_str_time_to_datetimeobj(user_timept_str) < convert_str_time_to_datetimeobj(truckobj.leave_hub_at):
        return

    # Create list to hold package objects pending delivery
    packageobjs_pending_delivery = []

    # STARTING CONDITIONS (which will be updated as packages get delivered):
    start_address = truckobj.last_pkg  # Initially set to the hub address, or last packaage address if truck 3
    accumulated_hrs = truckobj.total_hours
    accumulated_miles = truckobj.total_mileage

    # Populate the empty list of pending deliveries with package objects
    for packageID in truckobj.package_list:
        mainHashtable.update_trucknum(packageID, truckobj.truck_number)
        p_obj = mainHashtable.get_item(packageID)
        packageobjs_pending_delivery.append(p_obj)
    # Set "en route" packages statuses
    for p in packageobjs_pending_delivery:
        mainHashtable.update_delivery_status(p.package_id, "En Route")

    # While package list is not empty...
    while packageobjs_pending_delivery:

        # Deliver 9:00 AM deadline packages first:
        for p in packageobjs_pending_delivery:
            if p.deadline == "9:00 AM":
                miles_between = distanceBetween(start_address, p.address)
                hrs_between = convert_miles_to_floathours(miles_between)
                # Only save to truck object and table if accumulated time plus this expected time <= user input time...
                if accumulated_hrs + hrs_between <= convert_str_time_to_floathrs(truckobj.leave_hub_at, user_timept_str):
                    accumulated_miles = accumulated_miles + miles_between
                    truckobj.total_mileage = accumulated_miles
                    accumulated_hrs = accumulated_hrs + hrs_between
                    truckobj.total_hours = accumulated_hrs
                    delivered_time = (convert_floathours_to_datetime(truckobj.leave_hub_at, accumulated_hrs)).strftime("%I:%M %p")
                    delivered_time_str = f"DELIVERED AT {delivered_time}"
                    mainHashtable.update_delivery_status(p.package_id, delivered_time_str)
                    start_address = p.address
                    truckobj.last_pkg = start_address
                    packageobjs_pending_delivery.remove(p)
                # If delivering the package will go past user input time, this means we're at a stopping point
                else:
                    return

        # Deliver 10:30 AM deadline packages next:
        for p in packageobjs_pending_delivery:
            if p.deadline == "10:30 AM":
                miles_between = distanceBetween(start_address, p.address)
                hrs_between = convert_miles_to_floathours(miles_between)
                # Only save to truck obj and table if accumulated time plus this expected time <= user input time...
                if accumulated_hrs + hrs_between <= convert_str_time_to_floathrs(truckobj.leave_hub_at, user_timept_str):
                    accumulated_miles = accumulated_miles + miles_between
                    truckobj.total_mileage = accumulated_miles
                    accumulated_hrs = accumulated_hrs + hrs_between
                    truckobj.total_hours = accumulated_hrs
                    delivered_time = (convert_floathours_to_datetime(truckobj.leave_hub_at, accumulated_hrs)).strftime("%I:%M %p")
                    delivered_time_str = f"DELIVERED AT {delivered_time}"
                    mainHashtable.update_delivery_status(p.package_id, delivered_time_str)
                    start_address = p.address
                    truckobj.last_pkg = start_address
                    packageobjs_pending_delivery.remove(p)
                # Else (meaning that travel time will exceed user input time)...
                else:
                    return


        # At 10:20AM, package 9 address is corrected
        # Check if user input time is after 10:20
        if convert_str_time_to_datetimeobj(user_timept_str) >= convert_str_time_to_datetimeobj("10:20 AM"):
            mainHashtable.update_address(9, "410 S State St", "Salt Lake City", "84111")
            if mainHashtable.get_item(9) in packageobjs_pending_delivery:
                index_p = packageobjs_pending_delivery.index(mainHashtable.get_item(9))
                packageobjs_pending_delivery[index_p] = mainHashtable.get_item(9)


        # Next, deliver all packages left until you reach end of day (versus user input time).
        # So, break points are either no packages left VERSUS user input time
        maxhours = convert_str_time_to_floathrs(truckobj.leave_hub_at, user_timept_str)

        while accumulated_hrs < maxhours:
            check2 = True

            for p in packageobjs_pending_delivery:
                # Find nearest package
                closest_pkgobj = closestPackageObj(start_address, packageobjs_pending_delivery)

                # Find distance and hours between current address and next package
                miles_between = distanceBetween(start_address, closest_pkgobj.address)
                hrs_between = convert_miles_to_floathours(miles_between)

                # Only save to truck object and table if accumulated time plus expected time <= max time...
                if accumulated_hrs + hrs_between <= maxhours:
                    accumulated_miles = accumulated_miles + miles_between
                    truckobj.total_mileage = accumulated_miles
                    accumulated_hrs = accumulated_hrs + hrs_between
                    truckobj.total_hours = accumulated_hrs
                    delivered_time = (convert_floathours_to_datetime(truckobj.leave_hub_at, accumulated_hrs)).strftime(
                        "%I:%M %p")
                    delivered_time_str = f"DELIVERED AT {delivered_time}"
                    mainHashtable.update_delivery_status(p.package_id, delivered_time_str)
                    start_address = p.address
                    truckobj.last_pkg = start_address
                    packageobjs_pending_delivery.remove(p)
                # When accumulated hrs plus hrs between > maxhours, then we're at stopping point
                else:
                    return

            # After the for-loop is done, check if package list is zero
            if len(packageobjs_pending_delivery) < 1:
                check2 = False
            if check2 == False:
                break

        # Get out of while loop if package list is empty
        if not packageobjs_pending_delivery:
            return

    # return


# GETTING USER INPUT:

# Method to check that user inputs a correctly formatted string for time
def is_valid_datetimeobject_format(input_str):
    try:
        # Attempt to parse input string
        datetime.strptime(input_str, "%I:%M %p")
        return True
    except ValueError:
        # If fails, return False
        return False

# User interface
running = True
while running:
    print(f"\nTRUCK DELIVERY ROUTE PROGRAM:")
    print("-" * 29)
    print(f"MENU OPTIONS:\n(a) Lookup All Package Statuses, with a time\n(b) Lookup One Package by ID, with a time\n(c) Lookup All Packages at End of Day, with TOTAL MILEAGE\n(x) Exit program")
    menuchoice = input("Please enter a, b, c, or x: ")

    if menuchoice == "x" or menuchoice == "X":
        print(f"Exiting program.")
        running = False
        break

    if menuchoice == "a" or menuchoice == "A":
        timeinput = input("Please enter the timepoint to look up, in a format such as 8:00 AM. \nYour input: ")

        if is_valid_datetimeobject_format(timeinput) == False:
            print("Please enter input in the valid datetime format. Try again.")
            continue

        # DELIVER PACKAGES USING TRUCK 1 and TRUCK 2
        deliverPackagesInTruck(truck1_obj, timeinput)
        deliverPackagesInTruck(truck2_obj, timeinput)

        # I will have truck 1 drive back to hub and switch to truck 3 for remaining packages

        # Retrieve truck 1's accumulated distance & time so far
        current_miles = truck1_obj.total_mileage
        current_hours = convert_miles_to_floathours(current_miles)

        # Find distance & hours between truck1's last delivered pkg address and the hub
        goback_distance = distanceBetween(truck1_obj.last_pkg, "4001 South 700 East")
        goback_time = convert_miles_to_floathours(goback_distance)

        # Update what distance & time will be once truck 1 gets back to hub
        new_mileage = current_miles + goback_distance
        truck1_obj.total_mileage = new_mileage
        new_hours = current_hours + goback_time
        truck1_obj.total_hours = new_hours

        # Find datetime obj of when truck1 gets back to hub
        truck1_return_time = convert_floathours_to_datetime(truck1_obj.leave_hub_at, new_hours)

        # DELIVER PACKAGES USING TRUCK 3
        # NOTE THAT TRUCK 3 CANNOT LEAVE UNTIL 10:20 AM BECAUSE OF Package 9's ADDRESS CHANGE
        if truck1_return_time <= convert_str_time_to_datetimeobj("10:20 AM"):
            # Create Truck 3 object
            truck3_obj = Truck("3", truck_3_packages, "10:20 AM")
        else:
            # Convert datetime object to string
            return_time_string = truck1_return_time.strftime("%I:%M %p")
            # Create Truck 3 object
            truck3_obj = Truck("3", truck_3_packages, return_time_string)

        deliverPackagesInTruck(truck3_obj, timeinput)

        print(f"Truck 1 accumulated mileage = {truck1_obj.total_mileage} miles")
        print(f"      Truck 1's package list: {", ".join(map(str, truck_1_packages))}")
        print(f"Truck 2 accumulated mileage = {truck2_obj.total_mileage} miles")
        print(f"      Truck 2's package list: {", ".join(map(str, truck_2_packages))}")
        print(f"Truck 3 accumulated mileage = {truck3_obj.total_mileage} miles")
        print(f"      Truck 3's package list: {", ".join(map(str, truck_3_packages))}")
        print(f"TOTAL MILEAGE OF ALL TRUCKS = {truck1_obj.total_mileage + truck2_obj.total_mileage + truck3_obj.total_mileage} MILES\n")
        print(mainHashtable)

        # Reset to defaults:

        # Re-initialize instance of Hashtable
        mainHashtable = Hashtable()
        # Re-load packages from csv into table
        loadPackageData("table_packages.csv")
        # Re-load distances from csv into dictionary
        symmetrical_distance_dict = loadDistanceData("table_distances.csv")
        # Re-load addresses from csv into dictionary
        address_dict = loadAddressData("table_addresses.csv")
        # Re-initialize truck 1 and 2 objects
        truck1_obj = Truck("1", truck_1_packages, "8:00 AM")
        truck2_obj = Truck("2", truck_2_packages, "9:05 AM")

    if menuchoice == "b" or menuchoice == "B":
        id_input = int(input("Please enter the Package ID number to look up: "))
        timeinput = input("Please enter the timepoint to look up, in a format such as 8:00 AM. \nYour input: ")

        if is_valid_datetimeobject_format(timeinput) == False:
            print("Please enter input in the valid datetime format. Try again.")
            continue

        # DELIVER PACKAGES USING TRUCK 1 and TRUCK 2
        deliverPackagesInTruck(truck1_obj, timeinput)
        deliverPackagesInTruck(truck2_obj, timeinput)

        # I will have truck 1 drive back to hub and switch to truck 3 for remaining packages

        # Retrieve truck 1's accumulated distance & time so far
        current_miles = truck1_obj.total_mileage
        current_hours = convert_miles_to_floathours(current_miles)

        # Find distance & hours between truck1's last delivered pkg address and the hub
        goback_distance = distanceBetween(truck1_obj.last_pkg, "4001 South 700 East")
        goback_time = convert_miles_to_floathours(goback_distance)

        # Update what distance & time will be once truck 1 gets back to hub
        new_mileage = current_miles + goback_distance
        truck1_obj.total_mileage = new_mileage
        new_hours = current_hours + goback_time
        truck1_obj.total_hours = new_hours

        # Find datetime obj of when truck1 gets back to hub
        truck1_return_time = convert_floathours_to_datetime(truck1_obj.leave_hub_at, new_hours)

        # DELIVER PACKAGES USING TRUCK 3
        # NOTE THAT TRUCK 3 CANNOT LEAVE UNTIL 10:20 AM BECAUSE OF Package 9's ADDRESS CHANGE
        if truck1_return_time <= convert_str_time_to_datetimeobj("10:20 AM"):
            # Create Truck 3 object
            truck3_obj = Truck("3", truck_3_packages, "10:20 AM")
        else:
            # Convert datetime object to string
            return_time_string = truck1_return_time.strftime("%I:%M %p")
            # Create Truck 3 object
            truck3_obj = Truck("3", truck_3_packages, return_time_string)

        deliverPackagesInTruck(truck3_obj, timeinput)

        id_str = "PACKAGE".ljust(10)
        addr_str = "DELIVERY ADDRESS".ljust(42)
        deadline_str = "DEADLINE".ljust(15)
        city_str = "CITY".ljust(20)
        zip_str = "ZIP".ljust(10)
        weight_str = "WEIGHT".ljust(10)
        trucknum_str = "ON TRUCK".ljust(18)
        status_str = "DELIV.STATUS"
        print(f"Selected Package Output:\n{id_str + addr_str + city_str + zip_str + weight_str + trucknum_str + deadline_str + status_str}")
        print(mainHashtable.get_item(id_input))

        # Reset to defaults:

        # Re-initialize instance of Hashtable
        mainHashtable = Hashtable()
        # Re-load packages from csv into table
        loadPackageData("table_packages.csv")
        # Re-load distances from csv into dictionary
        symmetrical_distance_dict = loadDistanceData("table_distances.csv")
        # Re-load addresses from csv into dictionary
        address_dict = loadAddressData("table_addresses.csv")
        # Re-initialize truck 1 and 2 objects
        truck1_obj = Truck("1", truck_1_packages, "8:00 AM")
        truck2_obj = Truck("2", truck_2_packages, "9:05 AM")

    if menuchoice == "c" or menuchoice == "C":
        end_of_day_time = "11:59 PM"

        # DELIVER PACKAGES USING TRUCK 1 and TRUCK 2
        deliverPackagesInTruck(truck1_obj, end_of_day_time)
        deliverPackagesInTruck(truck2_obj, end_of_day_time)

        # I will have truck 1 drive back to hub and switch to truck 3 for remaining packages

        # Retrieve truck 1's accumulated distance & time so far
        current_miles = truck1_obj.total_mileage
        current_hours = convert_miles_to_floathours(current_miles)

        # Find distance & hours between truck1's last delivered pkg address and the hub
        goback_distance = distanceBetween(truck1_obj.last_pkg, "4001 South 700 East")
        goback_time = convert_miles_to_floathours(goback_distance)

        # Update what distance & time will be once truck 1 gets back to hub
        new_mileage = current_miles + goback_distance
        truck1_obj.total_mileage = new_mileage
        new_hours = current_hours + goback_time
        truck1_obj.total_hours = new_hours

        # Find datetime obj of when truck1 gets back to hub
        truck1_return_time = convert_floathours_to_datetime(truck1_obj.leave_hub_at, new_hours)

        # DELIVER PACKAGES USING TRUCK 3
        # NOTE THAT TRUCK 3 CANNOT LEAVE UNTIL 10:20 AM BECAUSE OF Package 9's ADDRESS CHANGE
        if truck1_return_time <= convert_str_time_to_datetimeobj("10:20 AM"):
            # Create Truck 3 object
            truck3_obj = Truck("3", truck_3_packages, "10:20 AM")
        else:
            # Convert datetime object to string
            return_time_string = truck1_return_time.strftime("%I:%M %p")
            # Create Truck 3 object
            truck3_obj = Truck("3", truck_3_packages, return_time_string)

        deliverPackagesInTruck(truck3_obj, end_of_day_time)

        print(f"Truck 1 accumulated mileage = {truck1_obj.total_mileage} miles")
        print(f"      Truck 1's package list: {", ".join(map(str, truck_1_packages))}")
        print(f"Truck 2 accumulated mileage = {truck2_obj.total_mileage} miles")
        print(f"      Truck 2's package list: {", ".join(map(str, truck_2_packages))}")
        print(f"Truck 3 accumulated mileage = {truck3_obj.total_mileage} miles")
        print(f"      Truck 3's package list: {", ".join(map(str, truck_3_packages))}")
        print(
            f"TOTAL MILEAGE OF ALL TRUCKS = {truck1_obj.total_mileage + truck2_obj.total_mileage + truck3_obj.total_mileage} MILES\n")
        print(mainHashtable)

        # Reset to defaults:

        # Re-initialize instance of Hashtable
        mainHashtable = Hashtable()
        # Re-load packages from csv into table
        loadPackageData("table_packages.csv")
        # Re-load distances from csv into dictionary
        symmetrical_distance_dict = loadDistanceData("table_distances.csv")
        # Re-load addresses from csv into dictionary
        address_dict = loadAddressData("table_addresses.csv")
        # Re-initialize truck 1 and 2 objects
        truck1_obj = Truck("1", truck_1_packages, "8:00 AM")
        truck2_obj = Truck("2", truck_2_packages, "9:05 AM")


    continue


















