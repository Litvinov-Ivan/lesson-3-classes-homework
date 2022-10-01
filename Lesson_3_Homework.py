import json
import keyword


class ColorizeMixin:
    """
    Mixin class for changing the representation of class object.

    Methods
    -------
    __repr__(self):
        Returns title and price of the class object
        colorized with specified color.

        In case of empty advert behave as default __repr__.
    """

    def __repr__(self):
        """
        Returns title and price of the class object
        colorized with specified color.

        In case of empty advert behave as default __repr__.
        """
        if not hasattr(self, "title") and not hasattr(self, "title"):
            return object.__repr__(self)
        return f"\033[1;{self.repr_color_code};1m{self.title} | {self.price} ₽"


class Location:
    """
    Class for location field of dict processing.

    Attributes
    ----------
    Attributes are set dynamically based on dict.

    Methods
    -------
    __init__(self, location_dict: dict):
        Dynamically constructs all the attributes for the class object.

    __repr__(self):
        Returns string representation of the class object.
    """
    def __init__(self, location_dict: dict):
        """
        Dynamically constructs all the attributes for the class object.

        :param location_dict: dict
        """
        self.location_json = location_dict
        for k, v in location_dict.items():
            setattr(self, k, v)

    def __repr__(self):
        """
        Returns string representation of the class object.

        :return: str
        """
        return str(self.location_json)


class Advert(ColorizeMixin):
    """
    Class for adverts constructor.

    Attributes
    ----------
    Attributes are set dynamically based on input json.

    Methods
    -------
    __init__(self, *args, **kwargs):
        Dynamically constructs all the attributes for the class object.

        In case of negative 'price' attribute value is handled,
        raises a ValueError.

        Any keywords passed as attribute names will be set with '_' at the end.

        In case if 'location' is passed as dict
        it will be handled to Location Class constructor.

    price(self):
        Property which sets default value as zero
        in case if there is no 'price' field in input json.

        Returns price value.

        :return: int
    """
    repr_color_code = 33  # yellow

    def __init__(self, *args, **kwargs):
        """
        Dynamically constructs all the attributes for the class object.

        In case of negative 'price' attribute value is handled,
        raises a ValueError.

        Any keywords passed as attribute names will be set with '_' at the end.

        In case if 'location' is passed as dict
        it will be handled to Location Class constructor.

        :param args, kwargs
        """
        if len(args) == 2 and isinstance(args[0], str) and \
                isinstance(args[1], int):
            setattr(self, 'title', args[0])
            setattr(self, 'price_', args[1])
        else:
            if kwargs:
                self.dict_ = kwargs
            elif len(args) == 1 and isinstance(args[0], dict):
                self.dict_ = args[0]
            elif len(args) == 0:
                self.dict_ = {}
            for k, v in self.dict_.items():
                if k == "price":
                    if v < 0:
                        raise ValueError("must be >= 0")
                    else:
                        setattr(self, "price_", v)
                elif isinstance(v, dict) and k == "location":
                    setattr(self, k, Location(v))
                elif keyword.iskeyword(k):
                    setattr(self, f"{k}_", v)
                else:
                    setattr(self, k, v)

    @property
    def price(self):
        """
        Property which sets default value as zero
        in case if there is no 'price' field in input json.

        Returns price value.

        :return: int
        """
        if not hasattr(self, "price_"):
            return 0
        return self.price_


if __name__ == "__main__":
    lesson_str = """{
    "title": "python", "price": 1000,
    "location": {
    "address": "город Москва, Лесная, 7",
    "metro_stations": ["Белорусская"]
    }
    }
    """

    lesson_str_2 = """{
        "title": "python", "price": 100,
        "location": "город Москва, Лесная, 7"
        }
        """

    corgi_str = """{
        "title": "Вельш-корги",
        "price": 10000,
        "class": "dogs",
        "location": {
            "address": "поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }"""

    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad)
    print(lesson_ad.location)
    print(lesson_ad.location.address)

    corgi = json.loads(corgi_str)
    corgi_ad = Advert(corgi)
    print(corgi_ad)
    print(corgi_ad.location)
    print(corgi_ad.location.address)
    print(corgi_ad.class_)

    empty_ad = Advert()
    print(empty_ad)
    print(empty_ad.price)

    iphone_ad = Advert('iPhone X', 100)
    print(iphone_ad)
    print(iphone_ad.price)

    mac_ad = Advert(title='Apple Mac', price=50000, location={
        "address": "город Москва, Лесная, 20",
        "metro_stations": ["Белорусская", "Caвеловская"]
    })
    print(mac_ad.location)
    print(mac_ad.location.address)
    print(mac_ad)
