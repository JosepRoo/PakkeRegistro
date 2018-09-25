import serial
import pdfcrowd
import sys
from zplgrf import GRF
from PIL import Image
from io import BytesIO
from app.models.baseModel import BaseModel


class Package(BaseModel):
    def __init__(self, origin_zipcode: str, destiny_zipcode: str, weight: float, height: float, width: float,
                 length: float, _id: str = None):
        super().__init__(_id)
        self.origin_zipcode = origin_zipcode
        self.destiny_zipcode = destiny_zipcode
        self.weight = weight
        self.height = height
        self.width = width
        self.length = length

    @staticmethod
    def get_weight():
        ser = serial.Serial('COM7')
        s = ser.read(100)
        return float(s.strip())

    @staticmethod
    def print(weight, public_price, price_pakke):
        try:

            client = pdfcrowd.HtmlToImageClient(
                'JosepRoo', 'd508735c4b86f87fd4a3961d5195126b')

            # configure the conversion
            client.setOutputFormat('png')

            # run the conversion and store the result into an image variable
            image = client.convertString(set_html(weight, public_price, price_pakke))
            temp_buff = BytesIO()
            temp_buff.write(image)
            # need to jump back to the beginning before handing it off to PIL
            temp_buff.seek(0)
            image = Image.open(temp_buff)
            # image = image.resize([720, 1080]) next resolution
            image = image.resize([830, 1133])
            temp_buff.seek(0)
            image.save(temp_buff, format='PNG')
            grf = GRF.from_image(temp_buff.getvalue(), 'ZPL')
            grf.optimise_barcodes()
            print(grf.to_zpl(compression=3, quantity=1))
            import socket
            mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = "127.0.0.1"
            port = 9100
            try:
                mysocket.connect((host, port))  # connecting to host
                mysocket.send(bytes(grf.to_zpl(compression=3, quantity=1), "utf-8"))  # using bytes
                mysocket.close()  # closing connection
            except:
                print("Error with the connection")
            # Some random options

        except pdfcrowd.Error as why:
            # report the error
            sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

            # handle the exception here or rethrow and handle it at a higher level
            raise
