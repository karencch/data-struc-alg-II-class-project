# Learning source: WGU materials https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=eee77a88-4de8-4d42-a3c3-ac8000ece256

class Package:
    def __init__(self, package_id, address, deadline, city, zip, weight, status, truck_num="not loaded yet"):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status
        self.truck_num = truck_num


    def __str__(self):

        output_id = str(self.package_id).ljust(7)
        output_address = self.address.ljust(42)
        output_deadline = self.deadline.ljust(15)
        output_city = self.city.ljust(20)
        output_zip = self.zip.ljust(10)
        output_weight = str(self.weight).ljust(10)
        output_status = self.status
        output_truck_num = self.truck_num.ljust(18)
        return f"ID={output_id + output_address + output_city + output_zip + output_weight + output_truck_num + output_deadline + output_status}"

        # return f"ID={self.package_id}\t\tAddress={self.address}\t\t\tCity={self.city}\t\tZip={self.zip}\t\tWeight={self.weight}\t\tDeadline={self.deadline}\t\tStatus={self.status}"

