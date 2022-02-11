from enum import Enum


class UserData:
    users = [
        {
            "id": 2,
            "email": "huyviet2582000@gmail.com",
            "first_name": "Huy",
            "last_name": "Viet",
            "address": "Nhị Dinh 3, Điện Phước, Điện Bàn, Quảng Nam",
            "phone": "0909079675",
            "age": 21
        },
        {
            "id": 3,
            "email": "gonhungho123@gmail.com",
            "first_name": "Kiet",
            "last_name": "Tuan",
            "address": "161 Nguyễn Phong Sắc, Hưng Dũng, Thành phố Vinh, Nghệ An",
            "phone": "079475834",
            "age": 19
        },
        {
            "id": 4,
            "email": "ductai26998@gmail.com",
            "first_name": "Tai",
            "last_name": "Duc",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0909079675",
            "age": 21
        },
        {
            "id": 5,
            "email": "kimchilethi411@gmail.com",
            "first_name": "Chi",
            "last_name": "Kim",
            "address": "28 Ngô Xuân Thu, Hoà Hiệp Bắc, Liên Chiểu, Đà Nẵng",
            "phone": "098567812",
            "age": 20
        },
        {
            "id": 6,
            "email": "bangpham2501@gmail.com",
            "first_name": "Bang",
            "last_name": "Van",
            "address": "23 Quang Trung, Thành phố Vinh, Nghệ An",
            "phone": "097856764",
            "age": 20
        },
        {
            "id": 7,
            "email": "longvavet1325@gmail.com",
            "first_name": "Long",
            "last_name": "Ngoc",
            "address": "96 Quách Thị Trang, Hoà Xuân, Cẩm Lệ, Đà Nẵng",
            "phone": "0974754560",
            "age": 21
        },
        {
            "id": 8,
            "email": "Kimhoangle.23022000@gmail.com",
            "first_name": "Hoang",
            "last_name": "Kim",
            "address": "252 Huỳnh Ngọc Huệ, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0974754560",
            "age": 21
        },
        {
            "id": 9,
            "email": "nguyencongvinh1412@gmail.com",
            "first_name": "Vinh",
            "last_name": "Cong",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0327949281",
            "age": 21
        },
        {
            "id": 10,
            "email": "quangnhat358@gmail.com",
            "first_name": "Nhật",
            "last_name": "Quang",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0327949281",
            "age": 21
        },
        {
            "id": 11,
            "email": "quocbao080220@gmail.com",
            "first_name": "Bảo",
            "last_name": "Quốc",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0327949281",
            "age": 21
        },
        {
            "id": 12,
            "email": "nguyen2924092000@gmail.com",
            "first_name": "Vinh",
            "last_name": "Cong",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0327949281",
            "age": 21
        },
        {
            "id": 13,
            "email": "nguyenvantien3042k@gmail.com",
            "first_name": "Tiên",
            "last_name": "Văn",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0327949281",
            "age": 21
        },
        {
            "id": 14,
            "email": "duongthanhdung612@gmail.com",
            "first_name": "Dũng",
            "last_name": "Thanh",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0327949281",
            "age": 21
        },
        {
            "id": 15,
            "email": "huyentrang27092000@gmail.com",
            "first_name": "Trang",
            "last_name": "Huyền",
            "address": "15 Hùng Vương, TT. ái Nghĩa, Đại Lộc, Quảng Nam",
            "phone": "0327949281",
            "age": 21
        },
    ]


class RoleData(Enum):
    CUSTOMER = {
        "id": "aef45b7b6f9745428594caa9ed3ec5f8",
        "name": "CUSTOMER"
    }
    STAFF = {
        "id": "91a0e81fd2064dd182669d4dd592d209",
        "name": "STAFF"
    }
    ADMIN = {
        "id": "af63504a122c406f9fd9f3b7162b7591",
        "name": "ADMIN"
    }
