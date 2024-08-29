# Learning source: WGU materials at https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=f08d7871-d57a-496e-a6a1-ac7601308c71

class Hashtable:
    # Constructor with hashtable initial capacity parameter
    # Assigns all buckets with an empty list
    def __init__(self, initial_capacity=10):
        # initialize hashtable with empty bucket lists
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])


    # Method to insert a new item into the hashtable given a key
    # This method both inserts and updates
    def insert(self, key, item):
        # Determine bucket index where the item will go
        # Built-in hash function calculates a hash value for key
        bucket_index = hash(key) % len(self.table)
        # Get the list of items in the particular bucket / bucket index
        # In other words, remember that each bucket index has a list of kv pairs
        bucket_list = self.table[bucket_index]

        # Update key if it already exists in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # If given key does NOT already exist, insert at end of bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True


    # Method to find an item given a key
    def get_item(self, key):
        # Same code as above to find the bucket index
        bucket_index = hash(key) % len(self.table)
        # bucket_list is a list of the kv pairs at a specific bucket index
        bucket_list = self.table[bucket_index]

        # Search and return the item if found
        for kv in bucket_list:
            if kv[0]  == key:
                return kv[1]
        # Otherwise, return "None"
        return None


    # Method to remove an item given a key
    def remove(self, key):
        # Same code as above to find the bucket index
        bucket_index = hash(key) % len(self.table)
        # bucket_list is a list of the kv pairs at a specific bucket index
        bucket_list = self.table[bucket_index]

        # Remove the item if it exists
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0],kv[1]])


    # Method to update just delivery status
    def update_delivery_status(self, package_id, new_status):
        # Same code as above to find the bucket index
        bucket_index = hash(package_id) % len(self.table)
        # bucket_list is a list of the kv pairs at a specific bucket index
        bucket_list = self.table[bucket_index]

        for kv in bucket_list:
            if kv[0] == package_id:
                kv[1].status = new_status


    # Method to update just delivery address
    def update_address(self, package_id, address, city, zip):
        # Same code as above to find the bucket index
        bucket_index = hash(package_id) % len(self.table)
        # bucket_list is a list of the kv pairs at a specific bucket index
        bucket_list = self.table[bucket_index]

        for kv in bucket_list:
            if kv[0] == package_id:
                kv[1].address = address
                kv[1].city = city
                kv[1].zip = zip


    # Method to update just truck number on each package
    def update_trucknum(self, package_id, trucknum_str):
        # Same code as above to find the bucket index
        bucket_index = hash(package_id) % len(self.table)
        # bucket_list is a list of the kv pairs at a specific bucket index
        bucket_list = self.table[bucket_index]

        for kv in bucket_list:
            if kv[0] == package_id:
                kv[1].truck_num = trucknum_str


    def __str__(self):
        # First, must sort the list by package id
        list_table = []
        new_list = []
        for element in self.table:
            list_table.append(element)
        for elem in list_table:
            for i in elem:
                new_list.append(i)
        sorted_list = sorted(new_list, key=lambda x: (x[0]))

        # Format list into one package per line
        str_items = ""
        for j in sorted_list:
            str_items = str_items + str(j[1]) + "\n"

        id_str = "PACKAGE".ljust(10)
        addr_str = "DELIVERY ADDRESS".ljust(42)
        deadline_str = "DEADLINE".ljust(15)
        city_str = "CITY".ljust(20)
        zip_str = "ZIP".ljust(10)
        weight_str = "WEIGHT".ljust(10)
        trucknum_str = "ON TRUCK".ljust(18)
        status_str = "DELIV.STATUS"
        return f"Hashtable Output:\n{id_str + addr_str + city_str + zip_str + weight_str + trucknum_str + deadline_str + status_str}\n{str_items}"


    # Method to print whole table
    # def __str__(self):
    #     arr_items = []
    #     arr_string = ""
    #
    #     for element in self.table:
    #         for elem in element:
    #             arr_string = arr_string + str(elem[1]) + "\n"
    #             # print(f"{elem[1]}")
    #
    #     arr_string
    #     return f"Output Hashtable: \n{arr_string}"
    #
    #     # Method to print whole table
    #     # def __str__(self):
    #     #     arr_items = []
    #     #     arr_string = ""
    #     #
    #     #     for element in self.table:
    #     #         for elem in element:
    #     #             arr_string = arr_string + str(elem[1]) + "\n"
    #     #             # print(f"{elem[1]}")
    #     #
    #     #     arr_string
    #     #     return f"Output Hashtable: \n{arr_string}"


    # # Method to append a new item into the hashtable (WITHOUT replacing)
    # def append(self, item):
    #     # Same code as above to find the bucket index
    #     bucket_index = hash(item) % len(self.table)
    #     # bucket_list is a list of the kv pairs at a specific bucket index
    #     bucket_list = self.table[bucket_index]
    #
    #     # append the new item to the end of the bucket list
    #     bucket_list.append(item)

